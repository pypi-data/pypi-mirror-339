# Clase Reglas

# cinquillo/reglas.py
from .carta import Carta
from .mesa import Mesa

class Reglas:
    @staticmethod
    def es_jugada_valida(carta: Carta, mesa: Mesa) -> bool:
        return mesa.puede_colocar(carta)