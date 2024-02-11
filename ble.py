import asyncio
from bleak import BleakScanner
import subprocess
import datetime
import os  # ファイルの存在確認


async def main():
    for i in range(100):
        print(i, "start")
        ble_file, wifi_file = save_file_init()
        ble_devices = await get_ble_devices()
        for d in ble_devices:
            # print(d.rssi, d.address)
            save_ble_data(ble_devices, ble_file)
        print(i, "end")
        await asyncio.sleep(1)


async def get_ble_devices():
    devices = await BleakScanner.discover()
    return devices


def get_wifi_devices():
    output = subprocess.check_output(
        [
            "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport",
            "-s",
        ]
    )
    return output.decode("utf-8")


def time_init():
    dt_now = datetime.datetime.now()
    mouth = dt_now.month
    day = dt_now.day
    time = dt_now.strftime("%H:%M:%S")
    time = time.replace(":", "-")
    return (mouth, day, time)


def save_file_init():
    # ファイルの存在確認
    files = ["data", "data/ble", "data/wifi"]
    for f in files:
        if not os.path.exists(f):
            os.makedirs(f)
    # ble  name: mouth_date_time.csv
    # wifi name: mouth_date_time.csv
    mouth, day, time = time_init()
    ble_file = f"data/ble/{mouth}-{day}-{time}.csv"
    wifi_file = f"data/wifi/{mouth}-{day}-{time}.csv"
    with open(ble_file, "w") as f:
        f.write("rssi,address\n")
    return (ble_file, wifi_file)


def save_ble_data(ble_devices, ble_file):
    # csv として保存
    # rssi address
    # -47 18C80CB8-7DDF-9A59-4FC7-2EA46D29086C
    with open(ble_file, "a") as f:
        for d in ble_devices:
            f.write(f"{d.rssi},{d.address}\n")


def save_wifi_data(wifi_devices, wifi_file):
    wifi_devices = wifi_devices.split("\n")

    for count, device in enumerate(wifi_devices, start=1):
        if count == 1:  # Skip the first line
            continue

        # Split the device string into parts
        parts = device.split()

        # Get the SSID and RSSI
        if len(parts) < 2:
            continue
        ssid = parts[0]
        rssi = parts[1]

        err = False
        count = 1
        # rssi が-から始まらない場合
        while rssi[0] != "-":
            count += 1
            ssid += " " + rssi
            rssi = parts[count]
            if rssi[0] == "-":
                break
            if count > 5:
                err = True
                break

        if err:
            continue

        # Save the SSID and RSSI to a file
        with open(wifi_file, "a") as f:
            f.write(f"{ssid},{rssi}\n")


asyncio.run(main())
