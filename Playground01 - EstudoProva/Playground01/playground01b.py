# Neste Playground 01B, vamos trabalhar o MPlayer, além dos dispositivos vistos no Playground 01A.
# Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.


# Como estamos longe do laboratório, usaremos um simulador gráfico para representar os componentes.
# Para controlar o hardware simulado, basta colocar todo o código dentro da função main abaixo.
# Os comandos são os mesmos da teoria, só que dentro da main.
from extra.playground import rodar
import extra1
@rodar
def main():
    
    # Começamos importando as bibliotecas – sim, dentro da função main!
    from mplayer import Player
    
    from gpiozero import LED, Button
    from Adafruit_CharLCD import Adafruit_CharLCD
    from time import sleep
    
    led1 = LED(21)
    led2 = LED(22)
    led3 = LED(23)
    led4 = LED(24)
    led5 = LED(25)
    
    button1 = Button(11)
    button2 = Button(12)
    button3 = Button(13)
    
    lcd = Adafruit_CharLCD(2, 3, 4, 5, 6, 7, 16, 2)
    
    player = Player()
    player.loadlist("playlist.txt")
    player.volume = 30
    
    def pausa_tocar_playlist():
        player.pause()
        if(player.paused):
            led1.blink(on_time = 0.2, off_time = 0.2)
        else:
            led1.on()
    
    def avanca_proxima():
        if(player.speed == 2):
            print("solta botao e seta velocidade")
            player.speed = 1
        else:
            player.pt_step(1)
    
    def volta_faixa():
        if(player.time_pos > 2):
            player.time_pos = 0
        else:
            player.pt_step(-1)
    
    def aumenta_velocidade():
        player.speed = 2
        
    global inicio;
    inicio = 0
    global fim;
    fim = 0
    
    def rolarTexto(tamanhoFaixa):
        if (tamanhoFaixa < 16):
            return;
        
        global inicio;
        global fim;
        
        inicio +=1;
        fim += 1;
            
        if (inicio > tamanhoFaixa):
            inicio = 0;
            fim = 16;
      
    
    button2.when_pressed = pausa_tocar_playlist
    
    button3.when_held = aumenta_velocidade
    button3.when_released = avanca_proxima
    
    button1.when_pressed = volta_faixa

    while True:       
                
        if(player.metadata is not None and player.metadata['Title'] is not None):
            print(player.metadata)
            lcd.clear()
            faixa = player.metadata["Title"]
            lcd.message(str(faixa[inicio:fim]) + '\n')
            lcd.message('%02d:%02d de %02d:%02d' %
                        (player.time_pos / 60, player.time_pos % 60,
                        player.length / 60, player.length % 60))
            rolarTexto(len(faixa));
                      
        sleep(0.5)
    
    
    # Não escreva nenhum código depois do while True!
    # O loop infinito segura o programa, então nada aqui embaixo vai rodar.