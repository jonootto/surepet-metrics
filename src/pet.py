import asyncio
import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from os import environ
from typing import Dict, List
from datetime import datetime, timedelta
from time import sleep
from requests import packages

from surepy import Surepy
from surepy.entities import SurepyEntity
from surepy.entities.devices import SurepyDevice
from surepy.entities.pet import Pet


async def main():
    surepy = Surepy(auth_token=token)
    devices: List[SurepyDevice] = await surepy.get_devices()
    return devices


def timetowait():
    delta = timedelta(minutes=10)
    now = datetime.now()
    next_minute = (now + delta).replace(microsecond=0,second=0)
    wait_seconds = (next_minute - now)
    wait_seconds = int((wait_seconds).total_seconds())
    print("    " + str(wait_seconds)+"s until next")
    return(wait_seconds)


packages.urllib3.disable_warnings()
influxtoken = environ.get("INFLUX_TOKEN")
org = environ.get("ORG")
bucket = environ.get("BUCKET")
client = InfluxDBClient(url="https://192.168.1.254:8086", token=influxtoken, org=org, verify_ssl=False)
write_api = client.write_api(write_options=SYNCHRONOUS)
token = environ.get("SUREPY_TOKEN")

while True:
    devices = asyncio.run(main())

    for device in devices:
        print(device.name + " " + str(device.battery_level) + "%")
        p = Point("DeviceBattery").tag("Device Name",device.name).field("Battery",device.battery_level)
        write_api.write(bucket=bucket,org=org,record=p)

    sleeptime = timetowait()
    print(sleeptime)
    sleep(sleeptime)