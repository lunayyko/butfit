from django.db                  import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, id, password=None):
        if not id:
            raise ValueError('Users must have an id')

        user = self.model(id=id)

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    pk_id        = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    id           = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=80)

    objects = UserManager()

    USERNAME_FIELD  = 'id'

    def __str__(self):
        return f'{self.id}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    class Meta:
        db_table = 'users'