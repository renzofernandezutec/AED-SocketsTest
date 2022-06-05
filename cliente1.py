import socket
import threading
import SocketsCodigos
import json
import time
# import pygame
from random import randint

ContinuarHilo = False
socketCliente = None
NombreServidor, IP, Puerto = "", "", 5050
Formato = "utf-8"

#Variables Juego:
CartasActuales = []

def Connectar(ConnectarANube):
    if ConnectarANube:
        nombreServidor = "Linode Server"
        ip = "192.81.135.124"
    else:
        nombreServidor = socket.gethostname()
        ip = socket.gethostbyname(nombreServidor)
    return ip, Puerto


def CerrarConneccion():
    ContinuarHilo = False
    EnviarMensaje(SocketsCodigos.DESCONECTAR)
    exit()


def EnviarMensaje(comando, mensaje=""):
    if ContinuarHilo:
        socketCliente.send(str(f"{comando};{mensaje}").encode(Formato))
    else:
        print("No se ha enviado el mensaje")


def Listener():
    Salir = False
    while ContinuarHilo or not Salir:
        msg = socketCliente.recv(1024).decode(Formato)
        MSG = msg.split(";")

        if MSG[0] == SocketsCodigos.SolicitudDenegada:
            print(MSG[1])
            Salir = False  # Salir de listener
            return

        if MSG[0] not in (SocketsCodigos.RecivirCartas, SocketsCodigos.CartaEnMesa): #  Imprimir mensaje recivido
            print(f"Mensaje recivido: {str(msg)}")

        if MSG[0] == SocketsCodigos.CartaEnMesa:
            print(f"La actual carta en Mesa es: {MSG[1]}")

        if MSG[0] == SocketsCodigos.UsuarioConnectado:
            print(f"El usuario {MSG[1]} se ha connectado.")

        # if MSG[0] == SocketsCodigos.RecivirCartas:
        #     # cartas = [Tarjeta.convertirTarjetaAObjeto(carta) for carta in json.loads(MSG[1])]
        #     [print(carta) for carta in cartas]


def main():
    # Inicio del Juego
    NombreUsuario = input("Hola, inserte su nombre: ")
    #NombreDeJugador = "Renzo" + str(randint(1,5))

    ContinuarHilo = True

    socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketCliente.connect(Connectar(False))
    EnviarMensaje(SocketsCodigos.AgregarUsuario, NombreUsuario)

    # Crear Hilo para Escuchar
    listener = threading.Thread(target=Listener)
    listener.start()

    input("Menu")
    input("\n")

    # Finalizar Cliente
    CerrarConneccion()

main()