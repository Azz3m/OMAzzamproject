import re
r = re.compile(r'\b%s\b' % "is", re.I)
text = 'Why the narrator sounds so similiar to &rdquo;What if&rdquo; videos? This sounds more like a &rdquo;What if&rdquo; videos than a Nuclear medical med'
for m in re.finditer('What if', text):
         print('what if', m.start(), m.end() , text[m.start():m.end()])
