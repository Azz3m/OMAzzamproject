from django.shortcuts import render, redirect, get_object_or_404
from commentsclassifier.models import Langclassifier,Commentclassifier,Videocategoryclassifier
from django.http import JsonResponse
from comments.models import Comment,Videoinformation

import polyglot
from polyglot.detect import Detector
from langdetect import detect
from nltk.tokenize import sent_tokenize,word_tokenize
import re
import ast

from django.core.paginator import Paginator
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
        #print("setting up variables for lang_classifier processor  .....")
        print("setting up variables for lang_classifier processor  ....." )
        print("Try getting  Videoinformation object .... ")
        video_Object = get_object_or_404(Videoinformation,pk=comment_obj.video_object_id)
        print("successfully got Videoinformation object  under : ", comment_obj.videoInfo)
        print("fecthcing comment_classifier's object ......")
        lang_classifier = get_object_or_404(Langclassifier,comment_objID=comment_id)
        emoji_comment_dic = ast.literal_eval(lang_classifier.emoji_comment_dic)
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
        total_processed = len(pure_arabic_dic) + len(pure_english_dic) + len(mixed_lang_dic) + len(exceptions_dic) + len(mixed_lang_dic)+ len(other_language_dic)+ len(useless_comment_dic)+ len(arabic_with_others_dic)+ len(english_with_others_dic)+ len(ar_en_dic)+ len(emoji_comment_dic)
        print("setting up finishs successfully....")
        print("total_processed comments : ",str(total_processed))
        print("redirecting to comment classifier page .......")
        context = {
        "lang_classifier":lang_classifier,
        "comment_obj":comment_obj,
        "video_Object":video_Object,
        "total_processed":total_processed
        }
        return render(request,'commentsclassifier/langcommentsclassifier.html',context)
    else:
        lang_classifier = Langclassifier()
        response_dic = lang_classifier.comments_lang_classifier(user,comment_id)
        indicator = response_dic["state"]
        if indicator == "created":
            total_processed = 0
            lang_classifier = response_dic["lang_classifier"]
            lang_classifier.save()
            print("lang_classifier object created successfully")
            emoji_comment_dic = lang_classifier.emoji_comment_dic
            pure_emoji_dic=lang_classifier.pure_emoji_dic
            emoji_pure_arabic_dic = lang_classifier.emoji_pure_arabic_dic
            emoji_pure_english_dic = lang_classifier.emoji_pure_english_dic
            emoji_mixed_lang_dic = lang_classifier.emoji_mixed_lang_dic
            emoji_arabic_with_others_dic=lang_classifier.emoji_arabic_with_others_dic
            emoji_english_with_others_dic =lang_classifier.emoji_english_with_others_dic
            emoji_ar_en_dic=lang_classifier.emoji_ar_en_dic
            emoji_exceptions_dic = lang_classifier.emoji_exceptions_dic
            emoji_other_language_dic =lang_classifier.emoji_other_language_dic
            emoji_useless_comment_dic=lang_classifier.emoji_useless_comment_dic
            pure_arabic_dic = lang_classifier.pure_arabic_dic
            pure_english_dic = lang_classifier.pure_english_dic
            mixed_lang_dic = lang_classifier.mixed_lang_dic
            exceptions_dic = lang_classifier.exceptions_dic
            other_language_dic =lang_classifier.other_language_dic
            useless_comment_dic=lang_classifier.useless_comment_dic
            arabic_with_others_dic=lang_classifier.arabic_with_others_dic
            english_with_others_dic =lang_classifier.english_with_others_dic
            ar_en_dic=lang_classifier.ar_en_dic
            total_processed = len(pure_arabic_dic) + len(pure_english_dic) + len(mixed_lang_dic) + len(exceptions_dic) + len(mixed_lang_dic)+ len(other_language_dic)+ len(useless_comment_dic)+ len(arabic_with_others_dic)+ len(english_with_others_dic)+ len(ar_en_dic)+ len(emoji_comment_dic)
            print("Try getting  Videoinformation object .... ")
            video_Object = get_object_or_404(Videoinformation,pk=comment_obj.video_object_id)
            print("successfully got Videoinformation object  under : ", comment_obj.videoInfo)
            print("total_processed comments : ",str(total_processed))
            print("redirecting to comment classifier page .......")
            context = {
            "lang_classifier":lang_classifier,
            "comment_obj":comment_obj,
            "video_Object":video_Object,
            "total_processed":total_processed
            }
            return render(request,'commentsclassifier/langcommentsclassifier.html',context)
        else:
            return render(request,'commentsclassifier/langcommentsclassifier.html',{"status":"please insert a valid comment_id"})


def commentsclassifier(request,lang_classifier_obj_id):
    if Commentclassifier.objects.filter(langcommentsclassifier_objID=lang_classifier_obj_id).exists():
        comment_classifier_obj = get_object_or_404(Commentclassifier,langcommentsclassifier_objID=lang_classifier_obj_id)
        dictionary = ast.literal_eval(comment_classifier_obj.pure_english_dic)
        video_Object = comment_classifier_obj.video_Object
        tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)
        dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
        language_classifier_obj = get_object_or_404(Langclassifier,pk=lang_classifier_obj_id)
        total_processed = comment_classifier_obj.get_length(language_classifier_obj)
        context = {
        "total_processed":total_processed,
        "lang_classifier_obj_id":lang_classifier_obj_id,
        "video_Object":video_Object,
        "tags_indicator":tags_indicator,
        "predefined_tags_list":predefined_tags_list,
        "user_tags_list":user_tags_list,
        "comment_classifier_obj":comment_classifier_obj,
        "pure_english_dic":dictionary
        }
        return render(request,'commentsclassifier/commentsclassifier.html',context)

    else:
        user = request.user
        comment_classifier_obj = Commentclassifier()
        dictionary = comment_classifier_obj.comments_classifier(user,lang_classifier_obj_id)
        comment_classifier_obj.save()
        video_Object = comment_classifier_obj.video_Object
        tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)
        dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary.pure_english_dic)
        language_classifier_obj = get_object_or_404(Langclassifier,pk=lang_classifier_obj_id)
        total_processed = comment_classifier_obj.get_length(language_classifier_obj)
    context = {
    "total_processed":total_processed,
    "lang_classifier_obj_id":lang_classifier_obj_id,
    "video_Object":video_Object,
    "tags_indicator":tags_indicator,
    "predefined_tags_list":predefined_tags_list,
    "user_tags_list":user_tags_list,
    "comment_classifier_obj":comment_classifier_obj,
    "pure_english_dic":dictionary
    }
    return render(request,'commentsclassifier/commentsclassifier.html',context)

def langdictionariesfetcher(request,lang_classifier_obj_id):
    lang_classifier_obj = get_object_or_404(Langclassifier,pk=lang_classifier_obj_id)

    if request.method == 'POST':
        if request.POST['dic_name']:
            dictionary_name = request.POST['dic_name']
            status,dictionary_length = lang_classifier_obj.dictionary_fetcher(dictionary_name,lang_classifier_obj)
            if status == True:
                return JsonResponse({'success':dictionary_name,'dictionary_length':dictionary_length})
    return JsonResponse({'fail':"we didin't find any dictionaries "})

def langdectionaryviewer(request,comment_id,dic_name):
    if Langclassifier.objects.filter(comment_objID=comment_id).exists():
        lang_classifier_obj = get_object_or_404(Langclassifier,comment_objID=comment_id)
        dictionary_name = dic_name
        status,dictionary,video_Object = lang_classifier_obj.dictionary_viewer(lang_classifier_obj,dictionary_name)
        if status == True:
            context = {
            "video_Object":video_Object,
            "dic":dictionary,
            'dic_name':dic_name
            }
            return render(request,'commentsclassifier/lang_dic_viewer.html',context)

    return render(request , 'commentsclassifier/lang_dic_viewer.html')

def commentclassifierdictionariesfetcher(request,comment_classifier_obj_id):
    comment_classifier_obj = get_object_or_404(Commentclassifier,pk=comment_classifier_obj_id)
    if request.method == 'POST':
        if request.POST['dic_name']:
            dictionary_name = request.POST['dic_name']
            status,dictionary_length = comment_classifier_obj.dictionary_fetcher(dictionary_name,comment_classifier_obj)
            if status == True:
                return JsonResponse({'success':dictionary_name,'dictionary_length':dictionary_length})
    return JsonResponse({'fail':"we didin't find any dictionaries "})




def dectionaryviewer(request,lang_classifier_obj_id,dic_name):
    if Commentclassifier.objects.filter(langcommentsclassifier_objID=lang_classifier_obj_id).exists():
        comment_classifier_obj = get_object_or_404(Commentclassifier,langcommentsclassifier_objID=lang_classifier_obj_id)
        dictionary_name = dic_name
        status,dictionary,video_Object,tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.dictionary_viewer(comment_classifier_obj,dictionary_name)
        if status == True:
            video_titles_sets = list()
            video_specification_linker = list()
            for item in dictionary:
                if 'video_specification_linker' in dictionary[item]:
                    for id in dictionary[item]['video_specification_linker']:
                        temp = get_object_or_404(Videocategoryclassifier,pk=id)
                        video_specification_linker.append(temp.video_Object.video_title)
                        dictionary[item]['video_specification_linker'] = video_specification_linker
                    video_specification_linker = list()
                if 'video_titles_linker' in dictionary[item]:
                    for id in dictionary[item]['video_titles_linker']:
                        temp = get_object_or_404(Videocategoryclassifier,pk=id)
                        video_titles_sets.append(temp.video_Object.video_title)
                        dictionary[item]['video_titles_linker'] = video_titles_sets
                    video_titles_sets = list()

            context = {
            "video_Object":video_Object,
            "tags_indicator":tags_indicator,
            "predefined_tags_list":predefined_tags_list,
            "user_tags_list":user_tags_list,
            "comment_classifier_obj":comment_classifier_obj,
            "dic":dictionary,
            'dic_name':dic_name
            }
            return render(request,'commentsclassifier/dic_viewer.html',context)
        else:
            return render(request,'commentsclassifier/dic_viewer.html')
    return render(request , 'commentsclassifier/dic_viewer.html')
