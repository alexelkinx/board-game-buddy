from django.contrib import admin
from .models import Category, Game, Loan, Gamer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "owner",
        "is_borrowed",
        "created_at",
        "modified_at",
    )
    list_filter = ("category", "is_borrowed", "created_at")
    search_fields = ("title",)


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("game", "borrower", "borrowed_at", "returned_at", "is_active")
    list_filter = ("borrowed_at", "returned_at", "borrower")
    search_fields = ("game__title", "borrower__username")


admin.site.register(Gamer)
