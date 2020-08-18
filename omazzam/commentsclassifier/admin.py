from django.contrib import admin
from .models import Langclassifier
from .models import Commentclassifier

# Register your models here.
admin.site.register(Langclassifier)

admin.site.register(Commentclassifier)
