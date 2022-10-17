import requests


def test():
    import json
    URL = ""
    headers = {
        'requserid': '',
        'loginsession': ''
    }
    # redcode = json.loads(request.form["redcode"])
    redcode_json_path = "redcode.json"
    # with open(redcode_json_path, 'w', encoding="utf-8") as fr:
    #     fr.write(json.dumps(redcode))
    url = URL + ""
    files = {'file': open(redcode_json_path, 'rb')}
    req = requests.post(url, files=files, headers=headers, verify=False)
    return req.text
