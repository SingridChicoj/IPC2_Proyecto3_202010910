import xml.etree.ElementTree as ET
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

global fecha
global texto
global positivos
global negativos

fecha = []
texto = []
positivos = []
negativos = []


@app.route('/reset', methods=['DELETE'])
def resetear():
    fecha.clear()
    texto.clear()
    positivos.clear()
    negativos.clear()
    return jsonify({
        "message": "Se limpiaron las listas"
    })


@app.route('/upload_fileMessages', methods=['POST'])
def upload_fileMessages():
    global fecha
    global texto

    fecha = []
    texto = []

    if 'file' not in request.files:
        return jsonify({
            "message": "No se ha enviado un archivo"
        })
    archivo = request.files['file']
    contenidoarchivo = ET.fromstring(archivo.read().decode('utf-8'))
    # print(contenidoarchivo)

    for mensaje in contenidoarchivo.findall('.//MENSAJE'):
        for date in mensaje.findall('FECHA'):
            fecha.append({"fecha": date.text})
    print(fecha)

    for mensaje in contenidoarchivo.findall('.//MENSAJE'):
        for Texto in mensaje.findall('TEXTO'):
            texto.append({"texto": Texto.text})
    print(texto)

    response_data = {
        "fecha": fecha,
        "texto": texto
    }
    return jsonify(response_data)


@app.route('/upload_fileConfig2', methods=['POST'])
def upload_fileConfig2():
    global positivos
    global negativos

    positivos = []
    negativos = []
    if 'file' not in request.files:
        return jsonify({
            "message": "No se ha enviado un archivo"
        })
    archivo2 = request.files['file']
    '''contenidoarchivo2 = archivo2.read().decode('utf-8')
    print(contenidoarchivo2)'''
    contenido = ET.fromstring(archivo2.read().decode('utf-8'))

    for sentimiento in contenido.findall('.//sentimientos_positivos'):
        for palabra in sentimiento.findall('palabra'):
            positivos.append(palabra.text)
    print(positivos)

    for sentimiento in contenido.findall('.//sentimientos_negativos'):
        for palabra in sentimiento.findall('palabra'):
            negativos.append(palabra.text)
    print(negativos)

    response_data = {
        "positivos": positivos,
        "negativos": negativos
    }

    '''response_data = {
        "message": "Archivo leido"
    }'''
    return jsonify(response_data)


@app.route('/consultarHas', methods=['GET'])
def consultarHas():
    global fecha
    global texto
    fechaHAS = request.args.get('fecha')
    datos = []
    buffer = ""
    state = 0
    contador = 0

    for i in range(len(fecha)):
        if fecha[i].get('fecha') == fechaHAS:
            datos.append(texto[i].get('texto'))
            for c in texto[i].get('texto'):
                if state == 0:
                    if c == "#":
                        buffer += c
                        state = 1
                        continue
                if state == 1:
                    if c != "#":
                        buffer += c
                        continue
                    else:
                        buffer += c
                        state = 0
                        continue
            print(buffer, "+", contador)
    return jsonify(buffer)

@app.route('/consultarMenc', methods=['GET'])
def consultarMenc():
    global fecha
    global texto
    fechaHAS = request.args.get('fecha')
    datos = []
    buffer = ""
    state = 0
    contador = 0

    for i in range(len(fecha)):
        if fecha[i].get('fecha') == fechaHAS:
            datos.append(texto[i].get('texto'))
            for c in texto[i].get('texto'):
                if state == 0:
                    if c == "@":
                        buffer += c
                        state = 1
                        continue
                if state == 1:
                    if c != " ":
                        buffer += c
                        continue
                    else:
                        buffer += c
                        state = 0
                        continue
            print(buffer)
            #print(buffer, "+", contador)
    return jsonify(buffer)

@app.route('/obMensajes', methods=['GET'])
def obtenerMensajes():
    global fecha
    global texto
    response_data = {
        "messagesF": fecha,
        "messagesT": texto
    }
    return jsonify(response_data)


@app.route('/obConfig', methods=['GET'])
def obtenerConfiguracion():
    global positivos
    global negativos
    response_data = {
        "Spositivos": positivos,
        "Snegativos": negativos
    }
    return jsonify(response_data)


@app.route('/ayuda', methods=['GET'])
def ayuda():
    response_data = {
        "message": "Datos del estudiante:\nSingrid Cristabel Chicoj Martinez\n202010910\nIntroduccion a la Programacion y Computacion 2 Seccion D\nLink: https://github.com/SingridChicoj/IPC2_Proyecto3_202010910.git"
    }
    return jsonify(response_data)


if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)
