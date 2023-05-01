import json
from utils import connect_serial

if __name__ == "__main__":

	ser, filename = connect_serial(timeout=1)

	f = open(filename, 'wb')

	# set country
	country = "FR"

	try:
		countryInput = input("[?] Select a country (default '%s'): " % country)
		if countryInput != "":
			country = countryInput
	except KeyboardInterrupt:
		print("\n[+] Exiting...")
		exit()

	ser.write(("set country %s\r\n" % country).encode())
	ln = ser.read_until(b"\r\n").decode("utf-8")
	try:
		if (ln == None or len(ln) == 0):
			print("Empty country setting, exiting...")
			exit()
		try:
			j = json.loads(ln)
			recv_country = j.get("WIFI_COUNTRY")
			if recv_country != country:
				print("Error 1 setting country, exiting...")
				exit()
		except:
			print("Error 2 setting country, exiting...")
			exit()
	except:
		print("Error 3 setting country, exiting...")
		exit()	

	# set channel
	chan = 11
	try:
		chanInput = input("[?] Select a channel (default '%d'): " % chan)
		if chanInput != "":
			chan = int(chanInput)
	except KeyboardInterrupt:
		print("\n[+] Exiting...")
		exit()

	ser.write(("set chan %d\r\n" % (chan)).encode())
	ln = ser.read_until(b"\r\n").decode("utf-8")
	try:
		if (ln == None or len(ln) == 0):
			print("Empty channel setting, exiting...")
			exit()
		try:
			j = json.loads(ln)
			recv_chan = j.get("WIFI_CHANNEL")
			if recv_chan != chan:
				print("Error 1 setting channel, exiting...")
				exit()
		except:
			print("Error 2 setting channel, exiting...")
			exit()
	except:
		print("Error 3 setting channel, exiting...")
		exit()

	ser.write("wifi_sniff\r\n".encode())
	print("[+] Sniffer started...")

	try:
		while True:
			ln = ser.read_until(b"<STOP>")
			f.write(ln.replace(b"<STOP>", b""))
			f.flush()
	except KeyboardInterrupt:
		ser.write("stop\r\n".encode())
		print("[+] Stopping...")

	f.close()
	ser.close()
	print("[+] Done.")
