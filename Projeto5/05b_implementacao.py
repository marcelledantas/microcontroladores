# importação de bibliotecas
from gpiozero import LED, Button
from pymongo import MongoClient
from datetime import datetime
from flask import Flask
app = Flask(__name__)
# criação do servidor


# definição de funções das páginas
cliente = MongoClient("localhost", 27017)
banco = cliente["marana"]
colecao = banco["leds"]

# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]

def atualiza_led(led_pos, estado):
    if estado == True:
        leds[led_pos - 1].on()
    else:
        leds[led_pos - 1].off()
    
    #data/horário atual + lista com o estado (True/False) de cada LED

    agora = datetime.now()
    estado_led = []
    for led in leds:
        estado_led.append(led.is_lit)
     
    dados = {"date": agora, "estados": estado_led}
    colecao.insert(dados)

@app.route("/led/<int:led>/<string:estado>")
def mostrar_numero(led, estado):
    if(estado == 'on'):
        estado_novo = True
    else:
        estado_novo = False
    atualiza_led(led, estado_novo)
    return "led " + str(led) + " atualizado para estado " + estado


# rode o servidor
app.run(port=5000, debug=False)