#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import requests
import json
import numpy as np
import time

# OPERACION = 0.0001000
OPERACION = 1000

venta = None
opera = False
ganan = 1000.0000001
# ganan = 0.0005396
vactual = 0
data = []
listo = False

def tracking():
  global venta, opera, ganan, vactual, listo
  
  threading.Timer(0.9, tracking).start()
  
  response = requests.get('https://api.bitso.com/v3/ticker/?book=btc_mxn')
  
  if response.status_code != 200:
    raise ApiError('GET /tasks/ {}'. format(response.status_code))

  value = float(response.json()["payload"]["last"])
  vwap = float(response.json()["payload"]["vwap"])
  deal = value * OPERACION
  percent = (value * 100) / vwap
  data.append(value)

  if len(data) > 30:
    listo = True
    del data[0]

  if value > np.average(data) and not opera and listo:
    ganan -= OPERACION
    venta = deal
    opera = True
    vactual = np.average(data)

  if value < vactual and opera:
    ganan += float(deal) / float(value)
    opera = False

  print(value, vactual, value * ganan, ganan)


if __name__ == "__main__":
  thread = threading.Thread(target=tracking)
  thread.daemon = False
  thread.start()
