# coding=utf-8

#Converting from .pdf with PyPDF2 package
'''
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

print (getPDFContent("filename.pdf").encode("ascii", "ignore"))

#Converting with tika package

from tika import parser
text = parser.from_file('path')
print(text)
'''


from sys import argv
from os.path import isfile, splitext
from zipfile import ZipFile
from xml.etree.ElementTree import parse, XML
import HTMLParser


def help():
    print('For convertation .doc, .docx, .odt, .htm, .html, .fb2 files:\n\
           fliename \n\
           if whitespace within the filename, take it in quotation mark')
    exit()


def ok():
    print('Converting is done!')


def is_ascii(s):

    if (ord(s) in range(32, 122) ) or (ord(s) in range(1039, 1104))\
    or (ord(s) in (9,10,13)):
        return True
    return False


class Converter:
    def doc_txt(self, ifname, ofname):
        with open(ifname, 'rb') as ffr:
            data = ffr.read()

        start = data[:2800].rfind(b'\x00'*50) + 50
        end = start + data[start:].find(b'\x0d' + b'\x00'*10)
        if end < start: w95, end = True, start + data[start:].find(b'\x00'*10)
        else: w95 = False
        data = data[start:end]

        text, itemp = str(), 0


        while True:
            if w95 == False:
                try:
                    t = data[itemp:itemp+2]
                    if is_ascii(t.decode('utf-16le')) is True:
                        text += t.decode('utf-16le')

                except UnicodeDecodeError:
                    t = t.decode('cp1252', 'ignore')
                    if len (t) > 0:
                        for i in t:
                            if is_ascii(i) is True:
                                text += i
                itemp += 2
                if itemp >= len(data): break


            else:
                t = data.decode('cp1252', 'ignore')
                for i in t:
                    if is_ascii(i) is True:
                        text += i
                break

        with open(ofname, "wb") as ffw:
            ffw.write(b'\xef\xbb\xbf' + text.encode())
        return 1


    def docx_txt(self, ifname, ofname):
        with ZipFile(ifname, 'r') as y:
            z = y.read('word/document.xml')

        tree = XML(z)
        text = str()
        p = tree.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')
        for x in p:
            text += '\n'
            for y in x:
                for z in y:
                    if z.text is not None: text += (z.text)

        with open(ofname, "wb") as ffw:
            ffw.write(b'\xef\xbb\xbf' + text.encode())
        return 1


    def odt_txt(self, ifname, ofname):
        with ZipFile(ifname, 'r') as y:
            z = y.read('content.xml')

        tree = XML(z)
        text = str()
        p = tree.findall('.//{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p')
        for x in p:
            text += '\n'
            for y in x:
                if y.text is not None: text += (y.text)

        with open(ofname, "wb") as ffw:
            ffw.write(b'\xef\xbb\xbf' + text.encode())
        return 1


    def fb2_txt(self, ifname, ofname):
        with open(ifname, "rb") as ffr:
            data = ffr.read()

        try: data = data.decode('utf-8')
        except UnicodeDecodeError: data = data.decode('cp1252')

        class MyHTMLParser(HTMLParser):
            text = str()
            def handle_data(self, data):
                MyHTMLParser.text += data

        MyHTMLParser(strict=False).feed(data)

        with open(ofname, "wb") as ffw:
            ffw.write(b'\xef\xbb\xbf' + MyHTMLParser.text.encode())
        return 1


def convert(ifname):
    # type: (object) -> object

    """

    :rtype: object
    """
    ofname, iftype = splitext(ifname)[0] + '.txt', splitext(ifname)[1].lower()

    con = Converter()

    if iftype == '.doc':
        con.doc_txt(ifname, ofname)
    elif iftype == '.docx':
        con.docx_txt(ifname, ofname)
    elif iftype == '.odt':
        con.odt_txt(ifname, ofname)
    elif iftype in ('.fb2', '.html', '.htm'):
        con.fb2_txt(ifname, ofname)


'''def main():
    print('\"filename\"')
    convert()

    if len(argv) != 2:
        help()
        exit()

    if convert(argv[1]) == 1: ok()

if __name__ == '__main__':
    main()

'''
