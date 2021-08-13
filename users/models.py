from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from .managers import CustomUserManager

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=800)
    ROL_TYPE = (
        (0,'Hitman'),
        (1,'Manager'),
        (2,'Boss'),
    )
    rol = models.IntegerField(choices=ROL_TYPE, default=0)
    USER_STATUS = (
        (1,'Active'),
        (0,'Inactive'),
    )
    status = models.IntegerField(choices=USER_STATUS, default=1)
    description = models.TextField(max_length=800, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name + ' (' +self.email +')'

def initial_configuration(sender, **kwargs):
    hitman = kwargs["instance"]
    bosses = Boss.objects.filter(rol=2)
    hitman_group = Group.objects.get(id=3)
    hitman.groups.add(hitman_group)
    for boss in bosses:
        boss.lackeys.add(hitman)
        boss.save() 
             

post_save.connect(initial_configuration, sender=CustomUser)


class Boss(CustomUser):
    lackeys = models.ManyToManyField(CustomUser, related_name='lackeys', null=True, blank=True)

    @classmethod
    def save_child_from_parent(cls, user_obj, new_attrs):
        parent_link_field = Boss._meta.parents.get(user_obj.__class__, None)
        
        new_attrs[parent_link_field.name] = user_obj

        for field in user_obj._meta.fields:
            new_attrs[field.name] = getattr(user_obj, field.name)
        s = Boss(**new_attrs)
        s.save()
        return s

def boss_initial_configuration(sender, **kwargs):
    hitman = kwargs["instance"]
    boss_group = Group.objects.get(name='Manager')
    hitman.groups.add(boss_group)

post_save.connect(boss_initial_configuration, sender=Boss)


class ManagerHitman(models.Model):
    manager = models.ForeignKey(Boss, related_name='Manager', on_delete=models.CASCADE)
    hitman = models.ForeignKey(CustomUser, related_name='Hitman', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


