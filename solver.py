"""
Esse arquivo realiza a definição da classe Solver.
Dentro do contexto do algoritmo, ele concentra a maioria
das funções diretamente atreladas ao processo de digitalização
do cômodo medido.
"""


import matplotlib.pyplot as plt

from angle_wheel import AngleWheel
from typing import Tuple

class Solver():
    """
    Essa classe concentra todas rotinas de resolução do algoritmo
    Ela engloba uma instância da classe AngleWheel em si para
    realizar o tratamento e tracking de valores de ângulo
    Ela também passa os valores de distância pela função de calibração
    """

    def __init__(self):
        """
        Inicializa todos atributos necessários ao processo de digitalização/reconstrução
        """
        self.angle_wheel = AngleWheel() # armazena e processa informações de ângulo
        self.raw_data_points = [] # armazena os dados crus de entrada
        self.coordinates = [(0,0)] # armazena a lista de coordenadas do cômodo
        self.a = 0.98 # valor de 'a' na calibração ax + b
        self.b = 24.26 # valor de 'b' na calibração ax + b
        self.dist_calibration = lambda x: self.a*x + self.b # função de calibração de distância

    def _raw_input_data_to_proc_data(self, data: Tuple[float, float]) -> Tuple[float, float]:
        """
        Essa função realiza o processo de transformar os dados crus de entrada
        em dados utilizáveis para o processo de escolha e validação do ângulo
        para o cálculo da próxima coordenada
        """

        dist, raw_angle = data
        proc_angle = self.angle_wheel(raw_angle)
        proc_dist = self.dist_calibration(dist)
        return proc_dist, proc_angle

    def _proc_data_to_coord(self, point: Tuple[float, float]) -> Tuple[int,int]:
        """
        Essa função utiliza do objeto AngleWheel para realizar o cálculo da
        próxima coordenada com base nos valores de distância e ângulo do ponto
        atual. Internamente ela utiliza também do último valor de coordenada
        obtido.
        """
        return self.angle_wheel.data_to_coord(point, self.coordinates[-1])

    def process_entry(self, raw_point: Tuple[float, float]):
        """
        Essa função realiza o processamento completo de uma entrada de conjunto
        de dados. A nível de algoritmo, ela é o equivalente a dar um passo
        completo para um valor de entrada. Ela processa os valores, checa sua
        validade e, se válidos, os utiliza para calcular a próxima coordenada.
        """
        proc_point = self._raw_input_data_to_proc_data(raw_point)
        if proc_point[1] != -1:
            self.raw_data_points.append((proc_point[0],raw_point[1]))
            new_coordinate = self._proc_data_to_coord(proc_point)
            self.coordinates.append(new_coordinate)

    def plot(self, saving_path: str = ""):
        """
        Essa função realiza o plot da geometria digitalizada até o momento de
        seu chamamento. Para isso, ele usa do atributo .coordinates da classe.
        Se um argumento é passado para saving_path, a imagem plotada também
        será salva no path determinado por esse argumento.
        """
        x_points, y_points = zip(*self.coordinates) # Separa os valores x e y das coordenadas

        # Cálculo da proporção da imagem
        del_x = max(x_points) - min(x_points)
        del_y = max(y_points) - min(y_points)
        ratio = del_x/del_y
        fig, ax = plt.subplots(figsize=(6*ratio, 6))

        # O método plot irá ligar por linhas retas as coordenadas inseridas
        ax.plot(x_points, y_points)

        # Anota os valores de medida nas respectivas paredes
        for i in range(1,len(self.coordinates)):
            x = (x_points[i] - x_points[i-1])/2 + x_points[i-1]
            y = (y_points[i] - y_points[i-1])/2 + y_points[i-1]
            dist_val = self.raw_data_points[i-1][0]
            ax.text(x,y,f"{dist_val:.2f}", fontsize="xx-large")

        # Se um path é passado, salva a imagem
        if saving_path:
            # O path dado é utilizado para dar o título ao plot
            plt.title(saving_path.split("/")[-1].replace(".png",""))
            plt.savefig(saving_path)
        plt.show()
