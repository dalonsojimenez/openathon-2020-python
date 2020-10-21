from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel
import pyqtgraph as pg
from util import Extractor
import time
from rx.subject import Subject

class Monitor(QMainWindow):

    def __init__(self, refresh):

        super(Monitor, self).__init__()

        print('Se ha creado la clase Monitor')

        self.cpu = [0 for _ in range(100)]
        self.memory = [0 for _ in range(100)]
        self.freq = [0 for _ in range(100)]

        widget = QWidget()

        # Definimos el layout, en forma de vertical box
        vertical_box = QVBoxLayout()
        # Le indicamos que coja todo el ancho de la ventana
        vertical_box.addStretch(1)

        # Creamos un widget con el titulo para el gráfico de CPU
        self.cpu_label = QLabel()
        self.cpu_label.setText('CPU (0%)')

        # Añadimos el widget a nuestro layout
        vertical_box.addWidget(self.cpu_label)

        # Creamos un widget para mostrar el gráfico
        self.plot_cpu = pg.PlotWidget()

        self.cpu_x = list(range(100))

         # Ponemos el fondo en blanco
        self.plot_cpu.setBackground('k')
        # Definimos el rango del eje Y
        self.plot_cpu.setYRange(0, 100)
        # Definimos el color de la línea
        pen = pg.mkPen(color=(0, 255, 0))
        # Creamos la línea de la CPU
        self.data_line_cpu = self.plot_cpu.plot(self.cpu_x, self.cpu, pen=pen)

        # Añadimos el widget a nuestro layout
        vertical_box.addWidget(self.plot_cpu)

        # Creamos un widget con el titulo para el gráfico de RAM
        self.memory_label = QLabel()
        self.memory_label.setText('Memoria (0%)')

        # Añadimos el widget a nuestro layout
        vertical_box.addWidget(self.memory_label)
        
        # Creamos un widget para mostrar el gráfico
        self.plot_memory = pg.PlotWidget()

        self.memory_x = list(range(100))

         # Ponemos el fondo en blanco
        self.plot_memory.setBackground('k')
        # Definimos el rango del eje Y
        self.plot_memory.setYRange(0, 100)
        # Definimos el color de la línea
        pen = pg.mkPen(color=(0, 0, 255))
        # Creamos la línea de la CPU
        self.data_line_memory = self.plot_memory.plot(self.memory_x, self.memory, pen=pen)

        vertical_box.addWidget(self.plot_memory)

        # Creamos un widget con el titulo para el gráfico de Frecuencia
        self.freq_label = QLabel()
        self.freq_label.setText('Frecuencia actual (0 Mhz)')

        # Añadimos el widget a nuestro layout
        vertical_box.addWidget(self.freq_label)

        # Creamos un widget para mostrar el gráfico
        self.plot_freq = pg.PlotWidget()

        self.freq_x = list(range(100))

         # Ponemos el fondo en blanco
        self.plot_freq.setBackground('k')
        # Definimos el rango del eje Y
        self.plot_freq.setYRange(0, 100)
        # Definimos el color de la línea
        pen = pg.mkPen(color=(255, 0, 0))
        # Creamos la línea de la CPU
        self.data_line_freq = self.plot_freq.plot(self.freq_x, self.freq, pen=pen)

        # Añadimos el widget a nuestro layout
        vertical_box.addWidget(self.plot_freq)

        widget.setLayout(vertical_box)

        self.setCentralWidget(widget)

        self.extractor = Extractor()

        # Reactive application
        self.events_cpu = Subject()
        self.events_memory = Subject()
        self.events_freq = Subject()

        # Refrescamos los datos
        self.timer = QtCore.QTimer()
        self.timer.setInterval(refresh)
        self.timer.timeout.connect(self.get_cpu_data)
        self.timer.timeout.connect(self.get_memory_data)
        self.timer.timeout.connect(self.get_freq_data)
        self.timer.start()
        
        self.setWindowTitle('Mi monitor (Velocidad de refresco: {} ms)'.format(refresh))
        self.show()

    def update_cpu_data(self, nuevo_valor):
        # Eliminamos el primer valor del eje de las X y añadimos uno nuevo
        self.cpu_x = self.cpu_x[1:]
        self.cpu_x.append(self.cpu_x[-1] + 1)

        # Eliminamos el primer valor del eje de las Y y añadimos uno nuevo
        self.cpu = self.cpu[1:]
        self.cpu.append(nuevo_valor)
        self.data_line_cpu.setData(self.cpu_x, self.cpu)

        # Cambiamos el título de la gráfica
        self.cpu_label.setText('CPU ({}%)'.format(nuevo_valor))

    def update_memory_data(self, event):
        """
        Actualiza la información del gráfico de memoria
        :return:
        """
        # Remove the first X element and add a new value
        self.memory_x = self.memory_x[1:]
        self.memory_x.append(self.memory_x[-1] + 1)

        # Remove the first CPU element and add a new value
        self.memory = self.memory[1:]
        self.memory.append(event)
        self.data_line_memory.setData(self.memory_x, self.memory)

        self.memory_label.setText('Memoria ({}%)'.format(event))
    
    def update_freq_data(self, event):
        """
        Actualiza la información del gráfico de frecuencia
        :return:
        """
        min_freq = int(event._asdict()['min'])
        max_freq = int(event._asdict()['max'])
        current_freq = int(event._asdict()['current'])
        current_freq_perc = (current_freq - min_freq) * 100 / (max_freq - min_freq)

        self.plot_freq.setYRange(min_freq, max_freq)

        # Remove the first X element and add a new value
        self.freq_x = self.freq_x[1:]
        self.freq_x.append(self.freq_x[-1] + 1)

        # Remove the first CPU element and add a new value
        self.freq = self.freq[1:]
        self.freq.append(current_freq)
        self.data_line_freq.setData(self.freq_x, self.freq)

        self.freq_label.setText('Frecuencia actual ({} Mhz)'.format(current_freq))

    def get_cpu_data(self):
        """
        Método que recupera el valor de la CPU y envía un evento de forma reactiva
        """
        self.events_cpu.on_next(self.extractor.get_cpu_percent())

    def get_memory_data(self):
        """
        Método que recupera el valor de la memoria y envía un evento de forma reactiva
        """
        self.events_memory.on_next(self.extractor.get_virtual_memory_percent())
    
    def get_freq_data(self):
        """
        Método que recupera el valor de la frecuencia y envía un evento de forma reactiva
        """
        self.events_freq.on_next(self.extractor.get_cpu_freq())
