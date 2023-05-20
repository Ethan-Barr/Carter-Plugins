### YOU ONLY NEED TO RUN THIS ONCE ###
import requests
import json

reqUrl = "https://api.carterlabs.ai/webhook/add"



payload = json.dumps({
    "key": "ADD YOUR API KEY FROM CONTRLLER",
    "url": "https://carter-plugins.vercel.app/webhook" # Change this to the name of your vercel domain (Keep the /webhook for it to work)
})

response = requests.request("POST",
                            reqUrl,
                            data=payload,
                            headers={"Content-Type": "application/json"})
print(response.text)