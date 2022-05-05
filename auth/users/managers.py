from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name,
                    phone_number, email, password,
                    gender='U', birth_date=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not phone_number:
            raise ValueError(_('The Phone number must be set'))

        email = self.normalize_email(email)
        user = self.model(first_name=first_name,last_name=last_name,
                          gender=gender, birth_date=birth_date,
                          phone_number=phone_number,
                          email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name,
                         email, password, phone_number,
                         birth_date=None, gender='U', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(
            first_name=first_name, last_name=last_name,
            gender=gender, birth_date=birth_date,phone_number=phone_number,
            email=email, password=password, **extra_fields
        )
