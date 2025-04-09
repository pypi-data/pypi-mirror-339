# Clase MotorJuego

# cinquillo/motor.py
from .partida import Partida
from .jugador import Jugador

class MotorJuego:
    def __init__(self):
        self.partida: Partida | None = None

    def nueva_partida(self, jugadores: list[Jugador]):
        self.partida = Partida(jugadores)
        self.partida.iniciar()

    def jugar_turno(self):
        if self.partida.finalizada:
            return
        jugador = self.partida.jugadores[self.partida.turno_actual]
        if jugador.tiene_jugada_valida(self.partida.mesa):
            carta = jugador.jugar(self.partida.mesa)
            if carta:
                self.partida.mesa.colocar_carta(carta)
                self.partida.historial.append((jugador.nombre, carta))
                if len(jugador.mano) == 0:
                    self.partida.finalizada = True
                    return
        self.partida.siguiente_turno()