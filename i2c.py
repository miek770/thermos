#!/usr/bin/python
#-*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO

# Pin definitions
SDA = 3 # Serial Data
SCL = 5 # Serial Clock

# Signal definitions
OUT = GPIO.OUT
IN = GPIO.IN
HIGH = GPIO.HIGH
LOW = GPIO.LOW

# Tick definition
TICK = 0.01

class bus():
    def __init__(self, tick=TICK):
        # Signals setup
        self.sda_dir = None
        self.scl_dir = None
        self.sda_state = None
        self.scl_state = None
        
        self.set_dir(SDA, OUT)
        self.set_dir(SCL, OUT)
        self.set_state(SDA, HIGH)
        self.set_state(SCL, HIGH)

        # Tick definition
        self.tick = tick
        
    def start(self):
        if self.sda_dir == OUT and self.scl_dir == OUT:
            if self.sda_state == HIGH and self.scl_state == HIGH:
                self.set_state(SDA, LOW)
                return None
        print("Error: Invalid initial conditions for START signal.")
        return None

    def stop(self):
        if self.sda_dir == OUT and self.scl_dir == OUT:
            if self.sda_state == LOW and self.scl_state == HIGH:
                self.set_state(SDA, HIGH)
                return None
        print("Error: Invalid initial conditions for STOP signal.")
        return None

    def get_state(self, signal):
        if signal == SDA:
            return self.sda_state
        elif signal == SCL:
            return self.scl_state
        else:
            print("Error: Invalid signal.")
            return None
    
    def set_state(self, signal, state):
        if signal not in (SDA, SCL):
            print("Error: Invalid signal.")
            return None
        elif state not in (HIGH, LOW):
            print("Error: Invalid state.")
            return None
        elif self.get_dir(signal) == OUT:
            if self.get_state(signal) != state:
                GPIO.output(signal, state)
                if signal == SDA:
                    self.sda_state = state
                else:
                    self.scl_state = state
        else:
            print("Error: Pin", signal, "set as input.")
        
    def get_dir(self, signal):
        if signal == SDA:
            return self.sda_dir
        elif signal == SCL:
            return self.scl_dir
        else:
            print("Error: Invalid signal.")
            return None
        
    def set_dir(self, signal, direction):
        if signal not in (SDA, SCL):
            print("Error: Invalid signal.")
            return None
        elif direction not in (OUT, IN):
            print("Error: Invalid direction.")
            return None
        elif self.get_dir(signal) != direction:
            GPIO.setup(signal, direction)
            if signal == SDA:
                self.sda_dir = direction
                if direction == IN:
                    self.sda_state = None
            else:
                self.scl_dir = direction
                if direction == IN:
                    self.sda_state = None
