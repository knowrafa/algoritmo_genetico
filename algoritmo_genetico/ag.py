from itertools import chain
from math import pow, sin, cos, sqrt
from random import randint, getrandbits, random


class AlgoritmoGenetico:
    populacao = []
    valor_minimo = -100
    valor_maximo = 100
    tamanho_populacao = 100
    geracoes = 40
    populacoes = {
        '0': {

        }
    }

    # Objetivo: f6(0, 0) -> 1
    @staticmethod
    def f6(x, y):
        """
        Função de avaliação F6
        :param x: cromossomo x
        :param y: cromossomo y
        :return: avaliação dos cromossomos
        """
        calc = (pow((sin(sqrt(pow(x, 2) + pow(y, 2)))), 2) - 0.5
                ) / pow((1.0 + 0.001 * (pow(x, 2) + pow(y, 2))), 2)

        return float(format(0.5 - calc, ".5f"))

    def gerar_populacao_inicial(self, size=tamanho_populacao):
        """
        Gera a população inicial
        :param size: tamanho da população gerada
        :return: população inicial
        """
        acumulado = 0.0
        for pos in range(0, size):
            individuo = format(getrandbits(44), '044b')
            self.populacao.append(format(individuo))
            x_bin = individuo[0:22]
            y_bin = individuo[22:44]

            x10 = int(x_bin, 2)
            y10 = int(y_bin, 2)

            x = x10 * (200 / (pow(2, 22) - 1)) + self.valor_minimo
            y = y10 * (200 / (pow(2, 22) - 1)) + self.valor_minimo

            aptidao = self.f6(x, y)
            acumulado += aptidao
            acumulado = float(format(acumulado, ".5f"))

            self.populacoes['0'][str(pos)] = {
                'individuo': individuo,
                'aptidao': aptidao,
                'acumulado': acumulado
            }

        aptidoes = []
        for i in range(0, size):
            aptidoes.append(self.populacoes['0'][str(i)]['aptidao'])

        self.populacoes['0']['mais_apto'] = max(aptidoes)
        self.populacoes['0']['ultimo_acumulado'] = acumulado

        return self.populacao

    def selecao(self, geracao):
        genitores = {}
        while len(genitores) < int(self.tamanho_populacao/2):
            numero_aleatorio = float(format(random() * self.populacoes[geracao].get('ultimo_acumulado'), '.5f'))
            for chave, populacao in self.populacoes.get(geracao).items():
                if numero_aleatorio <= populacao.get('acumulado'):
                    if not genitores.get(chave):
                        genitores[chave] = populacao
                    break
        pass
    def crossover(self):
        pass

    def mutacao(self):
        pass

    def gerar_nova_populacao(self, geracao=1, size=tamanho_populacao):
        for pos in range(0, size):
            # Recebe o indivíduo da última população
            individuo = self.populacoes[str(geracao - 1)][str(pos)].get('individuo')

            self.selecao(str(geracao - 1))

            # self.populacoes['0'][str(pos)] = {
            #     'individuo': individuo,
            #     # 'aptidao': self.f6(x, y)
            # }


ag = AlgoritmoGenetico()
populacao = ag.gerar_populacao_inicial()

for geracao in range(1, ag.geracoes):
    mais_apto = ag.populacoes[str(geracao - 1)].get('mais_apto')
    if mais_apto == 1.00:
        print(f"Solucão encontrada na {geracao - 1}a geração")
    else:
        print(f"Mais apto da {geracao - 1}a geração: {mais_apto}")
    ag.gerar_nova_populacao(geracao=geracao, )
