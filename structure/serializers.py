from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Lesson, LessonView, Product

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = '__all__'

class ProductStatsSerializer(serializers.ModelSerializer):
    num_lessons_viewed = serializers.IntegerField()
    total_viewing_time = serializers.IntegerField()
    num_users_accessing = serializers.IntegerField()
    access_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Product
        fields = ('id', 'title','num_lessons_viewed', 'total_viewing_time', 'num_users_accessing', 'access_percentage')
