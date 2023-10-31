import xml.etree.ElementTree as ET
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

global resultadosMostrar
global positivos
global negativos

resultadosMostrar = []
positivos = []
negativos = []

@app.route('/upload_file',methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({
        "message": "No se ha enviado un archivo, intente de nuevo :("
        })
    file = request.files['file']
    # leer el contenido del archivo
    # Ahora el contenido lo convertimos a un string
    file_contents=file.read().decode('utf-8')
    # Print del contenido
    print(file_contents)
    return jsonify({
        "message": "El archivo fue cargado exitosamente y fue leido:)"
    })  


@app.route('/upload_fileMessages', methods=['POST'])
def upload_fileMessages():
    global resultadosMostrar
    if 'file' not in request.files:
        return jsonify({
            "message": "No se ha enviado un archivo"
        })
    archivo = request.files['file']
    #print(contenidoarchivo)
    contenidoarchivo = ET.fromstring(archivo.read())
    resultadosMostrar = [{
            "fecha": mensaje.find('FECHA').text,
            "mensaje": mensaje.find('TEXTO').text
        } for mensaje in contenidoarchivo.findall('.//MENSAJE')]
        
    if resultadosMostrar:
        return jsonify(resultadosMostrar)
    else:
        return jsonify({"message": "No se encontraron mensajes en el archivo XML"})


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
    contenidoarchivo2 = ET.fromstring(archivo2.read())
    #print(contenidoarchivo2)
    for sentimiento in contenidoarchivo2:
        if sentimiento.tag == 'sentimientos_positivos':
            for palabrap in sentimiento.findall('palabra'):
                positivos.append({"palabra": palabrap.text})
        if sentimiento.tag == 'sentimientos_negativos':
            for palabran in sentimiento.findall('palabra'):
                negativos.append({"palabra": palabran.text})
    
    response_data = {
        "positivos": positivos,
        "negativos" : negativos
    }
    return jsonify(response_data)


@app.route('/obMensajes', methods=['GET'])
def get_response_from_flask():
    global resultadosMostrar
    response_data={
        "messages": resultadosMostrar
    }
    return jsonify(response_data)

@app.route('/obConfig', methods=['GET'])
def get_response_from_flask2():
    global positivos
    global negativos
    response_data={
        "Spositivos": positivos,
        "Snegativos" : negativos
    }
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)