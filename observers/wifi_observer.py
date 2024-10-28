import pywifi
from pywifi import const
import time


def get_network_name():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    for profile in iface.network_profiles():
        if iface.status() == const.IFACE_CONNECTED:
            return (f"Connected to SSID: {profile.ssid}")


def check_wifi_status():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Assumes you have at least one Wi-Fi interface

    iface.scan()  # Trigger a scan
    iface_status = iface.status()  # Get the current status

    if iface_status == const.IFACE_CONNECTED:
        return "ON"
    else:
        return "OFF"

previos_wifi_status = None

def create_message(status):
    if status == "ON":
        network = get_network_name()
        return f"connted to {network}"
    else:
        return "Wi-Fi is off or disconnected."

def observe_wifi(callback):
    print("Wifi Observr Start")
    global previos_wifi_status
    while True:
        wifi_status = check_wifi_status()
        
        if previos_wifi_status == None:
            previos_wifi_status = wifi_status
            message = create_message(wifi_status)
            callback(message)
        
        if previos_wifi_status != wifi_status:
            previos_wifi_status = wifi_status
            message = create_message(wifi_status)
            callback(message)
            
        time.sleep(5)

def callback(message):
    print(message,"from callback")

if __name__ == "__main__":
    observe_wifi(callback)
