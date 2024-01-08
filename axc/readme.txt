VER: 1/1/2024

axc - arXiv crawler

REQUIREMENTS:
    python 3 libraries:
        BeautifulSoup

    pdflatex
    linux
    Windows/Mac UNTESTED


TODO:
    choose number of summaries
    auto download full papers where relevant
    find similar topics based on related keywords
    track new keywords and build database of relevant terms
        this will make it eaiser to look for news
    generalize keys list generation
    fix pdflatex hang




Functionality:
    request arxiv for summaries based on category and keywords
    formats the list of summaires into an attractive format


Usage per current version:
    "python ./main.py" produces pdfs in a folder with todays date

    IF THE PROGRAM HANGS it is likely a problem with the latex formatting, this will be fixes eventually, most issues can be resolved by pressing "enter" repeatedly
