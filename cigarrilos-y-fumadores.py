import random
import threading
import time

mesa = []

def agentePapel():
    global mesa
    while True:
        semaforoAgente.acquire()
        mesa.append("P")
        print("Coloco Papel")
        time.sleep(1)
        if len(mesa) == 2:
            despetarFumador()

def agenteTabaco():
    global mesa
    while True:
        semaforoAgente.acquire()
        mesa.append("T")
        print("Coloco Tabaco")
        time.sleep(1)
        if len(mesa) == 2:
            despetarFumador()

def agenteFosforos():
    global mesa
    while True:
        semaforoAgente.acquire()
        mesa.append("F")
        print("Coloco Fosforos")
        time.sleep(1)
        if len(mesa) == 2:
            despetarFumador()

def despetarFumador():
    global mesa

    ingrediente1 = mesa[0]
    ingrediente2 = mesa[1]

    if ingrediente1.upper() == "F" and ingrediente2.upper() == "T":
        semaforoFumadorConPapel.release()
    elif ingrediente1.upper() == "P" and ingrediente2.upper() == "T":
        semaforoFumadorConFosforos.release()
    elif ingrediente1.upper() == "P" and ingrediente2.upper() == "F":
        semaforoFumadorConTabaco.release()


def fumadorConPapel():
    global mesa
    while True:
        with semaforoFumadorConPapel:
            mesa.pop(0)
            mesa.pop(0)
            print("\nFumador con papel esta fumando 🚬\n")
            time.sleep(2)
            semaforoAgente.release()
            semaforoAgente.release()


def fumadorConFosforos():
    global mesa
    while True:
        with semaforoFumadorConFosforos:
            mesa.pop(0)
            mesa.pop(0)
            print("\nFumador con fosforos esta fumando 🚬\n")
            time.sleep(2)
            semaforoAgente.release()
            semaforoAgente.release()


def fumadorConTabaco():
    global mesa
    while True:
        with semaforoFumadorConTabaco:
            mesa.pop(0)
            mesa.pop(0)
            print("\nFumador con tabaco esta fumando 🚬\n")
            time.sleep(2)
            semaforoAgente.release()
            semaforoAgente.release()



semaforoAgente = threading.Semaphore(2)
semaforoFumadorConPapel = threading.Semaphore(0)
semaforoFumadorConFosforos = threading.Semaphore(0)
semaforoFumadorConTabaco = threading.Semaphore(0)

agentePapel = threading.Thread(target=agentePapel)
agenteTabaco = threading.Thread(target=agenteTabaco)
agenteFosforos = threading.Thread(target=agenteFosforos)

fumadorConPapelHilo = threading.Thread(target=fumadorConPapel)
fumadorConFosforosHilo = threading.Thread(target=fumadorConFosforos)
fumadorConTabacoHilo = threading.Thread(target=fumadorConTabaco)


agentePapel.start()
agenteTabaco.start()
agenteFosforos.start()

fumadorConPapelHilo.start()
fumadorConFosforosHilo.start()
fumadorConTabacoHilo.start()
