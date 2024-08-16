import socket

try:
    print("smtp.simmon.jp:", socket.gethostbyname('smtp.simmon.jp'))
except socket.gaierror as e:
    print(f"エラー (smtp.simmon.jp): {e}")

try:
    print("simmon.jp:", socket.gethostbyname('simmon.jp'))
except socket.gaierror as e:
    print(f"エラー (simmon.jp): {e}")