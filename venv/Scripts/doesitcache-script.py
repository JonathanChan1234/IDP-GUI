#!C:\Users\Jonathan\PycharmProjects\meterGUI\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'CacheControl==0.12.4','console_scripts','doesitcache'
__requires__ = 'CacheControl==0.12.4'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('CacheControl==0.12.4', 'console_scripts', 'doesitcache')()
    )
