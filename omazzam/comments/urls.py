from django.urls import path, include
from comments import views as cm
urlpatterns = [
    #url_content_details ="https://www.googleapis.com/youtube/v3/videos?id=fS0g9edDIVE&key=AIzaSyC31kvVVjb6TprshW1SMqwN8llGnnim6hc&part=snippet,contentDetails,statistics,status"
    #comment_url = "https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyC31kvVVjb6TprshW1SMqwN8llGnnim6hc&textFormat=plainText&part=snippet&videoId=fS0g9edDIVE&maxResults=100&pageToken="

    #https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=20&q=وائل+كفوري+-+مملكتي+السعيدة&type=video&key=AIzaSyC31kvVVjb6TprshW1SMqwN8llGnnim6hc
    path('commentsdetail/<int:comment_id>', cm.commentsdetail, name="commentsdetail"),
    path('tagviewer/<int:comment_id>/', cm.tagInsertor, name="tagviewer"),
    path('videoclassifer/<int:comment_id>/', cm.videoclassifer, name="videoclassifer"),
    path('videoclassifed/<int:video_id>/', cm.videoclassifed, name="videoclassifed"),
    path('recommandations/<int:video_id>/', cm.recommandations, name="recommandations"),


    ]
