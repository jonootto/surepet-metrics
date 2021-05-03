import asyncio
from prometheus_client import Gauge, start_http_server

from os import environ
from typing import Dict, List
from datetime import datetime, timedelta
from time import sleep
#from requests import packages

from surepy import Surepy
#from surepy.entities import SurepyEntity
from surepy.entities.devices import SurepyDevice
#from surepy.entities.pet import Pet


async def main():
    surepy = Surepy(auth_token=token)
    devices: List[SurepyDevice] = await surepy.get_devices()
    return devices


def timetowait(minutes):
    delta = timedelta(minutes=minutes)
    now = datetime.now()
    next_minute = (now + delta).replace(microsecond=0,second=0)
    wait_seconds = (next_minute - now)
    wait_seconds = int((wait_seconds).total_seconds())
    print("    " + str(wait_seconds)+"s until next")
    return(wait_seconds)

def wait(sleeptime,sleepstage):
    slept = 0
    for x in range(0,sleeptime,sleepstage):
        sleep(sleepstage)
        slept += sleepstage
        remaining = sleeptime - slept
        print(str(remaining) + "s until next")

        



token = environ.get("SUREPY_TOKEN")

start_http_server(6789)
g = Gauge('surepy_battery_percent','Battery Level',['device'])
while True:
    devices = asyncio.run(main())
    for device in devices:

        g.labels(device=device.name).set(device.battery_level)
        print(device.name + " " + str(device.battery_level) + "%")


    wait(timetowait(10),30)
