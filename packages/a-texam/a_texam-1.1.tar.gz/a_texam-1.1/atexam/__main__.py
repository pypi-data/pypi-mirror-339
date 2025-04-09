from atexam.app import app, socketio
import os
from threading import Timer
import webbrowser
import socket

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def open_browser():
    ip = get_ip_address()
    webbrowser.open(f"http://{ip}:5000")

def main():
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        Timer(1, open_browser).start()
    socketio.run(app, host="0.0.0.0", debug=True)

if __name__ == '__main__':
    main()
