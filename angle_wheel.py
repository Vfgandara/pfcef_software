"""
Esse arquivo realiza a definição da classe AngleWheel.
Ela é responsável por armazenar valores de ângulo dentro do algoritmo e
utilizá-los como critério de decisão para o cálculo dos próximos valores
de coordenada.
"""


import matplotlib.pyplot as plt
from time import sleep
from typing import Tuple
from looped_list import LoopedList

class AngleWheel():
    """
    Essa classe realiza todas funções relacionados ao registro e uso de valores
    de ângulo dentro do algoritmo. Ela mantém em si memória de qual foi a última
    direção em que uma parede foi traçada por meio de uma instância da classe
    LoopedList. Esses valores de direção são utilizados para determinar qual
    função será usada para o cálculo da próxima coordenada. Ainda mais, são
    rotinas dessa classe a normalização do ângulo e decisão entre +90, -90 ou
    inválido como valores finais de ângulo.
    """

    def __init__(self):
        """
        Inicializa todos atributos necessários ao processo de cálculos de ângulo
        """
        self.clear = True # Determina se a classe ainda não foi utilizada
        self.last_angle = 0 # Último valor de ângulo medido
        self.directions_wheel = LoopedList(["y+","x-","y-","x+"]) # Lista circular de direções
        self.current_direction = 0 # Índice da última direção atual
        self.direction_to_operation = {
            "x+": self.x_plus,
            "x-": self.x_minus,
            "y+": self.y_plus,
            "y-": self.y_minus
        } # Dicionário que mapeia entre direções e suas operações no plano cartesiano

    def __call__(self, angle_value: float) -> float:
        """
        Esse método define o comportamento quando uma instância da classe é
        chamada como um função, ex:

        >>> angle_wheel = AngleWheel()
        >>> angle_wheel()

        Basicamente repassa a chamada para o método ._get_orientation
        """
        angle = self._get_orientation(angle_value) #
        return angle #returns a 90 or -90 value

    def _normalize_angle(self,x: float) -> float:
        """
        Esse método é utilizado para mapear valores de ângulo maiores que 360
        ou menores que -360 para seus equivalentes dentro desse intervalo.
        """
        if x >= 0:
            turns = x//360
            return x - (turns)*360
        turns = x//-360
        return x + (turns)*360

    def _get_orientation(self, x: float) -> int:
        """
        Esse método realiza o processamento de um valor de ângulo para escolher
        entre +90, -90 ou inválido como valores de ângulo final
        """
        if self.clear:
            # Na primeira iteração o ângulo inicial sempre é considerado como 0
            self.clear = False
            self.last_angle = x
            return 0

        # A normalização é aplicada diretamente na diferença entre ângulos
        diff = self._normalize_angle(x - self.last_angle)

        self.last_angle = x # atualização do último valor de ângulo medido

        # Lógica de escolha de ângulo final
        abs_diff = abs(diff)
        if abs_diff >= 315 or abs_diff <= 45:
            return -1
        elif abs_diff >= 135 and abs_diff <= 225:
            return -1
        elif diff > 45 and diff < 135:
            return 90
        elif diff <= -45 and diff > -135:
            return -90
        elif abs_diff > 225 and abs(diff) < 315:
            if diff < 0:
                return 90
            return -90

    """
    Abaixo seguem todos os métodos de cálculo de coordenada com base na direção
    O nome do método é indicativo de sua função
    Todas elas aceitam a última coordenada e a distância medida pelo sensor como
    seus argumentos para o cálculo
    """
    def x_plus(self, previous_coord: Tuple[float, float], dist: float):
        return previous_coord[0] + dist, previous_coord[1]
    def x_minus(self, previous_coord, dist):
        return previous_coord[0] - dist, previous_coord[1]
    def y_plus(self, previous_coord, dist):
        return previous_coord[0], previous_coord[1] + dist
    def y_minus(self, previous_coord, dist):
        return previous_coord[0], previous_coord[1] - dist


    def _get_angle(self, angle: float) -> str:
        """
        Esse método atualiza dinamicamente o valor de direção para o desenho da
        próxima parede e retorna um identificador dessa direção, que é uma
        string com a direção (x ou y) e o sentido (+ ou -).
        Para isso ele utiliza da lista circular armazenada em self.directions_wheel
        e atualiza o seu indexador (self.current_direction)
        """
        if angle == 0:
            pass
        elif angle == 90:
            self.current_direction += 1
        else:
            self.current_direction -= 1
        return self.directions_wheel[self.current_direction]

    def data_to_coord(self, point: Tuple[float, float], previous_coord: Tuple[float, float]):
        """
        Esse método utiliza os valores finais dos sensores como entrada para o
        cálculo da nova coordenada
        """
        dist, angle = point
        direction = self._get_angle(angle)
        operation = self.direction_to_operation[direction]
        new_coord = operation(previous_coord,dist)
        return new_coord
