# Projeto: Escalonador com Listas de Prioridade e Prevenção de Inanição
## 1. Descrição do Projeto
Este projeto, parte da disciplina de Algoritmos e Estrutura de Dados I na faculdade ICEV, consiste na implementação de um escalonador de processos para um sistema operacional fictício, o "iCEVOS". O principal objetivo é desenvolver a lógica que decide qual processo deve usar a CPU, gerenciando múltiplos níveis de prioridade e evitando a inanição (starvation) de processos de baixa prioridade.

A implementação de todas as listas de processos foi realizada do zero, manipulando nós e referências/ponteiros diretamente, conforme a Regra Fundamental que proíbe o uso de estruturas de dados prontas.

## 2. Funcionalidades e Regras de Negócio
O escalonador foi implementado seguindo as seguintes regras:

Listas de Prioridade: Os processos são distribuídos em três listas de prioridade: alta (1), média (2) e baixa (3).

Execução Padrão: O escalonador prioriza a execução de processos da lista de alta prioridade. Se esta estiver vazia, ele busca por processos na lista de prioridade média e, em seguida, na lista de baixa prioridade.

Prevenção de Inanição (Anti-Starvation): Após 5 ciclos consecutivos de execução de processos de alta prioridade, o escalonador obrigatoriamente executa um processo de prioridade média. Se não houver, ele tenta executar um de baixa prioridade.

Gerenciamento de Recursos (Bloqueio): Processos que precisam do recurso "DISCO" são movidos para uma lista de bloqueados e não são executados imediatamente.

Desbloqueio: A cada novo ciclo, o processo mais antigo da lista de bloqueados é movido de volta para o final da sua fila de prioridade original.

Ciclos de CPU: A execução de um processo reduz seus ciclos_necessarios em 1. <br>Após a execução, se o processo não tiver terminado, ele retorna ao final de sua lista de prioridade.

## 3. Como Executar o Projeto
Para executar a simulação, siga as instruções abaixo:

Pré-requisitos<br>
Python 3.x instalado.

Arquivo de Entrada<br>
O programa recebe os dados de entrada de um arquivo de texto chamado processos.txt. Este arquivo deve estar na mesma pasta do script e conter os processos no seguinte formato:

id,nome,prioridade,ciclos,recurso(opcional)

Exemplo de processos.txt:

Plaintext

1,Tarefa_A,1,5,<br>
2,Tarefa_B,2,3,<br>
3,Tarefa_C,3,10,<br>
4,Tarefa_D,1,4,DISCO<br>
5,Tarefa_E,1,2,<br>
Execução

Abra o terminal na pasta do projeto e execute o seguinte comando:

Bash

python seu_script.py

A saída da simulação será exibida diretamente no console, mostrando o estado de todas as listas a cada ciclo de CPU e os eventos de execução, bloqueio e término de processos.

## 4. Informações do Projeto
Disciplina:	Algoritmos e Estrutura de Dados I<br>
Professor:	Dimmy Magalhães<br>
Integrante:	Artur Morais Silva - Matrícula 0030616<br>
Repositório: https://github.com/arturmorrais/Escalonador-de-Processos<br>
