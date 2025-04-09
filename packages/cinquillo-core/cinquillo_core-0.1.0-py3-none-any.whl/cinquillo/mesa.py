# Clase Mesa

# cinquillo/mesa.py
from .carta import Carta

class Mesa:
    def __init__(self):
        self.estado = {palo: [] for palo in ['oros', 'copas', 'espadas', 'bastos']}

    def puede_colocar(self, carta: Carta) -> bool:
        cartas_palo = self.estado[carta.palo]

        if carta.valor == 5:
            return True

        if not cartas_palo:
            return False

        # Baraja española de 40 cartas (sin 8 ni 9)
        valores_validos = list(range(1, 8)) + list(range(10, 13))

        if carta.valor not in valores_validos:
            return False

        index = valores_validos.index(carta.valor)
        vecinos = []
        if index > 0:
            vecinos.append(valores_validos[index - 1])
        if index < len(valores_validos) - 1:
            vecinos.append(valores_validos[index + 1])

        return any(v in cartas_palo for v in vecinos)

    def colocar_carta(self, carta: Carta):
        self.estado[carta.palo].append(carta.valor)
        self.estado[carta.palo].sort()
