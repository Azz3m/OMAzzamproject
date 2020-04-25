from django.urls import path, include
from commentsclassifier import views as cs

urlpatterns = [
    #http://127.0.0.1:8000/commentsclassifier/langclassify/19
    path('langclassify/<int:comment_id>', cs.langcommentsclassifier, name="langclassify"),
    #http://127.0.0.1:8000/commentsclassifier/classify/30
    path('classify/<int:lang_classifier_obj_id>', cs.commentsclassifier, name="classify"),

    


    ]
