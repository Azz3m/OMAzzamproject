from django.contrib import admin
from .models import Comment,Videoinformation,Usersearcher,Videocategoryclassifier

# Register your models here.

admin.site.register(Comment)
admin.site.register(Videoinformation)
admin.site.register(Videocategoryclassifier)
admin.site.register(Usersearcher)
