import requests
import time
from xml.etree import cElementTree as ET
import os
from bs4 import BeautifulSoup
from pathlib import Path
import subprocess
from datetime import date



def main():
    a = Path('./physics/boson~gate.html').read_text()
    soup = BeautifulSoup(a, 'lxml')
    cat = "physics"
    topic = "boson-gate"
    
    today = date.today()
    fd = today.strftime("%Y-%m-%d")
    if not (os.path.exists(f"./{fd}/")):
        os.makedirs(f"./{fd}/")

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
    

    
    for child in list(soup.contents[1].contents[0].contents[0].children):
        print(child.name)
        if child.name == "entry":

            cid = child.id.get_text()
            cupd = child.updated.get_text()
            cpub = child.published.get_text()
            ctitle = child.title.get_text()
            csum = child.summary.get_text()
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

'''


    texstr = texstr + '''\end{document}'''
    filepath = f"./{fd}/{cat}_{topic}.tex"
    file = open(filepath, "w")
    file.write(texstr)
    file.close()
    command = f'pdflatex -output-directory=./{fd}/ {filepath}'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
    print(result.stdout) 
    subprocess.run(f"rm {filepath}", shell=True, stdout=subprocess.PIPE, text=True)
    subprocess.run(f"rm ./{fd}/*.aux", shell=True, stdout=subprocess.PIPE, text=True)
    subprocess.run(f"rm ./{fd}/*.log", shell=True, stdout=subprocess.PIPE, text=True)

    
if __name__ == '__main__':
    main()