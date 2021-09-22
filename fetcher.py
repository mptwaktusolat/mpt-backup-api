import json
import time

import requests

reqUrl = "https://www.e-solat.gov.my/index.php"

jakim_code = [
    "JHR01", "JHR02", "JHR03", "JHR04", "KDH01", "KDH02", "KDH03", "KDH04",
    "KDH05", "KDH06", "KDH07", "KTN01", "KTN03", "MLK01", "NGS01", "NGS02",
    "PHG01", "PHG02", "PHG03", "PHG04", "PHG05", "PHG06", "PRK01", "PRK02",
    "PRK03", "PRK04", "PRK05", "PRK06", "PRK07", "PLS01", "PNG01", "SBH01",
    "SBH02", "SBH03", "SBH04", "SBH05", "SBH06", "SBH07", "SBH08", "SBH09",
    "SGR01", "SGR02", "SGR03", "SWK01", "SWK02", "SWK03", "SWK04", "SWK05",
    "SWK06", "SWK07", "SWK08", "SWK09", "TRG01", "TRG02", "TRG03", "TRG04",
    "WLY01", "WLY02"
]  # Total 58

failed_jakim_code = []

data = {}
data['solat'] = []

print(f'Total of {len(jakim_code)}')
print('\nStarting\n')

# Iterate each of the JAKIM code
for zone in jakim_code:

    params = {
        'r': 'esolatApi/takwimsolat',
        'period': 'month',
        'zone': zone,
    }

    try:
        response = requests.get(reqUrl, params=params)
        json_response = response.json()

        # Only put into json if everything's fine
        if (response.status_code == 200) and json_response['status'] == 'OK!':
            print(f"{zone} : {json_response['status']}")
            data['solat'].append(json_response)
        else:
            print(f'{zone} : Failed ({response.status_code})')
            failed_jakim_code.append(zone)
    except:
        # Catch
        print(f'{zone} : Failed due to exception')
        failed_jakim_code.append(zone)

    time.sleep(1)  # Pause 1 sec before the next api call

retryCount = 0

# Retry the failed request until all filled up
while len(failed_jakim_code) != 0:
    failed = '", "'.join(x for x in failed_jakim_code)
    print(f'\nFailed to fetch: "{failed}"')

    retryCount += 1
    print(f'\nRetrying failed requests. Attempt #{retryCount}\n')

    # Iterate each of the JAKIM code
    for zone in failed_jakim_code:

        params = {
            'r': 'esolatApi/takwimsolat',
            'period': 'month',
            'zone': zone,
        }

        try:
            response = requests.get(reqUrl, params=params)
            json_response = response.json()

            # Only put into json if everything's fine
            if (response.status_code
                    == 200) and json_response['status'] == 'OK!':
                print(f"{zone} : {json_response['status']}")
                data['solat'].append(json_response)
                failed_jakim_code.remove(zone)
            else:
                print(f'{zone} : Failed ({response.status_code})')
        except:
            # Catch
            print(f'{zone} : Failed due to exception')

        time.sleep(1)  # Pause 1 sec before the next api call

with open('db.json', 'w') as outfile:
    json.dump(data, outfile)
    print('\nFinish writing to db.json')

print(f'Operation finish at {time.strftime("%a, %d %b %Y %H:%M:%S")}')