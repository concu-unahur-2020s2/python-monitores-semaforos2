import random
import threading
import time

'''
ESTE CODIGO ESTA SIN TERMINAR
ESTE CODIGO ESTA SIN TERMINAR
ESTE CODIGO ESTA SIN TERMINAR
'''


listaSupermercado = []
listaCaja = []

cantidadMaximaDeClientes = 2

semaforoSupermercado = threading.Semaphore(cantidadMaximaDeClientes)
monitorCaja = threading.Condition()

class Supermercado(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while(True):
            semaforoSupermercado.acquire()
            listaSupermercado.append(cliente1)
            print("cliente", cliente1, "- Entró al supermercado")
            time.sleep(2)

class Cliente(threading.Thread):
    def __init__(self,nro):
        super().__init__()
        self.nro = nro

    def entroAlSuper(self):
        while True:
            if(listaSupermercado.__contains__(self)):
                print("cliente", self.nro, "- Todavia hay lugar, voy a entrar")
                time.sleep(5)
                self.voyALaCaja()
            else:    
                print("cliente",self.nro, "- Mi plata no vale? Me vuelvo a mi casa")
                exit()

    def voyALaCaja(self):
            with monitorCaja:
                listaCaja.append(self)
                monitorCaja.notify()
                print("cliente", self.nro, "- Elijo mis productos y me voy a la caja")
                time.sleep(2)    

    def run(self):
        self.entroAlSuper()
        


class Caja(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while(True):
            with monitorCaja:
                while(len(listaCaja) < 1):
                    monitorCaja.wait()
                    c = listaCaja.pop(0)
                    print("Despacho al cliente", c)
                    listaSupermercado.pop(0)
                    semaforoSupermercado.release()
                    time.sleep(2)    


super1 = Supermercado()
super1.start()

caja1 = Caja()
caja1.start()

while (True):
    idCliente=random.randrange(1,100)
    cliente1 = Cliente(idCliente)
    time.sleep(5)
    cliente1.start()

