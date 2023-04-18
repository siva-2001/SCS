from django.contrib.auth import models

class User(models.AbstractUser):
    pass
    # REQUIRED_FIELDS = ["email", "first_name", "last_name"]
