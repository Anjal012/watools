import time
from loguru import logger
import config

class SMSHandler:
    """Handler untuk SMS verification"""
    
    def __init__(self, adb_helper):
        self.adb = adb_helper
        logger.add(f"{config.LOG_DIR}/sms.log", level=config.LOG_LEVEL)
    
    def wait_and_extract_code(self, timeout=None):
        """
        Tunggu SMS masuk dan extract kode verifikasi
        
        Args:
            timeout: Waktu maksimal menunggu (default dari config)
        
        Returns:
            str: Verification code jika ditemukan, None jika timeout
        """
        if timeout is None:
            timeout = config.SMS_WAIT_TIME
        
        logger.info(f"SMS Handler: Waiting for verification code (timeout: {timeout}s)")
        
        code = self.adb.wait_for_sms(timeout)
        
        if code:
            logger.success(f"SMS verification code extracted: {code}")
            return code
        else:
            logger.error("Failed to extract SMS verification code")
            return None
    
    def input_verification_code(self, code):
        """
        Input kode verifikasi ke field WhatsApp
        
        Args:
            code: Verification code (6 digits)
        """
        if not code or len(code) != 6:
            logger.error(f"Invalid verification code format: {code}")
            return False
        
        try:
            logger.info(f"Inputting verification code: {code}")
            
            # Input setiap digit dengan delay kecil
            for digit in code:
                self.adb.type_text(digit)
                time.sleep(0.3)
            
            logger.success("Verification code entered successfully")
            time.sleep(1)
            
            # Press enter atau tap button confirm
            self.adb.press_key(66)  # Enter key
            
            return True
        except Exception as e:
            logger.error(f"Error inputting verification code: {str(e)}")
            return False
    
    def verify_sms_received(self):
        """
        Check jika SMS sudah diterima
        
        Returns:
            bool: True jika ada SMS, False jika tidak
        """
        sms_data = self.adb.get_sms_messages()
        if sms_data and len(sms_data) > 0:
            logger.info("SMS received detected")
            return True
        logger.warning("No SMS received yet")
        return False
