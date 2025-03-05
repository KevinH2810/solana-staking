from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SolanaWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet_address = models.CharField(max_length=44, unique=True)  # Solana addresses are 44 characters
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.wallet_address}"

class AuthenticationChallenge(models.Model):
    wallet_address = models.CharField(max_length=44)
    challenge_string = models.CharField(max_length=64)  # Random challenge string
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Challenge for {self.wallet_address}"

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

    class Meta:
        indexes = [
            models.Index(fields=['wallet_address', 'is_used']),
        ]
