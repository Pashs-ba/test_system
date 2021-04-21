from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password):
        user = self.model(username=username, password=password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.model(username=username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
