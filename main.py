import time
import serial
import keyboard
from serial.tools import list_ports
import winsound


# fungsi untuk mencari port yang aktif
def find_port():
    ports = list_ports.comports()
    for port in ports:
        if "COM7" in port.device:
            return port.device
    return None


# buka koneksi serial dengan timbangan
while True:
    port = find_port()
    if port is None:
        print("Tidak ada koneksi ke timbangan")
        time.sleep(1)
        continue
    try:
        ser = serial.Serial(port, 1200)
        print("Terhubung ke", port)
        break
    except serial.SerialException:
        print("Gagal terhubung ke", port)
        time.sleep(1)


def reverse_string(string):
    """
    Function to reverse the received string and move the negative sign to the front.
    """
    if '-' in string:
        return '-' + string[:-1][::-1]
    else:
        return string[::-1]


# main loop
last_weight = None
last_time = None

# baca data dari timbangan
while True:
    data = ser.read_until(b'=')
    # konversi data dari byte menjadi string
    data_string = data.decode(
        'utf-8', errors='ignore').strip().replace('=', '')
    # konversi nilai ke float dan ubah format desimal
    try:
        weight = float(reverse_string(data_string))
        weight = format(weight, ".3f")
        print("{} = {}".format(data_string, weight))
    except ValueError:
        continue
		
    if keyboard.is_pressed("ctrl"):
        print("You pressed ctrl")
        print("Nilai terkirim :", weight)
        winsound.Beep(2500, 1000)  # membuat beep
        keyboard.write(weight + "\n")
        continue


# tutup koneksi serial
ser.close()
