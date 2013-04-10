#!/usr/bin/python3
#-*- coding: utf-8 -*-

# Copyright 2012-2013 Michel Lavoie
# miek770(at)gmail.com

# This file is part of Thermos.

# Thermos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Thermos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Thermos.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
import os
import configparser
from time import sleep

# Variables globales
jours = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

def get_zero():
    zero = datetime.now()
    return datetime(zero.year,
                    zero.month,
                    zero.day - zero.weekday(),
                    0,
                    0)

def get_profils():
    # Importation des fichiers des configuration
    profils = dict()
    for file in os.listdir('profils'):
        if file[-5:] == '.conf':
            config = configparser.ConfigParser()
            config.read('profils/' + file)
            profils[file[:-5]] = config
            del(config)

    # Impression des fichiers importés
#    key_list = list(profils.keys())
#    key_list.sort()
#    
#    for key in key_list:
#        print(key)
#        for section in profils[key].sections():
#            print('    ' + section)
#            print('         temp = ' + profils[key][section]['temp'])
#            print('         vent = ' + profils[key][section]['vent'])
    return profils

def get_horaire(profil):
    horaire = []
    zero = get_zero()

    for plage in profils[profil].sections():
        if not '-' in plage:
            premier_jour = jours.index(plage.split('.')[0])
            dernier_jour = jours.index(plage.split('.')[0])
        else:
            premier_jour = jours.index(plage.split('-')[0])
            dernier_jour = jours.index(plage.split('-')[1].split('.')[0])
        for jour in range(premier_jour, dernier_jour+1):
            debut = datetime(zero.year,
                             zero.month,
                             zero.day + jour,
                             int(plage.split('.')[1].split(':')[0]),
                             int(plage.split(':')[1]))
            delta = debut - zero
            delta = int(delta.total_seconds())
            horaire.append((delta,
                            float(profils[profil][plage]['temp']),
                            profils[profil][plage]['vent']))

    horaire.sort(reverse=True)
#    print('(delta, \'temp\', \'vent\')')
#    print(horaire)
    return horaire

def get_current():
    # Détection d'où on se trouve dans l'horaire actuel
    zero = get_zero()
    verif = datetime.now()
#    verif = datetime(2012, 10, 20, 9, 59)
    delta = verif-zero
    delta = int(delta.total_seconds()) % 604800

    for plage in horaire:
        if delta > plage[0]:
            return plage
            break
    else:
        return horaire[0]

if __name__ == '__main__':
    profils = get_profils()
    for profil in profils:
        horaire = get_horaire(profil)
        print(profil, get_current())

        # Détection d'où on change de réglage pour toute la semaine
        for delta in range(0, 604800):
            for plage in horaire:
                if (delta >= plage[0]) and (delta-1 < plage[0]):
                    print(delta, plage)
                    break
