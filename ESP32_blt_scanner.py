import json
from utils import connect_serial
import time

SCAN_DURATION = 10

if __name__ == "__main__":

	ser, filename = connect_serial(timeout=1, default_filename="blt_scan.json")

	f = open(filename, 'wb')

	ser.write("blt_scan\r\n".encode())
	print("[+] Scanner started...")

	start_time = time.perf_counter()

	try:
		while True:
			ln = ser.read_until(b"<STOP>")
			f.write(ln.replace(b"<STOP>", b""))
			f.flush()
			if time.perf_counter() - start_time >= SCAN_DURATION + 2:
				break
	except KeyboardInterrupt:
		ser.write("stop\r\n".encode())
		print("[+] Stopping...")

	f.close()
	ser.close()
	print("[+] Done.")
