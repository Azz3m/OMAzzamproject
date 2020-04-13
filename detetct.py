import polyglot
from polyglot.detect import Detector
from nltk.tokenize import sent_tokenize,word_tokenize
from langdetect import detect
i=0
example = "emoji_comment_dic,emoji_pure_arabic_dic ,emoji_pure_english_dic ,emoji_mixed_lang_dic,emoji_arabic_with_others_dic,emoji_english_with_others_dic,emoji_mixed_lang_with_others_dic,emoji_exceptions_dic ,emoji_other_language_dic,emoji_useless_comment_dic,pure_arabic_dic,pure_english_dic,mixed_lang_dic, exceptions_dic ,other_language_dic, useless_comment_dic, arabic_with_others_dic, english_with_others_dic, mixed_lang_with_others_dic"
list = example .split(',')
print (len(list))

def pure_english_detector(text):
  language_string = ""
  for language in Detector(text).languages:
    print(language)
    language_string += " " + str(language)
  if language_string.find("code: en") != -1 and language_string.find("code: ar") == -1:
    print("English language detected")
    return True
  return False

def pure_arabic_detector(text):
  language_string = ""
  for language in Detector(text).languages:
    print(language)
    language_string += " " + str(language)
  if language_string.find("code: ar") != -1 and language_string.find("code: en") == -1:
    print("Arabic language detected")
    return True
  return False

def mixed_ar_en_detector(text):
  language_string = ""
  for language in Detector(text).languages:
    print(language)
    language_string += " " + str(language)
  if language_string.find("code: ar") != -1 and language_string.find("code: en") != -1:
    print("mixed language detected")
    return True
  return False


print("Coded By Eng.Azzam Ali")
print("******************************")
mixed_text = u"""
China (simplified Chinese: 中国; traditional Chinese: 中國),
officially the People's Republic of China (PRC), is a sovereign state located in East Asia.
الكاتب : المهندس عزام عزيز علي
"""

pure_arabic = u""" مرحبا كيف الحال , عزام علي """
pure_english = u""" Hi how are you doing? Mr.Azzam ,I'm new to opinion mining."""
web_version = " hhfdfhd"
print(len(web_version.split(" ")))
print(" ======  pure_arabic  text ===== ")
print(pure_arabic )
print("")
print(" ====== Testing three functions for pure_arabic ===== ")
print("pure_english_detector : ",pure_english_detector(pure_arabic))
print("pure_arabic_detector : ",pure_arabic_detector(pure_arabic))
print("mixed_ar_en_detector : ",mixed_ar_en_detector(pure_arabic))

print("")
print(" ====== pure_english text ===== ")
print(pure_english)
print("")
print(" ====== Testing three functions for pure_english ===== ")
print("pure_english_detector : ",pure_english_detector(pure_english))
print("pure_arabic_detector : ",pure_arabic_detector(pure_english))
print("mixed_ar_en_detector : ",mixed_ar_en_detector(pure_english))
print("")
print(" ====== mixed_text text ===== ")
print(mixed_text)
print("pure_english_detector : ",pure_english_detector(mixed_text))
print("pure_arabic_detector : ",pure_arabic_detector(mixed_text))
print("mixed_ar_en_detector : ",mixed_ar_en_detector(mixed_text))
print("")
print(" ====== web text ===== ")
print(web_version)
print("pure_english_detector : ",pure_english_detector(web_version))
print("pure_arabic_detector : ",pure_arabic_detector(web_version))
print("mixed_ar_en_detector : ",mixed_ar_en_detector(web_version))
