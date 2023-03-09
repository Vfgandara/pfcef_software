"""
Esse script orquestra a comunicação serial
entre o dispositivo e o algoritmo de reconstrução.
"""


import serial
import pandas as pd
from datetime import datetime

from solver import Solver
from serial_data_broker import SerialDataBroker

USB_PORT = '/dev/ttyUSB0' # Insira aqui o identificar da porta USB

 # Se AUTO_PLOT for ligado, irá realizar o processo de plotting cada vez
 # que um novo dado for recebido. O processo de plotting trava a execução
 # da aplicação até que o plot seja fechado, assim necessitando de ação
 # por parte do usuário
AUTO_PLOT = False

try:
    solver = Solver()
    serial_broker = SerialDataBroker(USB_PORT) #Inicializa a comunicação serial

    while (True): # Executa a coleta de dados até que o usuário a interrompa

        # O objeto serial_broker pode ser checado como uma booleana,
        # quando ele retorna True significa que um novo valor foi encontrado
        # e que ele foi armazenado internamente na instância serial_broker
        if serial_broker:
            distance, angle = serial_broker.parse_data() # obtem o dado parseado
            # Como o algoritmo é dinâmico, ele pode ser tratado em passos
            # A função abaixo realiza um passo do algoritmo
            solver.process_entry((distance,angle))
            print(f"Dado recebido:\ndistância: {distance}cm\tÂngulo: {angle}")

            if AUTO_PLOT:
                solver.plot() # realiza o plot com os dados atuais

# O KeyboardInterrupt é um input do usuário finalizando o processo de tomada de dados
except KeyboardInterrupt:
    if solver.raw_data_points: # Realiza o plot somente se dados tiverem sido gerados
        timestamp = str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))
        # O plot também realiza o salvamento da imagem final se passado um caminho
        solver.plot(saving_path = timestamp + "_output.png")
    serial_broker.stop_communication(USB_PORT)

except Exception as e:
    serial_broker.stop_communication(USB_PORT)
    raise e
