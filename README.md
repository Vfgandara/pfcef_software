# Firmware e Script de digitalização

Esse repositório conta com os códigos de firmware e software de reconstrução para o Projeto Final de Conclusão em Engenharia Física do aluno Víctor Fernandes Gandara

## Como usar

### Firmware

O arquivo de firmware para ser feito upload ao Arduino Nano é o `firmwarev3.ino`. Recomenda-se realizar esse processo por meio da [IDE Arduino](https://www.arduino.cc/en/software).

### Coleta de dados e digitalização

O script `main.py` deve ser executado com o dispositivo já conectado ao computador por meio do cabo USB. A porta USB é declarada dentro desse arquivo pela variável `USB_PORT`, que deve ser verificada antes da execução. Por padrão, seu valor é `/dev/ttyUSB0`, sendo essa uma porta típica para sistemas operacionais GNU+Linux.

Durante a execução, sempre que houver o recebimento de um dado pelo algoritmo mediante o pressionamento do botão do dispositivo, esse conjunto de dados será mostrado no terminal. 

Quando finalizada a tomada de dados, o script deve ser interrompido por meio de um `KeyboardInterrupt`. Usualmente, isso é feito por meio do pressionamento das teclas `Ctrl`e `c` com o terminal aberto e selecionado. 

O script irá então realizar o plot do resultado final e salvá-lo na mesma pasta da execução utilizando como nome do arquivo o timestamp atual. 

### Testes

O script de testes é o `testing.py`. Ele não necessita de nenhuma configuração prévia e irá utilizar de todos os arquivos com terminação `.txt` dentro da pasta `test_data/`. Cada arquivo será individualmente plotado e salvo nessa pasta. O script adiciona ruído tanto nos valores de distância como de ângulo com base nas métricas de erro apresentados na monografia e assumindo distribuição normal. 
