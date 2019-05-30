#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import requests
import json

def tracking():
  threading.Timer(1.0, tracking).start()
  response = requests.get('https://api.bitso.com/v3/ticker/?book=btc_mxn')
  if response.status_code != 200:
    raise ApiError('GET /tasks/ {}'. format(response.status_code))
  value = response.json()["payload"]["last"]
  print(value)

tracking()
