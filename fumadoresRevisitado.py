import random
import threading
import time

listaPapel = []
listaTabaco = []
listaFosforo = []

semaforoAgente = threading.Semaphore(2)
monitorFumadorConPapel = threading.Condition()
monitorFumadorConFosforos = threading.Condition()
monitorFumadorConTabaco = threading.Condition()


def mesa():
    while(True):
        with monitorFumadorConPapel:
            if(len(listaFosforo) > 0 and len(listaTabaco) > 0):
                monitorFumadorConPapel.notify()
       
        with monitorFumadorConFosforos:
            if(len(listaPapel) > 0 and len(listaTabaco) > 0):
                monitorFumadorConFosforos.notify()
       
        with monitorFumadorConTabaco:
            if(len(listaPapel) > 0 and len(listaFosforo) > 0):
                monitorFumadorConTabaco.notify()


class Agente(threading.Thread):
    def __init__(self,lista,semaforo,nro):
        super().__init__()
        self.lista = lista
        self.semaforo = semaforo
        self.nro = nro

    def run(self):
        while True:
            self.semaforo.acquire()
            self.lista.append(1)
            print("agente",self.nro, "cantidad", len(self.lista))
            time.sleep(2)


def fumadorConPapel():
    while True:
        with monitorFumadorConPapel:
            monitorFumadorConPapel.wait()
            listaFosforo.pop(0)  
            listaTabaco.pop(0)
            print("fumador1 con papel - tengo fosforo y tabaco en la mesa - voy a fumar")
            time.sleep(2)
            semaforoAgente.release()
            semaforoAgente.release()


def fumadorConFosforos():
    while True:
        with monitorFumadorConFosforos:
            monitorFumadorConFosforos.wait() 
            listaTabaco.pop(0)
            listaPapel.pop(0)
            print("fumador2 con fosforo - tengo tabaco y papel en la mesa - voy a fumar")
            time.sleep(2)
            semaforoAgente.release()
            semaforoAgente.release()


def fumadorConTabaco():
    while True:
        with monitorFumadorConTabaco:
            monitorFumadorConTabaco.wait()  
            listaPapel.pop(0)
            listaFosforo.pop(0) 
            print("fumador3 con tabaco - tengo papel y fosforo en la mesa - voy a fumar")
            time.sleep(2)
            semaforoAgente.release()
            semaforoAgente.release()






mesaHilo = threading.Thread(target=mesa)

agente1 = Agente(listaFosforo,semaforoAgente,1)
agente2 = Agente(listaPapel,semaforoAgente,2)
agente3 = Agente(listaTabaco,semaforoAgente,3)



fumadorConPapelHilo = threading.Thread(target=fumadorConPapel)
fumadorConFosforosHilo = threading.Thread(target=fumadorConFosforos)
fumadorConTabacoHilo = threading.Thread(target=fumadorConTabaco)



fumadorConPapelHilo.start()
fumadorConFosforosHilo.start()
fumadorConTabacoHilo.start()

agente1.start()
agente2.start()
agente3.start()


mesaHilo.start()