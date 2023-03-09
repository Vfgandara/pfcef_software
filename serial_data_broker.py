"""
Esse arquivo realiza a definição da classe SerialDataBroker.
Ela é responsável por estabelecer conexão com o dispositivo,
receber os dados e parseá-los para o seu uso pelo algoritmo.
"""


import os
import serial
from time import sleep
from typing import Tuple

class SerialDataBroker():
    """
    Essa classe concentra todas rotinas necessárias para a implementação
    da comunicação serial entre o dispositivo e o scipt que roda o algoritmo.
    Toda vez que seu método __bool__ é chamado por uma checagem do tipo "if",
    ele checa por novos dados e retorna se houve esse recebimento. Ele parseia
    os dados recebidos os retornando já em valores numéricos utilizáveis pelo
    algoritmo. Por fim, ela desempenha também o fechamento da comunicação,
    rotina essa chamada ao final do algoritmo, marcando seu fim.
    """
    def __init__(self, port: str = '/dev/ttyUSB0'):
        """
        Inicializa os atributos necessários, estabele a comunicação e espera
        pela chegada da mensagem de início de envio de dados
        """
        # estabelece a comunicação serial
        self.serial = serial.Serial(port = port, baudrate=9600)
        self.raw_message = "" # armazena a última mensagem recebida

        # para a execução até que seja recebida a mensagem de inicio de envio de dados
        while(1):
            # Lê a entrada serial e checa pela mensagem de início
            if "finalizada" in str(self.serial.readline()):
                print("Data Broker inicializado!")
                break # sai do loop e termina a inicialização

    def __bool__(self) -> bool:
        """
        Esse método define o comportamento da classe e suas instâncias ao serem
        tratadas como uma booleana. Ela é definida de forma a que, dentro do
        script principal (main.py), o simples ato de checar ela (if serial_broker,
        linha 31), faça com que ela primeiramente cheque se houve a chegada de
        um novo dado. A booleana retornada indica se houve tal recebimento.
        """
        self.raw_message = str(self.serial.readline())
        return "data" in self.raw_message

    def parse_data(self) -> Tuple[float, float]:
        """
        Esse método realiza o processo de parsing dos dados de entrada. Ele limpa
        a mensagem recebida e a separa nos valores de distância e de ângulo para
        serem convertidos para floats.
        """
        message = self.raw_message.strip()
        message = message.replace("\\","")
        message = message.replace("rn\'","")
        parsed_message = message.replace("b'data:","")
        distance, angle = parsed_message.split(" ")
        return float(distance), float(angle)

    def stop_communication(self, port = '/dev/ttyUSB0'):
        """
        Esse método é utilizado como a rotina de finalização da comunicação
        serial, fechando ela e utilizando do comando "fuser -k" para terminar
        o processo iniciado na porta USB.
        """
        self.serial.close()
        os.system(f'fuser -k {port}')
