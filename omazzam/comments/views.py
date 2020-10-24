from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import urllib.parse,urllib.error,urllib.request
from django.http import JsonResponse,HttpResponse
from django.core.paginator import Paginator
from itertools import chain
import json
from .models import Comment,Videoinformation,Usersearcher,video_data_url_builder,comments_data_url_builder,Videocategoryclassifier
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
                        status ,video_object = video_object.video_object_creator(user,video_detail_url,video_ID_parameter)
                        if status == True:
                            return render(request, 'comments/home.html',{'error': "eighter the video ID is incorrect or hasn't any comment ,and try again "})

                        else:

                            print("*************** 3 video_details_object created successfuly *************************")

                            video_object.save()


                            print("*************** 4 comment_object creation  *************************")
                            # creating Comment object
                            comments_object = Comment()
                            comments_status,comments_object = comments_object.comment_object_creator(user,user_api,video_object,comment_url,next_token)
                            if comments_status == False:
                                return render(request, 'comments/home.html',{'error': "This video hasn't had any comment yet ,select another one or add comment on it in order to continue "})
                            else:

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


def videoclassifer(request,comment_id):
    video_classifier_indicator = False
    user_tags_list = list()
    predefined_tags_list = list()
    comment = get_object_or_404(Comment,pk=comment_id)
    video_id = comment.video_object_id
    video = get_object_or_404(Videoinformation,pk=video_id)
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
    try :
        video_classified = Videocategoryclassifier.objects.get(video_id=video_id)

        domain = video_classified.video_domain
        video_title = ast.literal_eval(video_classified.video_title)

        video_specification = ast.literal_eval(video_classified.video_specification)


        video_classifier_indicator = True


        context = {
        "comment":comment,
        "tags_indicator":tags_indicator,
        "user_tags_list":user_tags_list,
        "predefined_tags_list":predefined_tags_list,
        "tags_indicator":tags_indicator,
        'video':video,
        'category_dictionary':video.category_dictionary,
        'video_classifier_indicator':video_classifier_indicator,
        'domain':domain,
        'video_title':video_title,
        'video_specification':video_specification,

        }
        return render(request, 'comments/video_classifier.html',context)


    except Videocategoryclassifier.DoesNotExist:
        video_classifier_indicator = False
        context = {
        "comment":comment,
        "tags_indicator":tags_indicator,
        "user_tags_list":user_tags_list,
        "predefined_tags_list":predefined_tags_list,
        "tags_indicator":tags_indicator,
        'video':video,
        'category_dictionary':video.category_dictionary,
        'video_classifier_indicator':video_classifier_indicator,

        }
        return render(request, 'comments/video_classifier.html',context)

#video classification view
def videoclassifed(request,video_id):
    user = request.user
    try:

        video_Object = Videoinformation.objects.get(pk=video_id)
        try :
            video_classified = Videocategoryclassifier.objects.get(video_id=video_id,user=user)
            if request.method == 'POST':
                if request.POST['video_domain'] and request.POST['video_title'] and request.POST['video_specification']:
                    specification_list = list()
                    title_list = list()
                    video_classified.video_domain = request.POST['video_domain']
                    title_list = request.POST['video_title']
                    video_classified.video_title =  title_list.split(',')
                    video_specification = request.POST['video_specification']
                    specification_list = video_specification.split(',')
                    video_classified.video_specification = specification_list
                    video_classified.save()
                    return JsonResponse({'success':"successfuly updated"})
        except Videocategoryclassifier.DoesNotExist:

            if request.method == 'POST':
                if request.POST['video_domain'] and request.POST['video_title'] and request.POST['video_specification']:
                    specification_list = list()
                    title_list = list()
                    video_domain = request.POST['video_domain']
                    video_title = request.POST['video_title']
                    title_list = video_title.split(',')
                    video_specification = request.POST['video_specification']
                    specification_list = video_specification.split(',')
                    video_classified = Videocategoryclassifier()
                    video_classified = video_classified.videocategoryclassifier_creator(user,video_Object,title_list,video_domain,specification_list)
                    video_classified.save()
                    return JsonResponse({'success':"successfuly classified"})

    except Videoinformation.DoesNotExist:
        return JsonResponse({'state':"video object not found"})


    return JsonResponse({'state':'we failed to classify the video'})

#recommandations views

def recommandations(request,video_id):
    try:
        video_Object = Videoinformation.objects.get(pk=video_id)
        video_sets = list()
        video_waching_urls = list()
        video_categories = list()
        video_ids = list()
        video_dates = list()
        if request.method == 'POST':
            if request.POST['video_title']:

                title_list = list()

                title_list = request.POST['video_title']
                try:
                    video_classified = get_object_or_404(Videocategoryclassifier , video_Object = video_Object)
                    video_classified.video_title =  title_list.split(',')
                    video_objects_sets = Videocategoryclassifier.objects.all().order_by('video_title')
                    for video in video_objects_sets:
                        for tag in video_classified.video_title:
                            if tag in video.video_title:
                                video_sets.append(video.video_Object.video_title)
                                video_categories.append(video.video_Object.video_category)
                                temp_user_search = get_object_or_404(Usersearcher,videoInfo= video.video_Object)
                                video_waching_urls.append(temp_user_search.watching_url)
                                video_ids.append(temp_user_search.comment_object_id)
                                video_dates.append(temp_user_search.searching_date_time)

                                break
                            else:
                                pass
                    context = {
                    'state':'success',
                    'video_sets':video_sets,
                    'video_categories':video_categories,
                    'video_waching_urls':video_waching_urls,
                    'video_ids':video_ids,
                    'video_dates':video_dates
                    }

                    return JsonResponse(context)

                except Videocategoryclassifier.DoesNotExist:
                    return JsonResponse({'state':"not-found"})



        return JsonResponse({'state':"successfuly proccessed"})
    except Videoinformation.DoesNotExist:
        return JsonResponse({'state':"fail to proccess"})

#comment Detail View
def commentsdetail(request,comment_id):
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


        watching_url = usersearcher.watching_url




        paginator = Paginator(texts, 1000)
        page = request.GET.get('page')
        texts = paginator.get_page(page)

        paginator2 = Paginator(authors, 1000)
        page2 = request.GET.get('page')
        authors = paginator2.get_page(page2)

        paginator3 = Paginator(images, 1000)
        page3 = request.GET.get('page')
        images = paginator3.get_page(page3)

        paginator4 = Paginator(channelsURL, 1000)
        page4 = request.GET.get('page')
        channelsURL = paginator4.get_page(page4)

        paginator5 = Paginator(dates, 1000)
        page5 = request.GET.get('page')
        dates = paginator5.get_page(page5)

        page_obj = zip(texts,authors,images,channelsURL,dates)
        texts = comment.textDisplay.split(',')
        paginator7 = Paginator(texts, 1000)
        page = request.GET.get('page')
        texts = paginator7.get_page(page)

        context = {
        "status":"success",
        "comment":comment,
        "size":size,
        "video":video,
        "comment_id":comment_id,
        "watching_url":watching_url,
        "user_tags_list":user_tags_list,
        "predefined_tags_list":predefined_tags_list,
        "tags_indicator":tags_indicator,
        'page_obj': page_obj,
        "page":texts
        }
        return render(request,'comments/comments.html',context)
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
                    #tag =repeative_characters_removal(tag)
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
                    #tag =repeative_characters_removal(tag)
                    user_tags.append(tag)
        else:
            user_tags.append("NO-TAGS")
        video.tags = {"predefined":predefined_tags,"userdefined":user_tags}

        video.save()
        return JsonResponse({'success':video.tags})


    else:
        print("fail")
        return JsonResponse({'fail':'error'})
