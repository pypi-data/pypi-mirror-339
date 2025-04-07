# Hack4U Academy Courses Library

Biblioteca para consultar los cursos de Hack4u.

## Cursos dispoinles:

- Introducción a Linux [15 horas]
- Personalización de Linux [3 horas]
- Python Ofensivo [35 horas]
- Introducción al Hacking [53 horas]

## Instalación

Instala el paquete usando `pip3`:

```python3
pip3 install PruebaCurso

## Uso básico

## Listar todos los cursos

```python
from hack4u import list_courses

for course in list_courses():
    print(course)
```
### Obtener un curso por nombre 

```python
from hack4u import search_course

course = search_course("Introducción a Linux")
print(course)
```
### Calcular duración total

```python3
from hack4u.utils import total_hours

print(f" Las horas totales de cursos de las que dispone Hack4u son de {_total_hours}h")
