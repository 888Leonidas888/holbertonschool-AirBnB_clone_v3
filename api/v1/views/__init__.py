#!/usr/bin/python3
"""Creamos nuestros Blueprint!!!"""

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
"""Esta línea siguiente evitara de errores de importación circulante"""
from api.v1.views.index import *
from api.v1.views.states import *
