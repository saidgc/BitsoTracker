#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import requests
import json

import time

venta = None
opera = False
ganan = 0.0005396
vactual = 1

def tracking():
  global venta, opera, ganan, vactual
  threading.Timer(0.9, tracking).start()
  response = requests.get('https://api.bitso.com/v3/ticker/?book=btc_mxn')
  if response.status_code != 200:
    raise ApiError('GET /tasks/ {}'. format(response.status_code))
  value = float(response.json()["payload"]["last"])
  vwap = float(response.json()["payload"]["vwap"])
  deal = float(value) * 0.0001
  percent = (value * 100) / vwap
  if percent > 100 and not opera:
    ganan -= 0.0001
    venta = deal
    opera = True
    vactual = vwap
  if ((value * 100) / vactual) < 100 and opera:
    ganan += deal / value
    opera = False
  print(value, vwap, value > vwap, percent, ganan)
  

tracking()
