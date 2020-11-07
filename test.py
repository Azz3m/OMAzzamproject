import spacy

"Tokenize input string using a spaCy pipeline"
nlp = spacy.blank('en')
nlp.add_pipe(nlp.create_pipe('sentencizer'))  # Very basic NLP pipeline in spaCy
doc = nlp('Azzam @#fsf 11254 fdf kite')
print(token.text for token in doc)
tokenized_text = ' '.join(token.text for token in doc)
print(tokenized_text)
