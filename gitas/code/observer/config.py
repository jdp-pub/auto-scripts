'''
config.py

This module provides utility functions for performing specific tasks.

Author: Jacob Purcell
Date: 01/02/24

Usage:
- Import the module: `import my_module`
- Call the functions: `my_module.some_function()`

Variables:
- userid: login id for github
- repo: list that stores repository informaiton, repo_path:branch

Functions:
- keygen

Classes:
- conf: class for using github
'''



userid = "jdp-pub"
email = "jacobdpurcell@outlook.com"

repo = [
    ["/home/jdp/Documents/Projects/auto-scripts/",f"working-{userid}", "git@github.com:jdp-pub/auto-scripts.git"],
    ["/home/jdp/Documents/Projects/examples/",f"working-{userid}", "git@github.com:jdp-pub/auto-scripts.git"],
]


class conf():
    def __init__(self, rpath, branch):
        self.rpath = rpath
        self.branch = branch