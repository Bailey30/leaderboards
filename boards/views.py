from os import add_dll_directory
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import FormView

from boards.redis_client import add_hash, add_sorted_set_value, get_hash, get_sorted_set

from .forms import ScoreForm

boards = [
    {
        "name": "Board one",
        "id": 0,
        "scores": [
            {"value": 234235, "username": "john"},
            {
                "value": 353445,
                "username": "guest",
            },
        ],
    },
    {
        "name": "Board two",
        "id": 1,
        "scores": [
            {"value": 345435, "username": "mary"},
            {
                "value": 444444,
                "username": "ass",
            },
        ],
    },
]


class IndexView(View):
    template_name = "boards/index.html"

    def get(self, request) -> HttpResponse:
        return render(request, self.template_name, {"boards": boards})


class BoardDetailView(TemplateView):
    template_name = "boards/board_detail.html"

    def get_context_data(self, **kwargs):
        board_id = kwargs["board_id"]
        scores = get_sorted_set(f"leaderboard:{board_id}")  # Fetch scores from Redis
        board = get_hash(f"leaderboard:{board_id}")  # Fetch metadata

        mapped_scores = [{"username": x, "value": int(y)} for x, y in scores]

        return {
            "board": {
                "id": board_id,
                "name": board.get("name", "Unknown"),
                "scores": mapped_scores,
            },
            "form": ScoreForm(),
        }


class ScoreFormView(FormView):
    template_name = "boards/score_form.html"
    form_class = ScoreForm

    def form_valid(self, form):
        print("kwargs:", self.kwargs)
        board_id = self.kwargs["board_id"]
        username = form.cleaned_data["username"]
        score = form.cleaned_data["score"]

        add_sorted_set_value(f"leaderboard:{board_id}", {username: int(score)})

        return HttpResponse(status=201)
