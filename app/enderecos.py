import os, dotenv, requests

dotenv.load_dotenv()

def buscar_cep(cep):

    #Token de acesso à API
    token = os.getenv('ACCESS_TOKEN_CEP')

    # Endpoint de CEP
    Base = "https://www.cepaberto.com/api/v3/cep?cep="
    URL = Base+cep

    # Cabeçalho com Token
    headers = {'Authorization': 'Token token=' + token}

    #Resposta da consulta
    resposta = requests.get(URL, headers=headers).json()
    return resposta