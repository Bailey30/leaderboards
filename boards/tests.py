import pytest
from asgiref.sync import sync_to_async
from django.test import TestCase, RequestFactory
from django.urls import reverse
from unittest.mock import patch, AsyncMock
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpRequest, request
from django.contrib.sessions.middleware import SessionMiddleware
from django.test.utils import override_settings


async def create_user():
    user = await sync_to_async(User.objects.create_user)(
        "alex", "test@hotmail.com", "Password1"
    )
    await sync_to_async(user.save)()
    return user


@patch("boards.views.get_all_leaderboards", new_callable=AsyncMock)
class BoardIndexViewTests(TestCase):
    async def test_should_load_no_boards(self, mock_get_all_leaderboards):
        mock_get_all_leaderboards.return_value = []
        response = await self.async_client.get(reverse("boards:index"))

        mock_get_all_leaderboards.assert_called_once_with()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["boards"], [])

    async def test_context_should_contain_correct_number_of_boards(
        self, mock_get_all_leaderboards
    ):
        mock_get_all_leaderboards.return_value = [
            {
                "name": "board one",
                "id": "0",
                "scores": [{"username": "user one", "value": "value one"}],
            },
            {
                "name": "board two",
                "id": "1",
                "scores": [{"username": "user two", "value": "value two"}],
            },
        ]

        response = await self.async_client.get(reverse("boards:index"))

        self.assertEqual(len(response.context["boards"]), 2)

    async def test_should_return_current_user_in_context(
        self, mock_get_all_leaderboards
    ):
        user = await create_user()
        await sync_to_async(self.client.force_login)(user=user)

        response = await sync_to_async(self.client.get)(reverse("boards:index"))
        self.assertEqual(response.context["auser"].username, "alex")


@patch("boards.views.get_scores_for_leaderboard", new_callable=AsyncMock)
@patch("boards.views.get_leaderboard", new_callable=AsyncMock)
class BoardDetailViewTests(TestCase):
    async def test_should_return_correct_leaderboard(
        self,
        mock_get_leaderboard,
        mock_get_scores_for_leaderboard,
    ):
        test_board_id = 1234
        mock_get_scores_for_leaderboard.return_value = [
            ("username", 111111),
            ("username2", 22222),
        ]
        mock_get_leaderboard.return_value = {"id": test_board_id, "name": "board one"}

        response = await self.async_client.get(
            reverse("boards:board_detail", kwargs={"board_id": test_board_id})
        )

        mock_get_scores_for_leaderboard.assert_called_once_with(test_board_id)
        mock_get_leaderboard.assert_called_once_with(test_board_id)

        self.assertEqual(response.context["board"]["id"], 1234)
        self.assertEqual(response.context["board"]["name"], "board one")
        self.assertEqual(
            response.context["board"]["scores"],
            [
                {"username": "username", "value": 111111},
                {"username": "username2", "value": 22222},
            ],
        )


@patch("boards.views.get_all_leaderboards", new_callable=AsyncMock)
class BoardsAuthentication(TestCase):
    def setUp(self):
        self.mock_boards = [
            {
                "name": "board one",
                "id": "0",
                "scores": [{"username": "user one", "value": "value one"}],
            },
            {
                "name": "board two",
                "id": "1",
                "scores": [{"username": "user two", "value": "value two"}],
            },
        ]
        self.login_data = {"username": "alex", "password": "Password1"}

    async def login_user(self):
        """Helper to log in user"""
        return await sync_to_async(self.client.post)(
            reverse("boards:login"), self.login_data, follow=True
        )

    async def test_request_should_contain_login_details(
        self, mock_get_all_leaderboards
    ):
        response = await sync_to_async(self.client.post)(
            reverse("boards:login"), self.login_data, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.wsgi_request.POST)
        self.assertIn("password", response.wsgi_request.POST)

    async def test_should_login_user(self, mock_get_all_leaderboards):
        mock_get_all_leaderboards.return_value = self.mock_boards

        await create_user()
        response = await self.login_user()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["auser"].username, "alex")

    async def test_should_logout_user(self, mock_get_all_leaderboards):
        mock_get_all_leaderboards.return_value = self.mock_boards

        await create_user()
        response = await sync_to_async(self.client.post)(
            reverse("boards:logout"), follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["auser"].username, "")
