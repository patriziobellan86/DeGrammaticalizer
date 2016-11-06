#-*- encoding:utf-8 -*-
"""
                               morphitDataExtractor.py

This module contains the class to extract and elaborate data from morphit

Everything you need is not here!

Vesion: 1.0-c stable
CODE TESTED ON Python 3.5 and Python 2.7
#==============================================================================
Università degli studi di Trento (Tn) - Italy
Center for Mind/Brain Sciences CIMeC
Language, Interaction and Computation Laboratory CLIC

@author: Patrizio Bellan
         patrizio.bellan@gmail.com
         patrizio.bellan@studenti.unitn.it

         github.com/patriziobellan86

#==============================================================================
"""
from __future__ import unicode_literals, with_statement, division

import codecs
import collections

person_reverse = {u's':u'p', u'p': u's'}

class MorphItDataExtractor(object):

    """
    This class extracts and elaborates data from morphit

    """
    def __init__(self, morphit):
        """
            __init__ needs only to knwo where is lexicon
        """
        self.MorphItFileName = morphit

        self.verbTags = ['VER','AUX','MOD','CAU','ASP']
        self.__verbi = collections.defaultdict(list)

        #load verbs from morphit
        self.__CaricaVerbi ()


    def QueryPersonaOpposta (self, tverb, infin, verbfeatures):
        """
         Args:
            tverb (str): verb
            infin (str): infinitive form of the verb
            verbfeatures (list): features of the verb

        Returns:
            verb changed if exist
            False instead


        This method return the same verb but conjugate with the opposite person

        es: sono (1 sing)         return: siamo (1 plur)

        """


        tverb = tverb.lower()
        infin = infin.lower()
        try:
            #list of all the conjugate verbs of the verb given
            verbs = self.__verbi[infin]
            try:
                #person reverse
                verbfeatures[3] = person_reverse[verbfeatures[3]]
                #looking for the candidates
                verbs = [verb for verb in verbs if verb[1] == verbfeatures]
                #choose only not abbreviate verb
                maxlenverb = verbs[0]
                for verb in verbs:
                    if len(verb[0]) > len(maxlenverb[0]):
                        maxlenverb = verb
                return maxlenverb
            except:
                return False
        except ValueError:
            return False


    def __CaricaVerbi (self):
        """
        This method loads verbs from morphit
        """
        with codecs.open(self.MorphItFileName,'r', 'utf-8') as f:
            for line in f.readlines():
                line = line.split()
                try:
                    if line[2][:3] in self.verbTags:
                        line[2]=line[2].split(u'+')
                        line[2][0]=line[2][0][line[2][0].find(u':')+1:]

                        self.__verbi[line[1]].append([line[0],line[2]])
                except:
                    pass