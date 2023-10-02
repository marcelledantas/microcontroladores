// Neste playground 06 B, vamos trabalhar com biliotecas para Arduino de terceiros.
// Veja os códigos de exemplo e programe o que está sendo soliticado em LETRAS MAIÚSCULAS.

// A gente começa o código importando as bibliotecas com o #include.
// Se você não tiver instalado as bibliotecas que eu pedi por email, a hora é agora!
#include <GFButton.h>
#include <ShiftDisplay.h>


// Depois dos includes, criamos as variáveis dos componentes.
// Os LEDs ficam como antes.
int led1 = 13;
int led2 = 12;
int led3 = 11;
int led4 = 10;


// Já o botão e o display são criados com o construtor das bibliotecas.
// Lembrando que aqui eu só faço a inicialização básica dos pinos.
// A configuração extra precisa ficar na setup.
GFButton botao1(A1);
GFButton botao2(A2);
GFButton botao3(A3);

ShiftDisplay display(4, 7, 8, COMMON_ANODE, 4, true);

int contBotao3 = 0;
// Só para lembrar, a função setup é executada 1 vez, no começo do programa.

void setup() {

  // Começamos inicializando a Serial.
  Serial.begin(9600);
  
  pinMode(led1, OUTPUT);
  digitalWrite(led1, HIGH);

  // A GFButton é parecida com a Button do Raspberry Pi.
  // Essas linhas são equivalentes ao when_pressed e when_released.
  botao1.setPressHandler(apertouBotao1);
  botao1.setReleaseHandler(soltouBotao1);

  botao2.setPressHandler(apertouBotao2);
  botao2.setReleaseHandler(soltouBotao2);

  botao3.setPressHandler(apertouBotao3);
  //botao3.setReleaseHandler(soltouBotao3);

  // Também posso aproveitar a setup e definir o valor inicial no display.
  
  // COMPILE O PROGRAMA INDO NO MENU Skecth > Exportar Binário Compilado.
  // DEPOIS VÁ NO SIMULIDE E ABRA O ARQUIVO playground06b.simu (sim, é um arquivo diferente do A).
  // RODE A NOVA SIMULAÇÃO CLICANDO NO PRIMEIRO BOTÃO VERMELHO NO TOPO.
  // VEJA O RESULTADO INICIAL NO DISPLAY.
  // DEPOIS ALTERNE A LINHA DESCOMENTADA, COMPILE, RODE E VEJA A DIFERENÇA NO DISPLAY.
  
  //display.set(42);
  //display.set(42, ALIGN_CENTER);
  //display.set(3.142);    // 1 casa decimal
  //display.set(3.142, 2); // 2 casas decimais


  // Vale lembrar que a função .set não é quem vai de fato ligar o display não.
  // Ela só prepara o que vai ser exibido depois.
  // A chamada da .update lá no loop é quem mostra o resultado.
}


// Depois da setup, a função loop fica sendo chamada continuamente.

void loop() {

  // Aqui eu preciso chamar a .process(), para ficar monitorando o botão.
  // Se esquecer de colocar isso, o GFButton não vai funcionar!
  botao1.process();

  botao2.process();
  // O display também precisa de algo aqui, para circular entre os caracteres.
  //display.update();

  botao3.process();

  display.update();

  // Lembre-se que o delay pode atrapalhar esses dois métodos.

  // COMPILE, ATUALIZE O FIRMWARE, ABRA O MONITOR SERIAL E RODE A SIMULAÇÃO PARA VER O BOTÃO EM AÇÃO.
  // EM SEGUIDA, DESCOMENTE A LINHA ABAIXO, RECOMPILE E RODE NOVAMENTE.
  // DEPOIS DE VER O EFEITO NEGATIVO NO BOTÃO E NO DISPLAY, COMENTE A LINHA NOVAMENTE.
  
  //delay(800);
}


// E aqui vem as funções associadas aos botões

void apertouBotao1 (GFButton &botao) {
  Serial.println("Botao 1 pressionado!");
}

void soltouBotao1 (GFButton &botao) {
  Serial.println("Botao 1 solto!");
}

// CRIE UM GFBUTTON PARA O BOTÃO 2 NO PINO A2.
// AO APERTÁ-LO, MOSTRE UM TEXTO NO DISPLAY COM AS INICIAIS DO SEU NOME.
// AO SOLTÁ-LO, COLOQUE UM TEXTO VAZIO NO DISPLAY.
// NÃO ESQUEÇA DE CHAMAR O PROCESS DELE NA LOOP!
void apertouBotao2(GFButton &botao){
  Serial.println("Botao 2 pressionado!");
  display.set("MMD");  
}

void soltouBotao2 (GFButton &botao) {
  Serial.println("Botao 1 solto!");
  display.set("");
}

// CRIE UM GFBUTTON PARA O BOTÃO 3 NO PINO A3.
// APÓS APERTÁ-LO 3 VEZES, ACENDA O LED 1.
// APÓS APERTÁ-LO OUTRAS 3 VEZES, APAGUE O LED 1.
// DICA: USE UMA VARIÁVEL GLOBAL PARA CONTAR.

void apertouBotao3(GFButton &botao){
  Serial.println("Botao 3 pressionado!");
  contBotao3 ++;

  if(contBotao3 == 3){
    digitalWrite(led1, LOW);
  } else if(contBotao3 == 6){
    digitalWrite(led1, HIGH);
  } 
}

