from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Game, Loan


class SimpleTests(TestCase):
    def test_home_view_status_code(self):
        response = self.client.get(reverse("boardgames:home"))
        self.assertEqual(response.status_code, 200)

    def test_category_creation(self):
        category = Category.objects.create(
            name="Strategy", description="Strategy games"
        )
        self.assertEqual(str(category), "Strategy")

class ModelTests(TestCase):
    def test_game_creation(self):
        category = Category.objects.create(name="Party", description="Party games")
        user = User.objects.create_user(username="tester")
        game = Game.objects.create(
            title="Codenames",
            category=category,
            num_players="2-8",
            avg_playing_time="15 minutes",
            min_age="10+",
            owner=user,
        )
        self.assertEqual(str(game), "Codenames (Available)")

    def test_can_borrow_more_limit(self):
        user = User.objects.create_user(username="loanuser")
        category = Category.objects.create(name="Card", description="Card games")
        game_titles = ["Uno", "Skip-Bo", "Phase 10"]

        for title in game_titles:
            game = Game.objects.create(
                title=title,
                category=category,
                num_players="2-6",
                avg_playing_time="30 min",
                min_age="7+",
                owner=user,
                is_borrowed=True,
            )
            Loan.objects.create(game=game, borrower=user)

        self.assertFalse(Loan.can_borrow_more(user))

    def test_game_form_valid(self):
        category = Category.objects.create(name="Deck Builder", description="Deck building games")
        form_data = {
            "title": "Dominion",
            "category": category.id,
            "num_players": "2-4",
            "avg_playing_time": "30 minutes",
            "min_age": "13+",
        }
        from .forms import GameForm
        form = GameForm(data=form_data)
        self.assertTrue(form.is_valid())


class ViewTests(TestCase):
    def test_category_list_view(self):
        response = self.client.get(reverse("boardgames:category_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "boardgames/category_list.html")

    def test_game_detail_view_status_code(self):
        user = User.objects.create_user(username="tester")
        category = Category.objects.create(name="Abstract", description="Abstract games")
        game = Game.objects.create(
            title="Azul",
            category=category,
            num_players="2-4",
            avg_playing_time="30–45 minutes",
            min_age="8+",
            owner=user,
        )
        response = self.client.get(reverse("boardgames:game_detail", args=[game.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "boardgames/game_detail.html")