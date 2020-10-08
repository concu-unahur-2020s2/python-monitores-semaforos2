import random
import threading
import time

listaSupermercado = []
listaCaja = []

cantidadMaximaDeClientes = 4

monitorCaja = threading.Condition()


class Cliente(threading.Thread):
    def __init__(self,nro):
        super().__init__()
        self.nro = nro

    def entroAlSuper(self):
        while True:
            if(len(listaSupermercado) < cantidadMaximaDeClientes):
                print("cliente", self.nro, "- Todavia hay lugar, voy a entrar")
                listaSupermercado.append(self)
                time.sleep(2)
                self.voyALaCaja()
            else:    
                print("cliente",self.nro, "- Mi plata no vale? Me vuelvo a mi casa")
                exit()

    def voyALaCaja(self):
            with monitorCaja:
                listaCaja.append(self)
                monitorCaja.notify()
                print("cliente", self.nro, "- Elijo mis productos y me voy a la caja")
                time.sleep(10)    

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
                    time.sleep(2)    



caja1 = Caja()
caja1.start()

while (True):
    idCliente=random.randrange(1,100)
    cliente1 = Cliente(idCliente)
    time.sleep(5)
    cliente1.start()




