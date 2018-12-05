import requests


text = input("What do you want it to say?")
fileName = text + ".wav"

response = requests.post("https://avatar.lyrebird.ai/api/v0/generate",
                        headers = {"Content-Type": "application/json", "Authorization": "Bearer oauth_1DsNoa3A6HKyfkDcDayCIwRRxyT"},
                        json = {"text": text},
                         stream=True)
print(response)

with open(fileName, 'wb+') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            file.flush()
