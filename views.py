from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import json
import os
import requests
from .permission import IsAdmin
import boto3
from datetime import datetime
from botocore.exceptions import ClientError
import logging
import os.path


class LogView(APIView):
    http_method_names = ['post']

    def post(self, request):
        # Logging Type: INFO, WARN, ERROR, DEBUG
        loggingType = request.data.get('type')
        message = request.data.get('message')
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        path = os.path.join("logs", "room-booking")
        file = os.path.join(path, "log-" + current_date + '.csv')

        try:
            f = open(file, "a+")
            f.write(message + "\n")
        except FileNotFoundError:
            f = open(file, "w+")
            f.write(message + "\n")
        finally:
            f.close()

        # Upload the file
        s3_client = boto3.client('s3')
        try:
            response = s3_client.upload_file(
                "log-" + current_date + '.csv', 'cubl-room-booking-log', "log-" + current_date + '.csv')
        except ClientError as e:
            logging.error(e)
            return False
        return True
