import sys
import logging
logging.basicConfig(stream=sys.stderr)

path = "/var/www/html/devop/BOG/Flask/g_wifi/g_wifi"
if path not in sys.path:
	sys.path.insert(0,path)
from g_wifi import app as application