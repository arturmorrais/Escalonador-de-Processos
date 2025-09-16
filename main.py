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