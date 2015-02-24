#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'Raúl Jornet Calomarde'
__contact__ = 'rjornetc@openmailbox.org'
__copyright__ = 'Copyright © 2015, Raúl Jornet Calomarde'
__license__ = '''License GPLv3+: GNU GPL version 3 or any later
This program isfree software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or any later
version. This program is distributed  in the hope that it will be
useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License for more details.
<http://www.gnu.org/licenses/>'''
__date__ = '06/02/2015'
__version__ = '1.3.1'

import sys, getopt
import svgwrite

COUNT = 0


def get_square(x,y,size):
    path = ' M %i,%i %i,%i %i,%i %i,%i z' % (x + size, y + size,
                                             x + size, y,
                                             x,        y,
                                             x,        y + size)
    return(path)


def draw_sponge(path, iterations, x, y, size):
    if progress:
        global count_progress
        print(str(100.*count_progress/total_progress)+'%')
        count_progress += 1
    unit_size = size/3.
    if iterations == 0:
        return(path)
    else:
        for xi in (0, 1, 2):
            for yi in (0, 1, 2):
                if xi == 1 and yi == 1:
                    path += get_square(x+xi*unit_size,y+yi*unit_size,unit_size)
                else:
                    path += draw_sponge('', iterations - 1, x+xi*unit_size, y+yi*unit_size, unit_size)
        return(path)


def get_recursive_calls_count(i):
    if i == 0:
        return(1)
    else:
        return(8 ** i + get_recursive_calls_count(i-1))



if __name__ == '__main__':

    iterations = 1
    progress = False
    svg = svgwrite.Drawing(filename = 'a',
                           size=('6561', '6561'),
                           profile='tiny')
    path = 'M 0,0 6561,0 6561,6561 0,6561 z'

    try:
        opts, args = getopt.getopt(sys.argv[1:],'hvi:p',['help',
                                                        'version',
                                                        'iterations=',
                                                        'progress'])
    except getopt.GetoptError:
        print('menger.py [-h] [-v]' +\
              'menget.py [-p] [-i <iterations>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('menger.py [-h] [-v]' +\
              'menget.py [-p] [-i <iterations>]')
            sys.exit()
        elif opt in ('-v', '--version'):
            print ('py-menger ' + __version__ + '\n' +\
                   __copyright__ + '\n' +\
                   __license__)
            sys.exit()
        elif opt in ('-i', '--iterations'):
            iterations = int(arg)
        elif opt in ('-p', '--progress'):
            progress = True
            count_progress = 0
            total_progress = get_recursive_calls_count(iterations)
    
    path += draw_sponge('', iterations, 0, 0, 6561)
    svg.add(svg.path(d=path))
    svg.save()
