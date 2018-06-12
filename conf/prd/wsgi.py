"""
WSGI config for WorldCup
"""
import os
import sys
import site


#os.environ.setdefault('NEWSFUSE_MONGO_HOST', '127.0.0.1')
site.addsitedir('/home/infolab/env/WorldCup/lib/python3.5/site-packages')
sys.path.append('/home/infolab/apps/WorldCup/app')
sys.stdout = sys.stderr

from WorldCup import app as application
if __name__ == "__main__":
	application.run()
