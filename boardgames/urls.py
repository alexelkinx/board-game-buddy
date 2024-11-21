from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = "boardgames"  # app name for namespacing

urlpatterns = [
    path("", views.home, name="home"),
    path(
        "login/",
        auth_views.LoginView.as_view(next_page=reverse_lazy("boardgames:home")),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page=reverse_lazy("boardgames:home")),
        name="logout",
    ),
    path("register/", views.register_view, name="register"),
    path("account/", views.account_view, name="account"),
    path("account/delete/", views.delete_account, name="delete_account"),
    path("account/edit/", views.edit_account, name="edit_account"),
    path("games/", views.CategoryListView.as_view(), name="category_list"),
    path("games/<int:category_id>/", views.GameListView.as_view(), name="game_list"),
    path("game/add/", views.add_game, name="add_game"),
    path("game/edit/<int:game_id>/", views.edit_game, name="edit_game"),
    path("game/delete/<int:game_id>/", views.delete_game, name="delete_game"),
    path("game/<int:pk>/detail", views.GameDetailView.as_view(), name="game_detail"),
    path("game/<int:game_id>/borrow/", views.borrow_game, name="borrow_game"),
    path("game/<int:game_id>/return/", views.return_game, name="return_game"),
]
