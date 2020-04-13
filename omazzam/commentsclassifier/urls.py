from django.urls import path, include
from commentsclassifier import views as cs

urlpatterns = [
    path('classify/<int:comment_id>', cs.langcommentsclassifier, name="classify"),
    ]
