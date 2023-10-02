# importação de bibliotecas
from threading import Timer
from gpiozero import LED
from gpiozero import MotionSensor
from time import sleep
from requests import post
from gpiozero import LightSensor
from gpiozero import DistanceSensor
from gpiozero import Button


chave = "ezr-HmmSmFGsNdh5hsrQDg7-6yiVKg2jka7qGvAcP-w"
evento = "Sensores"
endereco = "https://maker.ifttt.com/trigger/" + evento + "/with/key/" + chave

# definição de funções
#Crie um timer recorrente que imprima "olá"a cada 2 segundos.
def imprimir_ola():
 timer = Timer(1.0, imprimir_ola)
 print("Ola")
 timer.start()
 
#Acenda o LED 1 ao detectar um movimento, e apague-o ao 
#detectar a inércia.
# DICA: use when_motion e when_no_motion.
def acender_led1():
    led1.on()

def apagar_led1():
    led1.off()
    global timer
    timer = Timer(4.0, apagar_led2)
    timer.start()   
    
#Acenda o LED 2 ao detectar um movimento e apague-o 
#somente se não houver movimento por 8 segundos.
#↪ DICA: veja o algoritmo do Timer no slide anterior. O LED 2 
#nunca pode estar apagado se o LED 1 estiver aceso.
global timer
timer = None

def acender_led2():
    led2.on()
    acender_led1()
    
    global timer
    print("Acendendo led 2...")
    print(sensor.motion_detected)
    if timer != None:
        timer.cancel()
        timer = None
    
    
def apagar_led2():
    led2.off()

#Crie um applet no site do IFTTT que, ao receber um evento tipo 
#Webhook, acrescente os 2 valores fornecidos em uma linha no 
#documento "Sensores" do Google Docs, no formato "{{Value1}} 
#% de luz / {{Value2}} cm
def editar_doc():
    print("Webhook")
    dados = {"value1": sensor_luz.value * 100, "value2": sensor_dist.distance*100}
    resultado = post(endereco, json=dados)
    print(resultado.text)
 
# criação de componentes
timer = Timer(2,imprimir_ola)
timer.start()

led1 = LED(21)
led2 = LED(22)
sensor = MotionSensor(27)
sensor_luz = LightSensor(8)
sensor_dist = DistanceSensor(trigger=17, echo=18)
botao = Button(11)

sensor.when_motion = acender_led2
sensor.when_no_motion = apagar_led1

botao.when_pressed = editar_doc


# loop infinito
while True:
    sleep(1)