import subprocess
import time
from loguru import logger
import config

class ADBHelper:
    """Helper class untuk ADB (Android Debug Bridge) commands"""
    
    def __init__(self, host=config.BLUESTACKS_ADB_HOST, port=config.BLUESTACKS_ADB_PORT):
        self.host = host
        self.port = port
        self.device_id = f"{host}:{port}"
        logger.add(f"{config.LOG_DIR}/adb.log", level=config.LOG_LEVEL)
    
    def _execute_adb(self, command):
        """Execute ADB command"""
        try:
            full_command = f"adb -s {self.device_id} {command}"
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True, timeout=10)
            if result.returncode != 0:
                logger.error(f"ADB command failed: {full_command}\nError: {result.stderr}")
                return None
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"ADB execution error: {str(e)}")
            return None
    
    def connect_device(self):
        """Connect to BlueStacks device"""
        logger.info(f"Connecting to device: {self.device_id}")
        result = self._execute_adb("connect localhost:5555")
        if result and "connected" in result.lower():
            logger.success(f"Connected successfully: {result}")
            return True
        logger.error("Failed to connect to device")
        return False
    
    def get_devices(self):
        """Get list of connected devices"""
        result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
        devices = []
        for line in result.stdout.split('\n')[1:]:
            if line.strip() and 'device' in line:
                device_id = line.split()[0]
                devices.append(device_id)
        return devices
    
    def tap(self, x, y):
        """Tap on screen at coordinates (x, y)"""
        self._execute_adb(f"shell input tap {x} {y}")
        logger.debug(f"Tapped at ({x}, {y})")
    
    def type_text(self, text):
        """Type text on device"""
        # Escape special characters
        text = text.replace(" ", "%s")
        self._execute_adb(f"shell input text {text}")
        logger.debug(f"Typed: {text}")
    
    def press_key(self, key_code):
        """Press key by key code"""
        # Common key codes: 4 (back), 3 (home), 26 (power), 66 (enter)
        self._execute_adb(f"shell input keyevent {key_code}")
        logger.debug(f"Pressed key: {key_code}")
    
    def get_text_from_clipboard(self):
        """Get text from device clipboard"""
        result = self._execute_adb("shell getprop ro.clipboard.text")
        return result
    
    def take_screenshot(self, filename="screenshot.png"):
        """Take screenshot from device"""
        screenshot_path = f"screenshots/{filename}"
        self._execute_adb(f"shell screencap -p /sdcard/{filename}")
        self._execute_adb(f"pull /sdcard/{filename} {screenshot_path}")
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    def get_sms_messages(self):
        """Get SMS messages from device"""
        result = self._execute_adb("shell content query --uri content://sms/inbox")
        return result if result else None
    
    def wait_for_sms(self, timeout=120):
        """Wait for incoming SMS and extract verification code"""
        logger.info(f"Waiting for SMS verification code (timeout: {timeout}s)")
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            sms_data = self.get_sms_messages()
            if sms_data:
                # Parse SMS untuk extract kode verifikasi
                # Format: biasanya "Your WhatsApp code is: 123456"
                lines = sms_data.split('\n')
                for line in lines:
                    if 'body=' in line:
                        # Extract kode (digits only, biasanya 6 digit)
                        import re
                        codes = re.findall(r'\d{6}', line)
                        if codes:
                            logger.success(f"Verification code found: {codes[0]}")
                            return codes[0]
            
            time.sleep(config.SMS_CHECK_INTERVAL)
        
        logger.error("Timeout waiting for SMS verification code")
        return None
