from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
import json

from .backends import SolanaAuthBackend

def login_view(request):
    """Render the login page with wallet connection options."""
    return render(request, 'solana_auth_app/login.html')

@csrf_exempt
@require_http_methods(["POST"])
def request_challenge(request):
    """
    Endpoint to request a challenge string for wallet authentication.
    Expects a POST request with JSON body containing wallet_address.
    """
    try:
        data = json.loads(request.body)
        wallet_address = data.get('wallet_address')
        
        if not wallet_address:
            return JsonResponse({
                'error': 'Wallet address is required'
            }, status=400)

        # Create a new challenge
        auth_backend = SolanaAuthBackend()
        challenge_string = auth_backend.create_challenge(wallet_address)

        return JsonResponse({
            'challenge': challenge_string
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def verify_signature(request):
    """
    Endpoint to verify wallet signature and authenticate user.
    Expects a POST request with JSON body containing:
    - wallet_address
    - signature
    - challenge_string
    """
    try:
        data = json.loads(request.body)
        wallet_address = data.get('wallet_address')
        signature = data.get('signature')
        challenge_string = data.get('challenge_string')

        if not all([wallet_address, signature, challenge_string]):
            return JsonResponse({
                'error': 'Wallet address, signature, and challenge string are required'
            }, status=400)

        # Authenticate using the SolanaAuthBackend
        user = authenticate(
            request,
            wallet_address=wallet_address,
            signature=signature,
            challenge_string=challenge_string
        )

        if user:
            login(request, user)
            return JsonResponse({
                'success': True,
                'user_id': user.id,
                'username': user.username
            })
        else:
            return JsonResponse({
                'error': 'Authentication failed'
            }, status=401)

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)

@require_http_methods(["POST"])
def logout_view(request):
    """Endpoint to log out the current user."""
    logout(request)
    return JsonResponse({
        'success': True
    })
