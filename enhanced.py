import polyglot
from polyglot.detect import Detector
mixed_text = "Love this song ❤️ "

for line in mixed_text.strip().splitlines():
  for language in Detector(line).languages:
    print(language)
