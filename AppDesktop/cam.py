import cv2
import time

class GrabadorVideo:
    def __init__(self, tiempo_grabacion):
        self.tiempo_grabacion = tiempo_grabacion

    def grabar_video(self):
        # Crea un objeto de captura de video
        cap = cv2.VideoCapture(0)  # 0 indica el índice de la cámara predeterminada

        # Verifica si la cámara se ha abierto correctamente
        if not cap.isOpened():
            print("No se pudo abrir la cámara")
            exit()

        # Obtén las dimensiones del marco de captura
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        # Genera el nombre del archivo con un número secuencial
        numero_secuencial = 1
        nombre_archivo = f"video_{numero_secuencial}.mp4"
        while True:
            if not self.existe_archivo(nombre_archivo):
                break
            numero_secuencial += 1
            nombre_archivo = f"video_{numero_secuencial}.mp4"

        # Crea un objeto VideoWriter para guardar el video
        output = cv2.VideoWriter(nombre_archivo, cv2.VideoWriter_fourcc(*'mp4v'), 30, (frame_width, frame_height))

        # Establece el tiempo de inicio de la grabación
        start_time = time.time()

        while True:
            # Lee un marco de la cámara
            ret, frame = cap.read()

            if not ret:
                print("Error al leer el marco")
                break

            # Muestra el marco capturado
            cv2.imshow('Camara', frame)

            # Guarda el marco en el video de salida
            output.write(frame)

            # Verifica si ha pasado el tiempo de grabación especificado
            if time.time() - start_time >= self.tiempo_grabacion:
                break

            # Si se presiona la tecla 'q', sal del bucle
            if cv2.waitKey(1) == ord('q'):
                break

        # Libera los recursos
        cap.release()
        output.release()

        # Cierra todas las ventanas abiertas
        cv2.destroyAllWindows()

        print(f"Grabación finalizada. Video guardado como: {nombre_archivo}")

    def existe_archivo(self, nombre_archivo):
        try:
            with open(nombre_archivo, "r"):
                return True
        except FileNotFoundError:
            return False
