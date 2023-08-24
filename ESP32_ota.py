from utils import connect_serial

if __name__ == "__main__":

	ser, filename = connect_serial(timeout=1, default_filename="ota.log")

	f = open(filename, 'wb')

	ota_firmware = "C:/Users/Rock_/Desktop/Projects/ESP32_Network_Toolbox/ESP32_code/build/esp32_network_toolbox.bin"

	with open(ota_firmware, "rb") as firmwarefile:
		data = firmwarefile.read()

	size = len(data)

	print(f"[+] OTA file loaded with size: {size}")

	ser.write(f"version\r\n".encode())
	try:
		while True:
			ln = ser.read_until(b"\r\n")
			print(ln)
			f.write(ln)
			f.flush()
			if ln.startswith(b'{"VERSION":'):
				break
	except KeyboardInterrupt:
		print("[+] Stopping...")

	ser.write(f"ota_flash {size}\r\n".encode())
	print("[+] OTA started...")

	try:
		while True:
			ln = ser.read_until(b"\r\n")
			print(ln)
			f.write(ln)
			f.flush()
			if ln == b'esp_ota_begin succeeded \r\n':
				break
	except KeyboardInterrupt:
		print("[+] Stopping...")

	print("[+] Start sending.")

	try:
		for i in range(0, size, 4096):
			written = ser.write(data[i:i+4096])
			while True:
				ln = ser.read_until(b"\r\n")
				if ln == b"OK\r\n":
					break
				else:
					print(ln)
					f.write(ln)
					f.flush()
					if ln == b"OTA Update has Ended \r\n":
						break
	except KeyboardInterrupt:
		print("[+] Stopping...")

	print("[+] Sending done.")

	try:
		while True:
			ln = ser.read_until(b"\r\n")
			print(ln)
			f.write(ln)
			f.flush()
	except KeyboardInterrupt:
		print("[+] Stopping...")

	f.close()
	ser.close()
	print("[+] Done.")
