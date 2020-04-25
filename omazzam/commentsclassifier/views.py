from django.shortcuts import render, redirect, get_object_or_404
from commentsclassifier.models import Langclassifier,Commentclassifier
from comments.models import Comment,Videoinformation

import polyglot
from polyglot.detect import Detector
from langdetect import detect
from nltk.tokenize import sent_tokenize,word_tokenize
import re
import ast

# Create your views here.


def langcommentsclassifier(request,comment_id):
    user = request.user
    try:
        print("try getting comments object from database ......")
        comment_obj = get_object_or_404(Comment,pk=comment_id)
        comment_obj_indexer = "found"
        print("we found Comment object under : ", comment_obj)


        #print("getting comments object from database ......")
    except :
        print("we couldn't find any Comment object with id:( " + str(comment_id) + " ) in database ")

    if Langclassifier.objects.filter(comment_objID=comment_id).exists():
        total_processed = 0
        print ("we found comment_classifier object")

        #vaibles to hold the data
        #print("setting up variables for comments_classifier processor  .....")
        print("setting up variables for comments_classifier processor  ....." )
        print("Try getting  Videoinformation object .... ")
        video_Object = get_object_or_404(Videoinformation,pk=comment_obj.video_object_id)
        print("successfully got Videoinformation object  under : ", comment_obj.videoInfo)


        print("fecthcing comment_classifier's object ......")
        comments_classifier = get_object_or_404(Langclassifier,comment_objID=comment_id)

        emoji_comment_dic = ast.literal_eval(comments_classifier.emoji_comment_dic)
        pure_emoji_dic=ast.literal_eval(comments_classifier.pure_emoji_dic)
        emoji_pure_arabic_dic = ast.literal_eval(comments_classifier.emoji_pure_arabic_dic)
        emoji_pure_english_dic = ast.literal_eval(comments_classifier.emoji_pure_english_dic)
        emoji_mixed_lang_dic = ast.literal_eval(comments_classifier.emoji_mixed_lang_dic)
        emoji_arabic_with_others_dic=ast.literal_eval(comments_classifier.emoji_arabic_with_others_dic)
        emoji_english_with_others_dic =ast.literal_eval(comments_classifier.emoji_english_with_others_dic)
        emoji_ar_en_dic=ast.literal_eval(comments_classifier.emoji_ar_en_dic)
        emoji_exceptions_dic = ast.literal_eval(comments_classifier.emoji_exceptions_dic)
        emoji_other_language_dic =ast.literal_eval(comments_classifier.emoji_other_language_dic)
        emoji_useless_comment_dic=ast.literal_eval(comments_classifier.emoji_useless_comment_dic)
        pure_arabic_dic = ast.literal_eval(comments_classifier.pure_arabic_dic)
        pure_english_dic = ast.literal_eval(comments_classifier.pure_english_dic)
        mixed_lang_dic = ast.literal_eval(comments_classifier.mixed_lang_dic)
        exceptions_dic = ast.literal_eval(comments_classifier.exceptions_dic)
        other_language_dic =ast.literal_eval(comments_classifier.other_language_dic)
        useless_comment_dic=ast.literal_eval(comments_classifier.useless_comment_dic)
        arabic_with_others_dic=ast.literal_eval(comments_classifier.arabic_with_others_dic)
        english_with_others_dic =ast.literal_eval(comments_classifier.english_with_others_dic)
        ar_en_dic=ast.literal_eval(comments_classifier.ar_en_dic)
        total_processed = len(pure_arabic_dic) + len(pure_english_dic) + len(mixed_lang_dic) + len(exceptions_dic) + len(mixed_lang_dic)+ len(other_language_dic)+ len(useless_comment_dic)+ len(arabic_with_others_dic)+ len(english_with_others_dic)+ len(ar_en_dic)+ len(emoji_comment_dic)
        print("setting up finishs successfully....")
        print("total_processed comments : ",str(total_processed))
        print("redirecting to comment classifier page .......")
        return render(request,'commentsclassifier/langcommentsclassifier.html',{"video_Object":video_Object,"total_processed":total_processed,"emoji_comment_dic":emoji_comment_dic ,"pure_emoji_dic":pure_emoji_dic ,"emoji_pure_arabic_dic":emoji_pure_arabic_dic ,"emoji_pure_english_dic":emoji_pure_english_dic ,"emoji_mixed_lang_dic":emoji_mixed_lang_dic,"emoji_arabic_with_others_dic":emoji_arabic_with_others_dic ,"emoji_english_with_others_dic":emoji_english_with_others_dic ,"emoji_ar_en_dic": emoji_ar_en_dic,"emoji_exceptions_dic":emoji_exceptions_dic ,"emoji_other_language_dic":emoji_other_language_dic,"emoji_useless_comment_dic":emoji_useless_comment_dic ,"pure_arabic_dic":pure_arabic_dic,"pure_english_dic":pure_english_dic ,"mixed_lang_dic":mixed_lang_dic,"exceptions_dic":exceptions_dic ,"other_language_dic":other_language_dic ,"useless_comment_dic": useless_comment_dic,"arabic_with_others_dic": arabic_with_others_dic,"english_with_others_dic":english_with_others_dic,"ar_en_dic": ar_en_dic,"status":"found a comment_classifier object"})


    else:
        comments_classifier = Langclassifier()
        response_dic = comments_classifier.comments_lang_classifier(user,comment_id)
        indicator = response_dic["state"]

        if indicator == "created":
            total_processed = 0
            comments_classifier = response_dic["comment_classifier"]

            comments_classifier.save()
            print("comments_classifier object created successfully")
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
            total_processed = len(pure_arabic_dic) + len(pure_english_dic) + len(mixed_lang_dic) + len(exceptions_dic) + len(mixed_lang_dic)+ len(other_language_dic)+ len(useless_comment_dic)+ len(arabic_with_others_dic)+ len(english_with_others_dic)+ len(ar_en_dic)+ len(emoji_comment_dic)
            print("Try getting  Videoinformation object .... ")
            video_Object = get_object_or_404(Videoinformation,pk=comment_obj.video_object_id)
            print("successfully got Videoinformation object  under : ", comment_obj.videoInfo)
            print("total_processed comments : ",str(total_processed))
            print("redirecting to comment classifier page .......")
            return render(request,'commentsclassifier/langcommentsclassifier.html',{"video_Object":video_Object,"total_processed":total_processed,"emoji_comment_dic":emoji_comment_dic ,"pure_emoji_dic":pure_emoji_dic ,"emoji_pure_arabic_dic":emoji_pure_arabic_dic ,"emoji_pure_english_dic":emoji_pure_english_dic ,"emoji_mixed_lang_dic":emoji_mixed_lang_dic,"emoji_arabic_with_others_dic":emoji_arabic_with_others_dic ,"emoji_english_with_others_dic":emoji_english_with_others_dic ,"emoji_ar_en_dic": emoji_ar_en_dic,"emoji_exceptions_dic":emoji_exceptions_dic ,"emoji_other_language_dic":emoji_other_language_dic,"emoji_useless_comment_dic":emoji_useless_comment_dic ,"pure_arabic_dic":pure_arabic_dic,"pure_english_dic":pure_english_dic ,"mixed_lang_dic":mixed_lang_dic,"exceptions_dic":exceptions_dic ,"other_language_dic":other_language_dic ,"useless_comment_dic": useless_comment_dic,"arabic_with_others_dic": arabic_with_others_dic,"english_with_others_dic":english_with_others_dic,"ar_en_dic": ar_en_dic,"status":"found a comment_classifier object"})

            print("redirecting to comment classifier page ....... ")
            return render(request,'commentsclassifier/langcommentsclassifier.html',{"video_Object":video_Object,"comments_classifier":comments_classifier,"comment_obj":comment_obj,"total_processed":total_processed})

        else:
            return render(request,'commentsclassifier/langcommentsclassifier.html',{"status":"please insert a valid comment_id"})


def commentsclassifier(request,lang_classifier_obj_id):
    user = request.user
    comment_classifier_obj = Commentclassifier()
    print(comment_classifier_obj.comments_classifier(user,lang_classifier_obj_id))
    #print(obj)

    return render(request,'commentsclassifier/commentsclassifier.html',{"comment_classifier_obj":comment_classifier_obj})
