# -*- coding: utf-8 -*-

"""
                                DeGrammaticalizer.py

This module allows to insert this project into a pipeline

Vesion: 1.0-c stable
CODE TESTED ON Python 3.5 and Python 2.7
#=============================================================================
Università degli studi di Trento (Tn) - Italyy
Center for Mind/Brain Sciences CIMeC
Language, Interaction and Computation Laboratory CLIC

@author: Patrizio Bellan
         patrizio.bellan@gmail.com
         patrizio.bellan@studenti.unitn.it

         github.com/patriziobellan86

#==============================================================================
HOW TO USE IT:

patrizio@mintpatrizioCimec $ python  DeGrammaticalizer.py -h

usage: DeGrammaticalizer [-h] --corpus FILE [--examples EXAMPLES]
                         [--morphit MORPHIT]
                         [--outTrueSentence OUTTRUESENTENCE]
                         [--outFalseSentence OUTFALSESENTENCE]
                         [--outfile OUTFILE] [--licenze] [--project]

Description [...]

optional arguments:
  -h, --help            show this help message and exit
  --corpus FILE, -c FILE
                        corpus
  --examples EXAMPLES, -n EXAMPLES
                        number of samples to create
  --morphit MORPHIT, -m MORPHIT
                        morphit
  --outTrueSentence OUTTRUESENTENCE, -t OUTTRUESENTENCE
                        file contenent true sentences
  --outFalseSentence OUTFALSESENTENCE, -f OUTFALSESENTENCE
                        file contenent false sentences
  --outfile OUTFILE, -o OUTFILE
                        file mixed true and false sentences
  --licenze, -l         See Licenze
  --project, -p         See Project and contributors


#==============================================================================
EXAMPLE OF USE:
patrizio@mintpatrizioCimec $ python  DeGrammaticalizer.py -c
corpus -m morphitLexicon -o Examples -t True_Sentences -f False_Sentences

"""

import argparse
import os

import SentenceExtractor

#ARGUMENTS PARSER
try:
    parser = argparse.ArgumentParser(prog='DeGrammaticalizer',
        description="".join(open(os.path.dirname(os.path.realpath(__file__))+
        os.path.sep+"DESCRIPTION", "r").readlines()) + "\n" + \
        "".join(open(os.path.dirname(os.path.realpath(__file__))+
        os.path.sep+"LICENSE", "r").readlines()),
        epilog="".join(open(os.path.dirname(os.path.realpath(__file__))+
        os.path.sep+"CONTRIBUTORS", "r").readlines()))
except:
     parser = argparse.ArgumentParser(prog='DeGrammaticalizer')


# parameters
parser.add_argument('--corpus', '-c', required=True, action='store',
                    metavar="FILE", help="corpus")
# examples
parser.add_argument('--examples', '-n', required=False, action='store',
                    help="number of samples to create")
# morphit
parser.add_argument('--morphit', '-m', required=False, action='store',
                    help="morphit")
# true sents
parser.add_argument('--outTrueSentence', '-t', required=False, action='store',
                    help="file contenent true sentences")
# false sents
parser.add_argument('--outFalseSentence', '-f', required=False, action='store',
                    help="file contenent false sentences")
# Samples
parser.add_argument('--outfile', '-o', required=False, action='store',
                    help="file mixed true and false sentences")
# show License
parser.add_argument("--licenze", "-l", required=False, action="store_true",
                    help="See Licenze")
# show project and contributors
parser.add_argument("--project", "-p", required=False, action="store_true",
                    help="See Project and contributors")

args = parser.parse_args()

if args.licenze:
    print ("".join(open(os.path.dirname(os.path.realpath(__file__))+
            os.path.sep+"LICENSE", "r").readlines()))
elif args.project:
    print (("".join(open(os.path.dirname(os.path.realpath(__file__))+
            os.path.sep+"DESCRIPTION", "r").readlines()) + "\n" +
        "".join(open(os.path.dirname(os.path.realpath(__file__))+
            os.path.sep+"CONTRIBUTORS", "r").readlines())))
else:
    if not args.examples:
        args.examples = 15
    if not args.outTrueSentence:
        args.outTrueSentence = "TrueSentence.txt"
    if not args.outFalseSentence:
        args.outFalseSentence = "FalseSentence.txt"
    if not args.morphit:
        args.morphit = os.path.dirname(os.path.realpath(__file__))+ \
            os.path.sep+"morphitUtf8.txt"
    if not args.outfile:
        args.outfile = "Samples.txt"
    #start program
    ste = SentenceExtractor.SentenceExtractor(args.morphit, args.corpus,
                            [args.outTrueSentence, args.outFalseSentence])

    #save data
    ste.LoadIndex ()
    ste.SaveSamplesInTwoFiles (args.outfile, int(args.examples))
