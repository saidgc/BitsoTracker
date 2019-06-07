#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import requests
import json
import numpy as np
import time
import csv
import datetime


# tamaño de la operación
OPERACION = 0.0001000

venta = None
opera = False
ganan = 0.0005396
vactual = 0
data = []
listo = False

def tracking():
  # variables globales
  global venta, opera, ganan, vactual, listo
  
  # se crea el demonio que ejecuta la función cada .9 seg
  threading.Timer(0.9, tracking).start()
  
  # se hace la petición get a Bitso
  response = requests.get('https://api.bitso.com/v3/ticker/?book=btc_mxn')
  
  # se valida que el status de la petición se correcta
  if response.status_code != 200:
    raise ApiError('GET /tasks/ {}'. format(response.status_code))
  
  # datos proporcionados por el api de Bitso
  value = float(response.json()["payload"]["last"])
  vwap = float(response.json()["payload"]["vwap"])
  deal = value * OPERACION
  percent = (value * 100) / vwap
  data.append(value)

  # tiempo de ejecución para calcular una media
  if len(data) > 300:
    listo = True
    # la media se ira recorriendo segun el tiempo (~5 mins)
    del data[0]

  # se calcula la media
  if value > np.average(data) and not opera and listo:
    # si la media es más pequña que el valor actual, vende
    ganan -= OPERACION
    venta = deal
    opera = True
    # se guarda el valor actual del bitcoin para saber si habra
    # ganancias
    vactual = np.average(data)

  # si el valor actual de bitcoin es menor al valor en que se vendio
  # se ejecuta la compra
  if value < vactual and opera:
    ganan += float(deal) / float(value)
    opera = False

  # se muestran los datos en tiempo real
  print(value, vactual, value * ganan, ganan)

  row = [datetime.datetime.now(), value, vactual, (value * ganan), ganan]
  with open('datos.csv', 'a') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(row)
  csvFile.close()


if __name__ == "__main__":
  thread = threading.Thread(target=tracking)
  thread.daemon = False
  thread.start()
