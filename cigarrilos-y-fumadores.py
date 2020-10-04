import random
import threading
import time

papelEnMesa = []
fosforosEnMesa = []
tabacoEnMesa = []

###################
### Agentes
###################

def agentePapel():
    global papelEnMesa, fosforosEnMesa, tabacoEnMesa
    while True:
        semaforoAgente.acquire()
        semaforoLista.acquire()

        papelEnMesa.append(1)
        print("Coloco Papel")
        time.sleep(1)
        if len(fosforosEnMesa) + len(tabacoEnMesa) + len(papelEnMesa) == 2:
            despertarFumadores()
        
        semaforoLista.release()

def agenteTabaco():
    global papelEnMesa, fosforosEnMesa, tabacoEnMesa
    while True:
        semaforoAgente.acquire()
        semaforoLista.acquire()

        tabacoEnMesa.append(1)
        print("Coloco Tabaco")
        time.sleep(1)
        if len(fosforosEnMesa) + len(tabacoEnMesa) + len(papelEnMesa) == 2:
            despertarFumadores()
        
        semaforoLista.release()

def agenteFosforos():
    global papelEnMesa, fosforosEnMesa, tabacoEnMesa
    while True:
        semaforoAgente.acquire()
        semaforoLista.acquire()

        fosforosEnMesa.append(1)
        print("Coloco Fosforos")
        time.sleep(1)
        if len(fosforosEnMesa) + len(tabacoEnMesa) + len(papelEnMesa) == 2:
            despertarFumadores()

        semaforoLista.release()

#####################
### Despertador
#####################

def despertarFumadores():
    if len(fosforosEnMesa) >= 1 and len(tabacoEnMesa) >= 1:
        semaforoFumadorConPapel.release()
    elif len(papelEnMesa) >= 1 and len(tabacoEnMesa) >= 1:
        semaforoFumadorConFosforos.release()
    elif len(papelEnMesa) >= 1 and len(fosforosEnMesa) >= 1:
        semaforoFumadorConTabaco.release()


#####################
### Fumadores
#####################

def fumadorConPapel():
    global papelEnMesa, fosforosEnMesa, tabacoEnMesa
    while True:
        semaforoFumadorConPapel.acquire()
        semaforoLista.acquire()
        fosforosEnMesa.pop(0)
        tabacoEnMesa.pop(0)
        print("\nFumador con papel esta fumando 🚬\n")
        time.sleep(2)
        semaforoLista.release()
        semaforoAgente.release()
        semaforoAgente.release()


def fumadorConFosforos():
    global papelEnMesa, fosforosEnMesa, tabacoEnMesa
    while True:
        semaforoFumadorConFosforos.acquire()
        semaforoLista.acquire()
        papelEnMesa.pop(0)
        tabacoEnMesa.pop(0)
        print("\nFumador con fosforos esta fumando 🚬\n")
        time.sleep(2)
        semaforoLista.release()
        semaforoAgente.release()
        semaforoAgente.release()


def fumadorConTabaco():
    global papelEnMesa, fosforosEnMesa, tabacoEnMesa
    while True:
        semaforoFumadorConTabaco.acquire()
        semaforoLista.acquire()
        papelEnMesa.pop(0)
        fosforosEnMesa.pop(0)
        print("\nFumador con tabaco esta fumando 🚬\n")
        time.sleep(2)
        semaforoLista.release()
        semaforoAgente.release()
        semaforoAgente.release()

#################
### Threads
#################

agentePapel = threading.Thread(target=agentePapel)
agenteTabaco = threading.Thread(target=agenteTabaco)
agenteFosforos = threading.Thread(target=agenteFosforos)
fumadorConPapelHilo = threading.Thread(target=fumadorConPapel)
fumadorConFosforosHilo = threading.Thread(target=fumadorConFosforos)
fumadorConTabacoHilo = threading.Thread(target=fumadorConTabaco)


###################
### Semaforos
###################

semaforoAgente = threading.Semaphore(2)
semaforoLista = threading.Semaphore(1)
semaforoFumadorConPapel = threading.Semaphore(0)
semaforoFumadorConFosforos = threading.Semaphore(0)
semaforoFumadorConTabaco = threading.Semaphore(0)

##################
### Starts
##################

agentePapel.start()
agenteTabaco.start()
agenteFosforos.start()
fumadorConPapelHilo.start()
fumadorConFosforosHilo.start()
fumadorConTabacoHilo.start()
