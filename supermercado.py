import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

def cajero(monitor):
    print("Que pase el que sigue")
    while (True):
        with monitor:
            monitor.wait()
            print("Gracias por su compra")
            clientes.pop(0)

        
class Cliente(threading.Thread):
    def __init__(self, monitor):
        super().__init__()
        self.monitor = monitor
    
    def elegirProducto(self):
        time.sleep(2)
        with monitor:
            monitor.notify()


    def run(self):
        while (True):
            time.sleep(0.5)
            while  len(clientes)<10:
                clientes.append(0)
                self.elegirProducto()
                clientes.pop(0)
            print("Me voy a casa")

                    
clientes = []


clientes_monit = threading.Condition()


clientesA = Cliente(clientes_monit)
clientesA.start()

#intento de hacer el ejercicio con monitor, pero no salio.
