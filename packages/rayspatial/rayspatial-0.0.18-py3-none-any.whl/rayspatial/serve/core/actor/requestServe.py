import requests
import json
if __name__ == "__main__":
    english_text = {"ttt":"1111"}
    response = requests.post("http://127.0.0.1:8000/", ttt)
    french_text = response.text
    print(french_text)