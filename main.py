class Processo:
    def __init__(self, id_proc, nome, prioridade, ciclos, recurso=None):
        self.id_proc = id_proc
        self.nome = nome
        self.prioridade_original = prioridade
        self.prioridade_atual = prioridade
        self.ciclos_necessarios = ciclos
        self.recurso_necessario = recurso
        self.proximo = None