'''
install.py

initial setup, generates keys, logs into github, 
creates a background process that detects when desired 
repos are updated, auto push on change.

Author: Jacob Purcell
Date: 01/02/24

Usage:
- run as "python install.py"
- follow prompts, autosync will be enabled after program completion

Functions:
- keygen

Classes:
- user: your credentials, input before setup
 '''

import os


class user():
    def __init__(self):
        self.email = "your@email.com"
        self.uname = "jdp-pub"

def main():
    gu = user()

    kefile = f"id_rsa_github_{gu.uname}"
    os.system(f"ssh-keygen -t rsa -b 4096 -C \"{gu.email}\" -f ~/.ssh/")



if __name__ == '__main__':
    main()