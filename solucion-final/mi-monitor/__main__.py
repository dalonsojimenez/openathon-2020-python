import sys
from monitor import Monitor
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QKeySequence, QPalette, QColor
from PyQt5.QtCore import Qt
 
try:
     print('Bienvenido al Openathon VII!')
 
     refresh = sys.argv[1]   
     refresh = int(refresh)
     if refresh < 100 or refresh > 1000:
         raise ValueError
     print('La frecuencia de refresco es {}'.format(refresh))

     app = QApplication(sys.argv)

     # Force the style to be the same on all OSs:
     app.setStyle("Fusion")

     # Now use a palette to switch to dark colors:
     palette = QPalette()
     palette.setColor(QPalette.Window, QColor(53, 53, 53))
     palette.setColor(QPalette.WindowText, Qt.white)
     palette.setColor(QPalette.Base, QColor(25, 25, 25))
     palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
     palette.setColor(QPalette.ToolTipBase, Qt.black)
     palette.setColor(QPalette.ToolTipText, Qt.white)
     palette.setColor(QPalette.Text, Qt.white)
     palette.setColor(QPalette.Button, QColor(53, 53, 53))
     palette.setColor(QPalette.ButtonText, Qt.white)
     palette.setColor(QPalette.BrightText, Qt.red)
     palette.setColor(QPalette.Link, QColor(42, 130, 218))
     palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
     palette.setColor(QPalette.HighlightedText, Qt.black)
     app.setPalette(palette)

     monitor = Monitor(refresh)

     # Se subscribe al stream de eventos de CPU
     monitor.events_cpu.subscribe(
     on_next=lambda x: monitor.update_cpu_data(x),
     on_error=lambda e: print(e),
     on_completed=lambda: sys.exit(0)
     )
     # Se subscribe al stream de eventos de memoria
     monitor.events_memory.subscribe(
     on_next=lambda x: monitor.update_memory_data(x),
     on_error=lambda e: print(e),
     on_completed=lambda: sys.exit(0)
     )
     # Se subscribe al stream de eventos de frfrecuencia
     monitor.events_freq.subscribe(
     on_next=lambda x: monitor.update_freq_data(x),
     on_error=lambda e: print(e),
     on_completed=lambda: sys.exit(0)
     )

     sys.exit(app.exec_())

except IndexError as index_error:
     print('Por favor, tienes que indicar la velocidad de refresco como parámetro de entrada')
     sys.exit(-1)
except ValueError as value_error:
     print('{} no es un valor válido'.format(refresh))
     print('Por favor, la velocidad de refresco tiene que ser un número entre 100 y 1000')
     sys.exit(-1)