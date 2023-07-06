// Declara el pin al que está conectado el LED
//led rojo - 11
//led verde - 10
//led azul - 9
//led blanco - 6
//led infrarojo - 5

const int LedRojo = 11;
const int LedVerde = 10;
const int LedAzul = 9;
const int LedBlanco = 6;
const int LedInfrarrojo = 5;
bool start = false;

#define MAX_SIZE 50  // Tamaño máximo del array

void iniciar(int duracion, int descanso, int nVeces, int led) {
  delay(3000);
  for (int i = 0; i < nVeces; i++) {
    // Encender el LED
    digitalWrite(led, HIGH);
    // Duración
    delay(duracion);

    digitalWrite(led, LOW);
    // Descanso
    delay(descanso);
  }
  delay(3000);
  start = false;
}



void setup() {
  // Inicializar el puerto serie
  Serial.begin(9600);

  // Configura el pin como salida
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(5, OUTPUT);
}

void loop() {
digitalWrite(5, HIGH);

  if (Serial.available() > 0) {   // Si hay datos disponibles en el puerto serial
    char receivedData[MAX_SIZE];  // Array para almacenar los datos recibidos
    int values[MAX_SIZE];         // Array para almacenar los números convertidos

    // Leer la cadena de datos del puerto serial
    int bytesRead = Serial.readBytesUntil('\n', receivedData, MAX_SIZE);
    receivedData[bytesRead] = '\0';  // Agregar el carácter nulo al final de la cadena

    // Dividir la cadena en tokens y convertirlos en números
    char* token = strtok(receivedData, ",");
    int i = 0;
    while (token != NULL && i < MAX_SIZE) {
      values[i] = atoi(token);    // Convertir el token a entero
      token = strtok(NULL, ",");  // Obtener el siguiente token
      i++;
    }

    //activar pupilometro iniciar(int duracion, int descanso, int nVeces, int led);
    // iniciar(values[0], values[1], values[2], values[3]);

    // entrada 2000,2000,3,11
    
    // Imprimir los valores almacenados en el array   2000,2000,3,11
    Serial.println(values[1]);
    start= true;
    if (start == true) {
      iniciar(values[0], values[1], values[2],values[3]);
    }
     /*for (int j = 0; j < i; j++) {
      Serial.print("Valor ");
      Serial.print(j);
      Serial.print(": ");
      Serial.println(values[j]);
    }*/
  }
}
