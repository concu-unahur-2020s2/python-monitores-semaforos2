import threading
import time
import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(threadName)s] - %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

clientes = []
filaCaja = []
cantMaxSuper = 3
cantClientes = 4
semaforoCaja = threading.Semaphore(0)
semaforoSuper = threading.Semaphore(0)

class Cliente(threading.Thread):
    def __init__(self,numero):
        super().__init__()
        self.name = f'Cliente {numero}'


    def entraAlSuper(self):
        clientes.append(1)
        logging.info('Eligiendo productos')
        time.sleep(2)
    
    def despertarCajero(self):
        if len(filaCaja) == 1:
            semaforoCaja.release()

    def irALaCaja(self):
        logging.info('Me voy a pagar')
        filaCaja.append(1)
        self.despertarCajero()
    
    
    def run(self):
        if len(clientes) == cantMaxSuper:
            logging.info('El super esta lleno, me voy a casa')
        else:
            self.entraAlSuper()
            self.irALaCaja()
            semaforoSuper.acquire()
            clientes.pop(0)
            logging.info('Me voy a casa sin dinero')



class Cajero(threading.Thread):
    def __init__(self):
        super().__init__()
        self.name = 'Cajero'

    def atender(self):
        if len(filaCaja) == 0 :
            semaforoCaja.acquire()
            logging.info('Me voy a dormir')
        logging.info('Que pase el que sigue')
        filaCaja.pop(0)
        logging.info('Estoy atendiendo')
        time.sleep(1)
        semaforoSuper.release()

    def run(self):
        while(True):
            self.atender()

Cajero().start()

for i in range(cantClientes):
    Cliente(i).start()





