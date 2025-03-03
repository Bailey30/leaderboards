from django.http import HttpResponse
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

    def get_context_data(self, **kwargs):
        board_id = kwargs["board_id"]

        scores = get_scores_for_leaderboard(board_id)  # Fetch scores from Redis
        board = get_leaderboard(board_id)  # Fetch metadata

        return {
            "board": {
                "id": board_id,
                "name": board.get("name", "Unknown"),
                "scores": map_scores(scores),
            },
            "form": ScoreForm(),
        }
