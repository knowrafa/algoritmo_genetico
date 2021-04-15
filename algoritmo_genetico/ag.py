from itertools import chain
from math import pow, sin, cos, sqrt
from random import randint, getrandbits


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
    def f6(self, x, y):
        """
        Função de avaliação F6
        :param x: cromossomo x
        :param y: cromossomo y
        :return: avaliação dos cromossomos
        """
        calc = (pow((sin(sqrt(pow(x, 2) + pow(y, 2)))), 2) - 0.5
                ) / pow((1.0 + 0.001 * (pow(x, 2) + pow(y, 2))), 2)

        return 0.5 - calc

    def gerar_populacao_inicial(self, size=tamanho_populacao):
        """
        Gera a população inicial
        :param size: tamanho da população gerada
        :return: população inicial
        """

        for pos in range(0, size):
            individuo = format(getrandbits(44), '044b')
            self.populacao.append(format(individuo))
            x_bin = individuo[0:22]
            y_bin = individuo[22:44]

            x10 = int(x_bin, 2)
            y10 = int(y_bin, 2)

            x = x10 * (200 / (pow(2, 22) - 1)) + self.valor_minimo
            y = y10 * (200 / (pow(2, 22) - 1)) + self.valor_minimo

            self.populacoes['0'][str(pos)] = {
                'individuo': individuo,
                'aptidao': self.f6(x, y)
            }

        aptidoes = []
        for i in range(0, size):
            aptidoes.append(self.populacoes['0'][str(i)]['aptidao'])
        self.populacoes['0']['mais_apto'] = max(aptidoes)

        return self.populacao

    def gerar_nova_populacao(self, geracao=1, size=tamanho_populacao):
        for pos in range(0, size):
            # Recebe o indivíduo da última população
            individuo = self.populacoes[str(geracao-1)][str(pos)].get('individuo')

            self.populacoes['0'][str(pos)] = {
                'individuo': individuo,
                'aptidao': self.f6(x, y)
            }


ag = AlgoritmoGenetico()
populacao = ag.gerar_populacao_inicial()
print(ag.populacoes['0'].get('mais_apto'))

for geracao in range(0, ag.geracoes):
    for i in range(0, ag.tamanho_populacao):
        individuo = populacao[i]
        x_bin = individuo[0:22]
        y_bin = individuo[22:44]

        x10 = int(x_bin, 2)
        y10 = int(y_bin, 2)

        x = x10 * (200 / (pow(2, 22) - 1)) + ag.valor_minimo
        y = y10 * (200 / (pow(2, 22) - 1)) + ag.valor_minimo

        aptidao = ag.f6(x, y)
