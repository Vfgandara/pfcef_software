#include "Wire.h"
#include <MPU6050_light.h>
#define dist_sens_trig_pin 3 // Pino D3
#define dist_sens_echo_pin 2 // Pino D2
#define button_trig 9 // Pino D9
#define LOW_FILTER 5
MPU6050 mpu(Wire);
long tempo_voo;
float distancia;
float angulo_z;
bool trigger_buffer[LOW_FILTER];
int filter_index = 0;
int button_value = 0;
int button_sum = 0;
bool busy = true, trigger_status = false;

// Função de tradução do tempo de voo para valor de distância
float tempo_voo_para_dist(long tempo_voo){
  return (tempo_voo / 2.0) / 29.1;
}

// Laço de inicialização
void setup() {
  // Inicialização da comunicação serial
  Serial.begin(9600);

  // Inicialização dos pinos digitais
  pinMode(dist_sens_trig_pin, OUTPUT);
  pinMode(dist_sens_echo_pin, INPUT);
  pinMode(button_trig, INPUT);

  // Inicialização da comunicação I2C
  Wire.begin();
  
  // Inicialização do giroscópio
  byte mpu_status = mpu.begin();
  Serial.print(F("MPU6050 status: "));
  Serial.println(mpu_status); // Representação numérica da inicialização
  while(mpu_status!=0){ } // Caso o giroscópio não seja inicializado corretamente, o processamento é segurado
  

  // Calibração do giroscópio
  Serial.println(F("Calibrando o giroscópio..."));
  delay(1000);
  mpu.calcOffsets();
  Serial.println("Calibração finalizada!");
}

// Laço de execução recorrente
void loop() {
  // Atualização dos valores do giroscópio
  mpu.update(); // Deve ocorrer a cada passo do laço
  button_value = digitalRead(button_trig); // Leitura do valor do botão
  trigger_status = check_trigger(button_value); // Valor é passado pelo filtro e o status devolvido

  // Se ocorreu gatilho e o envio de dados não está ocupado
  if(trigger_status && !busy){
    busy = true; // Envio de dados se torna ocupado
    
    // Tomada de dado de distância
    digitalWrite(dist_sens_trig_pin, LOW); // Garante que o pino de gatilho não está ligado
    delayMicroseconds(2);
    digitalWrite(dist_sens_trig_pin, HIGH); // Ativa o gatilho de envio de sinal sonoro
    delayMicroseconds(10);// Pulso de 10 microsegundos
    digitalWrite(dist_sens_trig_pin, LOW); // Final do pulso
    tempo_voo = pulseIn(dist_sens_echo_pin, HIGH); // Retorna o tempo em microssegundos até chegada de um sinal no pino
    distancia = tempo_voo_para_dist(tempo_voo); // Retorna a distância a partir do tempo de voo
    
    // Tomada de dado de variação angular
    angulo_z = mpu.getAngleZ();
    
    // Envio de dado pela serial
    Serial.print("data:"); // Marcador de início de mensagem de dados
    Serial.print(distancia); // Valor de distância
    Serial.print(" "); // Separador
    Serial.println(angulo_z); // Valor de variação angular
  }

  // Se não houve gatilho, o botão não está mais sendo pressionado e o envio de dados deve ser liberado
  if(!trigger_status){
    busy = false;
  }
}

// Função de filtro digital do tipo passa-baixas para o botão
bool check_trigger(int button_value) {
  
  // Preenchimento do buffer de gatilho com novo valor lido
  trigger_buffer[filter_index] = button_value;
  filter_index += 1;
  if(filter_index >= LOW_FILTER){
    filter_index = 0;
  }

  // Conta o número de sinais 1
  button_sum = 0;
  for(int i=0;i<LOW_FILTER;i++){
  button_sum += trigger_buffer[i];
  }
  
  // Se todos os dinais são 1, retorna que houve gatilho
  if(button_sum==LOW_FILTER){
    return true;
  }
  return false; // Caso contrário, retorna que não houve
}
