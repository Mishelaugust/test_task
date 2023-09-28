from django.db import models
from django.contrib.auth.models import User

# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # Add any additional user-related fields here, if needed


class Product(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    discription = models.TextField()

class UserProductAccess(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    access_status = models.BooleanField(default=False)

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    video_link = models.URLField()
    duration_seconds = models.IntegerField()
    products = models.ManyToManyField(Product, related_name='lessons') # one lesson to many products
    # related_name for access queries

class LessonView(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_id = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    viewed_status = models.BooleanField(default=False)
    viewing_time_seconds = models.IntegerField(default=0)


