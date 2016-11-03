#-*- encoding:utf-8 -*-

from __future__ import unicode_literals, with_statement, division

import codecs
import collections

person_reverse = {u's':u'p', u'p': u's'}

class MorphItDataExtractor(object):
    
    """
    questa classe si occupa di estrarre i dati da morphIt
    
    """    
    def __init__(self, morphit):
        self.MorphItFileName = morphit
            
        self.verbTags = ['VER','AUX','MOD','CAU','ASP']
#==============================================================================
#         old
#==============================================================================
#        self.__verbi = []
#==============================================================================
#         new
#==============================================================================
        self.__verbi = collections.defaultdict(list)
#==============================================================================
#         end new
#==============================================================================
        
        #carico i dati di MorphIt in memoria, mantenendo solo i verbi
        self.__CaricaVerbi ()

#==============================================================================
#     new
#==============================================================================
    def getVerbi (self):
        return self.__verbi
        
        
    def QueryPersonaOpposta (self, tverb, infin, verbfeatures):
        """
            Questa funzione mi deve restituire la voce verbale della persona 
            opposta a quella che metto
            ad esempio se metto una prima persona singolare deve restitutire
            la prima persona plurare e viceversa
            
            restituirà false se non trova una corrispondenza
        """
        
        tverb = tverb.lower()
        infin = infin.lower() 
        try: 
            #lista dei potenziali verbi
#==============================================================================
#             old
#==============================================================================
#            verbs = [verb for verb in self.__verbi if verb[1] == infin]
#==============================================================================
#             new
#==============================================================================
            verbs = self.__verbi[infin]
            try: 
                #inverto la persona
                verbfeatures[3] = person_reverse[verbfeatures[3]]
                #trovo i verbi corrispondenti
                verbs = [verb for verb in verbs if verb[1] == verbfeatures]
                #prendo il verbo completo -> sono tra sono e son                
                maxlenverb = verbs[0]
                for verb in verbs:
                    if len(verb[0]) > len(maxlenverb[0]):
                        maxlenverb = verb        
                        
                #restituisco il verbo
#                print "accettato", tverb, maxlenverb
                return maxlenverb
            except:
#                print "rejected", infin, tverb
                
                return False
        except ValueError:
            return False
        
        
    def __CaricaVerbi (self):        
        with codecs.open(self.MorphItFileName,'r', 'utf-8') as f:
            for line in f.readlines():
                line = line.split()
                try:
                    
                    
#==============================================================================
#                     old
#                     for verbTag in self.verbTags:
#                         if line[2].startswith(verbTag):
#                             ....
#==============================================================================
#                    new 
                    if line[2][:3] in self.verbTags:
                        #modifico la terza colonna così da ottenere già i dati pronti per le ricerche successive
                        line[2]=line[2].split(u'+')
                        line[2][0]=line[2][0][line[2][0].find(u':')+1:]
                            
#==============================================================================
#                             print "s/p", line[2][3]   #plur / sing
#                             print "pers", line[2][2]   #persona
#                             print "temp", line[2][1]  #tempo verbale
#                             print "modo", line[2][0]  #modo
#==============================================================================
##                            
                            #carico la riga del verbo in memoria
#==============================================================================
#                             old
#==============================================================================
#                            self.__verbi.append(line)
#==============================================================================
#                             new
#==============================================================================
                        self.__verbi[line[1]].append([line[0],line[2]])
#==============================================================================
#                             end new
#==============================================================================
                except:
                    pass
                
if __name__ == '__main__':
    a =MorphItDataExtractor("morphitUtf8.txt")
    print "fine caricamento"
    b=a.getVerbi()
    print b['giocare']