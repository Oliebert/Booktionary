# !/bin/python3
# -*- coding: utf-8 -*-

import os

from collections import namedtuple, defaultdict
import io

import kivy.app
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import Converter
from os.path import splitext
import dictionary


IndexEntry = namedtuple('IndexEntry', ('offset', 'size'))

DefinitionPartType = namedtuple('DefinitionPartType',
                                ('TEXT', 'HTML'))('m', 'h')
DefinitionPart = namedtuple('DefinitionPart', ('type', 'data'))


class Load_Dictionary_Screen(Screen):
    
    def load_dic(self,path, filename):

        new_dic = os.path.join(path, filename[0])

        sm.get_screen(
            'Main_Screen').ids.DictLoadButton.dict_path = new_dic  # get_screen - gibt Text aus einen anderen Screen zurück

        sm.current = 'Main_Screen'  # kehrt zu main Screen zurück


def get_words_from_text(text):  # nimmt den ganzen Text und trennt den in die Wörter

    splitline = text.split()

    return splitline

count = {}


def sort_words_by_frequency(words):

    # sortiert die Wörter nach Häufigkeit

    for i in words:

        i = i.lower()

        if i in count:

            count[i] = count[i] + 1

        else:

            count[i] = 1  

    gefiltert = sorted(count.items(), key=lambda x: x[1], reverse=True)

    return gefiltert


class Main_Screen(Screen):

    def button_pressed(self):

        dic_path = self.ids.DictLoadButton.dict_path
        dic = dictionary.Dictionary(dic_path)
        textline = self.ids.T1.text  # Zugriff auf class Main_Screen, TextInput, id: text
        words = get_words_from_text(textline)
        srt = sort_words_by_frequency(words)
        word1 = ""
        word2 = ""

        for word in srt:

            word = next(iter(word))  # it returns the next value from the iterator, trennt sets in Wörter
            word1 = word1 + word + "\n"  # every Word from new line

            if word in dic:

                for entry in dic[word]:

                    word2 = word2 + entry.data  # add translation

        self.ids.T2.text = word2


class Load_file_Screen(Screen):

    def open_file(self, path, filename):

        text_path = os.path.join(path, filename[0])
        file_name = os.path.basename(text_path)  # gibt filename zurück
                                                 # get_screen - gibt Text aus einen anderen Screen zurück
        if file_name.endswith('.txt'):

            with open(os.path.join(path, filename[0])) as f:

                sm.get_screen('Main_Screen').ids.T1.text = f.read() # get_screen - gibt Text aus einen anderen Screen zurück
                sm.current = 'Main_Screen'  # kehrt zu main Screen zurück

        else:

            ofname, iftype = splitext(file_name)[0] + '.txt', splitext(file_name)[1].lower()

            con = Converter.Converter()

            if iftype == '.doc':
                con.doc_txt(file_name, ofname)
            elif iftype == '.docx':
                con.docx_txt(file_name, ofname)
            elif iftype == '.odt':
                con.odt_txt(file_name, ofname)
            elif iftype in ('.fb2', '.html', '.htm'):
                con.fb2_txt(file_name, ofname)


            with open(ofname, 'r') as f:
                sm.get_screen(
                    'Main_Screen').ids.T1.text = f.read()  # get_screen - gibt Text aus einen anderen Screen zurück
                sm.current = 'Main_Screen'  # kehrt zu main Screen zurück


class Save_translation_Screen(Screen):

    def save(self, path, filename):

        with io.open(os.path.join(path, filename), 'w') as f:
            f.write(sm.get_screen('Main_Screen').ids.T2.text)
            sm.current = 'Main_Screen'

    def selected(self, filename):
        print ("selected: %s" % filename[0])


root = Builder.load_file('benutzeroberfläche.kv')

sm = ScreenManager()

sm.add_widget(Main_Screen(name='Main_Screen'))

sm.add_widget(Load_file_Screen(name='Load_file_Screen'))

sm.add_widget(Save_translation_Screen(name='Save_translation_Screen'))

sm.add_widget(Load_Dictionary_Screen(name='Load_Dictionary_Screen'))


class Whatever(kivy.app.App):
    def build(self):  # Initializieren und Zurückgeben die Root Widgets:

        return sm

if __name__ == '__main__':
    Whatever().run()
