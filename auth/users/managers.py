from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name,
                    gender, birth_date, phone_number,
                    email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not phone_number:
            raise ValueError(_('The Phone number must be set'))
        if not first_name or last_name:
            raise ValueError(_('The Name must be set'))

        email = self.normalize_email(email)
        user = self.model(first_name=first_name,last_name=last_name,
                          gender=gender, birth_date=birth_date,
                          phone_number=phone_number,
                          email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name,
                        gender, birth_date, phone_number,
                        email, password):
        user = self.create_user(
            first_name=first_name, last_name=last_name,
            gender=gender, birth_date=birth_date,
            phone_number=phone_number, email=email, password=password
        )
        user.admin = True
        user.save(using=self._db)
        return user
