import requests
import mingus.core.notes as notes


def get_aircraft():
    request = requests.get('http://192.168.1.139/dump1090-fa/data/aircraft.json')
    json = request.json()
    targets = json['aircraft']
    aircraft = []

    for target in targets:
        if target.get('alt_baro'):
            if target.get('flight'):
                if target.get('lat'):
                    if target.get('lon'):
                        if target.get('mag_heading'):
                            aircraft.append(target)

    return aircraft

