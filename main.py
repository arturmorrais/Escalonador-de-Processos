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