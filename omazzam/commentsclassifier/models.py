from django.db import models
from django.contrib.auth.models import User
from comments.models import Comment,Videoinformation
from django.shortcuts import get_object_or_404
import polyglot
from polyglot.detect import Detector
from nltk.tokenize import sent_tokenize,word_tokenize
import pyarabic.araby as araby
from langdetect import detect
import re,ast

# Create your models here.

class Langclassifier(models.Model):


    #instance variables of the model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_Object = models.OneToOneField(Videoinformation, on_delete=models.CASCADE)
    comment_object = models.OneToOneField(Comment, on_delete=models.CASCADE)
    video_ObjectID =  models.IntegerField()
    comment_objID = models.IntegerField()
    emoji_comment_dic = models.TextField()
    pure_emoji_dic = models.TextField()
    emoji_pure_arabic_dic = models.TextField()
    emoji_pure_english_dic = models.TextField()
    emoji_mixed_lang_dic = models.TextField()
    emoji_arabic_with_others_dic = models.TextField()
    emoji_english_with_others_dic =models.TextField()
    emoji_ar_en_dic = models.TextField()
    emoji_exceptions_dic = models.TextField()
    emoji_other_language_dic = models.TextField()
    emoji_useless_comment_dic = models.TextField()
    pure_arabic_dic = models.TextField()
    pure_english_dic = models.TextField()
    mixed_lang_dic = models.TextField()
    exceptions_dic = models.TextField()
    other_language_dic = models.TextField()
    useless_comment_dic = models.TextField()
    arabic_with_others_dic = models.TextField()
    english_with_others_dic = models.TextField()
    ar_en_dic = models.TextField()

    #patterns for the regular expressions
    only_chars_pattern = re.compile(r'[\u0600-\u06ff]|[\u0750-\u077f]|[\ufb50-\ufbc1]|[\ufbd3-\ufd3f]|[\ufd50-\ufd8f]|[\ufd92-\ufdc7]|[\ufe70-\ufefc]|[\uFDF0-\uFDFD]|[a-zA-Z]',flags=re.UNICODE)
    special_chars_pattern =  re.compile(r"[-()\"#\[\]/@;:<>{}\'+=~|.!?’,]",flags=re.UNICODE)
    emoji_pattern = re.compile(r'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])|(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])|[\U00010000-\U0010ffff]', flags=re.UNICODE)
    only_digits_pattern = re.compile(r'[0-9]',flags=re.UNICODE)
    repeative_chars_pattern = re.compile(r'(\w)\1*',flags=re.UNICODE)
    #functions of the model language Type Detectors
       # English language Detection
    def pure_english_detector(self,text):
      language_string = ""
      for language in Detector(text).languages:
        language_string += " " + str(language)
      if language_string.find("code: en") != -1 and language_string.find("code: ar") == -1:
        #print("English language detected")
        language_string = ""
        return True
      return False
       # Arabic language Detection
    def pure_arabic_detector(self,text):
      language_string = ""
      for language in Detector(text).languages:
        language_string += " " + str(language)
      if language_string.find("code: ar") != -1 and language_string.find("code: en") == -1:
          language_string = ""
          return True
      return False

       # English & Arabic languages Detection
    def mixed_ar_en_detector(self,text):
      language_string = ""
      for language in Detector(text).languages:
        #print(language)
        language_string += " " + str(language)
      if language_string.find("code: ar") != -1 and language_string.find("code: en") != -1:
        #print("mixed language detected")
        language_string = ""
        return True
      return False

       # text among one single world (Arabic & English) language Detection
    def lang_detector_among_one_word(self,text):
        english = False
        arabic = False
        mixed = False
        for word in word_tokenize(text):
            try:
                if detect(word) == 'en':
                    english = True

                if detect(word) == 'ar':
                    arabic = True
            except:
                pass
        if english == False and arabic == False:
            return "not_found" , "not_found"
        if english == True and arabic == True:
            mixed = True
            ar_en_dic = text
            return "mixed", ar_en_dic
        else:
            mixed=False
            if english == True and arabic == False:
                english_with_others_dic = text
                return "eng_with_other", english_with_others_dic
            if english == False and arabic == True:
                arabic_with_others_dic = text
                return "ar_with_other", arabic_with_others_dic



       # emoji Detection
    def emoji_detector(self,text):
        if self.emoji_pattern.search(text) == None:
            return False
        else:
            return True

       # pure alphabetic character text checker
    def special_chars_digits_removal(self,text):
        special_chars_removed = re.sub(self.special_chars_pattern,'',text).strip()
        digits_removed = re.sub(self.only_digits_pattern,'',special_chars_removed).strip()
        if digits_removed.strip():
            return True , digits_removed.strip()
        else:
            return False ,"False"

        #repeative_characters_removal
    def repeative_characters_removal(self,text):
        shaped_string = self.repeative_chars_pattern.sub(r'\1',text).strip()
        return shaped_string
        #two word bugs fixer
    def two_words_detect_bug(self,text):
        extend_comment_list = text.split(" ") + text.split(" ") +text.split(" ")
        new_single_comment = " ".join(str(x) for x in extend_comment_list)
        return new_single_comment
        # text with emoji processing
    def txt_with_emoji_processing(self,text):
        emoji_removed = re.sub(self.emoji_pattern,"",text).strip()
        special_chars_removed = re.sub(self.special_chars_pattern,'',emoji_removed).strip()
        digits_removed = re.sub(self.only_digits_pattern,'',special_chars_removed).strip()
        if digits_removed.strip():
            return True
        else:
            return False

        #pure emoji finder
    def pure_emoji(self,text):
        if self.only_chars_pattern.search(text) == None:
            return "found",text
        else:
            return "not_found", "not_found"

    def reshaping(self,list):

        temp = list.replace("'","")
        temp = temp.replace("[","")
        temp = temp.replace("]","")
        return temp


    def comments_lang_classifier(self,user,comment_id):

        #vaibles to hold the data
        #print("setting up variables for comments_classifier proccess  .....")
        total_processed = 0
        emoji_comment_dic = {}
        pure_emoji_dic={}
        emoji_pure_arabic_dic = {}
        emoji_pure_english_dic = {}
        emoji_mixed_lang_dic = {}
        emoji_arabic_with_others_dic={}
        emoji_english_with_others_dic ={}
        emoji_ar_en_dic={}
        emoji_exceptions_dic = {}
        emoji_other_language_dic ={}
        emoji_useless_comment_dic={}
        pure_arabic_dic = {}
        pure_english_dic = {}
        mixed_lang_dic = {}
        exceptions_dic = {}
        other_language_dic ={}
        useless_comment_dic={}
        arabic_with_others_dic={}
        english_with_others_dic ={}
        ar_en_dic={}
        comment_obj_indexer = "not_found"
        try:
            print("try getting comments object from database ......")
            comment_obj = get_object_or_404(Comment,pk=comment_id)
            comment_obj_indexer = "found"
            print("we found Comment object under : ", comment_obj)


            #print("getting comments object from database ......")
        except :
            print("we couldn't find any Comment object with id:( " + str(comment_id) + " ) in database ")





        if comment_obj_indexer == "found":
            print("classifier object not found : Try to create a new object .....")
            comment_obj = get_object_or_404(Comment,pk=comment_id)
            print("we found comment object under : ", comment_obj)

            comments_list = comment_obj.textDisplay.split(',')


            authors_list  = comment_obj.authorDisplayName
            urls_list  = comment_obj.authorChannelUrl
            images_list  = comment_obj.authorProfileImageUrl
            dates_list  = comment_obj.updatedAt

            authors_list =self.reshaping(authors_list)
            urls_list =self.reshaping(urls_list)
            images_list =self.reshaping(images_list)
            dates_list =self.reshaping(dates_list)
            authors_list  = authors_list.split(',')
            urls_list  = urls_list.split(',')
            images_list  = images_list.split(',')
            dates_list  = dates_list.split(',')




            i=0
            print("comments_classifier based on languages & emojis started .....")
            index = -1
            for single_comment in comments_list:
                i+=1
                index += 1
                single_comment =self.reshaping(single_comment)
                single_comment = single_comment.lower()
                single_comment = self.repeative_characters_removal(single_comment)
                single_comment = single_comment.replace("’","")
                print(str(i)+"  processing comment : ",single_comment)

                author = authors_list[index]
                url = urls_list[index]
                img = images_list[index]
                date = dates_list[index]

                if len(single_comment.split(" "))>2:
                    if self.emoji_detector(single_comment) == False:
                        processed = single_comment.replace("&comma;"," ")
                        processed = processed.replace("&rsquo;"," ")
                        processed =processed.replace("&rdquo;"," ")

                        indicator , shaped_string = self.special_chars_digits_removal(processed)
                        try:
                            if indicator == True:

                                if self.pure_english_detector(shaped_string) == True :
                                    pure_english_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                                    #print(str(i) + " *** pure_english **** " , single_comment)
                                if self.pure_arabic_detector(shaped_string) == True :
                                    pure_arabic_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":araby.strip_tashkeel(single_comment),"i":i}
                                    #print(str(i) + " ***  pure_arabic **** " , single_comment)
                                if self.mixed_ar_en_detector(shaped_string) == True :
                                    mixed_lang_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                                    #print(str(i) + " *** mixed_ar_en_detector *** " , single_comment)
                                if self.mixed_ar_en_detector(shaped_string) == False and self.pure_arabic_detector(shaped_string) == False and self.pure_english_detector(shaped_string) == False:
                                    other_language_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}

                                    #print(str(i) +"other language detected : " , single_comment)
                                ##print(str(i) + " *** cause a problem *** " , single_comment)
                            else :
                                useless_comment_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}

                        except:

                            indicator , temp =self.lang_detector_among_one_word(araby.strip_tashkeel(single_comment))
                            if indicator == "mixed":
                                ar_en_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                            elif indicator == "eng_with_other":
                                english_with_others_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                            elif indicator == "ar_with_other":
                                arabic_with_others_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                            else:
                                other_language_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                            #print(str(i) + " (error in detection language) Need more processing ",single_comment)

                            #print(str(i) +"useless comment ")

                    else:
                        emoji_comment_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                        emoji_indictor ,emoji_temp = self.pure_emoji(single_comment)
                        if emoji_indictor == "found":
                            pure_emoji_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                        else:
                            if self.txt_with_emoji_processing(single_comment) == True:
                                emoji_removed = re.sub(self.emoji_pattern,"",single_comment).strip()
                                try:

                                    if self.pure_english_detector(emoji_removed) == True :
                                        emoji_pure_english_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                                        #print(str(i) + " *** pure_english **** " , single_comment)
                                    if self.pure_arabic_detector(emoji_removed) == True :
                                        emoji_pure_arabic_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":araby.strip_tashkeel(single_comment),"i":i}
                                        #emoji_pure_arabic_dic[i] = single_comment
                                        #print(str(i) + " ***  pure_arabic **** " , single_comment)
                                    if self.mixed_ar_en_detector(emoji_removed) == True :
                                        emoji_mixed_lang_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                                        #print(str(i) + " *** mixed_ar_en_detector *** " , single_comment)
                                    if self.mixed_ar_en_detector(emoji_removed) == False and self.pure_arabic_detector(emoji_removed) == False and self.pure_english_detector(emoji_removed) == False:
                                        emoji_other_language_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}



                                        #print(str(i) +"other language detected : " , single_comment)
                                    ##print(str(i) + " *** cause a problem *** " , single_comment)
                                except :
                                    emoji_exceptions_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                                    indicator , temp = self.lang_detector_among_one_word(single_comment)
                                    if indicator == "mixed":
                                        ar_en_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                                    elif indicator == "eng_with_other":
                                        english_with_others_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                                    elif indicator == "ar_with_other":
                                        arabic_with_others_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                                    else:
                                        other_language_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}



                            #print(str(i) + " (Emoji detected)  Need more processing  : ",single_comment)

                else:
                    new_single_comment = self.two_words_detect_bug(single_comment)
                    if self.emoji_detector(new_single_comment) == False:
                        processed = new_single_comment.replace("&comma;"," ")
                        processed = processed.replace("&rsquo;"," ")
                        processed =processed.replace("&rdquo;"," ")

                        indicator , shaped_string = self.special_chars_digits_removal(processed)
                        if indicator == True:

                            #single_comment = strip_emoji(single_comment)
                            try:
                                if self.pure_english_detector(shaped_string) == True :
                                    pure_english_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                                    #print(str(i) + " *** pure_english **** " , single_comment)
                                if self.pure_arabic_detector(shaped_string) == True :
                                    pure_arabic_dic[i] ={"author":author,"url":url,"img":img,"date":date,"single_comment":araby.strip_tashkeel(single_comment),"i":i}
                                    #print(str(i) + " ***  pure_arabic **** " , single_comment)
                                if self.mixed_ar_en_detector(shaped_string) == True :
                                    mixed_lang_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                                    #print(str(i) + " *** mixed_ar_en_detector *** " , single_comment)
                                if self.mixed_ar_en_detector(shaped_string) == False and self.pure_arabic_detector(shaped_string) == False and self.pure_english_detector(shaped_string) == False:
                                    other_language_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}


                                    #print(str(i) +"other language detected : " , single_comment)
                                ##print(str(i) + " *** cause a problem *** " , single_comment)
                            except :

                                indicator , temp = self.lang_detector_among_one_word(single_comment)
                                if indicator == "mixed":
                                    ar_en_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                                elif indicator == "eng_with_other":
                                    english_with_others_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                                elif indicator == "ar_with_other":
                                    arabic_with_others_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                                else:
                                    other_language_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                        else:
                            useless_comment_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                            #print(str(i) +"useless comment " , single_comment)


                    else:
                        emoji_comment_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                        emoji_indictor ,emoji_temp = self.pure_emoji(single_comment)
                        if emoji_indictor == "found":
                            pure_emoji_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                        else:
                            if self.txt_with_emoji_processing(single_comment) == True:
                                emoji_removed = re.sub(self.emoji_pattern,"",single_comment).strip()
                                try:

                                    if self.pure_english_detector(emoji_removed) == True :
                                        emoji_pure_english_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                                        #print(str(i) + " *** pure_english **** " , single_comment)
                                    if self.pure_arabic_detector(emoji_removed) == True :
                                        emoji_pure_arabic_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":araby.strip_tashkeel(single_comment),"i":i}
                                        #print(str(i) + " ***  pure_arabic **** " , single_comment)
                                    if self.mixed_ar_en_detector(emoji_removed) == True :
                                        emoji_mixed_lang_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}
                                        #print(str(i) + " *** mixed_ar_en_detector *** " , single_comment)
                                    if self.mixed_ar_en_detector(emoji_removed) == False and self.pure_arabic_detector(emoji_removed) == False and self.pure_english_detector(emoji_removed) == False:
                                        emoji_other_language_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}


                                        #print(str(i) +"other language detected : " , single_comment)
                                    ##print(str(i) + " *** cause a problem *** " , single_comment)
                                except :

                                    indicator , temp = self.lang_detector_among_one_word(single_comment)
                                    if indicator == "mixed":
                                        ar_en_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                                    elif indicator == "eng_with_other":
                                        english_with_others_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                                    elif indicator == "ar_with_other":
                                        arabic_with_others_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":temp,"i":i}
                                    else:
                                        emoji_other_language_dic[i] = {"author":author,"url":url,"img":img,"date":date,"single_comment":single_comment,"i":i}



            print("start getting video object from database")
            video_object_id = comment_obj.video_object_id
            video_information_object = get_object_or_404(Videoinformation,pk=video_object_id)
            print(" video object getted successfully ")
            print("creates comments_classifier object ")

            self.user = user
            self.video_Object = video_information_object
            self.comment_object = comment_obj
            self.video_ObjectID = video_information_object.id
            self.comment_objID = comment_obj.id
            self.emoji_comment_dic = emoji_comment_dic
            self.pure_emoji_dic = pure_emoji_dic
            self.emoji_pure_arabic_dic = emoji_pure_arabic_dic
            self.emoji_pure_english_dic = emoji_pure_english_dic
            self.emoji_mixed_lang_dic = emoji_mixed_lang_dic
            self.emoji_arabic_with_others_dic = emoji_arabic_with_others_dic
            self.emoji_english_with_others_dic =emoji_english_with_others_dic
            self.emoji_ar_en_dic = emoji_ar_en_dic
            self.emoji_exceptions_dic = emoji_exceptions_dic
            self.emoji_other_language_dic = emoji_other_language_dic
            self.emoji_useless_comment_dic = emoji_useless_comment_dic
            self.pure_arabic_dic = pure_arabic_dic
            self.pure_english_dic = pure_english_dic
            self.mixed_lang_dic = mixed_lang_dic
            self.exceptions_dic = exceptions_dic
            self.other_language_dic = other_language_dic
            self.useless_comment_dic = useless_comment_dic
            self.arabic_with_others_dic = arabic_with_others_dic
            self.english_with_others_dic = english_with_others_dic
            self.ar_en_dic = ar_en_dic


            print("comments_classifier object created successfully")

            print("redirecting to comment classifier page ....... ")
            total_processed = len(self.pure_arabic_dic) + len(self.pure_english_dic) + len(self.mixed_lang_dic) + len(self.exceptions_dic) + len(self.mixed_lang_dic)+ len(self.other_language_dic)+ len(self.useless_comment_dic)+ len(self.arabic_with_others_dic)+ len(self.english_with_others_dic)+ len(self.ar_en_dic)+ len(self.emoji_comment_dic)
            print(total_processed)
            comment_classifier = self
            return {"state":"created","comment_classifier":comment_classifier}
            #print("getting comments object from database ......")
        else:
            return {"state":"not_found"}



    def __str__(self):
        return " username: " +self.user.username + " /// video_title: " + self.video_Object.video_title + " /// key_api: " + self.comment_object.key_api

class Commentclassifier(models.Model):
        #instance variables of the model

        user = models.ForeignKey(User, on_delete=models.CASCADE)
        video_Object = models.OneToOneField(Videoinformation, on_delete=models.CASCADE)
        comment_object = models.OneToOneField(Comment, on_delete=models.CASCADE)
        langcommentsclassifier = models.OneToOneField(Langclassifier, on_delete=models.CASCADE)
        video_ObjectID =  models.IntegerField()
        comment_objID = models.IntegerField()
        emoji_comment_dic = models.TextField()
        pure_emoji_dic = models.TextField()
        emoji_pure_arabic_dic = models.TextField()
        emoji_pure_english_dic = models.TextField()
        emoji_mixed_lang_dic = models.TextField()
        emoji_arabic_with_others_dic = models.TextField()
        emoji_english_with_others_dic =models.TextField()
        emoji_ar_en_dic = models.TextField()
        emoji_exceptions_dic = models.TextField()
        emoji_other_language_dic = models.TextField()
        emoji_useless_comment_dic = models.TextField()
        pure_arabic_dic = models.TextField()
        pure_english_dic = models.TextField()
        mixed_lang_dic = models.TextField()
        exceptions_dic = models.TextField()
        other_language_dic = models.TextField()
        useless_comment_dic = models.TextField()
        arabic_with_others_dic = models.TextField()
        english_with_others_dic = models.TextField()
        ar_en_dic = models.TextField()




        def comments_classifier(self,user,lang_classifier_obj_id):
            lang_classifier_obj = get_object_or_404(Langclassifier,pk=lang_classifier_obj_id)
            video_information_object = lang_classifier_obj.video_Object
            comment_obj = lang_classifier_obj.comment_object
            self.user = user
            self.video_Object = video_information_object
            self.comment_object = comment_obj
            self.video_ObjectID = video_information_object.id
            self.comment_objID = comment_obj.id
            self.langcommentsclassifier = lang_classifier_obj
            emoji_comment_dic = {}
            pure_emoji_dic={}
            emoji_pure_arabic_dic = {}
            emoji_pure_english_dic = {}
            emoji_mixed_lang_dic = {}
            emoji_arabic_with_others_dic={}
            emoji_english_with_others_dic ={}
            emoji_ar_en_dic={}
            emoji_exceptions_dic = {}
            emoji_other_language_dic ={}
            emoji_useless_comment_dic={}
            pure_arabic_dic = {}
            pure_english_dic = {}
            mixed_lang_dic = {}
            exceptions_dic = {}
            other_language_dic ={}
            useless_comment_dic={}
            arabic_with_others_dic={}
            english_with_others_dic ={}
            ar_en_dic={}

            emoji_comment_dic = ast.literal_eval(lang_classifier_obj.emoji_comment_dic)
            pure_emoji_dic=ast.literal_eval(lang_classifier_obj.pure_emoji_dic)
            emoji_pure_arabic_dic = ast.literal_eval(lang_classifier_obj.emoji_pure_arabic_dic)
            emoji_pure_english_dic = ast.literal_eval(lang_classifier_obj.emoji_pure_english_dic)
            emoji_mixed_lang_dic = ast.literal_eval(lang_classifier_obj.emoji_mixed_lang_dic)
            emoji_arabic_with_others_dic=ast.literal_eval(lang_classifier_obj.emoji_arabic_with_others_dic)
            emoji_english_with_others_dic =ast.literal_eval(lang_classifier_obj.emoji_english_with_others_dic)
            emoji_ar_en_dic=ast.literal_eval(lang_classifier_obj.emoji_ar_en_dic)
            emoji_exceptions_dic = ast.literal_eval(lang_classifier_obj.emoji_exceptions_dic)
            emoji_other_language_dic =ast.literal_eval(lang_classifier_obj.emoji_other_language_dic)
            emoji_useless_comment_dic=ast.literal_eval(lang_classifier_obj.emoji_useless_comment_dic)
            pure_arabic_dic = ast.literal_eval(lang_classifier_obj.pure_arabic_dic)
            pure_english_dic = ast.literal_eval(lang_classifier_obj.pure_english_dic)
            mixed_lang_dic = ast.literal_eval(lang_classifier_obj.mixed_lang_dic)
            exceptions_dic = ast.literal_eval(lang_classifier_obj.exceptions_dic)
            other_language_dic =ast.literal_eval(lang_classifier_obj.other_language_dic)
            useless_comment_dic=ast.literal_eval(lang_classifier_obj.useless_comment_dic)
            arabic_with_others_dic=ast.literal_eval(lang_classifier_obj.arabic_with_others_dic)
            english_with_others_dic =ast.literal_eval(lang_classifier_obj.english_with_others_dic)
            ar_en_dic=ast.literal_eval(lang_classifier_obj.ar_en_dic)

            tags=ast.literal_eval(video_information_object.tags)
            user_tags = tags['userdefined']
            predefined_tags = tags['predefined']


            for item in pure_english_dic:
                index = pure_english_dic[item]['i']
                single_comment = pure_english_dic[item]['single_comment']

                if len(predefined_tags) ==1 and  predefined_tags[0] == "NO-TAGS" :
                    pass
                else:
                    for tag in predefined_tags:
                        if tag in single_comment:
                            print(str(index) +" predefined ("+tag +") "+str(single_comment.count(tag))+" ",single_comment)
                        else:
                            pass
                if len(user_tags) ==1 and  user_tags[0] == "NO-TAGS" :
                    pass
                else:
                    for tag in user_tags:
                        if tag in single_comment:
                            print(str(index) + " userdefined ("+tag +") "+str(single_comment.count(tag))+" ",single_comment)
                        else:
                            pass



            return self

        def __str__(self):
            return " username: " +self.user.username + " /// video_title: " + self.video_Object.video_title + " /// key_api: " + self.comment_object.key_api






# test of the language detect process
'''
    #patterns for the regular expressions
    only_chars = re.compile(r'[\u0600-\u06ff]|[\u0750-\u077f]|[\ufb50-\ufbc1]|[\ufbd3-\ufd3f]|[\ufd50-\ufd8f]|[\ufd92-\ufdc7]|[\ufe70-\ufefc]|[\uFDF0-\uFDFD]|[a-zA-Z]',flags=re.UNICODE)
    special_chars =  re.compile(r"[-()\"#\[\]/@;:<>{}\'+=~|.!?,]",flags=re.UNICODE)
    emoji_pattern = re.compile(r'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])|(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])|[\U00010000-\U0010ffff]', flags=re.UNICODE)
    only_digits = re.compile(r'[0-9]',flags=re.UNICODE)
      # English language Detection
    def pure_english_detector(text):
      language_string = ""
      for language in Detector( text).languages:
        language_string += " " + str(language)
      if language_string.find("code: en") != -1 and language_string.find("code: ar") == -1:
        ##print("English language detected")
        language_string = ""
        return True
      return False
       # Arabic language Detection
    def pure_arabic_detector(text):
      language_string = ""
      for language in Detector(text).languages:
        language_string += " " + str(language)
      if language_string.find("code: ar") != -1 and language_string.find("code: en") == -1:
          language_string = ""
          return True
      return False

       # English & Arabic languages Detection
    def mixed_ar_en_detector(text):
      language_string = ""
      for language in Detector(text).languages:
        ##print(language)
        language_string += " " + str(language)
      if language_string.find("code: ar") != -1 and language_string.find("code: en") != -1:
        ##print("mixed language detected")
        language_string = ""
        return True
      return False

       # text among one single world (Arabic & English) language Detection
    def lang_detector_among_one_word(text):
        english = False
        arabic = False
        mixed = False
        for word in word_tokenize(text):
            try:
                if detect(word) == 'en':
                    english = True

                if detect(word) == 'ar':
                    arabic = True
            except:
                pass
        if english == False and arabic == False:
            return "not_found" , "not_found"
        if english == True and arabic == True:
            mixed = True
            ar_en = text
            return "mixed", ar_en
        else:
            mixed=False
            if english == True and arabic == False:
                english_with_others = text
                return "eng_with_other", english_with_others
            if english == False and arabic == True:
                arabic_with_others = text
                return "ar_with_other", arabic_with_others



       # emoji Detection
    def emoji_detector(text):
        if emoji_pattern.search(text) == None:
            return False
        else:
            return True

       # pure alphabetic character text checker
    def special_chars_digits_removal(text):
        special_chars_removed = re.sub(special_chars,'',text).strip()
        digits_removed = re.sub(only_digits,'',special_chars_removed).strip()
        if digits_removed.strip():
            return True , digits_removed.strip()
        else:
            return False ,"False"
        #two word bugs fixer
    def two_words_detect_bug(text):
        extend_comment_list = text.split(" ") + text.split(" ") +text.split(" ")
        new_single_comment = " ".join(str(x) for x in extend_comment_list)
        return new_single_comment
        # text with emoji processing
    def txt_with_emoji_processing(text):
        emoji_removed = re.sub(emoji_pattern,"",text).strip()
        special_chars_removed = re.sub(special_chars,'',emoji_removed).strip()
        digits_removed = re.sub(only_digits,'',special_chars_removed).strip()
        if digits_removed.strip():
            return True
        else:
            return False

        #pure emoji finder
    def pure_emoji(text):
        if only_chars.search(text) == None:
            return "found",text
        else:
            return "not_found", "not_found"

    print("Coded By Eng.Azzam Ali")
    print("******************************")
    mixed_text = u"""
    China (simplified Chinese: 中国; traditional Chinese: 中國),
    officially the People's Republic of China (PRC), is a sovereign state located in East Asia.
    الكاتب : المهندس عزام عزيز علي
    """

    pure_arabic = u""" مرحبا كيف الحال , عزام علي """
    pure_english = u""" Hi how are you doing? Mr.Azzam ,I'm new to opinion mining."""


    print(" ======  pure_arabic  text ===== ")
    print(pure_arabic )
    print("")
    print(" ====== Testing three functions for pure_arabic ===== ")
    print("self.pure_english_detector : ",self.pure_english_detector(pure_arabic))
    print("self.pure_arabic_detector : ",self.pure_arabic_detector(pure_arabic))
    print("self.mixed_ar_en_detector : ",self.mixed_ar_en_detector(pure_arabic))

    print("")
    print(" ====== pure_english text ===== ")
    print(pure_english)
    print("")
    print(" ====== Testing three functions for pure_english ===== ")
    print("self.pure_english_detector : ",self.pure_english_detector(pure_english))
    print("self.pure_arabic_detector : ",self.pure_arabic_detector(pure_english))
    print("self.mixed_ar_en_detector : ",self.mixed_ar_en_detector(pure_english))
    print("")
    print(" ====== mixed_text text ===== ")
    print(mixed_text)
    print("self.pure_english_detector : ",self.pure_english_detector(mixed_text))
    print("self.pure_arabic_detector : ",self.pure_arabic_detector(mixed_text))
    print("self.mixed_ar_en_detector : ",self.mixed_ar_en_detector(mixed_text))
'''
