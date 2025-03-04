from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.base import TemplateView

from boards.redis_client import (
    get_all_leaderboards,
    get_leaderboard,
    get_scores_for_leaderboard,
)
from boards.utils import map_scores

from .forms import ScoreForm


class IndexView(View):
    template_name = "boards/index.html"

    async def get(self, request) -> HttpResponse:
        boards = await get_all_leaderboards()
        print("boards:", boards)
        return render(request, self.template_name, {"boards": boards})


class BoardDetailView(TemplateView):
    template_name = "boards/board_detail.html"

    async def get(self, request, *args, **kwargs):
        print("kwargs:", kwargs)
        board_id = kwargs["board_id"]

        if not board_id:
            raise Http404("Board ID not provided,")

        scores = await get_scores_for_leaderboard(board_id)  # Fetch scores from Redis
        board_info = await get_leaderboard(board_id)  # Fetch metadata

        return render(
            request,
            self.template_name,
            {
                "board": {
                    "id": board_id,
                    "name": board_info.get("name", "Unknown"),
                    "scores": map_scores(scores),
                },
                "form": ScoreForm(),
            },
        )
