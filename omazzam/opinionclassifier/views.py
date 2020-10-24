from django.shortcuts import render,get_object_or_404
from opinionclassifier.models import Englishproccessing
import os
import ast
from django.core.paginator import Paginator
from commentsclassifier.models import Langclassifier,Commentclassifier,Videocategoryclassifier
from django.http import JsonResponse
from django.contrib.staticfiles.storage import staticfiles_storage
# Create your views here.
def opinionclassifier(request,commentsclassifier_id):
    english_proccessing = Englishproccessing()

    index = 0
    if Commentclassifier.objects.filter(id=commentsclassifier_id).exists():
        comment_classifier_obj = get_object_or_404(Commentclassifier, id=commentsclassifier_id)
        lang_classifier_obj_id = comment_classifier_obj.langcommentsclassifier_objID
        comments_dic = ast.literal_eval(comment_classifier_obj.pure_english_dic)
        print(len(comments_dic))
        total_processed = comment_classifier_obj.get_length(comment_classifier_obj)
        texts = list()

        video_Object = comment_classifier_obj.video_Object
        video_classified = get_object_or_404(Videocategoryclassifier,video_Object=video_Object)
        video_titles_sets = video_classified.video_title
        print(video_titles_sets)

        status,dictionary,video_Object,tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.dictionary_viewer(comment_classifier_obj,'pure_english_dic')
        #comment_classifier_obj.save()
        dictionay_length_pairs = comment_classifier_obj.dictionay_length_pairs('found',comment_classifier_obj)
        context = {
            "dictionay_length_pairs":dictionay_length_pairs,
            "total_processed":total_processed,
            "tags_indicator":tags_indicator,
            "predefined_tags_list":predefined_tags_list,
            "user_tags_list":user_tags_list,
            'comments_dic':comments_dic,
            'video_titles_sets' : video_titles_sets,
            'comment_classifier_obj':comment_classifier_obj,
            "lang_classifier_obj_id":lang_classifier_obj_id,
            "video_Object":video_Object,

        }
        return render(request,'opinionclassifier/opinionclassifier.html',context)
    else:
        return render(request,'opinionclassifier/opinionclassifier.html')


def omcommentclassifierdictionariesfetcher(request,comment_classifier_obj_id):
    comment_classifier_obj = get_object_or_404(Commentclassifier,pk=comment_classifier_obj_id)
    if request.method == 'POST':
        if request.POST['dic_name']:
            dictionary_name = request.POST['dic_name']
            num_samples = request.POST['num_samples']
            category = request.POST['category']
            servicetype = request.POST['servicetype']
            if dictionary_name == "ALL" :
                english_proccessing = Englishproccessing()
                dic, dictionaries =  english_proccessing.dictionaries_among_one_category(category,comment_classifier_obj)
                return JsonResponse({'success':'ALL','dictionary_length':len(dictionaries),'num_samples':num_samples,"category":category,'servicetype':servicetype})
            else:
                status,dictionary_length = comment_classifier_obj.dictionary_fetcher(dictionary_name,comment_classifier_obj)
                if status == True:
                    return JsonResponse({'success':dictionary_name,'dictionary_length':dictionary_length,'num_samples':num_samples,"category":category,'servicetype':servicetype})
                return JsonResponse({'fail':"we didin't find any dictionaries "})
    return JsonResponse({'fail':"we didin't find any dictionaries "})




def omdectionaryviewer(request,lang_classifier_obj_id,num_samples,dic_name,category,servicetype):

    dictionary_among_one_category = {}
    print(dic_name, category, num_samples)
    if Commentclassifier.objects.filter(langcommentsclassifier_objID=lang_classifier_obj_id).exists():
        prediction_capability = False
        comment_classifier_obj = get_object_or_404(Commentclassifier,langcommentsclassifier_objID=lang_classifier_obj_id)

        english_proccessing = Englishproccessing()
        dic, dictionaries =  english_proccessing.dictionaries_among_one_category(category,comment_classifier_obj)
        dictionary_name = dic_name
        dictionaries_list = ['pure_english_dic','emoji_pure_english_dic','emoji_english_with_others_dic','english_with_others_dic','ALL']

        if dictionary_name in dictionaries_list:

            prediction_capability = True
            if dictionary_name == 'ALL':
                status,dictionary,video_Object,tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.dictionary_viewer(comment_classifier_obj,'pure_english_dic')
                dictionary = dictionaries
            else:

                status,dictionary,video_Object,tags_indicator,predefined_tags_list,user_tags_list = comment_classifier_obj.dictionary_viewer(comment_classifier_obj,dictionary_name)

            if status == True:
                video_titles_linker_total, video_specification_linker_total = comment_classifier_obj.dictionary_related_videos(dictionary)
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
                polarities = list()
                video_titles_linker = list()
                video_specification_linker = list()
                polarity_dic = {}
                vp = 0
                vn = 0
                pos = 0
                neg = 0
                n = 0
                ig = 0
                index = 0
                english_proccessing = Englishproccessing()
                dictionary_among_one_category = english_proccessing.dictionary_among_one_category(category,comment_classifier_obj)
                comments_over_time_for_one_dic = english_proccessing.comments_over_time_for_one_dic(dictionary)

                for comment in dictionary:

                    if len(dictionary[comment]['single_comment'])>0:
                        texts.append(dictionary[comment]['single_comment'])
                        polarity = english_proccessing.main(dictionary[comment]['single_comment'],num_samples)
                        index += 1
                        print(index , dictionary[comment]['single_comment'])
                        if polarity == 0:
                            dictionary[comment]['polarity'] = 'very_negative'
                            vn += 1
                            polarity_dic['very_negative'] = vn
                        elif polarity == 1:
                            dictionary[comment]['polarity'] = 'negative'
                            neg += 1
                            polarity_dic['negative'] = neg
                        elif polarity == 2:
                            dictionary[comment]['polarity'] = 'neutral'
                            n += 1
                            polarity_dic['neutral'] = n
                        elif polarity == 3:
                            dictionary[comment]['polarity'] = 'positive'
                            pos += 1
                            polarity_dic['positive'] = pos
                        elif polarity == 4:
                            dictionary[comment]['polarity'] = 'very_positive'
                            vp += 1
                            polarity_dic['very_positive'] = vp
                        else:
                            dictionary[comment]['polarity'] = "ignored"
                            ig += 1
                            polarity_dic['ignored'] = ig
                    else:
                        dictionary[comment]['polarity'] = "ignored"
                        ig += 1
                        polarity_dic['ignored'] = ig
                        pass

                for key,item in dictionary.items():
                    texts.append(item['single_comment'])
                    authors.append(item['author'])
                    images.append(item['img'])
                    channelsURL.append(item['url'])
                    dates.append(item['date'])
                    indexes.append(item['i'])
                    polarities.append(item['polarity'])

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

                paginator1000 = Paginator(authors, 1000)
                page1000 = request.GET.get('page')
                authors = paginator1000.get_page(page1000)

                paginator3 = Paginator(images, 1000)
                page3 = request.GET.get('page')
                images = paginator3.get_page(page3)

                paginator4 = Paginator(channelsURL,1000)
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

                paginator11000 = Paginator(user_tag_repeat, 1000)
                page = request.GET.get('page')
                user_tag_repeat = paginator11000.get_page(page)

                paginator13 = Paginator(userdefined, 1000)
                page = request.GET.get('page')
                userdefined = paginator13.get_page(page)

                paginator14 = Paginator(video_titles_linker, 1000)
                page = request.GET.get('page')
                video_titles_linker = paginator14.get_page(page)

                paginator15 = Paginator(video_specification_linker, 1000)
                page = request.GET.get('page')
                video_specification_linker = paginator15.get_page(page)

                paginator16 = Paginator(polarities, 1000)
                page = request.GET.get('page')
                polarities = paginator16.get_page(page)


                page_obj = zip(texts,authors,images,channelsURL,dates,indexes,predefined_pack,predefined_tag_repeat,predefined,userdefined,user_tag_repeat,userdefined_pack,video_titles_linker,video_specification_linker,polarities)
                texts = list()
                for key,item in dictionary.items():
                    texts.append(item['single_comment'])



                paginator7 = Paginator(texts, 1000)
                page = request.GET.get('page')
                texts = paginator7.get_page(page)
                polarity_descision = english_proccessing.polarity_decision_for_one_dic(polarity_dic)
                if polarity_descision == "None":
                    context = {

                    "status" : "There is no Comments in this dic ."
                    }
                else:

                    context = {
                    'servicetype' : servicetype ,
                    'num_samples' : num_samples ,
                    'prediction_capability' : prediction_capability ,
                    'dictionary_among_one_category':dictionary_among_one_category ,
                    'comments_over_time_for_one_dic' : comments_over_time_for_one_dic ,
                    'status' : "prediction completed successfully",
                    "lang_classifier_obj_id":lang_classifier_obj_id,
                    "video_Object":video_Object,
                    "tags_indicator":tags_indicator,
                    "predefined_tags_list":predefined_tags_list,
                    "user_tags_list":user_tags_list,
                    "comment_classifier_obj":comment_classifier_obj,
                    "polarity_dic" :polarity_dic,
                    'polarity_descision' : polarity_descision ,
                    'video_titles_linker_total':video_titles_linker_total,
                    'video_specification_linker_total':video_specification_linker_total,
                    "dic":dictionary,
                    'dic_name':dic_name,
                    'page_obj': page_obj,
                    "page":texts
                    }
                return render(request,'opinionclassifier/dic_viewer.html',context)

        else:
            context = {
            'prediction_capability' : prediction_capability ,
            'status' : "prediction for "+ dic_name +" is under developing .",

            }
            return render(request,'opinionclassifier/dic_viewer.html',context)

    else:

        context = {
        'status' : "comment_classifier_obj not found ",
        }

        return render(request,'opinionclassifier/dic_viewer.html',context)


def explain(request):
    text=""
    english_proccessing = Englishproccessing()
    text = request.POST['text']
    print(text)
    exp = english_proccessing.explanation_plotter(text)
    html = exp.as_html()

    return JsonResponse({'success':html})
