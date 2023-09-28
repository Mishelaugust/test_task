from django.contrib import admin
from .models import*

admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(LessonView)
admin.site.register(UserProductAccess)

