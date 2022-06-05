import socket
import SocketsCodigos
import threading
import pickle
import json
import time
# from Objetos import Tarjeta

Usuarios = []
UsuariosObjetos = []
NombreServidor = socket.gethostname()
IP = socket.gethostbyname(NombreServidor)
Puerto = 5050
Formato = "utf-8"

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((socket.gethostname(), Puerto)) # Servidor Local
#servidor.bind(("", Puerto))  # Servidor Nube
servidor.listen(100)

# Juego


def FormatearMensaje(comando, mensaje=""):
    return f"{str(comando)};{str(mensaje)}"


def EscribirAJugador(idJugador,mensaje):
    UsuariosObjetos[idJugador].send(mensaje.encode(Formato))


def EscribirATodosMenosActual(actual, mensaje):
    for i in range(len(UsuariosObjetos)):
        if i != actual:
            UsuariosObjetos[i].send(mensaje.encode(Formato))


def EscribirAClientes(Mensajes, mismoMensaje):
    for i in range(len(UsuariosObjetos)):
        if mismoMensaje:
            UsuariosObjetos[i].send(Mensajes.encode(Formato))
        else:
            UsuariosObjetos[i].send(Mensajes[i].encode(Formato))


def ControladorCliente(conn, addr):
    global CartaEnMesa,seGano
    print(f"El cliente con IP: {addr} se ha conectado.\n")
    connectado = True
    idJugador = threading.active_count()-2
    nombreJugador = ""

    UsuariosObjetos.append(conn)
    while connectado:
        msg = conn.recv(1024).decode(Formato)
        print(f"Mensaje recivido: {str(msg)}")
        MSG = msg.split(";")

        # if MSG[0] == SocketsCodigos.AgregarUsuario:
        #     nombreJugador = str(MSG[1])
        #     Jugadores.append(nombreJugador)
        #     conn.send(f"Hola  {nombreJugador}".encode(Formato))
        #     print(f"Jugadores connectados: {Jugadores}")
        #     if threading.active_count()-1 == 2:  # Empezar juego porque ya hay dos jugadores
        #         EscribirAClientes(FormatearMensaje(SocketsCodigos.EnviarJugadores,json.dumps(Jugadores)), True)
        #         time.sleep(1)
        #         IniciarJuego()
        # elif MSG[0] == SocketsCodigos.MandarCartaServidor:
        #     CartaEnMesa = Tarjeta.convertirTarjetaAObjeto(json.loads(MSG[1]))
        #     MazoPrincipal.append(CartaEnMesa)  # Se agrega carta al final
        #     EscribirAClientes(FormatearMensaje(SocketsCodigos.CartaEnMesa, CartaEnMesa), True)
        #     if not seGano:
        #         EscribirATodosMenosActual(idJugador, FormatearMensaje(SocketsCodigos.InidicarTurnoActual, ""))
        #         time.sleep(0.5)

        # elif MSG[0] == SocketsCodigos.DESCONECTAR:
        #     print(f"El cliente : {nombreJugador} se ha desconnectado.")
        #     JugadoresObjetos.pop(idJugador)
        #     Jugadores.pop(idJugador)
        #     connectado = False

    # conn.close()


def IniciarServidor():
    servidor.listen()
    while True:
        conn, addr = servidor.accept()
        hilo = threading.Thread(target=ControladorCliente, args=(conn, addr))
        hilo.start()
        print(f"Numero de clientes connectados: {threading.activeCount()-1}")

print("Se ha iniciado el servidor de BlockChain")
print(f"Servidor: {NombreServidor} IP: {IP}")
print(f"Puerto: {Puerto}")
print()
IniciarServidor()
