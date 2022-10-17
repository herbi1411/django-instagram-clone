from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

PROFILE_PATH = "profile_images"

def profile_image_path(instance, filename): # 반드시 이 2개의 변수 사용
    return f'{PROFILE_PATH}/{instance.username}/{filename}'

class User(AbstractUser):
    profile_image = models.ImageField(default=f"{PROFILE_PATH}/default_profile.png", upload_to=profile_image_path)
    followings = models.ManyToManyField("self", symmetrical=False, related_name="followers")
    about = models.TextField(max_length=200, blank=True)