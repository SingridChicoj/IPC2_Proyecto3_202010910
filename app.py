import sys
import os
import xml.etree.ElementTree as ET

from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

global fecha
global texto
global positivos
global negativos
global hashtags
global menciones
global Chashtags
global Cmenciones
global fechaHAS


fecha = []
texto = []
positivos = []
negativos = []
hashtags = []
menciones = []
Chashtags = 0
Cmenciones = 0
fechaHAS = ""


@app.route('/reset', methods=['POST'])
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
    #print(fecha)

    for mensaje in contenidoarchivo.findall('.//MENSAJE'):
        for Texto in mensaje.findall('TEXTO'):
            texto.append({"texto": Texto.text})
    #print(texto)

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
    #print(positivos)

    for sentimiento in contenido.findall('.//sentimientos_negativos'):
        for palabra in sentimiento.findall('palabra'):
            negativos.append(palabra.text)
    #print(negativos)

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
    global Chashtags
    global fechaHAS
    global hashtags

    fechaHAS = request.args.get('fecha')
    hashtags = []
    buffer = ""
    state = 0
    Chashtags = 0
    contador = 1

    for i in range(len(fecha)):
        if fecha[i].get('fecha') == fechaHAS:
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
                        if hashtags:
                            for i in range(len(hashtags)):
                                if hashtags[i].get('hashtag') == buffer:
                                    if buffer == "":
                                        continue
                                    else:
                                        contador = int(hashtags[i].get('cantidad'))
                                        contador += 1
                                        hashtags[i] = {'hashtag': buffer, 'cantidad': contador}
                                        buffer = ""
                                        contador = 1
                                        continue
                        if buffer == "":
                            continue
                        else:
                            hashtags.append({'hashtag': buffer, 'cantidad': contador})
                            buffer = ""
                            contador = 1
                            Chashtags += 1
                            continue
    return jsonify(hashtags)

@app.route('/consultarMenc', methods=['GET'])
def consultarMenc():
    global fecha
    global texto
    global Cmenciones
    global menciones

    fechaHAS = request.args.get('fecha')
    menciones = []
    buffer = ""
    state = 0
    Cmenciones = 0
    contador = 1
    
    for i in range(len(fecha)):
        if fecha[i].get('fecha') == fechaHAS:
            for c in texto[i].get('texto'):
                if state == 0:
                    if c == "@":
                        buffer += c
                        state = 1
                        Cmenciones += 1
                        continue
                if state == 1:
                    if c != " ":
                        buffer += c
                        continue
                    else:
                        buffer += c
                        state = 0
                        if menciones:
                            for i in range(len(menciones)):
                                if menciones[i].get('Arroba') == buffer:
                                    if buffer == "":
                                        continue
                                    else:
                                        contador = int(menciones[i].get('cantidad'))
                                        contador += 1
                                        menciones[i] = {'menciones': buffer, 'cantidad': contador}
                                        buffer = ""
                                        contador = 1
                                        continue
                        if buffer == "":
                            continue
                        else:
                            menciones.append({'Menciones': buffer, 'cantidad': contador})
                            buffer = ""
                            contador = 1
                            continue
    return jsonify(menciones)

@app.route('/consultarSentimientos', methods=['GET'])
def consultarSentimientos():
    global fecha
    global texto
    global positivos
    global negativos
    fechaHAS = request.args.get('fecha')
    datos = []
    consp = 0
    palabra = ""

    for i in range(len(fecha)):
        if fecha[i].get('fecha') == fechaHAS:
            datos.append(texto[i].get('texto'))
            for c in texto[i].get('texto'):
                if c != " ":
                    if c == ",":
                        c = ""
                    palabra += c
                else:
                    #print(palabra)
                    for i in range(len(positivos)):
                        if palabra == positivos[i]:
                            consp += 1
                            print(palabra)
                    palabra = ""
    return jsonify(datos)

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

@app.route('/escribirxml', methods=['POST'])
def escritura_xml():
    global fecha
    global texto
    global Chashtags
    global Cmenciones
    global fechaHAS
    contador = 0

    mens_recibidos = ET.Element("MENSAJES_RECIBIDOS")
    Rtiempo = ET.SubElement(mens_recibidos, "TIEMPO")
    for i in range(len(fecha)):
        if fechaHAS == fecha[i].get('fecha'):
            contador += 1
    lista_fecha = ET.SubElement(Rtiempo, "FECHA")
    lista_fecha.text = str(fechaHAS)
    lista_mensajes = ET.SubElement(Rtiempo, "MSJ_RECIBIDOS")
    lista_mensajes.text = str(contador)
    lista_menciones = ET.SubElement(Rtiempo, "USR_MENCIONADOS")
    lista_menciones.text = str(Cmenciones)
    lista_hashtag = ET.SubElement(Rtiempo, "HASH_INCLUIDOS")
    lista_hashtag.text = str(Chashtags)

    #General xml
    my_data = ET.tostring(mens_recibidos)
    my_data = str(my_data)
    pretty(mens_recibidos)
    arbol_xml = ET.ElementTree(mens_recibidos)
    arbol_xml.write('resumenMensajes.xml', encoding="UTF-8", xml_declaration=True)


def pretty(element, indent = '    '):
        cola = [(0, element)]
        while cola:
            level, element = cola.pop(0)
            hijos = [(level + 1, hijo) for hijo in list(element)]
            if hijos:
                element.text = '\n' + indent * (level + 1)
            if cola:
                element.tail = '\n' + indent * cola[0][0]
            else:
                element.tail = '\n' + indent * (level - 1)
            cola[0:0] = hijos

@app.route('/grafica', methods=['GET'])
def grafica():
    global fechaHAS
    global menciones
    global hashtags
    f = open('bb.dot', 'w')

    text = """
        digraph G {fontname="Helvetica,Arial,sans-serif"
        node [fontname="Helvetica,Arial,sans-serif"]
        edge [fontname="Helvetica,Arial,sans-serif"]
        a0 [shape=none label=<
        <TABLE border="0" cellspacing="10" cellpadding="10" style="rounded" bgcolor="#9fdbe6:#7678bc" gradientangle="315">\n"""

    text += """<TR>\n"""
    text += """<TD bgcolor="#ca8bf5:#3e4160">Consultar hashtags</TD>"""
    text += """<TD bgcolor="#ca8bf5:#3e4160">"""+ str("Fecha: " + fechaHAS)+"""</TD>\n"""
    for i in range(len(hashtags)):
        text += """<TD bgcolor="#ca8bf5:#3e4160">"""+ str(hashtags[i])+"""</TD>\n"""
    text += """</TR>\n"""
    text += """<TR>\n"""

    text += """<TD bgcolor="#ca8bf5:#3e4160">Consultar menciones</TD>"""
    text += """<TD bgcolor="#ca8bf5:#3e4160">"""+ str("Fecha: " + fechaHAS)+"""</TD>\n"""
    for i in range(len(menciones)):
        text += """<TD bgcolor="#ca8bf5:#3e4160">"""+ str(menciones[i])+"""</TD>\n"""
    text += """</TR>\n"""
    text += """</TABLE>>];
                }\n"""
    f.write(text) 
    f.close()
    os.environ["PATH"] += os.pathsep + 'C:\Program Files\Graphviz\bin'
    #os.system('dot -Tpng bb.dot -o partedjango\myapp\static\grafo.png')      
    os.system('dot -Tpng bb.dot -o grafo.png') 


if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)
