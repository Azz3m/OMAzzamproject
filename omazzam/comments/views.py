from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import urllib.parse,urllib.error,urllib.request
from django.http import JsonResponse,HttpResponse
import json
from .models import Comment,Videoinformation,Usersearcher,video_data_url_builder,comments_data_url_builder
import re
import ast


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



def commentsDetail(request,comment_id):
    try:
        user_tags_list = list()
        predefined_tags_list = list()
        comment = get_object_or_404(Comment,pk=comment_id)
        video_id = comment.video_object_id
        video = get_object_or_404(Videoinformation,pk=video_id)
        usersearcher = get_object_or_404(Usersearcher,video_object_id=video_id)
        video_tags = ast.literal_eval(video.tags)

        if video_tags["predefined"]==["NO-TAGS"] and video_tags["userdefined"]==["NO-TAGS"] :
            tags_indicator = False
        elif video_tags["predefined"]!=["NO-TAGS"] and video_tags["userdefined"]==["NO-TAGS"]:
            tags_indicator = True
            for item in video_tags["predefined"]:
                predefined_tags_list.append(item)
        elif video_tags["predefined"]==["NO-TAGS"] and video_tags["userdefined"]!=["NO-TAGS"]:
            tags_indicator = True
            for item in video_tags["userdefined"]:
                user_tags_list.append(item)
        else:
            tags_indicator = True
            for item in video_tags["userdefined"]:
                user_tags_list.append(item)
            tags_indicator = True
            for item in video_tags["predefined"]:
                predefined_tags_list.append(item)

        #texts = json.loads(comment.textDisplay)
        size =  comment.numberOfComments
        texts = comment.textDisplay.split(',')
        authors = comment.authorDisplayName.split(',')
        images = comment.authorProfileImageUrl.split(',')
        channelsURL = comment.authorChannelUrl.split(',')
        dates = comment.updatedAt.split(',')
        comments_details = zip(texts,authors,images,channelsURL,dates)
        watching_url = usersearcher.watching_url
        return render(request,'comments/comments.html',{'status':"success",'comment':comment,'comments_details':comments_details,'size':size,"video":video,"comment_id":comment_id,"comments":comment.textDisplay,"watching_url":watching_url,"user_tags_list":user_tags_list,"predefined_tags_list":predefined_tags_list,"tags_indicator":tags_indicator})
    except :
        return render(request,'comments/comments.html',{'status':"please enter a valid comment_object_id "})



def tagInsertor(request,comment_id):
    video_tags = list()
    predefined_tags = list()
    user_tags = list()
    def repeative_characters_removal(text):
        repeative_chars_pattern = re.compile(r'(\w)\1*',flags=re.UNICODE)
        shaped_string = repeative_chars_pattern.sub(r'\1',text).strip()
        return shaped_string
    if request.method == 'POST':
        tag_list = list()

        comment = get_object_or_404(Comment,pk=comment_id)
        video_id = comment.video_object_id
        video = get_object_or_404(Videoinformation,pk=video_id)
        video_tags = ast.literal_eval(video.tags)
        if request.POST['predefined_tags']:
            predefined_tags_str = request.POST['predefined_tags']
            if predefined_tags_str!="":
                temp = predefined_tags_str.split(',')
                for tag in temp:
                    tag = tag.replace("[","")
                    tag = tag.replace("]","")
                    tag = tag.replace(" '","")
                    tag = tag.replace("'","")
                    tag = tag.lower()
                    tag =repeative_characters_removal(tag)
                    predefined_tags.append(tag)
        else:
            predefined_tags.append("NO-TAGS")

        if request.POST['user_tags']:
            user_tags_str = request.POST['user_tags']
            if user_tags_str!="":
                temp = user_tags_str.split(',')
                for tag in temp:
                    tag = tag.replace("[","")
                    tag = tag.replace("]","")
                    tag = tag.replace(" '","")
                    tag = tag.replace("'","")
                    tag = tag.lower()
                    tag =repeative_characters_removal(tag)
                    user_tags.append(tag)
        else:
            user_tags.append("NO-TAGS")
        video.tags = {"predefined":predefined_tags,"userdefined":user_tags}

        video.save()
        return JsonResponse({'success':video.tags})


    else:
        print("fail")
        return JsonResponse({'fail':'error'})
