import random
import threading
import time
import logging

limiteDeClientes = 2
cantidadDeClientes = 3
clientesDentro = []
filaParaCaja = []
semaforoCajero = threading.Semaphore(0)
semaforoCliente = threading.Semaphore(0)

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

class Cliente(threading.Thread):
    def __init__(self, numero):
        super().__init__()
        self.name = f'Cliente {numero}'

    def entrarAlSuper(self):
        clientesDentro.append(1)
        logging.info("Eligiendo productos..")
        time.sleep(2)

    def ponerseEnFila(self):
        filaParaCaja.append(1)
        logging.info("Me puse en fila")
        self.despertarAlCajero()

    def despertarAlCajero(self):
        if len(filaParaCaja) == 1:
            print('Cachetaso al cajero')
            semaforoCajero.release()

    def run(self):
        if len(clientesDentro) == limiteDeClientes:
            logging.info('El super esta lleno, me voy a casa.')
        else:
            self.entrarAlSuper()
            self.ponerseEnFila()
            semaforoCliente.acquire()
            clientesDentro.pop(0)
            logging.info('Ya compre, me fui a casa.')

class Cajero(threading.Thread):
    def __init__(self):
        super().__init__()
        self.name = 'Cajero'

    def atender(self):
        if len(filaParaCaja) == 0:
            logging.info('Me voy a dormir')
            semaforoCajero.acquire()
        filaParaCaja.pop(0)
        logging.info('Estoy atendiendo')
        time.sleep(1)
        semaforoCliente.release()

    def run(self):
        while True:
            self.atender()


Cajero().start()

for i in range(cantidadDeClientes):
    Cliente(i).start()

