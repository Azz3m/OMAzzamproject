from django.urls import path, include
from opinionclassifier import views as oc
from comments import views 
urlpatterns = [
    path('opinionclassifier/<int:commentsclassifier_id>/',oc.opinionclassifier,name='opinionclassifier'),
    path('omdictionariesfetcher/<int:comment_classifier_obj_id>/', oc.omcommentclassifierdictionariesfetcher, name="omdictionariesfetcher"),
    path('omdectionaryviewer/<int:lang_classifier_obj_id>/<str:num_samples>/<str:dic_name>/<str:category>/<str:servicetype>/', oc.omdectionaryviewer, name="omdectionaryviewer"),

    path('explain/',oc.explain,name="explain"),
    ]
