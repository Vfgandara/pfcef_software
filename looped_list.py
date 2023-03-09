"""
Esse arquivo contém a classe LoopedList, que é usada dentro da classe AngleWheel
para manter registro da última direção utilizada no algoritmo e qual deverá ser
a próxima
"""


class LoopedList(list):
    """
    Essa classe simplesmente herda o comportamento da lista built-in do Python
    e a modifica para que, se um índice maior que seu tamanho seja usado, ela
    retorne o valor correspondente se a lista se repetisse infinitamente.
    """
    def __getitem__(self, i):
        max = len(self) # valor máximo do índice
        index = i - max*(i//max) # cálculo do índice equivalente
        return super().__getitem__(index) # chamamento do comportamento da lista built-in com novo índice
