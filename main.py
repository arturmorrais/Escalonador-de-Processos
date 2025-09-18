import os
import time

class Processo:
    def __init__(self, id_proc, nome, prioridade, ciclos, recurso=None):
        self.id_proc = id_proc
        self.nome = nome
        self.prioridade_original = prioridade
        self.prioridade_atual = prioridade
        self.ciclos_necessarios = ciclos
        self.recurso_necessario = recurso
        self.proximo = None

Prioridade_alta = 1
Prioridade_media = 2
Prioridade_baixa = 3

class ListaProcessos:
    def __init__(self):
        self.cabeca = None
        self.cauda = None

    def adicionar_fim(self, processo):
        if self.cabeca is None:
            self.cabeca = processo
            self.cauda = processo
        else:
            self.cauda.proximo = processo
            self.cauda = processo
            processo.proximo = None

    def remover_inicio(self):
        if self.cabeca is None:
            return None
        processo = self.cabeca
        self.cabeca = self.cabeca.proximo
        if self.cabeca is None:
            self.cauda = None
        processo.proximo = None
        return processo

    def esta_vazia(self):
        return self.cabeca is None

    def __repr__(self):
        processos = []
        atual = self.cabeca
        while atual:
            processos.append('P(id={}, prio={}, ciclos={})'.format(atual.id_proc, atual.prioridade_atual, atual.ciclos_necessarios))
            atual = atual.proximo
        return ' -> '.join(processos)

class Scheduler:
    def __init__(self):
        self.lista_alta_prioridade = ListaProcessos()
        self.lista_media_prioridade = ListaProcessos()
        self.lista_baixa_prioridade = ListaProcessos()
        self.lista_bloqueados = ListaProcessos()
        self.contador_ciclos_alta = 0

    def executar_ciclo_de_cpu(self):
        print('\nInício do Ciclo de CPU')
        if not self.lista_bloqueados.esta_vazia():
            processo = self.lista_bloqueados.remover_inicio()
            if processo:
                print('DESBLOQUEADO: Processo ID {} ({}) retornou para a fila de prioridade {}'.format(processo.id_proc, processo.nome, processo.prioridade_original))
                if processo.prioridade_original == Prioridade_alta:
                    self.lista_alta_prioridade.adicionar_fim(processo)
                elif processo.prioridade_original == Prioridade_media:
                    self.lista_media_prioridade.adicionar_fim(processo)
                else:
                    self.lista_baixa_prioridade.adicionar_fim(processo)

        processo_em_execucao = None

        if self.contador_ciclos_alta >= 5:
            if not self.lista_media_prioridade.esta_vazia():
                processo_em_execucao = self.lista_media_prioridade.remover_inicio()
                self.contador_ciclos_alta = 0
                print('Regra de anti-inanição ativada!')
            elif not self.lista_baixa_prioridade.esta_vazia():
                processo_em_execucao = self.lista_baixa_prioridade.remover_inicio()
                self.contador_ciclos_alta = 0
                print('Regra de anti-inanição ativada (nenhum processo médio)!')

        if processo_em_execucao is None:
            if not self.lista_alta_prioridade.esta_vazia():
                processo_em_execucao = self.lista_alta_prioridade.remover_inicio()
                self.contador_ciclos_alta += 1
            elif not self.lista_media_prioridade.esta_vazia():
                processo_em_execucao = self.lista_media_prioridade.remover_inicio()
                self.contador_ciclos_alta = 0
            elif not self.lista_baixa_prioridade.esta_vazia():
                processo_em_execucao = self.lista_baixa_prioridade.remover_inicio()
                self.contador_ciclos_alta = 0

        if processo_em_execucao:
            print('EXECUTANDO: Processo ID {} ({}), prioridade {}. Ciclos restantes: {}'.format(
                processo_em_execucao.id_proc, processo_em_execucao.nome, processo_em_execucao.prioridade_atual, processo_em_execucao.ciclos_necessarios))

            if processo_em_execucao.recurso_necessario == 'DISCO':
                print(
                    'BLOQUEADO: Processo ID {} ({}) precisa de recurso "DISCO".'.format(processo_em_execucao.id_proc, processo_em_execucao.nome))
                processo_em_execucao.recurso_necessario = None
                self.lista_bloqueados.adicionar_fim(processo_em_execucao)
            else:
                processo_em_execucao.ciclos_necessarios -= 1
                if processo_em_execucao.ciclos_necessarios <= 0:
                    print('TERMINADO: Processo ID {} ({}).'.format(processo_em_execucao.id_proc, processo_em_execucao.nome))
                else:
                    if processo_em_execucao.prioridade_atual == Prioridade_alta:
                        self.lista_alta_prioridade.adicionar_fim(processo_em_execucao)
                    elif processo_em_execucao.prioridade_atual == Prioridade_media:
                        self.lista_media_prioridade.adicionar_fim(processo_em_execucao)
                    else:
                        self.lista_baixa_prioridade.adicionar_fim(processo_em_execucao)
        else:
            print('Nenhum processo para executar. Fim da simulação.')

def carregar_processos(caminho_arquivo):
    processos = []
    if not os.path.exists(caminho_arquivo):
        print('Erro: Arquivo "{}" não encontrado.'.format(caminho_arquivo))
        return processos
    
    with open(caminho_arquivo, 'r') as f:
        pass
    return processos

def carregar_processos(caminho_arquivo):
    processos = []
    if not os.path.exists(caminho_arquivo):
        print('Erro: Arquivo "{}" não encontrado.'.format(caminho_arquivo))
        return processos

    with open(caminho_arquivo, 'r') as f:
        for linha in f:
            try:
                partes = linha.strip().split(',')
                if len(partes) < 4:
                    continue
                
                id_proc = int(partes[0])
                nome = partes[1].strip()
                prioridade = int(partes[2])
                ciclos = int(partes[3])
                
                recurso = partes[4].strip().upper() if len(partes) > 4 and partes[4] else None
                if recurso != 'DISCO':
                    recurso = None

                processo = Processo(id_proc, nome, prioridade, ciclos, recurso)
                processos.append(processo)
            except (ValueError, IndexError):
                print('Aviso: Linha inválida no arquivo de processos: "{}"'.format(linha.strip()))
                continue
    return processos

def main():
    caminho_arquivo = 'processos.txt'
    processos_iniciais = carregar_processos(caminho_arquivo)
    if not processos_iniciais:
        return

    scheduler = Scheduler()
    for p in processos_iniciais:
        if p.prioridade_atual == Prioridade_alta:
            scheduler.lista_alta_prioridade.adicionar_fim(p)
        elif p.prioridade_atual == Prioridade_media:
            scheduler.lista_media_prioridade.adicionar_fim(p)
        else:
            scheduler.lista_baixa_prioridade.adicionar_fim(p)
    
    ciclo = 0
    while True:
        ciclo += 1
        print('\n======== CICLO {} ========'.format(ciclo))
        print('Estado atual das filas:')
        print('  Fila Alta Prioridade: {}'.format(scheduler.lista_alta_prioridade))
        print('  Fila Média Prioridade: {}'.format(scheduler.lista_media_prioridade))
        print('  Fila Baixa Prioridade: {}'.format(scheduler.lista_baixa_prioridade))
        print('  Fila Bloqueados: {}'.format(scheduler.lista_bloqueados))
        print('-' * 20)
        
        if (scheduler.lista_alta_prioridade.esta_vazia() and
                scheduler.lista_media_prioridade.esta_vazia() and
                scheduler.lista_baixa_prioridade.esta_vazia() and
                scheduler.lista_bloqueados.esta_vazia()):
            print('\nTodos os processos foram executados. Fim da simulação.')
            break

        scheduler.executar_ciclo_de_cpu()
        time.sleep(1)

if __name__ == '__main__':
    main()