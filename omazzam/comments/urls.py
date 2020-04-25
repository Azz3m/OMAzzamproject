from django.urls import path, include
from comments import views
urlpatterns = [
    path('commentsdetail/<int:comment_id>', views.commentsDetail, name="commentsdetail"),
    path('tagviewer/<int:comment_id>/', views.tagInsertor, name="tagviewer"),
    ]
