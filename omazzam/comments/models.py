from django.db import models
from django.contrib.auth.models import User

#
from django.utils import timezone
import urllib.parse,urllib.error,urllib.request
import json
import re
#Ignore SSL Certificate
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode.CERT_NONE

# Create your models here.

def video_data_url_builder(main_url,user_api,video_ID_parameter):
    return main_url + "videos?id=" + video_ID_parameter + "&key=" + user_api + "&part=snippet,statistics,status"

def comments_data_url_builder(main_url,user_api,video_ID_parameter,next_token):
    return main_url+"commentThreads?key="+ user_api +"&textFormat=plainText&part=snippet&videoId="+ video_ID_parameter +"&maxResults=100&pageToken="+next_token



class Videoinformation(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_at = models.TextField()
    video_ID = models.TextField()
    video_title = models.TextField()
    channel_ID = models.TextField()
    channel_title = models.TextField()
    tags = models.TextField()
    video_desciption = models.TextField()
    statics_view_counts = models.IntegerField()
    statics_like_counts =  models.IntegerField()
    statics_dislike_counts = models.IntegerField()
    statics_comments_counts = models.IntegerField()
    video_category_ID = models.IntegerField()
    category_dictionary ={
        	2 : 'Autos & Vehicles',
        	1 :  'Film & Animation',
        	10 : 'Music',
        	15 : 'Pets & Animals',
        	17 : 'Sports',
        	18 : 'Short Movies',
        	19 : 'Travel & Events',
        	20 : 'Gaming',
        	21 : 'Videoblogging',
        	22 : 'People & Blogs',
        	23 : 'Comedy',
        	24 : 'Entertainment',
        	25 : 'News & Politics',
        	26 : 'Howto & Style',
        	27 : 'Education',
        	28 : 'Science & Technology',
        	29 : 'Nonprofits & Activism',
        	30 : 'Movies',
        	31 : 'Anime/Animation',
        	32 : 'Action/Adventure',
        	33 : 'Classics',
        	34 : 'Comedy',
        	35 : 'Documentary',
        	36 : 'Drama',
        	37 : 'Family',
        	38 : 'Foreign',
        	39 : 'Horror',
        	40 : 'Sci:Fi/Fantasy',
        	41 : 'Thriller',
        	42 : 'Shorts',
        	43 : 'Shows',
        	44 : 'Trailers',
    }
    video_category = models.CharField(max_length=255)
    repeative_chars_pattern = re.compile(r'(\w)\1*',flags=re.UNICODE)

    def repeative_characters_removal(self,text):
        shaped_string = self.repeative_chars_pattern.sub(r'\1',text).strip()
        return shaped_string

    def video_object_creator(self,user,video_detail_url,video_ID_parameter):
        tag_list = list()
        self.user = user
        # fetching video's details
        print('*****************  0   ********************************  0  *********************** *******  \n')
        print ("\n ******* Coded By Azzam Ali ," , "Video ID is : " ,video_ID_parameter ,'*******')
        #print('*****************  1   ********************************  1   *********************** ******* \n')
        #print('******* the very first built comments URL from API  ******* : \n' ,comment_url)
        print('################################################################################### \n')
        print('******* the very first built video detail URL is from API ******* : \n' ,video_detail_url)
        print('*****************     ******************************** *********************** ******* : \n')
        vedio_details_json_recieved = urllib.request.urlopen(video_detail_url).read()
        response_for_video_details = vedio_details_json_recieved.decode("utf-8")
        video_details_processing_recieved = json.loads(response_for_video_details)
        print("*************** 3 video details object creation  *************************")


        self.publish_at = video_details_processing_recieved.get('items')[0]['snippet']['publishedAt']
        self.video_ID = video_details_processing_recieved.get('items')[0]['id']

        self.video_title = video_details_processing_recieved.get('items')[0]['snippet']['title']
        self.channel_ID = video_details_processing_recieved.get('items')[0]['snippet']['channelId']
        self.channel_title = video_details_processing_recieved.get('items')[0]['snippet']['channelTitle']
        try:
            tags_list = video_details_processing_recieved.get('items')[0]['snippet']['tags']
            temp = tags_list
            for tag in temp:
                tag = tag.lower()
                tag = self.repeative_characters_removal(tag)
                tag_list.append(tag)
            self.tags = tag_list
        except:
            print("This video has no tags")
            self.tags = ["NO-TAGS"]
        self.video_desciption = video_details_processing_recieved.get('items')[0]['snippet']['description']
        self.statics_view_counts = video_details_processing_recieved.get('items')[0]['statistics']['viewCount']
        self.statics_like_counts =  video_details_processing_recieved.get('items')[0]['statistics']['likeCount']
        self.statics_dislike_counts = video_details_processing_recieved.get('items')[0]['statistics']['dislikeCount']
        self.statics_comments_counts = video_details_processing_recieved.get('items')[0]['statistics']['commentCount']
        self.video_category_ID = video_details_processing_recieved.get('items')[0]['snippet']['categoryId']
        dictionary = self.category_dictionary
        if int(self.video_category_ID) in dictionary:
            self.video_category = dictionary.get(int(self.video_category_ID))
        else:
            self.video_category = "UNKNOWN CATEGORY"
        #return self


    def __str__(self):
        return self.user.username + " " + self.video_title + " " + self.video_ID



class Comment(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    videoInfo = models.OneToOneField(Videoinformation,on_delete = models.CASCADE)
    video_object_id = models.IntegerField()
    key_api = models.CharField(max_length=255)
    video_id = models.TextField()
    authorDisplayName = models.TextField()
    authorProfileImageUrl = models.TextField()
    authorChannelUrl = models.TextField()
    textDisplay = models.TextField()
    publishedAt = models.TextField()
    updatedAt = models.TextField()
    numberOfComments = models.IntegerField()

    def __str__(self):
        return self.user.username + " " + self.videoInfo.video_title + " " + self.video_id


    def comment_object_creator(self,user,user_api,video_information,comment_url,next_token):

        #fetching video's comments
        #fetching video's comments
        main_url = "https://www.googleapis.com/youtube/v3/"
        comments_json_recieved = urllib.request.urlopen(comment_url).read()
        response_for_comments = comments_json_recieved.decode("utf-8")
        comments_processing_recieved = json.loads(response_for_comments)
        video_id = comments_processing_recieved.get('items')[0].get('snippet').get('topLevelComment').get('snippet').get('videoId')

        comments_list = []
        authors_names_list = []
        authors_image_url_list = []
        authors_profile_url_list = []
        publishedAt_list = []
        updatedAt = []
        i = 0
        if 'nextPageToken' not in comments_processing_recieved:
            print('*****************   4  *************************** 4     *******************  \n')
            print('******** there is NO token , the fetch proccess is statring *************** ')
            for items in comments_processing_recieved.get('items'):
                i += 1
                #making lists of video's comments informations
                clear_comment = items.get('snippet').get('topLevelComment').get('snippet').get('textDisplay')
                clear_comment = clear_comment.replace("'","&rsquo;")
                clear_comment = clear_comment.replace('"',"&rdquo;")
                clear_comment = clear_comment.replace(",","&comma;")
                comments_list.append(clear_comment)
                authors_names_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('authorDisplayName'))
                authors_image_url_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('authorProfileImageUrl'))
                authors_profile_url_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('authorChannelUrl'))
                publishedAt_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('publishedAt'))
                updatedAt.append(items.get('snippet').get('topLevelComment').get('snippet').get('updatedAt'))
            #making comment object

            self.user = user
            self.video_object_id = video_information.id
            self.videoInfo  = video_information
            self.key_api = user_api
            self.video_id = video_id
            self.authorDisplayName = authors_names_list
            self.authorProfileImageUrl = authors_image_url_list
            self.authorChannelUrl = authors_profile_url_list
            self.textDisplay = comments_list
            self.publishedAt = publishedAt_list
            self.updatedAt = updatedAt
            self.numberOfComments = i
            print('*****************     ******************************** *********************** ******* \n')
            print('there is NO token , fetching is finished')
            print('*****************     ******************************** *********************** ******* \n')
            print('we fetch :(  ' ,str(i),'  )comments.')
            print('*****************     ******************************** *********************** *******  \n')



        else:
            index = 1
            print('there is token(s) with code +  (   '+ comments_processing_recieved.get('nextPageToken')[0:6] +'  )......., fetching proccess is statring .....')
            print('*****************  4   ******************************** 4  ********************* \n')
            while 'nextPageToken' in comments_processing_recieved:
                for items in comments_processing_recieved.get('items'):
                    i += 1
                    #making lists of video's comments informations
                    clear_comment = items.get('snippet').get('topLevelComment').get('snippet').get('textDisplay')
                    clear_comment = clear_comment.replace("'","&rsquo;")
                    clear_comment = clear_comment.replace('"',"&rdquo;")
                    clear_comment = clear_comment.replace(",","&comma;")
                    comments_list.append(clear_comment)
                    authors_names_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('authorDisplayName'))
                    authors_image_url_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('authorProfileImageUrl'))
                    authors_profile_url_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('authorChannelUrl'))
                    publishedAt_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('publishedAt'))
                    updatedAt.append(items.get('snippet').get('topLevelComment').get('snippet').get('updatedAt'))
                next_token = comments_processing_recieved.get('nextPageToken')
                comment_url = comments_data_url_builder(main_url,user_api,video_id,next_token)

                index+=1
                print('*****************  5  fetching stage( '+ str(index)+' ) ***********************')
                comments_json_recieved = urllib.request.urlopen(comment_url).read()
                response_for_comments = comments_json_recieved.decode("utf-8")
                comments_processing_recieved = json.loads(response_for_comments)
            if 'nextPageToken' not in comments_processing_recieved:
                print('*****************  6   ******************************** 6 ***************** *******  \n')
                print('***** reaching to the end of page of the comments  , fetching is about to be finished .....')
                for items in comments_processing_recieved.get('items'):
                    i += 1
                    #making lists of video's comments informations
                    clear_comment = items.get('snippet').get('topLevelComment').get('snippet').get('textDisplay')
                    clear_comment = clear_comment.replace("'","&rsquo;")
                    clear_comment = clear_comment.replace('"',"&rdquo;")
                    clear_comment = clear_comment.replace(",","&comma;")
                    comments_list.append(clear_comment)
                    authors_names_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('authorDisplayName'))
                    authors_image_url_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('authorProfileImageUrl'))
                    authors_profile_url_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('authorChannelUrl'))
                    publishedAt_list.append(items.get('snippet').get('topLevelComment').get('snippet').get('publishedAt'))
                    updatedAt.append(items.get('snippet').get('topLevelComment').get('snippet').get('updatedAt'))
            #making comment object

            self.user = user
            self.video_object_id = video_information.id
            self.videoInfo  = video_information
            self.key_api = user_api
            self.video_id = video_id
            self.authorDisplayName = authors_names_list
            self.authorProfileImageUrl = authors_image_url_list
            self.authorChannelUrl = authors_profile_url_list
            self.textDisplay = comments_list
            self.publishedAt = publishedAt_list
            self.updatedAt = updatedAt
            self.numberOfComments = i

            print('*****************     ******************************** *********************** ******* \n')
            print('there is token(s) , fetching is finished')
            print('*****************     ******************************** *********************** ******* \n')
            print('we fetch :(  ' ,str(i),'  )comments.')
            print('*****************     ******************************** *********************** *******  \n')







class Usersearcher(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    videoInfo = models.OneToOneField(Videoinformation,on_delete = models.CASCADE)
    video_object_id = models.IntegerField()
    comment_object_id = models.IntegerField()
    video_ID = models.TextField()
    video_title = models.TextField()
    watching_url = models.TextField()
    key_api = models.TextField()
    content_url_api = models.TextField()
    comments_url_api = models.TextField()
    searching_date_time = models.DateTimeField()

    def __str__(self):
        return self.user.username + " " + self.video_title + " " + self.user.profile.api_key

    def user_search_object_creator(self,user,video_object,comment_object,video_detail_url,comment_url):
        self.user = user
        self.videoInfo = video_object
        self.video_object_id = video_object.id
        self.comment_object_id = comment_object.id
        self.video_ID = video_object.video_ID
        self.video_title = video_object.video_title
        self.watching_url = "https://www.youtube.com/embed/" + video_object.video_ID
        self.key_api = comment_object.key_api
        self.content_url_api = video_detail_url
        self.comments_url_api = comment_url
        self.searching_date_time = timezone.datetime.now()
