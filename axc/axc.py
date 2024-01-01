import requests
import time
from xml.etree import cElementTree as ET
import os
from bs4 import BeautifulSoup
from pathlib import Path
import subprocess
from datetime import date


def export(keys: list, a: list):
     index = 0
     
     
     for kc in keys:
          print(f"generating {kc[0]}:{kc[1]}")
          soup = BeautifulSoup(a[index].text, 'lxml')
          cat = kc[0]
          topic = kc[1].replace("~", "-")
          today = date.today()
          fd = today.strftime("%Y-%m-%d")
          if not (os.path.exists(f"./{fd}/{cat}/")):
               os.makedirs(f"./{fd}/{cat}/")

          texstr = r'''
\documentclass{article}

\usepackage[margin=0.45in]{geometry}
\usepackage{braket}
\usepackage{graphicx}% Include figure files
\usepackage{dcolumn}% Align table columns on decimal point
\usepackage{bm}% bold math
\usepackage{amsfonts}
\usepackage{color}   
\usepackage{comment}
\usepackage{float}
\usepackage[export]{adjustbox}
\usepackage{amsmath}

\begin{document}



\title{''' + cat + r''':''' + topic.replace("_","~") + r'''}

\maketitle

     '''

          cid = ""
          cupd = ""
          cpub = ""
          ctitle = ""
          csum = ""
          cterm = ""
          cauth = ""
          ccom = ""

          for child in list(soup.contents[1].contents[0].contents[0].children):

               if child.name == "entry":

                    cid = child.id.get_text()
                    cupd = child.updated.get_text()
                    cpub = child.published.get_text()
                    ctitle = child.title.get_text()
                    csum = child.summary.get_text()

                    # clean summary
                    if ' /' in csum:
                         csum = csum.split()
                         for word in csum:
                              if word.startswith(" \\"):
                                   csum[csum.find(word)] = "$" + word + "$"

                         csum = ' '.join(csum)


                    cterm = child.category['term']
                    cauth = ""
                    ccom = ""
                    for ca in child:
                         if ca.name == "author":
                              cauth = cauth + ca.get_text()[0:-1]
                              cauth = cauth + ", "

                         if ca.name == "arxiv:comment":
                              ccom = ca.get_text()
                    cauth = cauth[0:-2]

                    texstr = texstr + r'''\section{''' + ctitle \
+ r'''} 
\subsection*{''' + cauth + r'''}

\subsubsection*{Metadata}

ID: ''' + cid + r'''\\
UPDATED: ''' + cupd + r'''\\
PUBLISHED: ''' + cpub + r'''\\
''' + cterm + r''' :: ''' + ccom + r'''\\

\subsection*{Summary}

''' + csum + r'''

\noindent\rule{\textwidth}{1pt}

'''

          print(f"writing {topic}.tex")
          texstr = texstr + '''\end{document}'''
          filepath = f"./{fd}/{cat}/{topic}.tex"
          file = open(filepath, "w")
          file.write(texstr)
          file.close()
          print(f"compiling {topic}.pdf")
          command = f'pdflatex -output-directory=./{fd}/{cat} {filepath}'
          result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
          print(result.stdout) 
          print(f"cleaning directory")
          subprocess.run(f"rm ./{fd}/{cat}/*.tex", shell=True, stdout=subprocess.PIPE, text=True)
          subprocess.run(f"rm ./{fd}/{cat}/*.aux", shell=True, stdout=subprocess.PIPE, text=True)
          subprocess.run(f"rm ./{fd}/{cat}/*.log", shell=True, stdout=subprocess.PIPE, text=True)
          index = index+1



def clean(keys: list, path: str):

          
     return [(i[0],i[1].replace(" ", path)) for i in keys]

def query(keys: str):
     keys = clean(keys, "~")
     reql = []
     base_url = "http://export.arxiv.org/api/query"


     index = 1
     for i in keys:
          sq = i[0] + ":" + i[1]
          
          params = {
               "search_query" : sq,
               "start" : "0",
               "max_results" : "10"
          }

          reql.append(requests.get(base_url, params=params))
          print(f"{index/len(keys)*100.0}% | {i[0]}:{i[1]}; {reql[-1].status_code}")
          if index != len(keys):
               time.sleep(5)

          index = index + 1

     return reql

