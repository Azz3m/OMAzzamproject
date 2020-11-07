from django.shortcuts import render, redirect, get_object_or_404
from commentsclassifier.models import Langclassifier,Commentclassifier,Videocategoryclassifier
from django.http import JsonResponse
from comments.models import Comment,Videoinformation
from django.core.paginator import Paginator
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
        dictionay_length_pairs = lang_classifier.dictionay_length_pairs('found',lang_classifier)
        context = {
        "dictionay_length_pairs":dictionay_length_pairs,
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
            dictionay_length_pairs = lang_classifier.dictionay_length_pairs('create',lang_classifier)
            context = {
            'dictionay_length_pairs': dictionay_length_pairs,
            "lang_classifier":lang_classifier,
            "comment_obj":comment_obj,
            "comment_id":comment_obj.id,
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
        video_classified_obj = get_object_or_404(Videocategoryclassifier,video_Object=video_Object)
        video_titles_sets = ast.literal_eval(video_classified_obj.video_title)
        tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.tag_list_setter(video_Object)
        dictionary = comment_classifier_obj.dic_tag_pack_viewer(dictionary)
        language_classifier_obj = get_object_or_404(Langclassifier,pk=lang_classifier_obj_id)
        total_processed = comment_classifier_obj.get_length(language_classifier_obj)
        dictionay_length_pairs = comment_classifier_obj.dictionay_length_pairs('found',comment_classifier_obj)
        context = {
        "dictionay_length_pairs":dictionay_length_pairs,
        "total_processed":total_processed,
        "lang_classifier_obj_id":lang_classifier_obj_id,
        "video_Object":video_Object,
        "video_titles_sets" :video_titles_sets,
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
        dictionay_length_pairs = comment_classifier_obj.dictionay_length_pairs('create',comment_classifier_obj)
        video_classified_obj = get_object_or_404(Videocategoryclassifier,video_Object=video_Object)
        video_titles_sets = ast.literal_eval(video_classified_obj.video_title)
        context = {
        "dictionay_length_pairs":dictionay_length_pairs,
        "total_processed":total_processed,
        "lang_classifier_obj_id":lang_classifier_obj_id,
        "video_Object":video_Object,
        "video_titles_sets" :video_titles_sets,
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
            category = request.POST['category']
            status,dictionary_length = lang_classifier_obj.dictionary_fetcher(dictionary_name,lang_classifier_obj)
            if status == True:
                return JsonResponse({'success':dictionary_name,'dictionary_length':dictionary_length,'category':category})
    return JsonResponse({'fail':"we didin't find any dictionaries "})

def langdectionaryviewer(request,comment_id,dic_name ,category):
    dictionary_among_one_category = {}
    if Langclassifier.objects.filter(comment_objID=comment_id).exists():
        lang_classifier_obj = get_object_or_404(Langclassifier,comment_objID=comment_id)
        dictionary_name = dic_name
        dictionary_among_one_category = lang_classifier_obj.dictionary_among_one_category(category,lang_classifier_obj)
        status,dictionary,video_Object = lang_classifier_obj.dictionary_viewer(lang_classifier_obj,dictionary_name)
        if status == True:
            texts = list()
            authors = list()
            images = list()
            channelsURL = list()
            dates = list()
            indexes = list()
            predefined = list()
            predefined_pack = list()
            predefined_tag_repeat = list()
            userdefined = list()
            userdefined_pack = list()
            user_tag_repeat = list()

            video_titles_linker = list()
            video_specification_linker = list()
            for key,item in dictionary.items():
                texts.append(item['single_comment'])
                authors.append(item['author'])
                images.append(item['img'])
                channelsURL.append(item['url'])
                dates.append(item['date'])
                indexes.append(item['i'])

                if 'predefined_pack' in item:
                    predefined_pack.append(item['predefined_pack'])
                    predefined_tag_repeat.append(item['predefined_tag_repeat'])
                    predefined.append(item['predefined'])
                else:
                    predefined_pack.append(False)
                    predefined_tag_repeat.append(False)
                    predefined.append(False)

                if 'userdefined' in item:
                    userdefined.append(item['userdefined'])
                    user_tag_repeat.append(item['user_tag_repeat'])
                    userdefined_pack.append(item['userdefined_pack'])
                else:
                    userdefined.append(False)
                    user_tag_repeat.append(False)
                    userdefined_pack.append(False)

                if 'video_titles_linker' in item:
                    video_titles_linker.append(item['video_titles_linker'])
                else:

                    video_titles_linker.append(False)
                if 'video_specification_linker' in item:
                    video_specification_linker.append(item['video_specification_linker'])
                else:
                    video_specification_linker.append(False)


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

            paginator6 = Paginator(indexes, 1000)
            page = request.GET.get('page')
            indexes = paginator6.get_page(page)

            paginator8 = Paginator(predefined_pack, 1000)
            page = request.GET.get('page')
            predefined_pack = paginator8.get_page(page)

            paginator9 = Paginator(predefined_tag_repeat, 1000)
            page = request.GET.get('page')
            predefined_tag_repeat = paginator9.get_page(page)

            paginator10 = Paginator(predefined, 1000)
            page = request.GET.get('page')
            predefined = paginator10.get_page(page)

            paginator11 = Paginator(userdefined_pack, 1000)
            page = request.GET.get('page')
            userdefined_pack = paginator11.get_page(page)

            paginator12 = Paginator(user_tag_repeat, 1000)
            page = request.GET.get('page')
            user_tag_repeat = paginator12.get_page(page)

            paginator13 = Paginator(userdefined, 1000)
            page = request.GET.get('page')
            userdefined = paginator13.get_page(page)

            paginator14 = Paginator(video_titles_linker, 1000)
            page = request.GET.get('page')
            video_titles_linker = paginator14.get_page(page)

            paginator15 = Paginator(video_specification_linker, 1000)
            page = request.GET.get('page')
            video_specification_linker = paginator15.get_page(page)



            page_obj = zip(texts,authors,images,channelsURL,dates,indexes,predefined_pack,predefined_tag_repeat,predefined,userdefined,user_tag_repeat,userdefined_pack,video_titles_linker,video_specification_linker)
            texts = list()
            for key,item in dictionary.items():
                texts.append(item['single_comment'])



            paginator7 = Paginator(texts, 1000)
            page = request.GET.get('page')
            texts = paginator7.get_page(page)



            context = {
            'dictionary_among_one_category': dictionary_among_one_category,
            "video_Object":video_Object,
            'comment_id':comment_id,
            "dic":dictionary,
            'dic_name':dic_name,
            "dic":dictionary,
            'page_obj': page_obj,
            "page":texts

            }
            return render(request,'commentsclassifier/lang_dic_viewer.html',context)

    return render(request , 'commentsclassifier/lang_dic_viewer.html')

def commentclassifierdictionariesfetcher(request,comment_classifier_obj_id):
    comment_classifier_obj = get_object_or_404(Commentclassifier,pk=comment_classifier_obj_id)
    if request.method == 'POST':
        if request.POST['dic_name']:
            dictionary_name = request.POST['dic_name']
            category = request.POST['category']
            servicetype = request.POST['servicetype']
            print(dictionary_name,category,servicetype)
            status,dictionary_length = comment_classifier_obj.dictionary_fetcher(dictionary_name,comment_classifier_obj)
            if status == True:
                return JsonResponse({'success':dictionary_name,'dictionary_length':dictionary_length,'category':category,'servicetype':servicetype})
    return JsonResponse({'fail':"we didin't find any dictionaries "})



# servicetype = allComments,relatedWithOthers,relatedTothisVideo
def dectionaryviewer(request,lang_classifier_obj_id,dic_name,category,servicetype):
    dictionary_among_one_category = {}
    dictionary = {}
    if Commentclassifier.objects.filter(langcommentsclassifier_objID=lang_classifier_obj_id).exists():
        comment_classifier_obj = get_object_or_404(Commentclassifier,langcommentsclassifier_objID=lang_classifier_obj_id)
        dictionary_name = dic_name

        dictionary_among_one_category = comment_classifier_obj.dictionary_among_one_category(category,comment_classifier_obj)
        status,dictionary,video_object,tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.dictionary_viewer(comment_classifier_obj,dictionary_name)
        video_classified_obj = get_object_or_404(Videocategoryclassifier,video_Object=video_object)
        video_classified_titles_tag = ast.literal_eval(video_classified_obj.video_title)
        video_classified_specifiaction_tag = ast.literal_eval(video_classified_obj.video_specification)

        if status == True:

            video_titles_linker = list()
            video_specification_linker = list()
            video_titles_sets = list()

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

            related_vid_dic = {}
            if servicetype == "relatedTothisVideo":
                for key, item in dictionary.items():
                    if 'video_specification_linker' in item:
                        related_vid_dic[str(key)] = item

            elif servicetype == "relatedWithOthers":
                for key, item in dictionary.items():
                    if 'video_titles_linker' in item:
                        related_vid_dic[str(key)] = item

            else:
                print('allComments')
                pass


            if len(related_vid_dic) > 0 :
                dictionary = related_vid_dic
            else:
                pass


            video_titles_linker_total, video_specification_linker_total = comment_classifier_obj.dictionary_related_videos(dictionary)

            texts = list()
            authors = list()
            images = list()
            channelsURL = list()
            dates = list()
            indexes = list()
            predefined = list()
            predefined_pack = list()
            predefined_tag_repeat = list()
            userdefined = list()
            userdefined_pack = list()
            user_tag_repeat = list()
            video_specification_linker = list()
            video_titles_linker = list()
            video_title_tags = list()
            video_specification_tags = list()
            video_specification_tags_packs = list()
            video_title_tags_packs =list()
            video_titles = list()
            video_specification = list()
            title_tag_pack = list()
            specification_tag_pack = list()
            temp_title_tag = list()
            temp_repeat = list()
            temp_specification_tag = list()


            for key,item in dictionary.items():
                texts.append(item['single_comment'])
                authors.append(item['author'])
                images.append(item['img'])
                channelsURL.append(item['url'])
                dates.append(item['date'])
                indexes.append(item['i'])


                if 'predefined_pack' in item:
                    predefined_pack.append(item['predefined_pack'])
                    predefined_tag_repeat.append(item['predefined_tag_repeat'])
                    predefined.append(item['predefined'])
                else:
                    predefined_pack.append(False)
                    predefined_tag_repeat.append(False)
                    predefined.append(False)

                if 'userdefined' in item:
                    userdefined.append(item['userdefined'])
                    user_tag_repeat.append(item['user_tag_repeat'])
                    userdefined_pack.append(item['userdefined_pack'])
                else:
                    userdefined.append(False)
                    user_tag_repeat.append(False)
                    userdefined_pack.append(False)

                if 'video_titles_linker' in item:
                    video_titles_linker.append(item['video_titles_linker'])
                    video_titles.append(item['video_title'])
                    temp_title_tag = item['video_title']
                    temp_repeat = item['video_title_repeat']

                    title_tag_pack.append(zip(temp_title_tag,temp_repeat))

                else:
                    title_tag_pack.append(False)
                    video_titles_linker.append(False)
                    video_titles.append(False)

                if 'video_specification_linker' in item:
                    video_specification_linker.append(item['video_specification_linker'])
                    video_specification.append(item['video_specification'])
                    temp_specification_tag = item['video_specification']
                    temp_repeat = item['video_specification_repeat']
                    specification_tag_pack.append(zip(temp_specification_tag,temp_repeat))

                else:
                    specification_tag_pack.append(False)
                    video_specification_linker.append(False)
                    video_specification.append(False)


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

            paginator6 = Paginator(indexes, 1000)
            page = request.GET.get('page')
            indexes = paginator6.get_page(page)

            paginator8 = Paginator(predefined_pack, 1000)
            page = request.GET.get('page')
            predefined_pack = paginator8.get_page(page)

            paginator9 = Paginator(predefined_tag_repeat, 1000)
            page = request.GET.get('page')
            predefined_tag_repeat = paginator9.get_page(page)

            paginator10 = Paginator(predefined, 1000)
            page = request.GET.get('page')
            predefined = paginator10.get_page(page)

            paginator11 = Paginator(userdefined_pack, 1000)
            page = request.GET.get('page')
            userdefined_pack = paginator11.get_page(page)

            paginator12 = Paginator(user_tag_repeat, 1000)
            page = request.GET.get('page')
            user_tag_repeat = paginator12.get_page(page)

            paginator13 = Paginator(userdefined, 1000)
            page = request.GET.get('page')
            userdefined = paginator13.get_page(page)

            paginator14 = Paginator(video_titles_linker, 1000)
            page = request.GET.get('page')
            video_titles_linker = paginator14.get_page(page)

            paginator15 = Paginator(video_specification_linker, 1000)
            page = request.GET.get('page')
            video_specification_linker = paginator15.get_page(page)


            paginator16 = Paginator(title_tag_pack, 1000)
            page = request.GET.get('page')
            title_tag_pack = paginator16.get_page(page)

            paginator17 = Paginator(specification_tag_pack, 1000)
            page = request.GET.get('page')
            specification_tag_pack = paginator17.get_page(page)

            paginator18 = Paginator(video_titles, 1000)
            page = request.GET.get('page')
            video_titles = paginator18.get_page(page)

            paginator19 = Paginator(video_specification, 1000)
            page = request.GET.get('page')
            video_specification = paginator19.get_page(page)




            page_obj = zip(texts,authors,images,channelsURL,dates,indexes,predefined_pack,predefined_tag_repeat,predefined,userdefined,user_tag_repeat,userdefined_pack,video_titles_linker,video_specification_linker,video_titles,video_specification,title_tag_pack,specification_tag_pack)
            texts = list()
            for key,item in dictionary.items():
                texts.append(item['single_comment'])




            paginator7 = Paginator(texts, 1000)
            page = request.GET.get('page')
            texts = paginator7.get_page(page)

            context = {
            'servicetype':servicetype,
            'dictionary_among_one_category': dictionary_among_one_category,
            "lang_classifier_obj_id":lang_classifier_obj_id,
            "video_Object":video_object,
            "tags_indicator":tags_indicator,
            "predefined_tags_list":predefined_tags_list,
            "user_tags_list":user_tags_list,
            "comment_classifier_obj":comment_classifier_obj,
            'video_titles_linker_total':video_titles_linker_total,
            'video_specification_linker_total':video_specification_linker_total,
            'video_classified_titles_tag' :video_classified_titles_tag ,
            'video_classified_specifiaction_tag': video_classified_specifiaction_tag,
            "dic":dictionary,
            'dic_name':dic_name,
            'page_obj': page_obj,
            "page":texts
            }
            return render(request,'commentsclassifier/dic_viewer.html',context)
        else:
            return render(request,'commentsclassifier/dic_viewer.html')
