#-*- encoding:utf-8 -*-

from __future__ import unicode_literals, with_statement, division

import codecs

person_reverse = {u's':u'p', u'p': u's'}

class MorphItDataExtractor(object):
    
    """
    questa classe si occupa di estrarre i dati da morphIt
    
    """    
    def __init__(self, morphit):
        self.MorphItFileName = morphit
            
        self.verbTags = ['VER','AUX','MOD','CAU','ASP']
        self.__verbi = []
        
        #carico i dati di MorphIt in memoria, mantenendo solo i verbi
        self.__CaricaVerbi ()

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
            verbs = [verb for verb in self.__verbi if verb[1] == infin]
            try: 
                #inverto la persona
                verbfeatures[3] = person_reverse[verbfeatures[3]]
                verbs = [verb for verb in verbs if verb[2] == verbfeatures]

                
                maxlenverb = verbs[0]
                for verb in verbs:
                    if len(verb[0]) > len(maxlenverb[0]):
                        maxlenverb = verb
                #restituisco il verbo con la persona cambiata
                return maxlenverb
              
            except:
                return False
        except ValueError:
            return False
        
        
    def __CaricaVerbi (self):        
        with codecs.open(self.MorphItFileName,'r', 'utf-8') as f:
            for line in f.readlines():
                line = line.split()
                try:
                    for verbTag in self.verbTags:
                        if line[2].startswith(verbTag):
                            #modifico la terza colonna così da ottenere già i dati pronti per le ricerche successive
                            line[2]=line[2].split(u'+')
                            line[2][0]=line[2][0][line[2][0].find(u':')+1:]

#                            print "s/p", line[2][3]   #plur / sing
#                            print "pers", line[2][2]   #persona
#                            print "temp", line[2][1]  #tempo verbale
#                            print "modo", line[2][0]  #modo
##                            
                            #carico la riga del verbo in memoria
                            self.__verbi.append(line)
                            
                except:
                    pass
               