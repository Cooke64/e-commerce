from typing import Dict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken

from core.services import generate_code, send_email
from customer.models import User


def get_confirmation_code(username: str) -> None:
    """Создает для юзера код подтверждения и отправляет его по указанному адресу.
     """
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist as e:
        raise e
    confirmation_code = generate_code()
    user.code = confirmation_code
    user.is_active = False
    user.save()
    send_email(email=user.email, message=f'код подтверждения {confirmation_code}')


def get_tokens_for_user(user: str) -> Dict[str, str]:
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
