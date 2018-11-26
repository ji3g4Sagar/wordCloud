#!/usr/bin/env/python
#-*- coding: utf-8 -*-
import wave
import contextlib
import math
import speech_recognition
from os import listdir
from os.path import isfile, isdir, join
from pypinyin import lazy_pinyin
from pydub import AudioSegment
import jieba
import re
import urllib.request
import os
import multiprocessing.dummy as mp
                

class voiceAnalysis():

    def __init__(self):
        os.chdir("/home/visteam/www/yuan/voiceapi") 
        jieba.set_dictionary('app/jieba_dict/dict.txt.big')
        jieba.load_userdict('app/jieba_dict/mymedword.txt')
        self.result = []
        self.result_dic = dict()
        self.stopword_set = set()
        self.medword_set = set()
        self.setting_stopwords(self.stopword_set)  
        self.setting_medwords(self.medword_set)
        self.filePath = ""
    def clean_irr_words(self, ob_string):
        """         clear num & en         """
        RE = re.search(r'[0-9a-zA-Z]+', ob_string)
        while RE:
            ob_string = ob_string.replace(RE.group(), '')
            RE = re.search(r'[0-9a-zA-Z]+', ob_string)
        """        clear baseline            """
        RE = re.search(r'_+', ob_string)
        while RE:
            ob_string = ob_string.replace(RE.group(), '')
            RE = re.search(r'_+', ob_string)
        return ob_string   
    def setting_stopwords(self, Set):
        with open('app/jieba_dict/mystopwords.txt', 'r', encoding='utf-8') as stopwords:
            for stopword in stopwords:
                Set.add(stopword.strip('\n')) 
    def setting_medwords(self, Set):
        with open('app/jieba_dict/mymedword.txt', 'r', encoding = 'utf-8') as medwords:
            for medword in medwords:
                RE = re.search(r'\s[0-9]+\s[a-z]\n[\s]*', medword)
                while RE:
                    medword = medword.replace(RE.group(), '')
                    RE = re.search(r'\s[0-9]+\s[a-z]\n[\s]*', medword)
                # print(medword)
                Set.add(medword)   
    def tokenize(self, the_string):
        #print(the_string)
        if self.result:
            self.result.clear()
        the_string = self.clean_irr_words(the_string)
        words = jieba.cut(the_string)
        for word in words:
            if word not in self.stopword_set:
                self.result.append(word)
        return self.result
    def processJob(self, n):
        try:
            n = float(n)/2
            r = speech_recognition.Recognizer()
            print("第",n,"秒")
            with speech_recognition.AudioFile(self.filePath) as source:
                    audio = r.record(source, offset = n, duration = 3)
                    #n = n + 0.5
            words = r.recognize_google(audio,language='zh-tw')
            print(words)
            #count the keywords
            for x in self.tokenize(words):
                if x not in self.result_dic.keys():
                    self.result_dic.update({x:1})
                else:
                    self.result_dic[x] += 1
            print(words)
            print(self.result_dic)
        except:
            print("Voice Error")
    def foo(self, s):
        print(s)

    def analysisVoice(self, fileName):
        localFilePath = "/home/visteam/www/yuan/voiceapi/downloadvoice/"
        filePath = localFilePath + fileName
        if self.filePath:
            self.filePath = ""
        self.filePath = filePath
        if (os.path.isfile(filePath)):
            sound = AudioSegment.from_file(filePath)
            time = math.ceil(sound.duration_seconds)
            print("------------------totally ",time," sec--------------------")
            #r = speech_recognition.Recognizer()
            n = 0 # for offset
            #m = 3 #for duration
            p = mp.Pool(50)
            #p.map(self.foo, range(0,100,2))
            p.map(self.processJob, range(int(time)*2))
            p.close()
            p.join()
            #for x in range(int(time)*2):
            #    try:
            #        print("第",n,"秒")
            #        with speech_recognition.AudioFile(filePath) as source:
            #                audio = r.record(source, offset = n, duration = m)
            #                n = n + 0.5
            #        words = r.recognize_google(audio,language='zh-tw')
            #        print(words)
                    #count the keywords
                    #for x in self.tokenize(words):
                    #    if x not in self.result_dic.keys():
                    #        self.result_dic.update({x:1})
                    #    else:
                    #        self.result_dic[x] += 1
                    #print(words)
                   # print(self.result_dic)
            #    except:
            #        print("Voice Error")
                #print("\n")
            return self.result_dic
        else:
            print("File doesn't exist!\n")
