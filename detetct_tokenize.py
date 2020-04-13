from nltk.tokenize import word_tokenize
from langdetect import detect
mixed_lang_with_others_dic = {}
english_with_others_dic = {}
arabic_with_others_dic = {}
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
    if english == True and arabic == True:
        mixed = True
        mixed_lang_with_others_dic["mixed"] = text
    else:
        mixed=False
        if english == True and arabic == False:
            english_with_others_dic["eng"] = text
        if english == False and arabic == True:
            arabic_with_others_dic["ar"] = text
    return mixed_lang_with_others_dic ,english_with_others_dic ,arabic_with_others_dic
example = "༼ᕗຈل͜ຈ༽ᕗ "
print(lang_detector_among_one_word(example))
