from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import urllib.parse,urllib.error,urllib.request
from django.http import JsonResponse
import json
from .models import Comment,Videoinformation,Usersearcher,video_data_url_builder,comments_data_url_builder




# Create your views here.
def home(request):
        state_for_loader = 'none'
        if request.method == 'POST':
            if request.POST['videoSearch']:
                video_ID_parameter = request.POST['videoSearch']

                user = request.user
                main_url = "https://www.googleapis.com/youtube/v3/"
                user_api = request.user.profile.api_key

                next_token = ""
                video_detail_url = video_data_url_builder(main_url,user_api,video_ID_parameter)
                comment_url = comments_data_url_builder(main_url,user_api,video_ID_parameter,next_token)

                #url_content_details ="https://www.googleapis.com/youtube/v3/videos?id=fS0g9edDIVE&key=AIzaSyC31kvVVjb6TprshW1SMqwN8llGnnim6hc&part=snippet,contentDetails,statistics,status"
                #comment_url = "https://www.googleapis.com/youtube/v3/commentThreads?key=AIzaSyC31kvVVjb6TprshW1SMqwN8llGnnim6hc&textFormat=plainText&part=snippet&videoId=fS0g9edDIVE&maxResults=100&pageToken="
                if Videoinformation.objects.filter(video_ID=video_ID_parameter).exists():
                    video_object = get_object_or_404(Videoinformation, video_ID=video_ID_parameter)
                    if Comment.objects.filter(video_object_id=video_object.id).exists():
                        comments_object = get_object_or_404(Comment,video_object_id=video_object.id)
                        print("we found in datatbase this a comment object ")

                        return redirect("/comments/commentsdetail/"+str(comments_object.id))
                    else:
                        try:

                            print("*************** 3 video_details_object creation  *************************")
                            # creating Videoinformation object
                            video_object = Videoinformation()
                            video_object.video_object_creator(user,video_detail_url,video_ID_parameter)
                            print("*************** 3 video_details_object created successfuly *************************")

                            video_object.save()


                            print("*************** 4 comment_object creation  *************************")
                            # creating Comment object
                            comments_object = Comment()
                            comments_object.comment_object_creator(user,user_api,video_object,comment_url,next_token)

                            comments_object.save()


                            print("*************** 4 comment_object created successfuly *************************")

                            print(" ")

                            print("*************** 5 creating user_search object : \n")
                            # creating Usersearcher object
                            user_search =Usersearcher()
                            user_search.user_search_object_creator(user,video_object,comments_object,video_detail_url,comment_url)
                            user_search.save()
                            print("*************** 5 user_search created successfuly *************************")
                            return redirect("/comments/commentsdetail/"+str(comments_object.id))
                        except:
                            return render(request, 'comments/home.html',{'error':'no internet connection'})

                else:
                    try:

                        print("*************** 3 video_details_object creation  *************************")
                        # creating Videoinformation object
                        video_object = Videoinformation()
                        video_object.video_object_creator(user,video_detail_url,video_ID_parameter)
                        print("*************** 3 video_details_object created successfuly *************************")

                        video_object.save()


                        print("*************** 4 comment_object creation  *************************")
                        # creating Comment object
                        comments_object = Comment()
                        comments_object.comment_object_creator(user,user_api,video_object,comment_url,next_token)

                        comments_object.save()


                        print("*************** 4 comment_object created successfuly *************************")

                        print(" ")

                        print("*************** 5 creating user_search object : \n")
                        # creating Usersearcher object
                        user_search =Usersearcher()
                        user_search.user_search_object_creator(user,video_object,comments_object,video_detail_url,comment_url)
                        user_search.save()
                        print("*************** 5 user_search created successfuly *************************")
                        return redirect("/comments/commentsdetail/"+str(comments_object.id))
                    except:
                        return render(request, 'comments/home.html',{'error':'no internet connection'})


            else:
                return render(request, 'comments/home.html',{'error':"please put a valid youtube's URL or ID"})
        else :
            return render(request, 'comments/home.html')



def commentsdetail(request,comment_id):
    comment = get_object_or_404(Comment,pk=comment_id)
    video_id = comment.video_object_id
    video = get_object_or_404(Videoinformation,pk=video_id)
    #texts = json.loads(comment.textDisplay)
    size =  comment.numberOfComments
    texts = comment.textDisplay.split(',')
    authors = comment.authorDisplayName.split(',')
    images = comment.authorProfileImageUrl.split(',')
    channelsURL = comment.authorChannelUrl.split(',')
    dates = comment.updatedAt.split(',')
    comments_details = zip(texts,authors,images,channelsURL,dates)
    return render(request,'comments/comments.html',{'comments_details':comments_details,'size':size,"video":video,"comment_id":comment_id,"comments":comment.textDisplay})

def getId(request,comment_id):
    try:
        comment = get_object_or_404(Comment,pk=comment_id)
        comments = Comment.objects
        return render(request,'comments\commentsTest.html',{'comment_id':comment_id,'comments':comments,'comment':comment})
    except :
        return JsonResponse({'comment_id':"not found"})
