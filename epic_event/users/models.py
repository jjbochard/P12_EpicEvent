from crm.models import Department
from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=12, unique=True, blank=False, null=False)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="departments",
        blank=True,
        null=True,
    )
    date_updated = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        return self.department.name == "Management"

    def has_module_perms(self, app_label):
        return self.department.name == "Management"

    def is_manager(self):
        return self.department_id == 1

    def is_sales(self):
        return self.department_id == 2

    def is_support(self):
        return self.department_id == 4
