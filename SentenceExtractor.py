# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import random
#import sys

import morphItDataExtractor


TANL_VERB = u'V'
morph_translator_mod = {'g':'ger', 'f':'inf', 'i':'ind', 'c':'sub', 'd':'cond', 'm':'impf', 'p':'part'}    
morph_translator_ten = {'p': 'pres', 'f': 'fut', 'i':'impf', 'r': 'past'}

class SentenceExtractor:
    def __init__ (self, corpus, filesOut):
        self.filenameIndex = 'INDEX'
        self.__corpusFilename = corpus
        self.__fileOutTrue = filesOut[0]
        self.__fileOutFalse = filesOut[1]
        
        self.index = []
        self.morphs = morphItDataExtractor.MorphItDataExtractor()


    def CreateIndexSentences (self):    
        with open(self.__corpusFilename, 'r') as filein:
            file_size = os.fstat(filein.fileno()).st_size
            while filein.tell() < file_size:
                pos, _ = self.ExtractSentence (filein, filein.tell(), file_size)
                if pos:
                    self.index.append (pos)
                
                
    def ExtractSentence (self, filepointer, pos, file_size):
        line= [True]
        sentence = []
        filepointer.seek (pos, 0)
        pos_start = pos
        while line[0] != u'\n' and filepointer.tell() < file_size:
            line = filepointer.readline()
            line = line.split(u'\t')
            sentence.append(line[:6]) 
        sentence = sentence[:-1]
        try:
            #Estraggo i verbi della frase
            verbs = [verb for verb in sentence if verb[3] == TANL_VERB] 
            #a random scelgo un verbo
            indVerb = random.randint (0, len(verbs)-1)
            
            verbfeatures = verbs[indVerb][-1].split(u'|')
#struct features read           
#            num=s|
#            per=3|
#            mod=i|
#            ten=p            
            verbfeatures[0] = verbfeatures[0][-1]   #sing/plur
            verbfeatures[1] = verbfeatures[1][-1]  #pers
            verbfeatures[2] = morph_translator_mod[verbfeatures[2][-1]]   #modo
            verbfeatures[3] = morph_translator_ten[verbfeatures[3][-1]]   #tempo    
            #ora devo ordinare le feats in modo compatibile per morphit
           
            verbfeatures.append(verbfeatures[1])
            verbfeatures.append(verbfeatures[0])
            verbfeatures.pop(0)
            verbfeatures.pop(0)
            
            if self.morphs.QueryPersonaOpposta(verbs[indVerb][1],
                                               verbs[indVerb][2],
                                                verbfeatures):
                return pos_start, sentence
            return False, False    
        except:
#            print "ERR", sentence
            return False, False
                
   
    def LoadIndex (self):
        try:
            with open(self.filenameIndex, 'r') as inxf:
                self.index = [ind.strip() for ind in inxf.readlines()]
        except:
            self.CreateIndexSentences()
            self.SaveIndexSentence () 
    
    def SaveIndexSentence (self):
        with open(self.filenameIndex, 'a') as inxf:
            for inx in self.index:
                inxf.write (unicode(inx) + u'\n')
                
    def SaveSamplesInTwoFiles (self, n):
        #apro i due file
#tempo code for send data to Roberto
        with open ("SAMPLES", 'a') as fs:
            with open(self.__fileOutTrue, 'a') as ft :
                with open(self.__fileOutFalse, 'a') as ff:
                     while n > 0:
                         sample = self.CreateSample ()
                         if sample and sample[0] and sample[1]:
                             ft.write (u'**'+sample[0] + u'**\n')
                             ff.write (u'**'+sample[1] + u'**\n')
                             
                             fs.write ("\n\nORIGINALE: \n" + sample[0] + "\nMODIFICATA: \n" + sample[1])

                             n -= 1
    
    def CreateSample (self):
        """
            Questa funzione crea un esempio segliendolo casualmente 
        """
        indice = random.randint(0,len(self.index)-1)
   
        _, tsent = self.LoadSentence (self.index[indice])
                                                                          
        if tsent:            
            #estrazione verbi dalla frase 
            verbs = [verb for verb in tsent if verb[3] == TANL_VERB]
            #scelgo un verbo a caso all'interno della frase
            indVerb = random.randint (0, len(verbs)-1)
            #estraggo i parametri del verbo
            verbfeatures = verbs[indVerb][-1].split(u'|')
#struct features read           
#            num=s|
#            per=3|
#            mod=i|
#            ten=p       
            try:
                verbfeatures[0] = verbfeatures[0][-1]   #sing/plur
                verbfeatures[1] = verbfeatures[1][-1]  #pers
                verbfeatures[2] = morph_translator_mod[verbfeatures[2][-1]]   #modo
                verbfeatures[3] = morph_translator_ten[verbfeatures[3][-1]]   #tempo   
                #ora devo ordinare le feats in modo compatibile per morphit
           
                verbfeatures.append(verbfeatures[1])
                verbfeatures.append(verbfeatures[0])
                verbfeatures.pop(0)
                verbfeatures.pop(0)
            except:
                return False
                
            fsent = self.morphs.QueryPersonaOpposta(verbs[indVerb][1],
                                         verbs[indVerb][2], verbfeatures)
            
            fsent = fsent[0]
#            print "FSENT", fsent
#            print "TSENT", tsent
#            print verbs[indVerb][1]
            if fsent and fsent != verbs[indVerb][1]:
#======================DECOMMENTARE QUANO DEBUG FINITO========================================================
#                 true_sent = " ".join([w[1].lower() for w in tsent]).strip()
#==============================================================================
                true_sent = " "
                for ele in tsent:
                    if ele[1] == verbs[indVerb][1]:
                        true_sent += '__'+verbs[indVerb][1]+'___'
                    else:
                        true_sent += " " + ele[1]
                        
#                pos = 0
#                print "count ", tsent.count(verbs[indVerb][1])
                for ele in tsent:
                    if ele[1] == verbs[indVerb][1]:
                        ele[1] = '__'+fsent+'___'
                
#                for i in range(tsent.count(verbs[indVerb][1])):
#                    print "pos",pos
#                    pos = tsent.index(verbs[indVerb][1], pos)
#                    tsent[pos] = fsent
                false_sent = " ".join([w[1].lower() for w in tsent]).strip()  
                true_sent = true_sent.strip()
                
                return true_sent, false_sent
                
            return False
        else:
            return False                       
                    
#                    
#                    
#                    if ele == verbs[indVerb][1]:
#                        
#                false_sent = " ".join([w[1].lower() for w in tsent]) 
#                #ricostruisco le frasi
#                tsent = " ".join ([w[1].lower() for w in tsent]) 
#    #            print tsent
#                temp = fsent[0]
#                fsent = tsent.replace(verbs[indVerb][1], fsent[0])
##                print type(fsent), fsent
#                tsent = tsent.replace(verbs[indVerb][1],'___'+str(verbs[indVerb][1])+'___')
#                fsent = fsent.replace(fsent[0],'___'+str(temp)+'___')
#                print "True\n", tsent
#                print "_________", verbs[indVerb][1]
#                print "False\n", fsent
#                print "_________", temp
#                
#                return true_sent, fsent.strip()
#                
#            return False
#        else:
#            return False                 
                 
    def LoadSentence (self, inx):
        with open ( self.__corpusFilename, 'r') as fc:
            return self.ExtractSentence(fc, int(inx), os.fstat(fc.fileno()).st_size)


            
if __name__=='__main__':
    a=SentenceExtractor("corpus", ['True','False'])
    a.LoadIndex ()
    a.SaveSamplesInTwoFiles (50)
    print "Fine"
#    print a.index