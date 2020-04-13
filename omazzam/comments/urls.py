from django.urls import path, include
from comments import views
urlpatterns = [
    path('commentsdetail/<int:comment_id>', views.commentsdetail, name="commentsdetail"),
    path('commentid/<int:comment_id>', views.getId, name="commentid"),
    ]
