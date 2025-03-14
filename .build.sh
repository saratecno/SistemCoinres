#!/usr/bin/env bash

# Actualizar pip
pip install --upgrade pip  

# Instalar dependencias
pip install -r requirements.txt  

# Ejecutar migraciones
python manage.py migrate  

# Recolectar archivos estáticos
python manage.py collectstatic --noinput