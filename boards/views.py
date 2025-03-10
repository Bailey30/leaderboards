from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout

from boards.redis_client import (
    get_all_leaderboards,
    get_leaderboard,
    get_scores_for_leaderboard,
)
from boards.utils import map_scores

from .forms import LoginForm, LogoutForm, RegistrationForm, ScoreForm


class IndexView(View):
    template_name = "boards/index.html"

    async def get(self, request) -> HttpResponse:
        boards = await get_all_leaderboards()
        user = await request.auser()
        return render(request, self.template_name, {"boards": boards, "auser": user})


class BoardDetailView(TemplateView):
    template_name = "boards/board_detail.html"

    async def get(self, request, *args, **kwargs):
        board_id = kwargs["board_id"]
        if not board_id:
            raise Http404("Board ID not provided,")

        scores = await get_scores_for_leaderboard(board_id)  # Fetch scores from Redis
        board_info = await get_leaderboard(board_id)  # Fetch metadata

        user = await request.auser()

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
                "auser": user,
            },
        )


class RegistrationView(FormView):
    template_name = "boards/registration.html"
    form_class = RegistrationForm

    def form_valid(self, form):
        param = self.request.GET.get("source", "index")

        redirect_url = reverse(f"boards:{param}")
        user = form.save()

        login(self.request, user)

        return HttpResponseRedirect(redirect_url)

    def form_invalid(self, form):
        param = self.request.GET.get("source", "")

        return render(
            self.request, self.template_name, self.get_context_data(form=form)
        )


class Login(FormView):
    template_name = "boards/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        # print("post:", self.request.POST)
        # print("available attributes:", dir(self))
        # print(Login.__mro__)  # Shows method resolution order
        # help(FormView) # Shows breakdown of methods, and inheritance of a class.
        param = self.request.GET.get("source", "index")

        username = self.request.POST["username"]
        password = self.request.POST["password"]

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            redirect_url = reverse(f"boards:{param}")
            return HttpResponseRedirect(redirect_url)

        return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class Logout(FormView):
    form_class = LogoutForm

    def form_valid(self, form) -> HttpResponseRedirect:
        param = self.request.GET.get("source", "index")

        redirect_url = reverse(f"boards:{param}")

        logout(self.request)

        return HttpResponseRedirect(redirect_url)
