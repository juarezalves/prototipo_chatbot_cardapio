
# coding: utf-8

# In[38]:

from datetime import date

import psycopg2
import json
from sqlite3 import Error
from flask import Flask
from flask import request
from datetime import datetime
from datetime import timedelta

def cria_conexao():
    try:
        connection = psycopg2.connect (user="postgres",
                                   password="rsf159753",
                                   host="127.0.0.1",
                                   port="5432",
                                   database="botweb_1")
        cursor = connection.cursor ()
        return cursor
    except Error as e:
        print(e)
    return None


def lista_cardapio_por_data(cur, data, tipo):
    if tipo == 'almoco':
        cur.execute("SELECT almoco FROM cardapio WHERE data = %s", (data,))
    else:
        cur.execute ("SELECT jantar FROM cardapio WHERE data = %s", (data,))
    rows = cur.fetchall()
    for row in rows:
        return row[0]

def lista_cardapio_por_periodo(cur, data_inicial, data_final, tipo):
    if tipo == 'almoco':
        cur.execute("SELECT dia_semana, almoco FROM cardapio WHERE data BETWEEN %s AND %s", (data_inicial, data_final))
    else:
        cur.execute ("SELECT dia_semana, jantar FROM cardapio WHERE data BETWEEN %s AND %s", (data_inicial, data_final))
    rows = cur.fetchall()
    return str(rows)

def almoco_dia(data):
    tipo = 'almoco'
    db = cria_conexao()
    if data == '':
        data_atual = datetime.now ()
        data = str (data_atual)
    data_str = data[0:10]
    refeicao = lista_cardapio_por_data(db, data_str, tipo)
    if refeicao != None:
        return "Hoje temos " + refeicao
    else:
        return None
    db.close ()

def jantar_dia(data):
    tipo = 'jantar'
    db = cria_conexao()
    if data == '':
        data_atual = datetime.now()
        data = str (data_atual)
    data_str = data[0:10]
    refeicao = lista_cardapio_por_data(db, data_str, tipo)
    if refeicao != None:
        return "Hoje temos " + refeicao
    else:
        return None
    db.close ()

def almoco_dia_seguinte(data):
    tipo = 'almoco'
    db = cria_conexao ()
    data_str = data[0:10]
    refeicao = lista_cardapio_por_data (db, data_str, tipo)
    if refeicao != None:
        return "Amanhã teremos " + refeicao
    else:
        return None
    db.close ()

def jantar_dia_seguinte(data):
    tipo = 'jantar'
    db = cria_conexao ()
    data_str = data[0:10]
    refeicao = lista_cardapio_por_data (db, data_str, tipo)
    if refeicao != None:
        return "Amanhã teremos " + refeicao
    else:
        return None
    db.close ()


def almoco_semanal(data_final):
    tipo = 'almoco'
    db = cria_conexao ()
    data_atual = datetime.now()
    data_inicial = str(data_atual)
    data_inicial = data_inicial[0:10]
    data_final = data_final[0:10]
    refeicoes = lista_cardapio_por_periodo (db, data_inicial, data_final, tipo)
    if refeicoes != None:
        return "Esta semana teremos " + refeicoes
    else:
        return None
    db.close ()

def jantar_semanal(data_final):
    tipo = 'jantar'
    db = cria_conexao ()
    data_atual = datetime.now ()
    data_inicial = str (data_atual)
    data_inicial = data_inicial[0:10]
    data_final = data_final[0:10]
        #extrai_ultimo_dia_semana(data_inicial)
    refeicoes = lista_cardapio_por_periodo (db, data_inicial, data_final, tipo)
    if refeicoes != None:
        return "Esta semana teremos " + refeicoes
    else:
        return None
    db.close ()

def refeicao_dia(data):
    db = cria_conexao ()
    agora = datetime.now()
    if data == '':
        data = str (agora)
        data = data[0:10]

    if agora.hour < 14:
        return almoco_dia(data)
    else:
        return jantar_dia(data)

app = Flask(__name__)

@app.route("/", methods=['POST'])
def main():
    data = request.get_json (silent=True)
    action = data['queryResult']['action']
    resp = ''
    if action == 'almoco_dia':
        resp = almoco_dia(data['queryResult']['parameters']['data'])
    elif action =='almoco_dia_seguinte':
        resp = almoco_dia_seguinte(data['queryResult']['parameters']['data'])
    elif action == 'almoco_semanal':
        resp = almoco_semanal(data['queryResult']['parameters']['data']['endDate'])
    elif action == 'refeicao_dia':
        resp = refeicao_dia(data['queryResult']['parameters']['data'])
    elif action == 'jantar_dia':
        resp = jantar_dia(data['queryResult']['parameters']['data'])
    elif action == 'jantar_dia_seguinte':
        resp = jantar_dia_seguinte(data['queryResult']['parameters']['data'])
    elif action == 'jantar_semanal':
        resp = jantar_semanal(data['queryResult']['parameters']['data']['endDate'])


    if resp == "" or resp == None:
        resposta = {
            "fulfillmentText": "Não há informações de cardápio registradas para esta data ou período."
        }
    else:
        resposta = {
            "fulfillmentText": resp + ". Bom apetite!"
        }
    
    return json.dumps (resposta)

if __name__ == '__main__':
    app.run(debug=True)

