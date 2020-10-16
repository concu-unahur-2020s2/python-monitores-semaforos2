import random
import logging
import threading
import time

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

cantidadMaxClientes = 3
clientesEnSuper = []
clientesEnCaja = []
semaforoCajero = threading.Semaphore(0)

class Cliente(threading.Thread):
    def __init__(self, numero):
        super().__init__()
        self.name = f'Cliente {numero}'

    def entrarAlSuper(self):
        clientesEnSuper.append(self)
        logging.info('Eligiendo productos')
        time.sleep(2)
        self.irALaCaja()

    def irALaCaja(self):
        clientesEnCaja.append(self)
        logging.info('Haciendo la fila')
        self.despertarCajero()
    
    def despertarCajero(self):
        if(clientesEnCaja.index(self) == 0):
            logging.info('Despierto al cajero')
            semaforoCajero.release()
    
    def puedoEntrar(self):
        return len(clientesEnSuper) < cantidadMaxClientes
        
    def run(self):
        if(self.puedoEntrar()):
            self.entrarAlSuper()
            clientesEnSuper.pop(0)
            logging.info('Terminé de comprar')
        else:
            logging.info('El supermercado está lleno, mejor vuelvo más tarde')


class Cajero(threading.Thread):
    def __init__(self):
        super().__init__()
        self.name = 'Cajero'
    
    def atenderClientes(self):
        if(self.noHayNadieParaAtender()):
            logging.info('Voy a dormir')
            semaforoCajero.acquire()
        else:
            clientesEnCaja.pop(0)
            time.sleep(2)
            logging.info('Atendí un cliente')

    def noHayNadieParaAtender(self):
        return len(clientesEnCaja) == 0

    def run(self):
        while(True):
            self.atenderClientes()

Cajero().start()

for i in range(5):
    Cliente(i).start()