# importação de bibliotecas
from gpiozero import LED, Button
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
from flask import Flask
from gpiozero import MotionSensor
from threading import Timer
from time import sleep
from gpiozero import LightSensor


app = Flask(__name__)
# criação do servidor
global timer
timer = None

# definição de funções das páginas
cliente = MongoClient("localhost", 27017)
banco = cliente["marana"]
colecao = banco["leds"]

# criação dos componentes
leds = [LED(21), LED(22), LED(23), LED(24), LED(25)]
botoes = [Button(11), Button(12), Button(13), Button(14)]

#Controle o LED 1 também de acordo com sensor de 
#movimento: acenda-o quando houver movimento, e 
#apague depois de 10 segundos sem movimento, 
#chamando a função atualiza_led da Implementação.
#↪ DICA: copie e adapte o código dos Testes Iniciais.
def acender_led1():
    global timer
    atualiza_led(1, True)
    if timer != None:
        timer.cancel()
        timer = None



def apagar_led1():
    global timer
    timer = Timer(10.0, apagar_led21)
    timer.start()   

def apagar_led21():
    atualiza_led(1, False)

def apagar_led2():
    atualiza_led(2, False)
    
    
#Controle o LED 2 de acordo com a luz captada: acenda
    #o caso esteja escuro e apague-o caso esteja claro, 
#chamando a função atualiza_led da Implementação.
#↪ DICA: use when_dark / when_light.
def acender_led2():
    atualiza_led(2, True)


#Quando o programa iniciar, busque o dado mais recente 
#no banco e restaure o estado anterior dos LEDs.
#↪ DICA: você pode passar um critério de busca vazio + 
#ordenação para a find_one
def busca_dado():
    busca = {}
    ordenacao = [ ["date", DESCENDING] ]
    documento = colecao.find_one(busca, sort=ordenacao)
    print(documento["estados"])
    
    for led_idx, led_estado in enumerate(documento["estados"]):
        atualiza_led(led_idx+1, led_estado)


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
    
#Crie uma página que verifique e exiba o estado de todos 
#os LEDs, seguindo o formato HTML dos slides 
#anteriores.
#↪ DICA: gere o HTML dentro da função, concatenando 
#strings dentro de um for.
@app.route("/")
def pagina_estado_leds():
    pag = "<html>"
    
    pag = pag + "<ul>"
    for led_idx, led in enumerate(leds):
        if leds[led_idx].is_lit:
            str_led = "acesa"
        else:
            str_led = "apagada"
        pag = pag + "<li>Luz " + str(led_idx+1)+": "+str_led +"</li>"
    
    pag = pag + "</ul></html>"
    
    
    return pag
        

@app.route("/led/<int:led>/<string:estado>")
def mostrar_numero(led, estado):
    if(estado == 'on'):
        estado_novo = True
    else:
        estado_novo = False
    atualiza_led(led, estado_novo)
    return "led " + str(led) + " atualizado para estado " + estado


sensor = MotionSensor(27)
sensor.when_motion = acender_led1
sensor.when_no_motion = apagar_led1

sensor_luz = LightSensor(8)
sensor_luz.when_dark = acender_led2
sensor_luz.when_light = apagar_led2

busca_dado()
pagina_estado_leds()
# rode o servidor
app.run(port=5000, debug=False)

# loop infinito
while True:
    sleep(1)
