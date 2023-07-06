import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QRadioButton, QLineEdit, QPushButton, QComboBox, QLabel, QMessageBox
from PyQt5.QtGui import QIntValidator
import serial
import time
import tkinter as tk
from tkinter import messagebox
from cam import GrabadorVideo

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.TiempoGrabacion = 0 
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Interfaz pupilometro')
        self.setGeometry(300, 300, 300, 200)

        main_layout = QVBoxLayout()

        ungroup = QGroupBox('Comunicación COM')
        ungroup_layout = QVBoxLayout()

        self.combobox = QComboBox()  # Convertir en atributo de clase
        self.combobox.addItem('COM1')
        self.combobox.addItem('COM2')
        self.combobox.addItem('COM3')
        self.combobox.addItem('COM4')
        self.combobox.addItem('COM5')
        self.combobox.addItem('COM6')
        self.combobox.addItem('COM7')

        input_text_label = QLabel('VELOCIDAD DE TRASMISIÓN')
        self.input_text = QLineEdit()  # Convertir en atributo de clase
        self.input_text.setValidator(QIntValidator())

        button2 = QPushButton('Comprobar conexión')
        button2.clicked.connect(self.ComprobarConexion)  # Conectar el botón a la función enviar_datos

        ungroup_layout.addWidget(self.combobox)
        ungroup_layout.addWidget(input_text_label)
        ungroup_layout.addWidget(self.input_text)
        ungroup_layout.addWidget(button2)

        ungroup.setLayout(ungroup_layout)
        main_layout.addWidget(ungroup)

        groupbox = QGroupBox('Radio Buttons')
        groupbox_layout = QVBoxLayout()


        self.comboboxLED = QComboBox()  # Convertir en atributo de clase
        self.comboboxLED.addItem('Rojo')
        self.comboboxLED.addItem('Azul')
        self.comboboxLED.addItem('Verde')
        self.comboboxLED.addItem('Blanco')
        
        groupbox_layout.addWidget(self.comboboxLED)
       
 

        groupbox.setLayout(groupbox_layout)
        main_layout.addWidget(groupbox)

        input1_label = QLabel('Tiempo de estímulo(ms):')
        estimulo_tiempo = QLineEdit()
        estimulo_tiempo.setValidator(QIntValidator())

        input2_label = QLabel('Descanso(ms):')
        descanso = QLineEdit()
        descanso.setValidator(QIntValidator())

        input3_label = QLabel('Número de ciclos:')
        nCiclos = QLineEdit()
        nCiclos.setValidator(QIntValidator())

        main_layout.addWidget(input1_label)
        main_layout.addWidget(estimulo_tiempo)

        main_layout.addWidget(input2_label)
        main_layout.addWidget(descanso)

        main_layout.addWidget(input3_label)
        main_layout.addWidget(nCiclos)

        button = QPushButton('Enviar')
        button.clicked.connect(lambda: self.enviarDatos(estimulo_tiempo.text(), descanso.text(), nCiclos.text()))

        main_layout.addWidget(button)

        self.setLayout(main_layout)



    def CategorizarLed(self, dato):
        colores = {
            'Rojo': 11,
            'Verde': 10,
            'Blanco': 6,
            'Azul': 9
        }

        # Obtener el número correspondiente al color utilizando el diccionario
        numero = colores.get(dato)
        return numero

    def verificar_puerto_com(self, puerto):
        try:
            arduino = serial.Serial(puerto)
            arduino.close()
            return True
        except serial.SerialException:
            return False

    def ComprobarConexion(self):
        puerto_com = self.combobox.currentText()
        if self.verificar_puerto_com(puerto_com):
            QMessageBox.information(self, 'Alerta', 'Si hay comunicación con el puerto')
        else:
            QMessageBox.information(self, 'Alerta', 'Error, no conectado')

    def enviar_datos(self, datos):
        # Obtener la configuración del puerto COM seleccionado
        # Obtener el valor seleccionado del QComboBox
        puerto_com = self.combobox.currentText()
        serialPort = int(self.input_text.text())
        arduino = serial.Serial(puerto_com, serialPort)  # Ajusta el puerto COM según corresponda
        time.sleep(2)  # Esperar a que Arduino establezca la conexión

        # Enviar número a Arduino
        arduino.write(str(datos).encode())
        
       

        QMessageBox.information(self, 'Alerta', 'Enviando instrucciones...')

        grabador = GrabadorVideo(tiempo_grabacion=self.TiempoGrabacion)
        grabador.grabar_video()
        # Cerrar la conexión serial
        arduino.close()

    def enviarDatos(self, estimulo_tiempo, descanso, nCiclos):
        comboLED = self.comboboxLED.currentText()
        numero = self.CategorizarLed(comboLED)
        mensaje = estimulo_tiempo + "," + descanso + "," + nCiclos + "," + str(numero)

        
        self.TiempoGrabacion = ((int(estimulo_tiempo)+int(descanso))*int(nCiclos)+6000)/1000
  # Crear una instancia de GrabadorVideo con un tiempo de grabación de 2 segundos
        
        
        # Llamar al método grabar_video en la instancia de GrabadorVideo
        

        self.enviar_datos(mensaje)

    def metodo(self):
        # Llama al método grabar_video en la instancia de GrabadorVideo
        self.grabador.grabar_video()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
