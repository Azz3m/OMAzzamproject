from django.urls import path, include
from commentsclassifier import views as cs

urlpatterns = [
    #http://127.0.0.1:8000/commentsclassifier/langclassify/19
    path('langclassify/<int:comment_id>', cs.langcommentsclassifier, name="langclassify"),
    #http://127.0.0.1:8000/commentsclassifier/classify/30
    path('classify/<int:lang_classifier_obj_id>', cs.commentsclassifier, name="classify"),


    path('langdictionariesfetcher/<int:lang_classifier_obj_id>', cs.langdictionariesfetcher, name="langdictionariesfetcher"),
    path('langdectionaryviewer/<int:comment_id>/<str:dic_name>/', cs.langdectionaryviewer, name="langdectionaryviewer"),


    path('dictionariesfetcher/<int:comment_classifier_obj_id>/', cs.commentclassifierdictionariesfetcher, name="dictionariesfetcher"),
    path('dectionaryviewer/<int:lang_classifier_obj_id>/<str:dic_name>/', cs.dectionaryviewer, name="dectionaryviewer"),



    ]
