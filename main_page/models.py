from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models import signals
from main_page.tasks import send_email
 
 


class UserAccountManager(BaseUserManager):
    use_in_migrations = True
 
    def _create_user(self, email, password, first_name, last_name, phone_number, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')
 
        if not password:
            raise ValueError('Password must be provided')
        
        if not first_name:
            raise ValueError('First name must be provided')

        if not last_name:
            raise ValueError('Last name must be provided')

        if not phone_number:
            raise ValueError('Phone number must be provided')
 
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_user(self, email=None, password=None, first_name=None, last_name=None, phone_number=None, **extra_fields):
        extra_fields['is_active'] = True
        return self._create_user(email, password, first_name, last_name, phone_number, **extra_fields)
 
    def create_superuser(self, email, password, **extra_fields):
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
 
        return self._create_user(email, password, first_name='admin', last_name='admin', phone_number=1234567891012, **extra_fields)
 
 
class User(AbstractBaseUser, PermissionsMixin):
 
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
 
    objects = UserAccountManager()
 
    email = models.EmailField('email', unique=True, blank=False, null=False)
    first_name = models.CharField('first name', blank=False, null=False, max_length=400)
    last_name = models.CharField('last name', blank=False, null=False, max_length=400)
    phone_number = models.CharField('phone_number', blank=False, null=False, max_length=13)
    address = models.CharField('address', blank=True, null=True, max_length=400)
    city = models.CharField('city', blank=True, null=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_active = models.BooleanField('active', default=True)
 
    def get_short_name(self):
        return self.email
 
    def get_full_name(self):
        return self.email
 
    def __unicode__(self):
        return self.email


def user_post_save(sender, instance, signal, *args, **kwargs):
    if not instance.is_staff:
        # Send verification email
        send_email.delay(instance.pk)

signals.post_save.connect(user_post_save, sender=User)