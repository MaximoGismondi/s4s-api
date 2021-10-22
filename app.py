from typing import Collection
import os
from algoritmo import algoritmo
import json
from flask import Flask, json, request, jsonify
from firebase_admin import credentials, firestore, initialize_app
app = Flask(__name__) #a

llaves = {
    "type": "service_account",
    "project_id": "proyectos4s-89b8a",
    "private_key_id": str(os.environ.get('private_key_id')),
    "private_key": str(os.environ.get('private_key')).replace('\\n', '\n'),
    "client_email": "firebase-adminsdk-2kpop@proyectos4s-89b8a.iam.gserviceaccount.com",
    "client_id": "108558504320900989171",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2kpop%40proyectos4s-89b8a.iam.gserviceaccount.com"
}

cred = credentials.Certificate(llaves)
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

from flask_cors import CORS, cross_origin
from flask import Flask
import gunicorn
import copy, random, time
import copy, operator
import plotly.graph_objects as go
from datetime import datetime
import threading
from time import sleep

class Materia():
    def __init__(self, nombre, curso, posibleProfesores, posiblesAulas, cantModulos, modulosContinuos, color):
        self.nombre = nombre + "-" + curso
        self.curso = curso
        self.posibleProfesores = posibleProfesores
        self.posiblesAulas = posiblesAulas
        self.cantModulos = cantModulos
        self.modulosContinuos = modulosContinuos
        self.color = color

class Turno():
    def __init__(self, nombre, cantModulos):
        self.nombre = nombre
        self.cantModulos = cantModulos

class Posicion():
    def __init__(self, curso, dia, turno, modulo):
        self.curso = curso
        self.dia = dia
        self.turno = turno
        self.modulo = modulo

app = Flask("appUWU")
CORS(app)

@app.route('/adminONO', methods=['POST'])
def  esAdminOnoEsAdmin():
    content = request.json
    if str(os.environ.get('token')) == content['token']:
        idUsuario = request.args.get('idUsuario')
        print(idUsuario)
        doc_ref = db.collection(u'users').document(idUsuario)
        doc = doc_ref.get()
        if doc.exists:
            print(f'Document data:')
        else:
            return(u'No such document!')
    
        docDiccionario = doc.to_dict()
        print(docDiccionario.get("emailVerified"))
        return str(docDiccionario.get("emailVerified"))
    return "Nao Nao voce no teneu token"

@app.route('/', methods=['POST'])
def hello_world():
    content = request.json
    if str(os.environ.get('token')) == content['token']:
        return "A"
    return "Nao Nao voce no teneu token"

@app.route('/algoritmo', methods=['POST'])
def  hilos():
    content = request.json
    if str(os.environ.get('token')) == content['token']:
        nombreColegio = request.args.get('nombreColegio')
        hora = str(datetime.fromisoformat( datetime.now().isoformat(timespec='minutes') ))
        def math_fun():
            # The sleep here is simply to make it clear that this happens in the background
            sleep(1) 
            runAlgorithm(nombreColegio, hora)

        def fun():
            # Create thread to run math_fun for each argument in x 
            t = threading.Thread(target=math_fun)
            t.setDaemon(False)
            t.start()
            print("Ejecutado prro")

        fun()
        return hora
    return "Nao Nao voce no teneu token"

def runAlgorithm(nombreColegio = "jejeboi", hora = "algo fallo"):
    print(nombreColegio)
    doc_ref = db.collection(u'schools').document(nombreColegio)
    doc = doc_ref.get()
    if doc.exists:
        print(f'Document data:')
    else:
        return(u'No such document!')

    #docDiccionario es un diccionario de la escuela
    docDiccionario = doc.to_dict()
    aulas = []
    profesores = []
    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    cursos = []
    turnos = []
    materias = []
    horarios = []
    modulos = []
    disponibilidad = {}

    [cursos.append(i.get("nombre")) for i in docDiccionario["cursos"]]
    [aulas.append(i.get("nombre")) for i in docDiccionario["aulas"]]
    [profesores.append(i.get("nombre") + " " + i.get("apellido")) for i in docDiccionario["profesores"]]
    for i in docDiccionario["profesores"]:
        disponibilidad[i.get("nombre") + " " + i.get("apellido")] = i.get("disponibilidad")
        #print(i.get("disponibilidad"))
    for i in docDiccionario["turnos"]:
        if len(i.get("modulos")) > 0:
            nombreT = str(i.get("turno"))
            cantidadModulosT = len(i.get("modulos"))
            for i in i.get("modulos"):
                modulos.append(i)
            t = Turno(nombreT, cantidadModulosT)
            turnos.append(t)
    for curso in cursos:
        materias.append([])
        for i in docDiccionario["materias"]:

            if i.get("curso") == curso:
                nombreM = i.get("nombre")
                cursoM = i.get("curso")
                posiblesProfesoresM = []
                for profesor in i.get("profesoresCapacitados"):
                    if (i.get("profesoresCapacitados")[profesor]):
                        posiblesProfesoresM.append(profesor)
                posiblesAulasM = []
                for aula in i.get("aulasMateria"):
                    if (i.get("aulasMateria")[aula]):
                        posiblesAulasM.append(aula)
                cantidadDeModulosTotalM = i.get("cantidadDeModulosTotal")
                cantidadMaximaDeModulosPorDiaM = i.get("cantidadMaximaDeModulosPorDia")
                a = Materia(nombreM, cursoM, posiblesProfesoresM, posiblesAulasM, cantidadDeModulosTotalM, cantidadMaximaDeModulosPorDiaM, "red")
                materias[-1].append(a)
        materias[-1].append(Materia("Hueco",curso, [], [], 0, 99, "white"))    

    #curso
    #Dia
    #turnoo
    #modulo

    horarioDeDisponibilidad = []
    for j in dias:
        horarioDeDisponibilidad.append([])
        indexModulos = 0
        for k in turnos:
            horarioDeDisponibilidad[dias.index(j)].append([])
            for f in range(k.cantModulos):
                horarioDeDisponibilidad[dias.index(j)][turnos.index(k)].append(["Hueco"])
                for n in profesores:
                    if modulos[indexModulos]["inicio"] in disponibilidad[n][j][k.nombre] and disponibilidad[n][j][k.nombre][modulos[indexModulos]["inicio"]]:
                        horarioDeDisponibilidad[dias.index(j)][turnos.index(k)][f].append(n)
                indexModulos += 1

    try:
        horarios, materiasProfesores, horariosAulas = algoritmo(aulas, profesores, dias, cursos, turnos, materias, horarioDeDisponibilidad)
        horariosDiccionario = {}
        for curso in range(len(cursos)):
            horariosDiccionario[cursos[curso]] = {}
            for dia in range(len(dias)):
                horariosDiccionario[cursos[curso]][dias[dia]] = {}
                for turno in range(len(turnos)):
                    horariosDiccionario[cursos[curso]][dias[dia]][turnos[turno].nombre] = {}
                    for modulo in range(turnos[turno].cantModulos):
                        horariosDiccionario[cursos[curso]][dias[dia]][turnos[turno].nombre][str(modulo+1)] = horarios[curso][dia][turno][modulo].nombre


        horariosAulasDiccionario = {}
        for curso in range(len(cursos)):
            horariosAulasDiccionario[cursos[curso]] = {}
            for dia in range(len(dias)):
                horariosAulasDiccionario[cursos[curso]][dias[dia]] = {}
                for turno in range(len(turnos)):
                    horariosAulasDiccionario[cursos[curso]][dias[dia]][turnos[turno].nombre] = {}
                    for modulo in range(turnos[turno].cantModulos):
                        horariosAulasDiccionario[cursos[curso]][dias[dia]][turnos[turno].nombre][str(modulo+1)] = horariosAulas[curso][dia][turno][modulo]
        
        diccionarioColegio = {"horarios":horariosDiccionario, "materiasProfesores":materiasProfesores, "horariosAulas":horariosAulasDiccionario}
        escribir(diccionarioColegio, hora, nombreColegio)
    except:
       print("An exception occurred in your pp") 
    
def idGenerator():
    doc_ref = db.collection(u'school').document()
    return doc_ref.id

def escribir(my_data, hora, nombreColegio):
    print(my_data)
    db.document(u"schools/"+nombreColegio+"/horarios/"+hora).set(my_data)
    
    try:
        id = idGenerator()
        todo_ref.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

port = int(os.environ.get('PORT', 3304))
if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)
