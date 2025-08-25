import os


TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    raise LookupError('No telegram token provided')

SUPPORT_CHAT_ID = os.environ.get('SUPPORT_CHAT_ID')
if not SUPPORT_CHAT_ID:
    raise LookupError('No support chat ID provided')

DEBUG = False
