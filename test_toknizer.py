
from nltk.tokenize import sent_tokenize,word_tokenize
from langdetect import detect
example_text = "Hello Ms.Gady , how are you doing today? The weather is great and Python is awesome. The sky is clear and we should go to beach. اليوم حلو "

print(detect("يازلمة صاير بايخ "))

english = False
arabic = False
mixed = False

for word in word_tokenize(example_text):
    try:
        if detect(word) == 'en':
            english = True
            print("english deteced :", word)
        if detect(word) == 'ar':
            arabic = True
            print("Arabic deteced :", word)

    except:
        print("Faild to detect word :" , word)
if english == True and arabic == True:
    mixed = True
    print ("the text is mixed ")
else:
    mixed=False
    print ("the text is pure ")
