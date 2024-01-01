import requests
import config
import glui
import functions as fu

def main():

    #TODO:
    #   check credentials
    #   if there are no credentials, generate ssh and keys
    #   initialize persistent script
    #   script performs pushes and pulls using github api

    token = "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"

    cf = config.SSHConf("../", "jdp-pub", "", "auto-scripts", "main", token)

    fu.gitf(cf, True)

if __name__ == '__main__':
    main()