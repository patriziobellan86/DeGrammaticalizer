#-*- encoding:utf-8 -*-
"""
                               SentenceExtractor.py

This module is could be used to implement this project

Vesion: 1.0-c stable
CODE TESTED ON Python 3.5 and Python 2.7
#==============================================================================
Università degli studi di Trento (Tn) - Italyy
Center for Mind/Brain Sciences CIMeC
Language, Interaction and Computation Laboratory CLIC

@author: Patrizio Bellan
         patrizio.bellan@gmail.com
         patrizio.bellan@studenti.unitn.it

         github.com/patriziobellan86

#==============================================================================
HOW TO IMPLEMENT THIS PROJECT


"""


from __future__ import unicode_literals


import io
import os
import random

import morphItDataExtractor

# tag of verbs
TANL_VERB = u'V'
# translation tables
morph_translator_mod = {'g': 'ger', 'f': 'inf', 'i': 'ind',
                        'c': 'sub', 'd': 'cond', 'm': 'impf', 'p': 'part'}
morph_translator_ten = {'p': 'pres', 'f': 'fut', 'i': 'impf', 'r': 'past'}


class SentenceExtractor:
    """
     This class provide all the necessary to implement this project in another
     project
     the aim of this class is to create 3 files:
     samples: this file contain all the samples extrcted and marks the
              verb changed
     true_sents and false_sents: every row is an example extracted from corpus
         the latter file contatin the same sentences of the former but with
         the verbs changed (wrong)
    """
    def __init__(self, morphit, corpus, filesOut):
        """
        Args:
            morphit (str): path to morphit lexicon
            corpus (str): path to corpus
            filesOut (list) [True_sentence, False_sentence]: files to save samples
        """
        self.filenameIndex = os.path.dirname(os.path.realpath(__file__))+ \
            os.path.sep + 'INDEX'
        self.__corpusFilename = corpus
        self.__fileOutTrue = filesOut[0]
        self.__fileOutFalse = filesOut[1]
        self.__samples = []
        self.index = []
        self.morphs = morphItDataExtractor.MorphItDataExtractor(morphit)

    def CreateIndexSentences(self):
        """
        This method create a list of indexs.
        every index point to the beginning of a sentence in the corpus

        """
        with io.open(self.__corpusFilename, 'r', encoding="utf-8") as filein:
            file_size = os.fstat(filein.fileno()).st_size
            while filein.tell() < file_size:
                pos, _ = self.ExtractSentence(filein, filein.tell(), file_size)
                if pos:
                    self.index.append(pos)


    def ExtractSentence(self, filepointer, pos, file_size):
        """
         Args:
            filepointer (file_pointer): verb
            pos (int): position to point into file
            file_size (int): file size

        Returns:
            return pos_start, sentence (int)(list): beginning of the sentence and the sentence itself
            return False, False (bool)(bool): the sentence is not usable

        This method extract only usable sentences
        """
        line= [True]
        sentence = []
        filepointer.seek(pos, 0)
        pos_start = pos
        #sentence extraction
        while line[0] != u'\n' and filepointer.tell() < file_size:
            line = filepointer.readline()
            line = line.split(u'\t')
            sentence.append(line[:6])
        sentence = sentence[:-1]
        #sentence analysis
        try:
            # verbs extraction
            verbs = [verb for verb in sentence if verb[3] == TANL_VERB]
            # choose a verb randomly
            indVerb = random.randint (0, len(verbs)-1)
            # extract verb features
            verbfeatures = verbs[indVerb][-1].split(u'|')
#            struct features
#                        num=s|
#                        per=3|
#                        mod=i|
#                        ten=p

            verbfeatures[0] = verbfeatures[0][-1]   #sing/plur
            verbfeatures[1] = verbfeatures[1][-1]   #pers
            verbfeatures[2] = morph_translator_mod[verbfeatures[2][-1]]   #mod
            verbfeatures[3] = morph_translator_ten[verbfeatures[3][-1]]   #temp

            # compatibility with morphit
            verbfeatures.append(verbfeatures[1])
            verbfeatures.append(verbfeatures[0])
            verbfeatures.pop(0)
            verbfeatures.pop(0)

            # check if the verb is usable
            if self.morphs.QueryPersonaOpposta(verbs[indVerb][1],
                                               verbs[indVerb][2],
                                                verbfeatures):
                return pos_start, sentence
            return False, False
        except:
            return False, False


    def LoadIndex (self):
        """
         This method load the index file
        """
        try:
            with io.open(self.filenameIndex, 'r', encoding="utf-8") as inxf:
                self.index = [ind.strip() for ind in inxf.readlines()]
        except:
            self.CreateIndexSentences()
            self.SaveIndexSentence ()


    def SaveIndexSentence (self):
        """
         This method save indexs into file
        """
        with io.open(self.filenameIndex, 'a', encoding="utf-8") as inxf:
            for inx in self.index:
                 inxf.write (str(inx) + '\n')


    def SaveSamplesInTwoFiles (self,filename, n):
        """
         Args:
            filename (str): path file to save samples
            n (int): number of samples to extract

        This method save all samples into files
        """
        with io.open(filename, 'a', encoding="utf-8") as fs:
            with io.open(self.__fileOutTrue, 'a', encoding="utf-8") as ft:
                with io.open(self.__fileOutFalse, 'a', encoding="utf-8") as ff:
                    while n > 0:
                        sample = self.CreateSample()

                        if sample and len(sample) == 4:
                            ft.write(sample[2] + '\r\n')
                            ff.write(sample[3] + '\r\n')
                            fs.write("\n\nORIGINAL: \r\n" + sample[0] + "\r\nMODIFIC: \r\n" + sample[1])
                            n -= 1


    def CreateSample (self):
        """
            returns:
                False the sample is rejected
                list [true_sent, false_sent, true_clear, false_clear]
                            true_sent e false_sent have verb marked
                            true_clear e false_clear have not verb marked
        This method create a samples
        """
        # extraction of a random sentence
        indice = random.randint(0, len(self.index)-1)
        _, tsent = self.LoadSentence (self.index[indice])

        if tsent and not u'....' in [x[1] for x in tsent] and len(tsent) >= 9:
            # choose a verb in the sentence randomply
            verbs = [verb for verb in tsent if verb[3] == TANL_VERB]
            indVerb = random.randint (0, len(verbs)-1)
            # verb's features extraction
            verbfeatures = verbs[indVerb][-1].split(u'|')
            #struct features read
            #            num=s|
            #            per=3|
            #            mod=i|
            #            ten=p|
            try:
                verbfeatures[0] = verbfeatures[0][-1]   #sing/plur
                verbfeatures[1] = verbfeatures[1][-1]  #pers
                verbfeatures[2] = morph_translator_mod[verbfeatures[2][-1]]   #mod
                verbfeatures[3] = morph_translator_ten[verbfeatures[3][-1]]   #temp
                #feature ordinament
                verbfeatures.append(verbfeatures[1])
                verbfeatures.append(verbfeatures[0])
                verbfeatures.pop(0)
                verbfeatures.pop(0)
                # compute wrong verb
                fsent = self.morphs.QueryPersonaOpposta(verbs[indVerb][1],
                                             verbs[indVerb][2], verbfeatures)
                fsent = fsent[0]
#==============================================================================
#                 # exclusion of no fit sentence
        #spostata sopra
#                 if fsent and fsent != verbs[indVerb][1]:
#                     if u'....' in [x[1] for x in tsent] or len(tsent) < 9:
#                         return False
#
#==============================================================================
                if fsent and fsent != verbs[indVerb][1]:
                    #sentences creation
                    true_sent = false_sent = true_clear = false_clear = " "
                    for ele in tsent:
                        if ele[1] == verbs[indVerb][1]:
                            true_sent += ' __'+verbs[indVerb][1]+'___ '
                            true_clear += verbs[indVerb][1]
                            false_sent += ' __'+fsent+'__ '
                            false_clear += fsent
                            # trick
                            verbs[indVerb][1] = None
                        else:
                            true_sent += " " + ele[1]
                            true_clear += " " + ele[1]
                            false_sent += " " + ele[1]
                            false_clear += " " + ele[1]
                    #sentences cleaning and normalization
                    true_sent = true_sent.strip()
                    true_clear = true_clear.strip()
                    false_sent = false_sent.strip()
                    false_clear = false_clear.strip()

                    true_sent = true_sent[0].upper() + true_sent[1:]
                    true_clear = true_clear[0].upper() + true_clear[1:]
                    false_sent = false_sent[0].upper() + false_sent[1:]
                    false_clear = false_clear[0].upper() + false_clear[1:]

                    #sample return
                    if false_sent not in self.__samples:
                        self.__samples.append (false_sent)
                        return [true_sent, false_sent, true_clear, false_clear]
                    else:
                        return False
            except:
                return False
            return False
        else:
            return False


    def LoadSentence (self, inx):
        """
        Args:
            inx (int): index of the sentence
        Returns:
            list [sentence extracted from corpus]

        This method return a sentence extracted from corpus
        """
        with io.open ( self.__corpusFilename, 'r', encoding="utf-8") as fc:
            return self.ExtractSentence(fc, int(inx), os.fstat(fc.fileno()).st_size)


if __name__=='__main__':
    print ("Test Mode")
    a=SentenceExtractor('morphitUtf8.txt', "corpus", ['True','False'])
    a.LoadIndex ()
    a.SaveSamplesInTwoFiles ("SAMPLES", 30)