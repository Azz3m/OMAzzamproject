from django.db import models
from django.contrib.auth.models import User
from comments.models import Comment,Videoinformation,Videocategoryclassifier
from django.shortcuts import get_object_or_404
import polyglot
from django.http import JsonResponse
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

    def dictionay_length_pairs(self,state,lang_classifier):
        print("creating dictionay_length_pairs ")
        dictionay_length_pairs = {}
        if state == 'found':

            pure_emoji_dic=ast.literal_eval(lang_classifier.pure_emoji_dic)
            emoji_pure_arabic_dic = ast.literal_eval(lang_classifier.emoji_pure_arabic_dic)
            emoji_pure_english_dic = ast.literal_eval(lang_classifier.emoji_pure_english_dic)
            emoji_mixed_lang_dic = ast.literal_eval(lang_classifier.emoji_mixed_lang_dic)
            emoji_arabic_with_others_dic=ast.literal_eval(lang_classifier.emoji_arabic_with_others_dic)
            emoji_english_with_others_dic =ast.literal_eval(lang_classifier.emoji_english_with_others_dic)
            emoji_ar_en_dic=ast.literal_eval(lang_classifier.emoji_ar_en_dic)
            emoji_exceptions_dic = ast.literal_eval(lang_classifier.emoji_exceptions_dic)
            emoji_other_language_dic =ast.literal_eval(lang_classifier.emoji_other_language_dic)
            emoji_useless_comment_dic=ast.literal_eval(lang_classifier.emoji_useless_comment_dic)
            pure_arabic_dic = ast.literal_eval(lang_classifier.pure_arabic_dic)
            pure_english_dic = ast.literal_eval(lang_classifier.pure_english_dic)
            mixed_lang_dic = ast.literal_eval(lang_classifier.mixed_lang_dic)
            exceptions_dic = ast.literal_eval(lang_classifier.exceptions_dic)
            other_language_dic =ast.literal_eval(lang_classifier.other_language_dic)
            useless_comment_dic=ast.literal_eval(lang_classifier.useless_comment_dic)
            arabic_with_others_dic=ast.literal_eval(lang_classifier.arabic_with_others_dic)
            english_with_others_dic =ast.literal_eval(lang_classifier.english_with_others_dic)
            ar_en_dic=ast.literal_eval(lang_classifier.ar_en_dic)

            dictionay_length_pairs = {
            'English' : len(emoji_pure_english_dic) + len(pure_english_dic) + len(emoji_english_with_others_dic) + len(english_with_others_dic),
            'pure_emoji' : len(pure_emoji_dic),
            'Arabic' : len(emoji_pure_arabic_dic) + len(arabic_with_others_dic) + len(pure_arabic_dic) + len(emoji_arabic_with_others_dic),

            'Mix' : len(emoji_mixed_lang_dic) + len(mixed_lang_dic) + len(ar_en_dic) + len(emoji_ar_en_dic),
            'Others' : len(other_language_dic) + len(emoji_other_language_dic) ,

            'useless_and_exceptions' : len(emoji_exceptions_dic) + len(emoji_useless_comment_dic) + len(useless_comment_dic) + len(exceptions_dic),
            }
        else:
            dictionay_length_pairs = {
            'English': len(lang_classifier.emoji_pure_english_dic) + len(lang_classifier.pure_english_dic) + len(lang_classifier.emoji_english_with_others_dic) + len(lang_classifier.english_with_others_dic),
            'pure_emoji' : len(lang_classifier.pure_emoji_dic),
            'Arabic' : len(lang_classifier.emoji_pure_arabic_dic) + len(lang_classifier.arabic_with_others_dic) + len(lang_classifier.pure_arabic_dic) + len(lang_classifier.emoji_arabic_with_others_dic),
            'Mix' : len(lang_classifier.emoji_mixed_lang_dic) + len(lang_classifier.mixed_lang_dic) + len(lang_classifier.ar_en_dic) + len(lang_classifier.emoji_ar_en_dic),
            'Others' : len(lang_classifier.other_language_dic) + len(lang_classifier.emoji_other_language_dic) ,
            'useless_and_exceptions' : len(lang_classifier.emoji_exceptions_dic) + len(lang_classifier.emoji_useless_comment_dic) + len(lang_classifier.useless_comment_dic) + len(lang_classifier.exceptions_dic),
            }
        print("dictionay_length_pairs created successfully")
        return dictionay_length_pairs

    def dictionary_among_one_category(self,category,lang_classifier):

        pure_emoji_dic=ast.literal_eval(lang_classifier.pure_emoji_dic)
        emoji_pure_arabic_dic = ast.literal_eval(lang_classifier.emoji_pure_arabic_dic)
        emoji_pure_english_dic = ast.literal_eval(lang_classifier.emoji_pure_english_dic)
        emoji_mixed_lang_dic = ast.literal_eval(lang_classifier.emoji_mixed_lang_dic)
        emoji_arabic_with_others_dic=ast.literal_eval(lang_classifier.emoji_arabic_with_others_dic)
        emoji_english_with_others_dic =ast.literal_eval(lang_classifier.emoji_english_with_others_dic)
        emoji_ar_en_dic=ast.literal_eval(lang_classifier.emoji_ar_en_dic)
        emoji_exceptions_dic = ast.literal_eval(lang_classifier.emoji_exceptions_dic)
        emoji_other_language_dic =ast.literal_eval(lang_classifier.emoji_other_language_dic)
        emoji_useless_comment_dic=ast.literal_eval(lang_classifier.emoji_useless_comment_dic)
        pure_arabic_dic = ast.literal_eval(lang_classifier.pure_arabic_dic)
        pure_english_dic = ast.literal_eval(lang_classifier.pure_english_dic)
        mixed_lang_dic = ast.literal_eval(lang_classifier.mixed_lang_dic)
        exceptions_dic = ast.literal_eval(lang_classifier.exceptions_dic)
        other_language_dic =ast.literal_eval(lang_classifier.other_language_dic)
        useless_comment_dic=ast.literal_eval(lang_classifier.useless_comment_dic)
        arabic_with_others_dic=ast.literal_eval(lang_classifier.arabic_with_others_dic)
        english_with_others_dic =ast.literal_eval(lang_classifier.english_with_others_dic)
        ar_en_dic=ast.literal_eval(lang_classifier.ar_en_dic)
        dic = {}
        if category == 'English':
            dic = {}
            print("English")
            dic = {
            'emoji_pure_english_dic' :len(emoji_pure_english_dic) ,
            'pure_english_dic': len(pure_english_dic) ,
            'emoji_english_with_others_dic':len(emoji_english_with_others_dic) ,
            'english_with_others_dic': len(english_with_others_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic
        if category == 'pure_emoji':
            dic = {}
            dic = {
            'pure_emoji' : len(pure_emoji_dic),
            }
            print("dictionay_length_pairs created successfully")
            return dic
        if category == 'Arabic':
            dic = {}
            dic = {
            'emoji_pure_arabic_dic' : len(emoji_pure_arabic_dic) ,
            'arabic_with_others_dic' : len(arabic_with_others_dic) ,
            'pure_arabic_dic' : len(pure_arabic_dic) ,
            'emoji_arabic_with_others_dic' : len(emoji_arabic_with_others_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic
        if category == 'Mix':
            dic = {}
            dic = {
            'emoji_mixed_lang_dic' : len(emoji_mixed_lang_dic) ,
            'mixed_lang_dic' :len(mixed_lang_dic) ,
            'ar_en_dic' : len(ar_en_dic) ,
            'emoji_ar_en_dic' :len(emoji_ar_en_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic
        if category == 'Others':
            dic = {}
            dic = {
            'other_language_dic' : len(other_language_dic) ,
            'emoji_other_language_dic': len(emoji_other_language_dic)
            }
            print("dictionay_length_pairs created successfully")
            return dic
        if category == 'useless_and_exceptions':
            dic = {}
            dic = {
            'emoji_exceptions_dic' :   len(emoji_exceptions_dic) ,
            'emoji_useless_comment_dic' :   len(emoji_useless_comment_dic) ,
            'useless_comment_dic'  :  len(useless_comment_dic) ,
            'exceptions_dic' :    len(exceptions_dic),
            }
            print("dictionay_length_pairs created successfully")
            return dic


    def comments_lang_classifier(self,user,comment_id):

        #vaibles to hold the data
        #print("setting up variables for comments_classifier Process  .....")
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
                #single_comment = self.repeative_characters_removal(single_comment)
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
            print("creating dictionay_length_pairs ")
            dictionay_length_pairs = {
            'English' : len(emoji_pure_english_dic) + len(pure_english_dic) + len(emoji_english_with_others_dic) + len(english_with_others_dic),
            'pure_emoji' : len(pure_emoji_dic),
            'Arabic' : len(emoji_pure_arabic_dic) + len(arabic_with_others_dic) + len(pure_arabic_dic) + len(emoji_arabic_with_others_dic),

            'Mix' : len(emoji_mixed_lang_dic) + len(mixed_lang_dic) + len(ar_en_dic) + len(emoji_ar_en_dic),
            'Others' : len(other_language_dic) + len(emoji_other_language_dic) ,

            'useless_and_exceptions' : len(emoji_exceptions_dic) + len(emoji_useless_comment_dic) + len(useless_comment_dic) + len(exceptions_dic),

            }
            print("dictionay_length_pairs created successfully")
            print("redirecting to comment classifier page ....... ")
            total_processed = len(self.pure_arabic_dic) + len(self.pure_english_dic) + len(self.mixed_lang_dic) + len(self.exceptions_dic) + len(self.mixed_lang_dic)+ len(self.other_language_dic)+ len(self.useless_comment_dic)+ len(self.arabic_with_others_dic)+ len(self.english_with_others_dic)+ len(self.ar_en_dic)+ len(self.emoji_comment_dic)
            print(total_processed)
            lang_classifier = self
            return {"state":"created","lang_classifier":lang_classifier}
            #print("getting comments object from database ......")
        else:
            return {"state":"not_found"}

    def dictionary_viewer(self,lang_classifier_obj,dictionary_name):
        status = False
        dictionary = {}
        video_Object = None
        tags_indicator = False
        predefined_tags_list = list()
        user_tags_list = list()

        if dictionary_name == 'pure_english_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.pure_english_dic)
            status = True
        if dictionary_name == 'pure_emoji_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.pure_emoji_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'pure_arabic_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.pure_arabic_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'mixed_lang_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.mixed_lang_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'emoji_pure_arabic_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.emoji_pure_arabic_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'emoji_pure_english_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.emoji_pure_english_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'emoji_mixed_lang_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.emoji_mixed_lang_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'emoji_arabic_with_others_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.emoji_arabic_with_others_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'emoji_english_with_others_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.emoji_english_with_others_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'emoji_ar_en_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.emoji_ar_en_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'emoji_exceptions_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.emoji_exceptions_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'emoji_other_language_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.emoji_other_language_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'ar_en_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.ar_en_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'english_with_others_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.english_with_others_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'arabic_with_others_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.arabic_with_others_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'other_language_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.other_language_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'exceptions_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.exceptions_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'emoji_useless_comment_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.emoji_useless_comment_dic)
            video_Object = lang_classifier_obj.video_Object
            status = True
        if dictionary_name == 'useless_comment_dic':
            dictionary = ast.literal_eval(lang_classifier_obj.useless_comment_dic)
            video_Object = lang_classifier_obj.video_Object

            status = True

        return status,dictionary,video_Object

    def dictionary_fetcher(self,dic_name,lang_classifier_obj):
        dictionary_name = dic_name

        if dictionary_name == 'pure_english_dic':
            return True,len(lang_classifier_obj.pure_english_dic)
        if dictionary_name == 'pure_arabic_dic':
            return True,len(lang_classifier_obj.pure_arabic_dic)
        if dictionary_name == 'ar_en_dic':
            return True,len(lang_classifier_obj.ar_en_dic)
        if dictionary_name == 'english_with_others_dic':
            return True,len(lang_classifier_obj.english_with_others_dic)
        if dictionary_name == 'arabic_with_others_dic':
            return True,len(lang_classifier_obj.arabic_with_others_dic)
        if dictionary_name == 'mixed_lang_dic':
            return True,len(lang_classifier_obj.mixed_lang_dic)
        if dictionary_name == 'other_language_dic':
            return True,len(lang_classifier_obj.other_language_dic)
        if dictionary_name == 'exceptions_dic':
            return True,len(lang_classifier_obj.exceptions_dic)
        if dictionary_name == 'pure_emoji_dic':
            return True,len(lang_classifier_obj.pure_emoji_dic)
        if dictionary_name == 'emoji_pure_arabic_dic':
            return True,len(lang_classifier_obj.emoji_pure_arabic_dic)
        if dictionary_name == 'emoji_pure_english_dic':
            return True,len(lang_classifier_obj.emoji_pure_english_dic)
        if dictionary_name == 'emoji_arabic_with_others_dic':
            return True,len(lang_classifier_obj.emoji_arabic_with_others_dic)
        if dictionary_name == 'emoji_english_with_others_dic':
            return True,len(lang_classifier_obj.emoji_english_with_others_dic)
        if dictionary_name == 'emoji_ar_en_dic':
            return True,len(lang_classifier_obj.emoji_ar_en_dic)
        if dictionary_name == 'emoji_mixed_lang_dic':
            return True,len(lang_classifier_obj.emoji_mixed_lang_dic)
        if dictionary_name == 'emoji_other_language_dic':
            return True,len(lang_classifier_obj.emoji_other_language_dic)
        if dictionary_name == 'emoji_exceptions_dic':
            return True,len(lang_classifier_obj.emoji_exceptions_dic)
        if dictionary_name == 'emoji_english_with_others_dic':
            return True,len(lang_classifier_obj.emoji_english_with_others_dic)
        if dictionary_name == 'emoji_useless_comment_dic':
            return True,len(lang_classifier_obj.emoji_useless_comment_dic)
        if dictionary_name == 'useless_comment_dic':
            return True,len(lang_classifier_obj.useless_comment_dic)
        else:
            return False,0

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
        langcommentsclassifier_objID = models.IntegerField()
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

        r = re.compile(r'\b%s\b' % "is", re.I)
    #begin comments_classifier

        def video_titles_linker(self,tag,video_titles_sets,video_id):
            video_list = list()


            for video in video_titles_sets:
                if tag in ast.literal_eval(video.video_title):
                    if video_id == video.id:
                        pass
                    else:
                        video_list.append(video.id)
                else:
                    pass




            return video_list


        def video_specifications_comment_linker(self,tag,video_specification_sets,video_id):
            video_list = list()


            for video in video_specification_sets:
                if tag in ast.literal_eval(video.video_specification):
                    if video_id == video.id:
                        #temp = get_object_or_404(Videocategoryclassifier,pk=video.id)
                        video_list.append(video.id)
                    else:
                        pass

                else:
                    pass




            return video_list

        def comment_classifier_among_video_classfier(self,dic,video_title,video_specification,video_id):
            video_titles_sets = Videocategoryclassifier.objects.all().order_by('video_title')
            video_specification_sets = Videocategoryclassifier.objects.all().order_by('video_specification')
            tags_list = list()
            total_comments_tags = 0

            comments_tags_details_dic ={}
            for item in dic:
                index = dic[item]['i']
                single_comment = dic[item]['single_comment']

                if len(video_specification) ==1 and  video_specification[0] == "NO-TAGS" :
                    pass
                else:
                    begin_list =list()
                    end_list =list()
                    video_specification_repeat = list()

                    tags_list = list()
                    for tag in video_specification:
                        if tag in single_comment:
                            dic[item]['video_specification_linker'] = self.video_specifications_comment_linker(tag,video_specification_sets,video_id)
                            total_comments_tags += 1
                            tags_list.append(tag)
                            dic[item]['video_specification'] = tags_list
                            video_specification_repeat.append(single_comment.count(tag))
                            dic[item]['video_specification_repeat'] = video_specification_repeat
                            dic[item]['video_specification_pack'] = None
                            for m in re.finditer(tag, single_comment):
                                begin_temp = m.start()
                                end_temp = m.end()
                                begin_list.append(begin_temp)
                                end_list.append(end_temp)
                                dic[item]['begin'] = begin_list
                                dic[item]['end'] = end_list


                            print(str(index) +" predefined ("+tag +") "+str(single_comment.count(tag))+" ",single_comment)
                        else:
                            pass
                if len(video_title) ==1 and  video_title[0] == "NO-TAGS" :
                    pass
                else:
                    begin_list =list()
                    end_list =list()
                    tags_list = list()
                    video_title_repeat = list()
                    for tag in video_title:
                        if tag in single_comment:

                            dic[item]['video_titles_linker'] = self.video_titles_linker(tag,video_titles_sets,video_id)


                            total_comments_tags += 1
                            tags_list.append(tag)
                            dic[item]['video_title'] = tags_list
                            video_title_repeat.append(single_comment.count(tag))
                            dic[item]['video_title_repeat'] = video_title_repeat
                            dic[item]['video_title_pack'] = None
                            for m in re.finditer(tag, single_comment):
                                begin_temp = m.start()
                                end_temp = m.end()
                                begin_list.append(begin_temp)
                                end_list.append(end_temp)
                                dic[item]['begin'] = begin_list
                                dic[item]['end'] = end_list
                                dic[item]['begin'] = m.start()
                                dic[item]['end'] = m.end()
                            print(str(index) + " video_title ("+tag +") "+str(single_comment.count(tag))+" ",single_comment)

                        else:
                            pass
            return dic





    #end
    # begin
        def tag_classifier(self,dic,user_tags,predefined_tags):

            tags_list = list()
            total_comments_tags = 0

            comments_tags_details_dic ={}
            for item in dic:
                index = dic[item]['i']
                single_comment = dic[item]['single_comment']

                if len(predefined_tags) ==1 and  predefined_tags[0] == "NO-TAGS" :
                    pass
                else:
                    begin_list =list()
                    end_list =list()
                    predefined_tag_repeat = list()
                    user_tag_repeat = list()
                    tags_list = list()
                    for tag in predefined_tags:
                        if tag in single_comment:

                            total_comments_tags += 1
                            tags_list.append(tag)
                            dic[item]['predefined'] = tags_list
                            predefined_tag_repeat.append(single_comment.count(tag))
                            dic[item]['predefined_tag_repeat'] = predefined_tag_repeat
                            dic[item]['predefined_pack'] = None
                            for m in re.finditer(tag, single_comment):
                                begin_temp = m.start()
                                end_temp = m.end()
                                begin_list.append(begin_temp)
                                end_list.append(end_temp)
                                dic[item]['begin'] = begin_list
                                dic[item]['end'] = end_list


                            print(str(index) +" predefined ("+tag +") "+str(single_comment.count(tag))+" ",single_comment)
                        else:
                            pass
                if len(user_tags) ==1 and  user_tags[0] == "NO-TAGS" :
                    pass
                else:
                    begin_list =list()
                    end_list =list()
                    tags_list = list()
                    user_tag_repeat = list()
                    for tag in user_tags:
                        if tag in single_comment:


                            total_comments_tags += 1
                            tags_list.append(tag)
                            dic[item]['userdefined'] = tags_list
                            user_tag_repeat.append(single_comment.count(tag))
                            dic[item]['user_tag_repeat'] = user_tag_repeat
                            dic[item]['userdefined_pack'] = None
                            for m in re.finditer(tag, single_comment):
                                begin_temp = m.start()
                                end_temp = m.end()
                                begin_list.append(begin_temp)
                                end_list.append(end_temp)
                                dic[item]['begin'] = begin_list
                                dic[item]['end'] = end_list
                                dic[item]['begin'] = m.start()
                                dic[item]['end'] = m.end()
                            print(str(index) + " userdefined ("+tag +") "+str(single_comment.count(tag))+" ",single_comment)

                        else:
                            pass
            return dic
        def get_length(self,lang_classifier_obj):
            length = 0
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
            length += len(pure_emoji_dic) +  len(other_language_dic) +  len(arabic_with_others_dic) +  len(exceptions_dic) +  len(mixed_lang_dic) +  len(emoji_mixed_lang_dic)
            length +=   len(emoji_pure_english_dic) +  len(emoji_pure_arabic_dic) +  len(emoji_useless_comment_dic) +  len(emoji_other_language_dic) +  len(emoji_exceptions_dic) +  len(emoji_english_with_others_dic) +  len(emoji_arabic_with_others_dic)
            length +=   len(ar_en_dic) +  len(english_with_others_dic) +  len(useless_comment_dic) +  len(emoji_arabic_with_others_dic) +  len(pure_english_dic) +  len(pure_arabic_dic) +  len(emoji_ar_en_dic)
            return length

        def get_length(self,lang_classifier_obj):
            length = 0
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
            length += len(pure_emoji_dic) +  len(other_language_dic) +  len(arabic_with_others_dic) +  len(exceptions_dic) +  len(mixed_lang_dic) +  len(emoji_mixed_lang_dic)
            length +=   len(emoji_pure_english_dic) +  len(emoji_pure_arabic_dic) +  len(emoji_useless_comment_dic) +  len(emoji_other_language_dic) +  len(emoji_exceptions_dic) +  len(emoji_english_with_others_dic) +  len(emoji_arabic_with_others_dic)
            length +=   len(ar_en_dic) +  len(english_with_others_dic) +  len(useless_comment_dic) +  len(emoji_arabic_with_others_dic) +  len(pure_english_dic) +  len(pure_arabic_dic) +  len(emoji_ar_en_dic)
            return length

        def tag_list_setter(self,video_Object):
            predefined_tags_list = list()
            user_tags_list = list()

            video_tags = ast.literal_eval(video_Object.tags)
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
            return tags_indicator,predefined_tags_list,user_tags_list

        def dic_tag_pack_viewer(self,dictionary):
            user_defined_repeat =list()
            user_defined_list = list()
            for item in dictionary:
                for tag_info in dictionary[item]:
                    if 'userdefined' in tag_info:

                        user_defined_list  = dictionary[item]['userdefined']

                        user_defined_repeat = dictionary[item]['user_tag_repeat']
                        zipped_userdefined_tags = zip(user_defined_list,user_defined_repeat)
                        dictionary[item]['userdefined_pack'] = zipped_userdefined_tags


            predefined_repeat_list =list()
            predefined_list = list()
            for item in dictionary:
                for tag_info in dictionary[item]:
                    if 'predefined' in tag_info:
                        predefined_list  = dictionary[item]['predefined']

                        predefined_repeat_list = dictionary[item]['predefined_tag_repeat']
                        zipped_predefined_tags = zip(predefined_list,predefined_repeat_list)
                        dictionary[item]['predefined_pack'] = zipped_predefined_tags
            return dictionary

        def dictionay_length_pairs(self,state,comment_classifier):
            print("creating dictionay_length_pairs ")
            if state == 'found':

                pure_emoji_dic=ast.literal_eval(comment_classifier.pure_emoji_dic)
                emoji_pure_arabic_dic = ast.literal_eval(comment_classifier.emoji_pure_arabic_dic)
                emoji_pure_english_dic = ast.literal_eval(comment_classifier.emoji_pure_english_dic)
                emoji_mixed_lang_dic = ast.literal_eval(comment_classifier.emoji_mixed_lang_dic)
                emoji_arabic_with_others_dic=ast.literal_eval(comment_classifier.emoji_arabic_with_others_dic)
                emoji_english_with_others_dic =ast.literal_eval(comment_classifier.emoji_english_with_others_dic)
                emoji_ar_en_dic=ast.literal_eval(comment_classifier.emoji_ar_en_dic)
                emoji_exceptions_dic = ast.literal_eval(comment_classifier.emoji_exceptions_dic)
                emoji_other_language_dic =ast.literal_eval(comment_classifier.emoji_other_language_dic)
                emoji_useless_comment_dic=ast.literal_eval(comment_classifier.emoji_useless_comment_dic)
                pure_arabic_dic = ast.literal_eval(comment_classifier.pure_arabic_dic)
                pure_english_dic = ast.literal_eval(comment_classifier.pure_english_dic)
                mixed_lang_dic = ast.literal_eval(comment_classifier.mixed_lang_dic)
                exceptions_dic = ast.literal_eval(comment_classifier.exceptions_dic)
                other_language_dic =ast.literal_eval(comment_classifier.other_language_dic)
                useless_comment_dic=ast.literal_eval(comment_classifier.useless_comment_dic)
                arabic_with_others_dic=ast.literal_eval(comment_classifier.arabic_with_others_dic)
                english_with_others_dic =ast.literal_eval(comment_classifier.english_with_others_dic)
                ar_en_dic=ast.literal_eval(comment_classifier.ar_en_dic)

                dictionay_length_pairs = {
                'English' : len(emoji_pure_english_dic) + len(pure_english_dic) + len(emoji_english_with_others_dic) + len(english_with_others_dic),
                'pure_emoji' : len(pure_emoji_dic),
                'Arabic' : len(emoji_pure_arabic_dic) + len(arabic_with_others_dic) + len(pure_arabic_dic) + len(emoji_arabic_with_others_dic),

                'Mix' : len(emoji_mixed_lang_dic) + len(mixed_lang_dic) + len(ar_en_dic) + len(emoji_ar_en_dic),
                'Others' : len(other_language_dic) + len(emoji_other_language_dic) ,

                'useless_and_exceptions' : len(emoji_exceptions_dic) + len(emoji_useless_comment_dic) + len(useless_comment_dic) + len(exceptions_dic),
                }
            else:
                dictionay_length_pairs = {
                'English': len(comment_classifier.emoji_pure_english_dic) + len(comment_classifier.pure_english_dic) + len(comment_classifier.emoji_english_with_others_dic) + len(comment_classifier.english_with_others_dic),
                'pure_emoji' : len(comment_classifier.pure_emoji_dic),
                'Arabic' : len(comment_classifier.emoji_pure_arabic_dic) + len(comment_classifier.arabic_with_others_dic) + len(comment_classifier.pure_arabic_dic) + len(comment_classifier.emoji_arabic_with_others_dic),
                'Mix' : len(comment_classifier.emoji_mixed_lang_dic) + len(comment_classifier.mixed_lang_dic) + len(comment_classifier.ar_en_dic) + len(comment_classifier.emoji_ar_en_dic),
                'Others' : len(comment_classifier.other_language_dic) + len(comment_classifier.emoji_other_language_dic) ,
                'useless_and_exceptions' : len(comment_classifier.emoji_exceptions_dic) + len(comment_classifier.emoji_useless_comment_dic) + len(comment_classifier.useless_comment_dic) + len(comment_classifier.exceptions_dic),
                }
            print("dictionay_length_pairs created successfully")
            return dictionay_length_pairs

        def dictionary_among_one_category(self,category,lang_classifier):

            pure_emoji_dic=ast.literal_eval(lang_classifier.pure_emoji_dic)
            emoji_pure_arabic_dic = ast.literal_eval(lang_classifier.emoji_pure_arabic_dic)
            emoji_pure_english_dic = ast.literal_eval(lang_classifier.emoji_pure_english_dic)
            emoji_mixed_lang_dic = ast.literal_eval(lang_classifier.emoji_mixed_lang_dic)
            emoji_arabic_with_others_dic=ast.literal_eval(lang_classifier.emoji_arabic_with_others_dic)
            emoji_english_with_others_dic =ast.literal_eval(lang_classifier.emoji_english_with_others_dic)
            emoji_ar_en_dic=ast.literal_eval(lang_classifier.emoji_ar_en_dic)
            emoji_exceptions_dic = ast.literal_eval(lang_classifier.emoji_exceptions_dic)
            emoji_other_language_dic =ast.literal_eval(lang_classifier.emoji_other_language_dic)
            emoji_useless_comment_dic=ast.literal_eval(lang_classifier.emoji_useless_comment_dic)
            pure_arabic_dic = ast.literal_eval(lang_classifier.pure_arabic_dic)
            pure_english_dic = ast.literal_eval(lang_classifier.pure_english_dic)
            mixed_lang_dic = ast.literal_eval(lang_classifier.mixed_lang_dic)
            exceptions_dic = ast.literal_eval(lang_classifier.exceptions_dic)
            other_language_dic =ast.literal_eval(lang_classifier.other_language_dic)
            useless_comment_dic=ast.literal_eval(lang_classifier.useless_comment_dic)
            arabic_with_others_dic=ast.literal_eval(lang_classifier.arabic_with_others_dic)
            english_with_others_dic =ast.literal_eval(lang_classifier.english_with_others_dic)
            ar_en_dic=ast.literal_eval(lang_classifier.ar_en_dic)

            if category == 'English':
                print("English")
                dic = {
                'emoji_pure_english_dic' :len(emoji_pure_english_dic) ,
                'pure_english_dic': len(pure_english_dic) ,
                'emoji_english_with_others_dic':len(emoji_english_with_others_dic) ,
                'english_with_others_dic': len(english_with_others_dic)
                }
                print("dictionay_length_pairs created successfully")
                return dic
            if category == 'pure_emoji':
                dic = {
                'pure_emoji' : len(pure_emoji_dic),
                }
                print("dictionay_length_pairs created successfully")
                return dic
            if category == 'Arabic':
                dic = {
                'emoji_pure_arabic_dic' : len(emoji_pure_arabic_dic) ,
                'arabic_with_others_dic' : len(arabic_with_others_dic) ,
                'pure_arabic_dic' : len(pure_arabic_dic) ,
                'emoji_arabic_with_others_dic' : len(emoji_arabic_with_others_dic)
                }
                print("dictionay_length_pairs created successfully")
                return dic
            if category == 'Mix':
                dic = {
                'emoji_mixed_lang_dic' : len(emoji_mixed_lang_dic) ,
                'mixed_lang_dic' :len(mixed_lang_dic) ,
                'ar_en_dic' : len(ar_en_dic) ,
                'emoji_ar_en_dic' :len(emoji_ar_en_dic)
                }
                print("dictionay_length_pairs created successfully")
                return dic
            if category == 'Others':
                dic = {
                'other_language_dic' : len(other_language_dic) ,
                'emoji_other_language_dic': len(emoji_other_language_dic)
                }
                print("dictionay_length_pairs created successfully")
                return dic
            if category == 'useless_and_exceptions':
                dic = {
                'emoji_exceptions_dic' :   len(emoji_exceptions_dic) ,
                'emoji_useless_comment_dic' :   len(emoji_useless_comment_dic) ,
                'useless_comment_dic'  :  len(useless_comment_dic) ,
                'exceptions_dic' :    len(exceptions_dic),
                }
                print("dictionay_length_pairs created successfully")
                return dic


        def dictionary_related_videos(self,dictionary):
            dic = {}
            video_titles_linker = 0
            video_specification_linker = 0
            for key,item in dictionary.items():
                if 'video_titles_linker' in item:
                    video_titles_linker += 1
                if 'video_specification_linker'in item:
                    video_specification_linker += 1
            return video_titles_linker, video_specification_linker

        def comments_classifier(self,user,lang_classifier_obj_id):
            lang_classifier_obj = get_object_or_404(Langclassifier,pk=lang_classifier_obj_id)
            video_classified_obj = get_object_or_404(Videocategoryclassifier,video_Object=lang_classifier_obj.video_Object)
            video_information_object = lang_classifier_obj.video_Object
            comment_obj = lang_classifier_obj.comment_object
            self.user = user
            self.video_Object = video_information_object
            self.comment_object = comment_obj
            self.video_ObjectID = video_information_object.id
            self.comment_objID = comment_obj.id
            self.langcommentsclassifier = lang_classifier_obj
            self.langcommentsclassifier_objID = lang_classifier_obj.id
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
            self.emoji_comment_dic = self.tag_classifier(emoji_comment_dic,user_tags,predefined_tags)
            self.pure_emoji_dic = self.tag_classifier(pure_emoji_dic,user_tags,predefined_tags)
            self.pure_english_dic = self.tag_classifier(pure_english_dic,user_tags,predefined_tags)
            self.pure_arabic_dic = self.tag_classifier(pure_arabic_dic,user_tags,predefined_tags)
            self.mixed_lang_dic = self.tag_classifier(mixed_lang_dic,user_tags,predefined_tags)
            self.emoji_pure_arabic_dic = self.tag_classifier(emoji_pure_arabic_dic,user_tags,predefined_tags)
            self.emoji_pure_english_dic =self.tag_classifier(emoji_pure_english_dic,user_tags,predefined_tags)
            self.emoji_mixed_lang_dic = self.tag_classifier(emoji_mixed_lang_dic,user_tags,predefined_tags)
            self.emoji_arabic_with_others_dic = self.tag_classifier(emoji_arabic_with_others_dic,user_tags,predefined_tags)
            self.emoji_english_with_others_dic = self.tag_classifier(emoji_english_with_others_dic,user_tags,predefined_tags)
            self.emoji_ar_en_dic = self.tag_classifier(emoji_ar_en_dic,user_tags,predefined_tags)
            self.emoji_exceptions_dic = self.tag_classifier(emoji_exceptions_dic,user_tags,predefined_tags)
            self.emoji_other_language_dic = self.tag_classifier(emoji_other_language_dic,user_tags,predefined_tags)
            self.emoji_useless_comment_dic= self.tag_classifier(emoji_useless_comment_dic,user_tags,predefined_tags)
            self.exceptions_dic = self.tag_classifier(exceptions_dic,user_tags,predefined_tags)
            self.other_language_dic = self.tag_classifier(other_language_dic,user_tags,predefined_tags)
            self.useless_comment_dic= self.tag_classifier(useless_comment_dic,user_tags,predefined_tags)
            self.arabic_with_others_dic= self.tag_classifier(arabic_with_others_dic,user_tags,predefined_tags)
            self.english_with_others_dic = self.tag_classifier(english_with_others_dic,user_tags,predefined_tags)
            self.ar_en_dic = self.tag_classifier(ar_en_dic,user_tags,predefined_tags)


            video_title = ast.literal_eval(video_classified_obj.video_title)
            video_specification = ast.literal_eval(video_classified_obj.video_specification)
            video_id = self.video_ObjectID
            self.emoji_comment_dic = self.comment_classifier_among_video_classfier(emoji_comment_dic,video_title,video_specification,video_id)
            self.pure_emoji_dic = self.comment_classifier_among_video_classfier(pure_emoji_dic,video_title,video_specification,video_id)
            self.pure_english_dic = self.comment_classifier_among_video_classfier(pure_english_dic,video_title,video_specification,video_id)
            self.pure_arabic_dic = self.comment_classifier_among_video_classfier(pure_arabic_dic,video_title,video_specification,video_id)
            self.mixed_lang_dic = self.comment_classifier_among_video_classfier(mixed_lang_dic,video_title,video_specification,video_id)
            self.emoji_pure_arabic_dic = self.comment_classifier_among_video_classfier(emoji_pure_arabic_dic,video_title,video_specification,video_id)
            self.emoji_pure_english_dic =self.comment_classifier_among_video_classfier(emoji_pure_english_dic,video_title,video_specification,video_id)
            self.emoji_mixed_lang_dic = self.comment_classifier_among_video_classfier(emoji_mixed_lang_dic,video_title,video_specification,video_id)
            self.emoji_arabic_with_others_dic = self.comment_classifier_among_video_classfier(emoji_arabic_with_others_dic,video_title,video_specification,video_id)
            self.emoji_english_with_others_dic = self.comment_classifier_among_video_classfier(emoji_english_with_others_dic,video_title,video_specification,video_id)
            self.emoji_ar_en_dic = self.comment_classifier_among_video_classfier(emoji_ar_en_dic,video_title,video_specification,video_id)
            self.emoji_exceptions_dic = self.comment_classifier_among_video_classfier(emoji_exceptions_dic,video_title,video_specification,video_id)
            self.emoji_other_language_dic = self.comment_classifier_among_video_classfier(emoji_other_language_dic,video_title,video_specification,video_id)
            self.emoji_useless_comment_dic= self.comment_classifier_among_video_classfier(emoji_useless_comment_dic,video_title,video_specification,video_id)
            self.exceptions_dic = self.comment_classifier_among_video_classfier(exceptions_dic,video_title,video_specification,video_id)
            self.other_language_dic = self.comment_classifier_among_video_classfier(other_language_dic,video_title,video_specification,video_id)
            self.useless_comment_dic= self.comment_classifier_among_video_classfier(useless_comment_dic,video_title,video_specification,video_id)
            self.arabic_with_others_dic= self.comment_classifier_among_video_classfier(arabic_with_others_dic,video_title,video_specification,video_id)
            self.english_with_others_dic = self.comment_classifier_among_video_classfier(english_with_others_dic,video_title,video_specification,video_id)
            self.ar_en_dic = self.comment_classifier_among_video_classfier(ar_en_dic,video_title,video_specification,video_id)

            comment_classifier = self


            return comment_classifier




        def dictionary_viewer(self,comment_classifier_obj,dictionary_name):
            status = False
            dictionary = {}
            video_Object = None
            tags_indicator = False
            predefined_tags_list = list()
            user_tags_list = list()

            if dictionary_name == 'pure_english_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.pure_english_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True


            if dictionary_name == 'pure_emoji_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.pure_emoji_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'pure_arabic_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.pure_arabic_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'mixed_lang_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.mixed_lang_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'emoji_pure_arabic_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.emoji_pure_arabic_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'emoji_pure_english_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.emoji_pure_english_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'emoji_mixed_lang_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.emoji_mixed_lang_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'emoji_arabic_with_others_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.emoji_arabic_with_others_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'emoji_english_with_others_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.emoji_english_with_others_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'emoji_ar_en_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.emoji_ar_en_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'emoji_exceptions_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.emoji_exceptions_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'emoji_other_language_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.emoji_other_language_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

            if dictionary_name == 'ar_en_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.ar_en_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True
            if dictionary_name == 'english_with_others_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.english_with_others_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True
            if dictionary_name == 'arabic_with_others_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.arabic_with_others_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True
            if dictionary_name == 'other_language_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.other_language_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True
            if dictionary_name == 'exceptions_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.exceptions_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True
            if dictionary_name == 'emoji_useless_comment_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.emoji_useless_comment_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True
            if dictionary_name == 'useless_comment_dic':

                dictionary = ast.literal_eval(comment_classifier_obj.useless_comment_dic)

                video_Object = comment_classifier_obj.video_Object
                tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)

                dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
                status = True

# begin

            return status,dictionary,video_Object,tags_indicator,predefined_tags_list,user_tags_list


        def dictionary_fetcher(self,dic_name,comment_classifier_obj):
            dictionary_name = dic_name
            if dictionary_name == 'pure_english_dic':
                return True,len(comment_classifier_obj.pure_english_dic)
            if dictionary_name == 'pure_arabic_dic':
                return True,len(comment_classifier_obj.pure_arabic_dic)
            if dictionary_name == 'ar_en_dic':
                return True,len(comment_classifier_obj.ar_en_dic)
            if dictionary_name == 'english_with_others_dic':
                return True,len(comment_classifier_obj.english_with_others_dic)
            if dictionary_name == 'arabic_with_others_dic':
                return True,len(comment_classifier_obj.arabic_with_others_dic)
            if dictionary_name == 'mixed_lang_dic':
                return True,len(comment_classifier_obj.mixed_lang_dic)
            if dictionary_name == 'other_language_dic':
                return True,len(comment_classifier_obj.other_language_dic)
            if dictionary_name == 'exceptions_dic':
                return True,len(comment_classifier_obj.exceptions_dic)
            if dictionary_name == 'pure_emoji_dic':
                return True,len(comment_classifier_obj.pure_emoji_dic)
            if dictionary_name == 'emoji_pure_arabic_dic':
                return True,len(comment_classifier_obj.emoji_pure_arabic_dic)
            if dictionary_name == 'emoji_pure_english_dic':
                return True,len(comment_classifier_obj.emoji_pure_english_dic)
            if dictionary_name == 'emoji_arabic_with_others_dic':
                return True,len(comment_classifier_obj.emoji_arabic_with_others_dic)
            if dictionary_name == 'emoji_english_with_others_dic':
                return True,len(comment_classifier_obj.emoji_english_with_others_dic)
            if dictionary_name == 'emoji_ar_en_dic':
                return True,len(comment_classifier_obj.emoji_ar_en_dic)
            if dictionary_name == 'emoji_mixed_lang_dic':
                return True,len(comment_classifier_obj.emoji_mixed_lang_dic)
            if dictionary_name == 'emoji_other_language_dic':
                return True,len(comment_classifier_obj.emoji_other_language_dic)
            if dictionary_name == 'emoji_exceptions_dic':
                return True,len(comment_classifier_obj.emoji_exceptions_dic)
            if dictionary_name == 'emoji_english_with_others_dic':
                return True,len(comment_classifier_obj.emoji_english_with_others_dic)
            if dictionary_name == 'emoji_useless_comment_dic':
                return True,len(comment_classifier_obj.emoji_useless_comment_dic)
            if dictionary_name == 'useless_comment_dic':
                return True,len(comment_classifier_obj.useless_comment_dic)
            else:
                return False,0

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
'''
            video_title = ast.literal_eval(video_classified_obj.video_title)
            video_specification = ast.literal_eval(video_classified_obj.video_specification)

            self.emoji_comment_dic = self.comment_classifier_among_video_classfier(emoji_comment_dic,video_title,video_specification)
            self.pure_emoji_dic = self.comment_classifier_among_video_classfier(pure_emoji_dic,video_title,video_specification)
            self.pure_english_dic = self.comment_classifier_among_video_classfier(pure_english_dic,video_title,video_specification)
            self.pure_arabic_dic = self.comment_classifier_among_video_classfier(pure_arabic_dic,video_title,video_specification)
            self.mixed_lang_dic = self.comment_classifier_among_video_classfier(mixed_lang_dic,video_title,video_specification)
            self.emoji_pure_arabic_dic = self.comment_classifier_among_video_classfier(emoji_pure_arabic_dic,video_title,video_specification)
            self.emoji_pure_english_dic =self.comment_classifier_among_video_classfier(emoji_pure_english_dic,video_title,video_specification)
            self.emoji_mixed_lang_dic = self.comment_classifier_among_video_classfier(emoji_mixed_lang_dic,video_title,video_specification)
            self.emoji_arabic_with_others_dic = self.comment_classifier_among_video_classfier(emoji_arabic_with_others_dic,video_title,video_specification)
            self.emoji_english_with_others_dic = self.comment_classifier_among_video_classfier(emoji_english_with_others_dic,video_title,video_specification)
            self.emoji_ar_en_dic = self.comment_classifier_among_video_classfier(emoji_ar_en_dic,video_title,video_specification)
            self.emoji_exceptions_dic = self.comment_classifier_among_video_classfier(emoji_exceptions_dic,video_title,video_specification)
            self.emoji_other_language_dic = self.comment_classifier_among_video_classfier(emoji_other_language_dic,video_title,video_specification)
            self.emoji_useless_comment_dic= self.comment_classifier_among_video_classfier(emoji_useless_comment_dic,video_title,video_specification)
            self.exceptions_dic = self.comment_classifier_among_video_classfier(exceptions_dic,video_title,video_specification)
            self.other_language_dic = self.comment_classifier_among_video_classfier(other_language_dic,video_title,video_specification)
            self.useless_comment_dic= self.comment_classifier_among_video_classfier(useless_comment_dic,video_title,video_specification)
            self.arabic_with_others_dic= self.comment_classifier_among_video_classfier(arabic_with_others_dic,video_title,video_specification)
            self.english_with_others_dic = self.comment_classifier_among_video_classfier(english_with_others_dic,video_title,video_specification)
            self.ar_en_dic = self.comment_classifier_among_video_classfier(ar_en_dic,video_title,video_specification)
'''
