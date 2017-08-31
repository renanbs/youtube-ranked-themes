from django.contrib import admin

# Register your models here.
from .models import Video, Comment, Thumb

admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Thumb)



