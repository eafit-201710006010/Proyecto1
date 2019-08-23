from flask import Flask, jsonify,request
from flask_cors import CORS
from datetime import datetime
from collections import Counter

app = Flask (__name__)
CORS(app)

tipo_medicion = {'sensor': 'FC28', 'variable': 'Humedad tierra', 'unidades': '%' }
 
mediciones = [
    {'fecha': '2019-08-09 09:10:00', **tipo_medicion , 'valor': 0.19},
    {'fecha': '2019-08-10 08:20:00', **tipo_medicion , 'valor': 0.22},
    {'fecha': '2019-08-11 04:90:00', **tipo_medicion , 'valor': 0.25},
    {'fecha': '2019-08-12 02:40:00', **tipo_medicion , 'valor': 0.25},
    {'fecha': '2019-08-12 01:80:00', **tipo_medicion , 'valor': 0.29}
]

@app.route("/")
def get():
     return tipo_medicion
    
@app.route("/mediciones", methods= ['GET'])
def getAll():
    return jsonify(mediciones)
   
@app.route('/mediciones',methods=['POST'])
def postOne():
    now = datetime.now()
    body = request.json
    body['fecha'] = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    mediciones.append({**body,**tipo_medicion})
    return jsonify(mediciones)

@app.route("/moda")
def getModa(): 
    datos = mediciones
    valores = []
    for i in datos:
        valores.append(i['valor'])

    moda = []
    repeticiones = 0

    for i in valores:
        n = valores.count(i)
        if n > repeticiones:
            repeticiones = n
            moda = i
  
    return jsonify("la moda es:"+ str(moda))


@app.route('/mediciones/<string:fecha>', methods=['DELETE'])
def deleteOne(fecha): 
    x = False
    for medicion in mediciones:
        if (fecha == medicion['fecha'].split(' ')[0]):
            x = True
            mediciones.remove(medicion)
    return 'Eliminado' if x else 'No se encontró'

@app.route('/mediciones/<string:fecha>', methods=['PUT'])
def putOne(fecha): 
    body = request.json
    x = False
    for medicion in mediciones:
        if (fecha in medicion['fecha']):
            x = True
            medicion['valor'] = body['valor']
    return 'Modificado' if x else 'No se encontró'

app.run(port=5000,debug=True)