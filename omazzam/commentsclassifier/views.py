from django.shortcuts import render, redirect, get_object_or_404
from commentsclassifier.models import Langclassifier
from comments.models import Comment,Videoinformation

import polyglot
from polyglot.detect import Detector
from langdetect import detect
from nltk.tokenize import sent_tokenize,word_tokenize
import re


# Create your views here.


def langcommentsclassifier(request,comment_id):
    user = request.user
    print("creates comments_classifier object ")
    try:

        comments_classifier = Langclassifier()
        response_dic = comments_classifier.comments_lang_classifier(user,comment_id)
        indicator = response_dic["state"]

        if indicator == "found":
            status = "we could  find a Comment_classifier object of the comment_object with  id:( " + str(comment_id) + " ) in database"
            comments_classifier = response_dic["comment_classifier"]
            print("redirecting to comment classifier page ....... ")
            total_processed = len(comments_classifier.pure_arabic_dic) + len(comments_classifier.pure_english_dic) + len(comments_classifier.mixed_lang_dic) + len(comments_classifier.exceptions_dic) + len(comments_classifier.mixed_lang_dic)+ len(comments_classifier.other_language_dic)+ len(comments_classifier.useless_comment_dic)+ len(comments_classifier.arabic_with_others_dic)+ len(comments_classifier.english_with_others_dic)+ len(comments_classifier.ar_en_dic)+ len(comments_classifier.emoji_comment_dic)

            emoji_comment_dic = comments_classifier.emoji_comment_dic
            pure_emoji_dic=comments_classifier.pure_emoji_dic
            emoji_pure_arabic_dic = comments_classifier.emoji_pure_arabic_dic
            emoji_pure_english_dic = comments_classifier.emoji_pure_english_dic
            emoji_mixed_lang_dic = comments_classifier.emoji_mixed_lang_dic
            emoji_arabic_with_others_dic=comments_classifier.emoji_arabic_with_others_dic
            emoji_english_with_others_dic =comments_classifier.emoji_english_with_others_dic
            emoji_ar_en_dic=comments_classifier.emoji_ar_en_dic
            emoji_exceptions_dic = comments_classifier.emoji_exceptions_dic
            emoji_other_language_dic =comments_classifier.emoji_other_language_dic
            emoji_useless_comment_dic=comments_classifier.emoji_useless_comment_dic
            pure_arabic_dic = comments_classifier.pure_arabic_dic
            pure_english_dic = comments_classifier.pure_english_dic
            mixed_lang_dic = comments_classifier.mixed_lang_dic
            exceptions_dic = comments_classifier.exceptions_dic
            other_language_dic =comments_classifier.other_language_dic
            useless_comment_dic=comments_classifier.useless_comment_dic
            arabic_with_others_dic=comments_classifier.arabic_with_others_dic
            english_with_others_dic =comments_classifier.english_with_others_dic
            ar_en_dic=comments_classifier.ar_en_dic
            return render(request,'commentsclassifier/commentsclassifier.html',{"total_processed":total_processed,"emoji_comment_dic":emoji_comment_dic ,"pure_emoji_dic":pure_emoji_dic ,"emoji_pure_arabic_dic":emoji_pure_arabic_dic ,"emoji_pure_english_dic":emoji_pure_english_dic ,"emoji_mixed_lang_dic":emoji_mixed_lang_dic,"emoji_arabic_with_others_dic":emoji_arabic_with_others_dic ,"emoji_english_with_others_dic":emoji_english_with_others_dic ,"emoji_ar_en_dic": emoji_ar_en_dic,"emoji_exceptions_dic":emoji_exceptions_dic ,"emoji_other_language_dic":emoji_other_language_dic,"emoji_useless_comment_dic":emoji_useless_comment_dic ,"pure_arabic_dic":pure_arabic_dic,"pure_english_dic":pure_english_dic ,"mixed_lang_dic":mixed_lang_dic,"exceptions_dic":exceptions_dic ,"other_language_dic":other_language_dic ,"useless_comment_dic": useless_comment_dic,"arabic_with_others_dic": arabic_with_others_dic,"english_with_others_dic":english_with_others_dic,"ar_en_dic": ar_en_dic,"status":"found a comment_classifier object"})

        elif indicator == "created":
            comments_classifier = response_dic["comment_classifier"]
            comments_classifier.save()
            print("comments_classifier object created successfully")
            print("redirecting to comment classifier page ....... ")
            total_processed = len(comments_classifier.pure_arabic_dic) + len(comments_classifier.pure_english_dic) + len(comments_classifier.mixed_lang_dic) + len(comments_classifier.exceptions_dic) + len(comments_classifier.mixed_lang_dic)+ len(comments_classifier.other_language_dic)+ len(comments_classifier.useless_comment_dic)+ len(comments_classifier.arabic_with_others_dic)+ len(comments_classifier.english_with_others_dic)+ len(comments_classifier.ar_en_dic)+ len(comments_classifier.emoji_comment_dic)

            emoji_comment_dic = comments_classifier.emoji_comment_dic
            pure_emoji_dic=comments_classifier.pure_emoji_dic
            emoji_pure_arabic_dic = comments_classifier.emoji_pure_arabic_dic
            emoji_pure_english_dic = comments_classifier.emoji_pure_english_dic
            emoji_mixed_lang_dic = comments_classifier.emoji_mixed_lang_dic
            emoji_arabic_with_others_dic=comments_classifier.emoji_arabic_with_others_dic
            emoji_english_with_others_dic =comments_classifier.emoji_english_with_others_dic
            emoji_ar_en_dic=comments_classifier.emoji_ar_en_dic
            emoji_exceptions_dic = comments_classifier.emoji_exceptions_dic
            emoji_other_language_dic =comments_classifier.emoji_other_language_dic
            emoji_useless_comment_dic=comments_classifier.emoji_useless_comment_dic
            pure_arabic_dic = comments_classifier.pure_arabic_dic
            pure_english_dic = comments_classifier.pure_english_dic
            mixed_lang_dic = comments_classifier.mixed_lang_dic
            exceptions_dic = comments_classifier.exceptions_dic
            other_language_dic =comments_classifier.other_language_dic
            useless_comment_dic=comments_classifier.useless_comment_dic
            arabic_with_others_dic=comments_classifier.arabic_with_others_dic
            english_with_others_dic =comments_classifier.english_with_others_dic
            ar_en_dic=comments_classifier.ar_en_dic
            return render(request,'commentsclassifier/commentsclassifier.html',{"total_processed":total_processed,"emoji_comment_dic":emoji_comment_dic ,"pure_emoji_dic":pure_emoji_dic ,"emoji_pure_arabic_dic":emoji_pure_arabic_dic ,"emoji_pure_english_dic":emoji_pure_english_dic ,"emoji_mixed_lang_dic":emoji_mixed_lang_dic,"emoji_arabic_with_others_dic":emoji_arabic_with_others_dic ,"emoji_english_with_others_dic":emoji_english_with_others_dic ,"emoji_ar_en_dic": emoji_ar_en_dic,"emoji_exceptions_dic":emoji_exceptions_dic ,"emoji_other_language_dic":emoji_other_language_dic,"emoji_useless_comment_dic":emoji_useless_comment_dic ,"pure_arabic_dic":pure_arabic_dic,"pure_english_dic":pure_english_dic ,"mixed_lang_dic":mixed_lang_dic,"exceptions_dic":exceptions_dic ,"other_language_dic":other_language_dic ,"useless_comment_dic": useless_comment_dic,"arabic_with_others_dic": arabic_with_others_dic,"english_with_others_dic":english_with_others_dic,"ar_en_dic": ar_en_dic,"status":"we created a new comment_classifier object"})

        else:
            return render(request,'commentsclassifier/commentsclassifier.html',{"status":"please insert a valid comment_id"})

        #print("getting comments object from database ......")
    except :
        print("we couldn't find any Comment object with id:( " + str(comment_id) + " ) in database ")
        return render(request,'commentsclassifier/commentsclassifier.html',{"status":"please insert a valid comment_id"})
