# coding=utf-8

#Converting from .pdf with PyPDF2 package
'''
import codecs
import PyPDF2
def getPDFContent(path):
    content = ""
    # Load PDF into pyPDF
    pdf = PyPDF2.PdfFileReader(open(path, "rb"))
    # Iterate pages
    for i in range(0, pdf.getNumPages()):
        # Extract text from page and add to content
        content += pdf.getPage(i).extractText() + "\n"
    # Collapse whitespace
    content = " ".join(content.replace(u"\xa0", " ").strip().split())
    return content
print (getPDFContent("mail.pdf").encode("ascii", "ignore"))

    #codecs.open(os.path.join(path, filename[0]), 'r', encoding='utf-8') as f:



from pyPdf import PdfFileReader, PdfFileWriter
pdf = pyPdf.PdfFileReader(open('mail.pdf', "rb"))
for page in pdf.pages:
    print (page.extractText())
'''

import PyPDF2
pdf_file = open('mail_cir.pdf', 'rb')
read_pdf = PyPDF2.PdfFileReader(pdf_file)
number_of_pages = read_pdf.getNumPages()
page = read_pdf.getPage(0)
page_content = page.extractText()
print (page_content.decode('cp1251').encode('utf-8'))
