import base58
from datetime import timedelta
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.utils import timezone
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.signature import Signature

from .models import SolanaWallet, AuthenticationChallenge

class SolanaAuthBackend(BaseBackend):
    def authenticate(self, request, wallet_address=None, signature=None, challenge_string=None):
        if not all([wallet_address, signature, challenge_string]):
            return None

        try:
            # Verify the wallet address format
            public_key = Pubkey.from_string(wallet_address)

            # Get the challenge
            challenge = AuthenticationChallenge.objects.filter(
                wallet_address=wallet_address,
                challenge_string=challenge_string,
                is_used=False,
                expires_at__gt=timezone.now()
            ).first()

            if not challenge:
                return None

            # Verify the signature
            try:
                signature_bytes = base58.b58decode(signature)
                sig = Signature.from_bytes(signature_bytes)
                message_bytes = challenge_string.encode()
                
                # Verify the signature
                if not Pubkey.verify_message(message_bytes, [sig], public_key):
                    return None
                
                # Mark challenge as used
                challenge.is_used = True
                challenge.save()

                # Get or create user
                wallet = SolanaWallet.objects.filter(wallet_address=wallet_address).first()
                if wallet:
                    user = wallet.user
                else:
                    # Create new user with wallet address as username
                    username = f"solana_{wallet_address[:8]}"
                    user = User.objects.create_user(username=username)
                    SolanaWallet.objects.create(user=user, wallet_address=wallet_address)

                # Update last login
                wallet = user.solanawallet
                wallet.last_login = timezone.now()
                wallet.save()

                return user

            except (ValueError, Exception) as e:
                print(f"Signature verification failed: {str(e)}")
                return None

        except ValueError:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def create_challenge(self, wallet_address):
        """Create a new authentication challenge for a wallet address."""
        import secrets

        # Generate a random challenge string
        challenge_string = secrets.token_hex(32)
        
        # Set expiration time (5 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=5)
        
        # Create and save the challenge
        challenge = AuthenticationChallenge.objects.create(
            wallet_address=wallet_address,
            challenge_string=challenge_string,
            expires_at=expires_at
        )
        
        return challenge_string
