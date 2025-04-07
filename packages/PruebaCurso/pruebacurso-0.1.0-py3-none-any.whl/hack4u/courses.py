#!/usr/bin/env python3

class Course:

    def __init__(self, name, length, link):

        self.name = name
        self.length = length
        self.link = link
        
    def __repr__(self):
        
        return f"El curso: {self.name}, tiene una duración de {self.length}h. El link referente a este curso es --> {self.link}"

   
courses = [
    Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalización de entorno en Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    Course("Python Ofensivo", 35, "https://hack4u.io/cursos/python-ofensivo/"),
    Course("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")
]

def list_courses():
    for i in courses:
        print(i)

def search_course(cname):
    _temp_finding_value = 0
    _temp_error_value = 0
    for course in courses:
        if course.name == cname:
            _temp_finding_value += 1
            return course
        else: 
            
            _temp_error_value += 1
    
    if _temp_error_value == len(courses):
        print(f"No existen cursos disponibles con el título: {cname}")
