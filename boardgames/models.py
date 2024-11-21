from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Unique category name
    description = models.TextField()
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=200, unique=True)  # Unique game title
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="games"
    )
    num_players = models.TextField()
    avg_playing_time = models.TextField()
    min_age = models.TextField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="games/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="games")
    is_borrowed = models.BooleanField(default=False)

    def __str__(self):
        status = "Borrowed" if self.is_borrowed else "Available"
        return f"{self.title} ({status})"

    def can_be_borrowed(self):
        return not self.is_borrowed

    def reset_image(self):
        if self.image:
            self.image.delete()  # Delete the image from the filesystem
        self.image = None  # Reset the image field to None
        self.save()  # Save the changes to the database


class Loan(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="loans")
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    borrowed_at = models.DateTimeField(default=timezone.now)
    returned_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-borrowed_at"]
        verbose_name_plural = "Loans"

    def is_active(self):
        return self.returned_at is None

    def __str__(self):
        status = "Returned" if self.returned_at else "Active"
        return f"{self.game.title} borrowed by {self.borrower.username} ({status} since {self.borrowed_at.date()})"

    @staticmethod
    def can_borrow_more(user):
        # Check if a user can borrow more games (less than 3 active loans).
        return Loan.objects.filter(borrower=user, returned_at__isnull=True).count() < 3


class Gamer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="gamer_profile"
    )
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    total_games_borrowed = models.PositiveIntegerField(default=0)

    @property
    def borrowed_games(self):
        return Loan.objects.filter(borrower=self.user, returned_at__isnull=True)

    @property
    def lending_history(self):

        borrowed_loans = Loan.objects.filter(borrower=self.user).order_by(
            "-borrowed_at"
        )

        # Filter out duplicate games
        unique_loans = []
        seen_games = set()

        for loan in borrowed_loans:
            if loan.game not in seen_games:
                unique_loans.append(loan)
                seen_games.add(loan.game)

        return unique_loans

    def reset_profile_picture(self):
        self.profile_picture = None
        self.save()

    def __str__(self):
        return self.user.username
