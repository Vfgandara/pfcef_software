"""
Esse script conduz os testes para os arquivos de dados
dentro da pasta test_data/
"""


import serial
from solver import Solver
from glob import glob
import numpy as np

def parse_data(raw_message):
    """
    Essa função realiza o papel equivalente ao parsing dos
    dados dentro do algoritmo, com adição de ruído aos dados
    """
    message = raw_message.strip()
    message = message.replace("\\","")
    message = message.replace("rn\'","")
    parsed_message = message.replace("data:","")

    distance, angle = parsed_message.split(" ")
    # Para remover a adição de ruído no sensor de distância, comente a linha abaixo
    distance = float(distance) + np.random.normal(0,3.66,1)
    # Para remover a adição de ruído no giroscópio, comente a linha abaixo
    angle = float(angle) + np.random.normal(0.15,2.01,1)

    return float(distance), float(angle)

test_data_paths = [i for i in glob("test_data/*.txt")]

for path in test_data_paths:
    solver = Solver() # Reinstanciar o Solver é o equivalente a reiniciar o algoritmo

    # Remove-se o processo de calibração dos dados pois eles foram criados
    # descontando o tamanho do dispositivo. O valor de 'b' nesse caso acaba
    # por gerar deformações irreais na geometria
    solver.a = 1
    solver.b = 0

    # Os arquivos de dados servem como falso envio de dados
    file = open(path, "r")
    # Eles são lidos linha a linha, mimicando o comportamento dinâmico
    # e incremental do algoritmo
    for message in file.readlines():
        if "data" in message:
            data_point = parse_data(message)
            solver.process_entry(data_point)
    solver.plot(saving_path=path.replace(".txt","_PLOT.png"))
    file.close()
