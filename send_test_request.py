import requests


def add_rule():
    url = 'http://46.101.147.231/save_rule'
    data = {
        "type": "auto",
        "priority": 5,
        "creator": 1,
        "param": "rma",
        # "param_value": "33333333",
        "emulate_algoritm": {
            "xn1": {"count_stop_previ": 10, "count_stop_self": 10, "weight": 4.50},
            "xn2": {"count_stop_previ": 14, "count_stop_self": 20, "weight": 18.90},
            "xn3": {"count_stop_previ": 15, "count_stop_self": 15, "weight": 37.00},
            "xn6": {"count_stop_previ": 30, "count_stop_self": 25, "weight": 15.00},
            "xn8": {"count_stop_previ": 11, "count_stop_self": 15, "weight": 23.00},
            "xn9": {"count_stop_previ": 12, "count_stop_self": 10, "weight": 48.20}
        }
    }
    headers = {'Content-type': 'application/json'}

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        print(response.content)
    else:
        print(f'Request failed with status code {response.status_code} ({response.content})')

add_rule()