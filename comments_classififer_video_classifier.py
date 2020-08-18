def comment_classifier_among_video_classfier(self,dic,video_title,video_specification):

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
            video_title_repeat = list()
            tags_list = list()
            for tag in video_specification:
                if tag in single_comment:

                    total_comments_tags += 1
                    tags_list.append(tag)
                    dic[item]['video_specification'] = tags_list
                    video_specification_repeat.append(single_comment.count(tag))
                    dic[item]['video_specification_repeat'] = video_specification_repeat
                    dic[item]['video_spec_pack'] = None
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

                    print(dic[item])
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
