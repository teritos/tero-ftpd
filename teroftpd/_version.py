"""Holder of the tero version number."""

VERSION = (0, 1)
__version__ = '.'.join([str(x) for x in VERSION])

# pylint: disable=W1401
BANNER = '''
 /$$$$$$$$/$$$$$$$$ /$$$$$$$   /$$$$$$                       
|__  $$__/ $$_____/| $$__  $$ /$$__  $$                      
   | $$  | $$      | $$  \ $$| $$  \ $$                      
   | $$  | $$$$$   | $$$$$$$/| $$  | $$                      
   | $$  | $$__/   | $$__  $$| $$  | $$                      
   | $$  | $$      | $$  \ $$| $$  | $$                      
   | $$  | $$$$$$$$| $$  | $$|  $$$$$$/                      
 /$$$$$$$$/$$$$$$$$/$$$$$$$_/ \______/                       
| $$_____/__  $$__/ $$__  $$                                 
| $$        | $$  | $$  \ $$                                 
| $$$$$     | $$  | $$$$$$$/                                 
| $$__/     | $$  | $$____/                                  
| $$        | $$  | $$                                       
| $$        | $$  | $$                                       
|_/$$$$$$  /$$$$$$$$_/$$$$$$$  /$$    /$$ /$$$$$$$$ /$$$$$$$ 
 /$$__  $$| $$_____/| $$__  $$| $$   | $$| $$_____/| $$__  $$
| $$  \__/| $$      | $$  \ $$| $$   | $$| $$      | $$  \ $$
|  $$$$$$ | $$$$$   | $$$$$$$/|  $$ / $$/| $$$$$   | $$$$$$$/
 \____  $$| $$__/   | $$__  $$ \  $$ $$/ | $$__/   | $$__  $$
 /$$  \ $$| $$      | $$  \ $$  \  $$$/  | $$      | $$  \ $$
|  $$$$$$/| $$$$$$$$| $$  | $$   \  $/   | $$$$$$$$| $$  | $$
 \______/ |________/|__/  |__/    \_/    |________/|__/  |__/

                    Given gently by::
                        - jcarizza
                        - redraw
                        - edvm

                    Version: %s
''' % __version__
