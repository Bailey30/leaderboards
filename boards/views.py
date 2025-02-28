from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import FormView

from boards.redis_client import (
    add_hash,
    add_sorted_set_value,
    get_all_leaderboard,
    get_hash,
    get_sorted_set,
)
from boards.utils import map_scores

from .forms import ScoreForm


class IndexView(View):
    template_name = "boards/index.html"

    def get(self, request) -> HttpResponse:
        boards = get_all_leaderboard()
        print("boards:", boards)
        return render(request, self.template_name, {"boards": boards})


class BoardDetailView(TemplateView):
    template_name = "boards/board_detail.html"

    def get_context_data(self, **kwargs):
        board_id = kwargs["board_id"]
        scores = get_sorted_set(f"leaderboard:{board_id}")  # Fetch scores from Redis
        board = get_hash(f"leaderboard:{board_id}")  # Fetch metadata

        return {
            "board": {
                "id": board_id,
                "name": board.get("name", "Unknown"),
                "scores": map_scores(scores),
            },
            "form": ScoreForm(),
        }
