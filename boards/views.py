from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib.auth import login
from asgiref.sync import sync_to_async

from boards.redis_client import (
    get_all_leaderboards,
    get_leaderboard,
    get_scores_for_leaderboard,
)
from boards.utils import map_scores

from .forms import RegistrationForm, ScoreForm


class IndexView(View):
    template_name = "boards/index.html"

    async def get(self, request) -> HttpResponse:
        boards = await get_all_leaderboards()
        print("boards:", boards)
        return render(request, self.template_name, {"boards": boards})


class BoardDetailView(TemplateView):
    template_name = "boards/board_detail.html"

    async def get(self, request, *args, **kwargs):
        users = await sync_to_async(list)(User.objects.all())
        print("users:", users)
        print("kwargs:", kwargs)
        board_id = kwargs["board_id"]
        user = await request.auser()
        # print("user", user.username)
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
                "user": user,
            },
        )


class RegistrationView(FormView):
    template_name = "boards/registration.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        print("form:", form)

        param = self.request.GET.get("source", "index")

        redirect_url = reverse(f"boards:{param}")
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(redirect_url)

    def form_invalid(self, form):
        print("request:", self.request)
        param = self.request.GET.get("source", "")
        print("param:", param)
        print(self.request.path)
        return render(
            self.request, self.template_name, self.get_context_data(form=form)
        )
