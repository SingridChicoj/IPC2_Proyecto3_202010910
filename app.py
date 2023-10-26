from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/upload_file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({
            "message": "No se ha enviado un archivo"
        })
    archivo = request.files['file']
    contenidoarchivo = archivo.read().decode('utf-8')
    print(contenidoarchivo)
    return jsonify({
        "message": "Archivo cargado"
    })

@app.route('/flask_response', methods=['GET'])
def get_response_from_flask():
    response_data={
        "message": "Respuesta desde flask al pedido GET"
    }
    return jsonify(response_data)

@app.route('/flask_response2', methods=['GET'])
def get_response_from_flask2():
    response_data={
        "message": "Otra respuesta desde flask al pedido GET"
    }
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(threaded=True, port=5000, debug=True)