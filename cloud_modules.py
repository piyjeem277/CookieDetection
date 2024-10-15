'''
***********************************************************************

NOTES FOR STUDEENTS
-------------------
Change this file appropriately
    1. update the endpoint URL
    2. update the API Key or update your environment variable
    3. (If required) change the logic

***********************************************************************
'''

import time
import json
import requests
import os

class CloudAnalyzer:
    def __init__(self):
        self.endPoint = 'https://2021csc048-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/24f98578-ebd0-42e6-beac-c96dd96e352c/detect/iterations/Iteration1/image'
        self.apiKey = 'd33c092f6a4044b6a5693c2e58acfc2e'

    def analyzeImage(self, filePath) -> int:
        start_time = time.time()
        url = self.endPoint
        headers = {
            'Prediction-Key': self.apiKey,
            'Content-Type': 'application/octet-stream'
        }
        with open(filePath, 'rb') as file:
            response = requests.post(url, headers=headers, data=file)

        rowNo = filePath[-6:-4]
        if response.status_code == 200:
            data = json.loads(response.text)

            #find any Bad cookie with prediction rate more than 0.8
            filtered_predictions = [
                prediction for prediction in data["predictions"]
                if prediction["probability"] > 0.8 and prediction["tagName"] == "Bad"
            ]
            badCount = len(filtered_predictions)
            print(f"ROW: {rowNo}   |   BAD: {badCount}  |  TIME: {(time.time() - start_time):.2f}s")

            time.sleep(0.6)
            return badCount
        else:
            print(f"* ROW: {rowNo}   |  FAILED: {response.status_code}  |  TIME: {(time.time() - start_time):.2f}s")
            return 0