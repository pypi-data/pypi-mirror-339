# Hack4U Academy Courses Library

Una biblioteca Python para consultar cursios de la academia Hack4U.

## Cursos disponibles:

- Introducion a Linux [15 horas]
- Personalizacion de Linux [3 horas]
- Introducion al Hacking [53 horas]
- Python Ofensivo [35 horas]

## Instalacio

Installa el paquete usando 'pip3':

```python3
pip3 install hack4u
```
## Uso basico

### Listar todos los Cursos

```python3
from hack4u import list_courses

for course in list_courses():
    print(course)
```

### Obtener un curso por nombre

```python3
from hack4u import get_course_by_name

course = get_course_by_name("Introducion a Linux")
print(course)
```

### Calcular duracion total de los Cursos

```python3
from hack4u.utils import total_duration

print(f"Duracion total: {total_duration()} horas")
```
