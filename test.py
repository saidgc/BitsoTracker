#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading

def printit():
  threading.Timer(5.0, printit).start()
  print("Hello, World!")

printit()
