import re
from pdfminer.high_level import extract_pages, extract_text

text = extract_text("./sample.pdf")

for line in text.split('\n'):
    a = line.find('STANJE PREDHODNEGA IZPISKA')
    print(a)
    print(line)