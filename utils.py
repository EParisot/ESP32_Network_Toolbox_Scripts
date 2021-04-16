import time
import serial
import serial.tools.list_ports
import json

BAUD_RATE = 115200

def connect_serial(timeout=None):
	try:
		ports_list = list(serial.tools.list_ports.comports())
		if len(ports_list) == 0:
			print("No COM port detected, exiting...")
			exit()
		for l in ports_list:
			print(l)
		first_port = str(ports_list[0]).split(" - ")[0]
		serialportInput = input("[?] Select a serial port (default '%s'): " % first_port)
		if serialportInput == "":
			serialport = first_port
		else:
			serialport = serialportInput
		canBreak = False
		while not canBreak:
			boardRateInput = input(
				"[?] Select a baudrate (default %d): " % BAUD_RATE)
			if boardRateInput == "":
				boardRate = BAUD_RATE
				canBreak = True
			else:
				try:
					boardRate = int(boardRateInput)
				except KeyboardInterrupt:
					print("\n[+] Exiting...")
					exit()
				except Exception:
					print("[!] Please enter a number!")
					continue
				canBreak = True
		filenameInput = input(
			"[?] Select a filename (default 'capture.pcap'): ")
		if filenameInput == "":
			filename = "capture.pcap"
		else:
			filename = filenameInput
	except KeyboardInterrupt:
		print("\n[+] Exiting...")
		exit()

	canBreak = False
	while not canBreak:
		try:
			ser = serial.Serial(serialport, boardRate, timeout=timeout)
			if (not ser.isOpen()):
				print("[!] Serial connection failed... Retrying...")
				time.sleep(2)
				continue
			ser.write("test\r\n".encode())
			res = ser.read_until(b"\r\n").decode("utf-8")
			if res != None and len(res):
				json_res = json.loads(res)
				if json_res != None and json_res.get("TEST") == "OK":
					canBreak = True
			else:
				print("[!] Serial connection failed... Retrying...")
				ser.close()
				time.sleep(2)
				continue
		except KeyboardInterrupt:
		    print("\n[+] Exiting...")
		    exit()
		except Exception as e:
		    print("[!] Serial connection failed with error: %s" % str(e))
		    time.sleep(2)
		    continue

	print("[+] Serial connected. Name: %s, rate: %s" % (ser.name, str(boardRate)))
	return ser, filename
