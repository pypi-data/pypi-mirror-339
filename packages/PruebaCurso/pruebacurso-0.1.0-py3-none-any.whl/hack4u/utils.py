#!/usr/bin/env python3

from .courses import *

def total_hours():
    _total_hours = 0
    for course in courses: 
        _total_hours += course.length
    
    if _total_hours != 0:
        print(f" Las horas totales de cursos de las que dispone Hack4u son de {_total_hours}h")
