#!/usr/bin/python3

from miniquant_ioc.application import init_app
import logging

from miniquant_ioc._version import version

logger = logging.getLogger("miniquant_ioc")

def main():

    print(f'version: {version}')
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level="INFO")    
    
    miniApp, cmdline = init_app()
    
    #loglevel = getattr(logging, (cmdline.logging or 'INFO').upper(), None)

    #logging.basicConfig(level=loglevel)
    
    miniApp.runIoc()

    
if __name__ == "__main__":
    main()
