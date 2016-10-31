# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 22:10:37 2016

@author: patrizio
"""

# -*- coding: utf-8 -*-

import argparse
import SentenceExtractor

print ("DeGrammaticalizer")

#ARGUMENTS PARSER    

parser = argparse.ArgumentParser(prog='DeGrammaticalizer', 
    description="".join(open("DESCRIPTION", "r").readlines()) + "\n" + \
    "".join(open("LICENSE", "r").readlines()),    
    epilog="".join(open("CONTRIBUTORS", "r").readlines()),              )

#parameters
parser.add_argument('--corpus','-c', required=True, action='store', 
                    metavar="FILE", help="corpus")
#examples                    
parser.add_argument('--examples', '-n',required=False, action='store',
#                    type=argparse.FileType('a'), metavar="FILE",
                    help="number of samples to create")
#show License
parser.add_argument('--outTrueSentence', '-t',required=False, action='store',
#                    type=argparse.FileType('a'), metavar="FILE",
                    help="file contenent true sentences")    
                    
parser.add_argument('--outFalseSentence', '-f',required=False, action='store',
#                    type=argparse.FileType('a'), metavar="FILE",
                    help="file contenent false sentences")                    
parser.add_argument('--outfile', '-o',required=False, action='store',
#                    type=argparse.FileType('a'), metavar="FILE",
                    help="file mixed true and false sentences")
#show License
parser.add_argument("--licenze", "-l","-L", required=False, action="store_true",
                        help="See Licenze")
#show project and contributors
parser.add_argument("--project", "-p","-P", required=False, action="store_true",
                        help="See Project and contributors")
                        
args = parser.parse_args()

if args.licenze:
    print ("".join(open("LICENSE", "r").readlines()))
elif args.project:
    print (("".join(open("DESCRIPTION", "r").readlines()) + "\n" +     
        "".join(open("CONTRIBUTORS", "r").readlines())))
else:
    if not args.examples:
        args.examples = 15
        
    if not args.outTrueSentence:
        args.outTrueSentence = "TrueSentence.txt"
    if not args.outFalseSentence:
        args.outFalseSentence = "FalseSentence.txt"
        
    ste = SentenceExtractor.SentenceExtractor(args.corpus, 
                            [args.outTrueSentence, args.outFalseSentence])
    if not args.outfile:
        args.outfile = "Samples.txt"
    
        
    ste.LoadIndex ()
    ste.SaveSamplesInTwoFiles (args.outfile, int(args.examples))
    print ("Samples Creati")