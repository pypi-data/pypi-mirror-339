# Clase Jugador y BotJugador

# cinquillo/jugador.py
from typing import Optional
from .carta import Carta

class Jugador:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.mano: list[Carta] = []

    def tiene_jugada_valida(self, mesa) -> bool:
        return any(mesa.puede_colocar(carta) for carta in self.mano)

    def jugar(self, mesa) -> Optional[Carta]:
        raise NotImplementedError
    