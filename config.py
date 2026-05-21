import os
from dotenv import load_dotenv

load_dotenv()

# BlueStacks Configuration
BLUESTACKS_ADB_HOST = os.getenv('BLUESTACKS_ADB_HOST', 'localhost')
BLUESTACKS_ADB_PORT = int(os.getenv('BLUESTACKS_ADB_PORT', '5555'))

# WhatsApp Configuration
WHATSAPP_PACKAGE = 'com.whatsapp'
WHATSAPP_ACTIVITY = 'com.whatsapp.Main'

# SMS Configuration
SMS_WAIT_TIME = int(os.getenv('SMS_WAIT_TIME', '120'))  # seconds
SMS_CHECK_INTERVAL = int(os.getenv('SMS_CHECK_INTERVAL', '5'))  # seconds

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_DIR = 'logs'

# Timeout Configuration
DEFAULT_TIMEOUT = 10
LONG_TIMEOUT = 30

# Test Configuration
PHONE_NUMBER = os.getenv('PHONE_NUMBER', '')  # Input saat runtime jika kosong
