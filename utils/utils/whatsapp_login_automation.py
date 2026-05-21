#!/usr/bin/env python3
"""
WhatsApp Automation Testing Tool
Automated login dengan SMS verification untuk WhatsApp
"""

import time
import os
from loguru import logger
from utils.adb_helper import ADBHelper
from utils.sms_handler import SMSHandler
import config

# Setup logging
if not os.path.exists(config.LOG_DIR):
    os.makedirs(config.LOG_DIR)
if not os.path.exists('screenshots'):
    os.makedirs('screenshots')

logger.add(f"{config.LOG_DIR}/whatsapp_automation.log", level=config.LOG_LEVEL)

class WhatsAppAutomation:
    """Main class untuk WhatsApp automation"""
    
    def __init__(self):
        self.adb = ADBHelper()
        self.sms_handler = SMSHandler(self.adb)
        logger.info("WhatsApp Automation initialized")
    
    def check_device_connection(self):
        """Check koneksi device"""
        logger.info("Checking device connection...")
        devices = self.adb.get_devices()
        
        if not devices:
            logger.error("No devices found. Please ensure BlueStacks is running and ADB is enabled.")
            logger.info("Steps to enable ADB in BlueStacks:")
            logger.info("1. Open BlueStacks")
            logger.info("2. Go to Settings > Advanced > Android Debug Bridge (ADB)")
            logger.info("3. Enable 'Enable Android Debug Bridge'")
            logger.info("4. Click 'Apply' and restart BlueStacks if needed")
            return False
        
        logger.success(f"Found devices: {devices}")
        
        if not self.adb.connect_device():
            logger.error("Failed to connect to BlueStacks device")
            return False
        
        logger.success("Device connected successfully")
        return True
    
    def open_whatsapp(self):
        """Buka aplikasi WhatsApp"""
        logger.info("Opening WhatsApp...")
        
        try:
            self.adb._execute_adb(f"shell am start -n {config.WHATSAPP_PACKAGE}/{config.WHATSAPP_ACTIVITY}")
            time.sleep(3)  # Wait for app to open
            logger.success("WhatsApp opened")
            self.adb.take_screenshot("whatsapp_opened.png")
            return True
        except Exception as e:
            logger.error(f"Failed to open WhatsApp: {str(e)}")
            return False
    
    def enter_phone_number(self, phone_number):
        """Input nomor telepon untuk login"""
        logger.info(f"Entering phone number: {phone_number}")
        
        try:
            # Tunggu input field muncul
            time.sleep(2)
            
            # Tap pada input field (koordinat bisa berbeda tergantung device)
            self.adb.tap(540, 400)  # Adjust coordinates if needed
            time.sleep(0.5)
            
            # Clear field
            self.adb.press_key(67)  # Backspace multiple times
            for _ in range(20):
                self.adb.press_key(67)
                time.sleep(0.05)
            
            # Type phone number
            self.adb.type_text(phone_number)
            time.sleep(0.5)
            
            logger.success(f"Phone number entered: {phone_number}")
            self.adb.take_screenshot("phone_number_entered.png")
            return True
        except Exception as e:
            logger.error(f"Failed to enter phone number: {str(e)}")
            return False
    
    def request_sms_verification(self):
        """Request SMS verification code"""
        logger.info("Requesting SMS verification...")
        
        try:
            # Tap button "Next" atau "Request SMS"
            # Koordinat bisa berbeda - adjust sesuai device Anda
            self.adb.tap(540, 500)  # "Next" button
            time.sleep(2)
            
            logger.info("SMS verification requested")
            self.adb.take_screenshot("sms_requested.png")
            return True
        except Exception as e:
            logger.error(f"Failed to request SMS verification: {str(e)}")
            return False
    
    def wait_for_sms_and_verify(self):
        """Tunggu SMS dan input kode verifikasi"""
        logger.info("Waiting for SMS verification code...")
        
        try:
            # Tunggu SMS
            code = self.sms_handler.wait_and_extract_code()
            
            if not code:
                logger.error("Failed to get verification code from SMS")
                return False
            
            logger.success(f"Got verification code: {code}")
            
            # Input kode verifikasi
            time.sleep(1)
            if not self.sms_handler.input_verification_code(code):
                logger.error("Failed to input verification code")
                return False
            
            logger.success("Verification code submitted")
            self.adb.take_screenshot("sms_verified.png")
            return True
        except Exception as e:
            logger.error(f"Failed to verify SMS: {str(e)}")
            return False
    
    def login(self, phone_number):
        """Main login flow"""
        logger.info("=" * 60)
        logger.info("Starting WhatsApp Login Automation")
        logger.info("=" * 60)
        
        # Step 1: Check device connection
        if not self.check_device_connection():
            logger.error("Device connection check failed")
            return False
        
        # Step 2: Open WhatsApp
        if not self.open_whatsapp():
            logger.error("Failed to open WhatsApp")
            return False
        
        # Step 3: Enter phone number
        if not self.enter_phone_number(phone_number):
            logger.error("Failed to enter phone number")
            return False
        
        # Step 4: Request SMS verification
        if not self.request_sms_verification():
            logger.error("Failed to request SMS verification")
            return False
        
        # Step 5: Wait for SMS and verify
        if not self.wait_for_sms_and_verify():
            logger.error("Failed to verify SMS")
            return False
        
        logger.success("=" * 60)
        logger.success("WhatsApp Login Successful!")
        logger.success("=" * 60)
        
        # Wait untuk app fully loaded
        time.sleep(5)
        self.adb.take_screenshot("login_success.png")
        
        return True

def main():
    """Main entry point"""
    print("\n" + "="*60)
    print("WhatsApp Automation Testing Tool")
    print("="*60 + "\n")
    
    # Get phone number
    phone_number = input("Enter your WhatsApp phone number (with country code, e.g., +62812345678): ").strip()
    
    if not phone_number.startswith('+'):
        print("[!] Phone number should start with '+' and include country code")
        phone_number = '+' + phone_number
    
    # Remove spaces and special characters
    phone_number = phone_number.replace(' ', '').replace('-', '')
    
    print(f"\n[*] Using phone number: {phone_number}")
    print("[*] Make sure:")
    print("    1. BlueStacks is running")
    print("    2. WhatsApp is installed in BlueStacks")
    print("    3. ADB debugging is enabled")
    print("    4. You will receive an SMS with verification code")
    print("\nStarting login process...\n")
    
    # Start automation
    automation = WhatsAppAutomation()
    success = automation.login(phone_number)
    
    if success:
        print("\n[✓] Login completed successfully!")
        print("[*] Check the 'logs' folder for detailed logs")
        print("[*] Screenshots saved in 'screenshots' folder")
    else:
        print("\n[✗] Login failed!")
        print("[*] Check the 'logs' folder for error details")
        print("[*] Adjust the tap coordinates if elements are not found")

if __name__ == "__main__":
    main()
