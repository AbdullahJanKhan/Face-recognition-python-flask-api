from flask.globals import request
import requests

Base = "http://127.0.0.1:5000/"

response = requests.post(Base + "/is_human")


print(response.json())
# response2 = requests.get(Base + "/exte")
# print(response2.json())
# print(responses.json())s