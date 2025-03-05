from django.contrib import admin
from .models import SolanaWallet, AuthenticationChallenge

@admin.register(SolanaWallet)
class SolanaWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'wallet_address', 'created_at', 'last_login')
    search_fields = ('user__username', 'wallet_address')
    readonly_fields = ('created_at', 'last_login')

@admin.register(AuthenticationChallenge)
class AuthenticationChallengeAdmin(admin.ModelAdmin):
    list_display = ('wallet_address', 'challenge_string', 'created_at', 'is_used', 'expires_at')
    search_fields = ('wallet_address',)
    list_filter = ('is_used', 'created_at')
    readonly_fields = ('created_at',)
