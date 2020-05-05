from cieloApi3 import *
from flask import Flask, jsonify, request, render_template
from random import random

import json

# Configure o ambiente
environment = Environment(sandbox=True)
# Configure seu merchant, para gerar acesse: https://cadastrosandbox.cieloecommerce.cielo.com.br/
merchant = Merchant('aac3c3b7-2597-4ce6-9b48-e960194e20bc', 'MELEUYUQPESUWKXAOXRMDWJXWEEULYSYPIDQPFWB')
# Crie uma instância de Sale informando o ID do pagamento
sale = Sale(random())

app = Flask(__name__)

@app.route("/")
def index_template():
    return render_template("pagamento.html")

@app.route("/form", methods=["PUT", "POST"])
def form():
    print(request)
    numeroDoCartao = request.form["numero"]
    nomeDoComprador = request.form['nome']
    cvv = request.form['cvv']
    parcelas = request.form['parcelas']
    mes = request.form['mes']
    ano = request.form['ano']
    valor = request.form['valor']
    
    sale.customer = Customer(nomeDoComprador)
    credit_card = CreditCard(cvv, 'Visa')
    credit_card.expiration_date = mes+'/'+ano
    credit_card.card_number = numeroDoCartao
    credit_card.holder = nomeDoComprador
    sale.payment = Payment(valor)
    sale.payment.credit_card = credit_card
    cielo_ecommerce = CieloEcommerce(merchant, environment)
    response_create_sale = cielo_ecommerce.create_sale(sale)
    print ('----------------------response_create_sale----------------------')
    print (json.dumps(response_create_sale, indent=2))
    print ('----------------------response_create_sale----------------------')
    payment_id = sale.payment.payment_id

    return render_template("resultado.html", mensagem=response_create_sale["Payment"]["ReturnMessage"])
   

if __name__ == "__main__":
    app.run(port = 8080, debug = True)

