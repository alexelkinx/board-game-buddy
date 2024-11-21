from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Loan, Category, Game
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.contrib import messages
from .forms import UserForm, GameForm, GamerProfileForm
from django.utils import timezone


def home(request):
    return render(request, "boardgames/home.html")


class CategoryListView(ListView):
    model = Category
    template_name = "boardgames/category_list.html"
    context_object_name = "categories"


class GameListView(ListView):
    model = Game
    template_name = "boardgames/game_list.html"
    context_object_name = "games"

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs["category_id"])
        return self.category.games.all()  # Use related_name for clarity

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category

        if self.request.user.is_authenticated:
            # Get the IDs of the games that the current user has borrowed and not yet returned
            borrowed_game_ids = Loan.objects.filter(
                borrower=self.request.user, returned_at__isnull=True
            ).values_list("game_id", flat=True)
            context["borrowed_game_ids"] = set(borrowed_game_ids)

        return context


class GameDetailView(DetailView):
    model = Game
    template_name = "boardgames/game_detail.html"
    context_object_name = "game"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()

        if self.request.user.is_authenticated:
            # Check if the user has borrowed the game and not returned it yet
            user_loan = Loan.objects.filter(
                game=game, borrower=self.request.user, returned_at__isnull=True
            ).first()
            context["has_borrowed"] = user_loan is not None

        return context


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # If POST, bind the form to the data
        if form.is_valid():
            user = form.save()  # Save the new user to the database
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")  # first password field
            user = authenticate(username=username, password=raw_password)  # Log in
            if user is not None:
                login(request, user)  # Log the user in
                return redirect("boardgames:account")  # Redirect to account page
    else:
        form = UserCreationForm()  # Render a blank form in case of a GET request

    # Render the registration page with the form context
    return render(request, "registration/register.html", {"form": form})


@login_required
def account_view(request):
    gamer = request.user.gamer_profile
    borrowed_games = gamer.borrowed_games
    lending_history = gamer.lending_history
    added_games = Game.objects.filter(owner=request.user)

    context = {
        "gamer": gamer,
        "borrowed_games": borrowed_games,
        "lending_history": lending_history,
        "added_games": added_games,
    }
    return render(request, "boardgames/account.html", context)


@login_required
def edit_account(request):
    user = request.user
    gamer = user.gamer_profile

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        gamer_form = GamerProfileForm(request.POST, request.FILES, instance=gamer)

        if user_form.is_valid() and gamer_form.is_valid():
            if gamer_form.cleaned_data.get("delete_profile_picture"):
                # Reset the profile picture
                gamer.reset_profile_picture()  # Reset profile picture to None
            else:
                gamer_form.save()  # Save the new profile picture (if uploaded)

            user_form.save()  # Save any changes to the user info
            return redirect("boardgames:account")
    else:
        user_form = UserForm(instance=user)
        gamer_form = GamerProfileForm(instance=gamer)

    context = {
        "user_form": user_form,
        "gamer_form": gamer_form,
    }
    return render(request, "boardgames/edit_account.html", context)


@login_required
def delete_account(request):
    if request.method == "POST":
        user = request.user
        loans = Loan.objects.filter(borrower=user, returned_at__isnull=True)

        for loan in loans:
            loan.returned_at = timezone.now()
            loan.save()

        user.delete()
        return HttpResponseRedirect(reverse("boardgames:home"))
    return render(request, "boardgames/delete_account.html")


@login_required
def add_game(request):
    if request.method == "POST":
        form = GameForm(request.POST, request.FILES)
        if form.is_valid():
            game = form.save(commit=False)
            game.owner = request.user  # Set the current user as the owner
            if not game.image:
                game.image = None
            game.save()
            messages.success(
                request, f"The game '{game.title}' has been added successfully."
            )
            return redirect("boardgames:game_detail", pk=game.id)
    else:
        form = GameForm()

    return render(request, "boardgames/add_game.html", {"form": form})


@login_required
def borrow_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    next_url = request.GET.get("next", request.path)

    if not game.can_be_borrowed():
        messages.error(request, "This game is already borrowed.")
        return redirect(next_url)

    if not Loan.can_borrow_more(request.user):
        messages.error(request, "You cannot borrow more than 3 games.")
        return redirect(next_url)

    # Create a loan
    Loan.objects.create(game=game, borrower=request.user)
    game.is_borrowed = True
    game.save()

    messages.success(request, f"You have successfully borrowed {game.title}.")
    return redirect(next_url)


@login_required
def return_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    next_url = request.GET.get("next", request.path)

    # Check if the game is borrowed by the current user
    loan = Loan.objects.filter(
        game=game, borrower=request.user, returned_at__isnull=True
    ).first()

    if loan:
        # Mark the game as returned
        loan.returned_at = timezone.now()
        loan.save()

        # Update the game's borrowed status
        game.is_borrowed = False
        game.save()

        messages.success(request, f"You have successfully returned {game.title}.")
    else:
        messages.error(request, "You haven't borrowed this game.")

    return redirect(next_url)


@login_required
def edit_game(request, game_id):
    game = get_object_or_404(Game, id=game_id, owner=request.user)

    if request.method == "POST":
        form = GameForm(request.POST, request.FILES, instance=game)

        if form.is_valid():
            # Check if the user wants to delete the image
            if "delete_image" in request.POST and game.image:
                game.reset_image()  # Call the reset_image method to delete the image

            form.save()  # Save the other game details
            messages.success(request, f"The game '{game.title}' has been updated.")
        return redirect("boardgames:game_detail", pk=game.id)
    else:
        form = GameForm(instance=game)

    return render(request, "boardgames/edit_game.html", {"form": form, "game": game})


@login_required
def delete_game(request, game_id):
    game = get_object_or_404(Game, id=game_id, owner=request.user)

    if request.method == "POST":
        game.delete()
        messages.success(request, f"The game '{game.title}' has been deleted.")
        return redirect("boardgames:account")

    return render(request, "boardgames/delete_game.html", {"game": game})
