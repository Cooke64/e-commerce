from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
            mail = self.normalize_email(email)
            return mail
        except ValidationError:
            raise ValueError('Должен быть емейл')

    def __create_user(self, email, username, password=None):
        if not username:
            raise ValueError('Должно быть имя пользователя')
        if email:
            email = self.email_validator(email)
        user = self.model(
            email=email,
            username=username
        )
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, password):
        if email:
            email = self.email_validator(email)
        user = self.__create_user(
            email=email,
            password=password,
            username=username,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        if email:
            email = self.email_validator(email)
        user = self.__create_user(
            email=email,
            password=password,
            username=username
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user
