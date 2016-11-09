# coding=utf-8

#Converting from .pdf with PyPDF2 package

import PyPDF2

class PdfConverter:

    def getPDFContent(path):
        content =""
        # Load PDF into pyPDF
        pdf = PyPDF2.PdfFileReader(open(path, "rb"))
        # Iterate pages
        for i in range(0, pdf.getNumPages()):
            # Extract text from page and add to content
            content += pdf.getPage(i).extractText() #+ "\n"
        # Collapse whitespace
        content = u" ".join(content.replace(u"\xa0", u" ").strip().split())
        content.encode('utf-8')
        return content
    print (getPDFContent("mail_cir.pdf").encode('utf-8'))

'''

from pyPdf import PdfFileReader, PdfFileWriter
pdf = pyPdf.PdfFileReader(open('mail.pdf', "rb"))
for page in pdf.pages:
    print (page.extractText())
'''

