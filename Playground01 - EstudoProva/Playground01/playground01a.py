# Neste Playground 01A, vamos trabalhar com LEDs, botões e LCDs.
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Como estamos longe do laboratório, usaremos um simulador gráfico para representar os componentes.
# Para controlar o hardware simulado, basta colocar todo o código dentro da função main abaixo.
# Os comandos são os mesmos da teoria, só que dentro da main.
from extra.playground import rodar

@rodar
def main():
    
    # Começamos importando as bibliotecas – sim, dentro da função main!
    from gpiozero import LED, Button
    from Adafruit_CharLCD import Adafruit_CharLCD
    from time import sleep
    
        
    # Agora podemos iniciar os componente. Vamos começar com os LEDs.
    # O número de cada um se refere ao pino do Raspberry Pi onde ele está conectado.
    led1 = LED(21)
    led2 = LED(22)
    led3 = LED(23)
    led4 = LED(24)
    led5 = LED(25)
    
    button1 = Button(11)
    button2 = Button(12)
    button3 = Button(13)
    
    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    
    #Testes iniciais: Projeto I: Implementação
    def pisca_led():
        led1.blink(on_time = 1, off_time = 3) 
    
    def muda_estado_led():
        print("toggle led 2")
        led2.toggle()
        
    
    global cont
    cont = 0
    def pisca_led3():
        global cont
        cont += 1
        lcd.clear()
        lcd.message(str(cont))
        led3.blink(n = 3, on_time = 1, off_time = 1)
    
    def controla_led5():
        if(button1.is_pressed and led1.is_lit):
            led5.on()
        else:
            led5.off()
        
    pisca_led()
    
    button1.when_pressed = muda_estado_led
    button3.when_pressed = pisca_led3
    
     
    while True:
        controla_led5()
        sleep(0.5)
        
        
    # Não escreva nenhum código depois do while True!
    # O loop infinito segura o programa, então nada aqui embaixo vai rodar.