#!/usr/bin/python
# -*- coding: utf-8 -*-
import pippy
while True:
  for i in range(1000):
    pippy.sound.playSine(pitch=22000, amplitude=25000, duration = 0.1, starttime = i*0.20)
    pippy.sound.playSine(pitch=21000, amplitude=25000, duration = 0.1, starttime = i*0.20+0.10)
  print "Pocket LRAD!"
  pippy.sound.audioOut()
exit(0)
