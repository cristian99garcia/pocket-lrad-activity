#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

orchlines = []
scorelines = []
instrlist = []

temp_path = os.path.expanduser("~/.temp_sound")


def _play(pitch, amplitude, duration, starttime, pitch_envelope,
          amplitude_envelope, instrument):
    if pitch_envelope == 'default':
        pitenv = 99
    else:
        pitenv = pitch_envelope

    if amplitude_envelope == 'default':
        ampenv = 100
    else:
        ampenv = amplitude_envelope

    if not 1 in instrlist:
        orchlines.append('instr 1\n')
        orchlines.append('kpitenv oscil 1, 1/p3, p6\n')
        orchlines.append('aenv oscil 1, 1/p3, p7\n')
        orchlines.append('asig oscil p5*aenv, p4*kpitenv, p8\n')
        orchlines.append('out asig\n')
        orchlines.append('endin\n\n')
        instrlist.append(1)

    scorelines.append('i1 %s %s %s %s %s %s %s\n' %
                      (str(starttime), str(duration), str(pitch),
                       str(amplitude), str(pitenv), str(ampenv),
                       str(instrument)))


def playSine(pitch=1000, amplitude=5000, duration=1, starttime=0,
             pitch_envelope='default', amplitude_envelope='default'):
    ''' Play a sine wave
    (pitch = [1000], amplitude = [5000], duration = [1], starttime = [0],
    pitch_envelope=['default'], amplitude_envelope=['default']) '''
    _play(pitch, amplitude, duration, starttime, pitch_envelope,
          amplitude_envelope, 1)


def audioOut(file=None):
    ''' Compile a .csd file and start csound to run it. If a string is
    given as argument, it write a wave file on disk instead of sending
    sound to hp. (file = [None]) '''
    if not os.path.isdir(temp_path):
        os.mkdir(temp_path)

    path = temp_path
    csd = open(os.path.join(path, 'temp.csd'), 'w')
    csd.write('<CsoundSynthesizer>\n\n')
    csd.write('<CsOptions>\n')

    if file is None:
        csd.write('-+rtaudio=alsa -odevaudio -m0 -d -b256 -B512\n')

    else:
        file = os.path.join(path, '%s.wav' % file)
        csd.write('-+rtaudio=alsa -o%s -m0 -W -d -b256 -B512\n' % file)

    csd.write('</CsOptions>\n\n')
    csd.write('<CsInstruments>\n\n')
    csd.write('sr=16000\n')
    csd.write('ksmps=50\n')
    csd.write('nchnls=1\n\n')

    for line in orchlines:
        csd.write(line)

    csd.write('\n</CsInstruments>\n\n')
    csd.write('<CsScore>\n\n')
    csd.write('f1 0 2048 10 1\n')
    csd.write('f2 0 2048 10 1 0 .33 0 .2 0 .143 0 .111\n')
    csd.write('f3 0 2048 10 1 .5 .33 .25 .2 .175 .143 .125 .111 .1\n')
    csd.write('f10 0 2048 10 1 0 0 .3 0 .2 0 0 .1\n')
    csd.write('f99 0 2048 7 1 2048 1\n')
    csd.write('f100 0 2048 7 0. 10 1. 1900 1. 132 0.\n')

    for line in scorelines:
        csd.write(line)

    csd.write('e\n')
    csd.write('\n</CsScore>\n')
    csd.write('\n</CsoundSynthesizer>')
    csd.close()

    os.system('csound ' + path + '/temp.csd >/dev/null 2>/dev/null')


while True:
    for i in range(1000):
        playSine(pitch=22000, amplitude=25000, duration = 0.1, starttime = i * 0.20)
        playSine(pitch=21000, amplitude=25000, duration = 0.1, starttime = i * 0.20 + 0.10)

    print "Pocket LRAD!"
    audioOut()

sys.exit(0)

