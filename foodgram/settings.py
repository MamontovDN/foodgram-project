import os
from dotenv import load_dotenv

load_dotenv()

if os.environ.get('SETTINGS_MODULE') == 'dev':
    from .settings_pack.settings_dev import *
else:
    from .settings_pack.settings_deploy import *
