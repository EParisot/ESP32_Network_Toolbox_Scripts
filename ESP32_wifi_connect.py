import json
from utils import connect_serial
import time

if __name__ == "__main__":

	ser, filename = connect_serial(timeout=1)

	f = open(filename, 'wb')

	ser.write("wifi_connect colloc\ 50 bienvenuecheznous\r\n".encode())
	print("[+] Connecting wifi...")

	try:
		tmp = b""
		while True:
			ln = ser.read_until(b"<STOP>")
			f.write(ln.replace(b"<STOP>", b""))
			f.flush()
			if len(tmp):
				ln = tmp + ln
			try:
				print(ln)
				json.loads(ln)
				tmp = b""
			except:
				tmp = ln
				continue
			try:
				ip = json.loads(ln)["IP"]
				if ip != "None":
					print("Connected with ip %s" % ip)
					break
			except:
				pass
	except KeyboardInterrupt:
		ser.write("stop\r\n".encode())
		print("[+] Stopping...")


	f.close()
	ser.close()
	print("[+] Done.")
