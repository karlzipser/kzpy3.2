In [36]: %paste
def rtf_encode_char(unichar):
    code = ord(unichar)
    if code < 128:
        return str(unichar)
    return '\\u' + str(code if code <= 32767 else code-65536) + '?'

def rtf_encode(unistr):
    return ''.join(rtf_encode_char(c) for c in unistr)

## -- End pasted text --

In [37]: rt
rtf_encode       rtf_encode_char  

In [37]: rtf_encode(u"Innocent is good \U0001f607 {} - {} pts")
Out[37]: 'Innocent is good \\u-10179?\\u-8697? {} - {} pts'

In [38]: import rtfunicode

In [39]: u"Innocent is good \U0001f607 {} - {} pts".encode('rtfunicode')
Out[39]: 'Innocent is good \\u-10179?\\u-8697? \\u123?\\u125? - \\u123?\\u125? pts'

In [40]: a=u"Innocent is good \U0001f607".encode('rtfunicode')

In [41]: print(a)
Innocent is good \u-10179?\u-8697?

In [42]: a
Out[42]: 'Innocent is good \\u-10179?\\u-8697?'

In [43]: b=a.replace('?','')

In [44]: c=b.replace('\\','\')
  File "<ipython-input-44-286d4f759271>", line 1
    c=b.replace('\\','\')
                        ^
SyntaxError: EOL while scanning string literal


In [45]: print(b)
Innocent is good \u-10179\u-8697

In [46]: text_to_file(b,opjD('temp2.rtf')
   ....: )

In [47]: text_to_file?
Signature: text_to_file(f, t)
Docstring: <no docstring>
File:      ~/kzpy3/utils/files.py
Type:      function

In [48]: text_to_file(opjD('temp2.rtf'),b)

In [49]: 








# change_fonts.py
# https://www.blog.pythonlibrary.org/2018/06/05/creating-pdfs-with-pyfpdf-and-python/

from fpdf import FPDF

def change_fonts():
    pdf = FPDF()
    pdf.add_page()
    font_size = 8
    for font in pdf.core_fonts:
        if any([letter for letter in font if letter.isupper()]):
            # skip this font
            continue
        pdf.set_font(font, size=font_size)
        txt =  u"Innocent is good \U0001f607 {} - {} pts".format(font, font_size)
        pdf.cell(0, 10, txt=txt, ln=1, align="L")
        font_size += 2
    
    pdf.output("change_fonts.pdf")
    
if __name__ == '__main__':
    change_fonts()


#!/usr/bin/env python
# -*- coding: utf8 -*-

from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

# Add a DejaVu Unicode font (uses UTF-8)
# Supports more than 200 languages. For a coverage status see:
# http://dejavu.svn.sourceforge.net/viewvc/dejavu/trunk/dejavu-fonts/langcover.txt
pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
pdf.set_font('DejaVu', '', 14)

text = u""" \U0001f609\U0001f60a
English: Hello World
Greek: Γειά σου κόσμος
Polish: Witaj świecie
Portuguese: Olá mundo
Russian: Здравствуй, Мир
Vietnamese: Xin chào thế giới
Arabic: مرحبا العالم
Hebrew: שלום עולם
"""

for txt in text.split('\n'):
    pdf.write(8, txt)
    pdf.ln(8)

# Add a Indic Unicode font (uses UTF-8)
# Supports: Bengali, Devanagari, Gujarati, 
#           Gurmukhi (including the variants for Punjabi) 
#           Kannada, Malayalam, Oriya, Tamil, Telugu, Tibetan
pdf.add_font('gargi', '', 'gargi.ttf', uni=True) 
pdf.set_font('gargi', '', 14)
pdf.write(8, u'Hindi: नमस्ते दुनिया')
pdf.ln(20)

# Add a AR PL New Sung Unicode font (uses UTF-8)
# The Open Source Chinese Font (also supports other east Asian languages)
pdf.add_font('fireflysung', '', 'fireflysung.ttf', uni=True)
pdf.set_font('fireflysung', '', 14)
pdf.write(8, u'Chinese: 你好世界\n')
pdf.write(8, u'Japanese: こんにちは世界\n')
pdf.ln(10)

# Add a Alee Unicode font (uses UTF-8)
# General purpose Hangul truetype fonts that contain Korean syllable 
# and Latin9 (iso8859-15) characters.
pdf.add_font('eunjin', '', 'Eunjin.ttf', uni=True)
pdf.set_font('eunjin', '', 14)
pdf.write(8, u'Korean: 안녕하세요')
pdf.ln(20)

# Add a Fonts-TLWG (formerly ThaiFonts-Scalable) (uses UTF-8)
pdf.add_font('waree', '', 'Waree.ttf', uni=True)
pdf.set_font('waree', '', 14)
pdf.write(8, u'Thai: สวัสดีชาวโลก')
pdf.ln(20)

# Select a standard font (uses windows-1252)
pdf.set_font('Arial', '', 14)
pdf.ln(10)
pdf.write(5, 'This is standard built-in font')

pdf.output("unicode.pdf", 'F')