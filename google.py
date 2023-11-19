import json
import requests

headers = {"Authorization": "Bearer ya29.a0AfB_byAExX9E60woYZbuBBpnZXUlkFpVoJN02vUzUNTFQW0Je5fm6oVPGcXKJJ25BKytpkIzdaaYROx4YFuAIuk_PYOcTMyXGmwH-Om7ojYLzcfiX_2ZIoWeTs1JLKF8xu0FFwjxhbk3IRTo8_B6kfbDSm3tuStRRhBAaCgYKAawSARMSFQHGX2Mi9iiKQeca1UzjF8RHJuohCw0171"}


para = {
    "name": "clave1",
}
files = {
    "data": ("metadata", json.dumps(para), "application/json; charset=UTF-8"),
    "file": open("P1.txt", "rb"),
}
r = requests.post(
    "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    headers=headers,
    files=files,
)
print(r.text)

