
# cinquillo/bot_jugador.py
from .jugador import Jugador
from .carta import Carta
from .mesa import Mesa

class BotJugador(Jugador):
    def jugar(self, mesa: Mesa) -> Carta | None:
        for carta in sorted(self.mano, key=lambda c: (c.palo, c.valor)):
            if mesa.puede_colocar(carta):
                self.mano.remove(carta)
                return carta
        return None