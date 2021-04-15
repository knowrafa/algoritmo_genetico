from itertools import chain
from math import pow, sin, cos, sqrt
from random import randint, getrandbits, random, seed


class AlgoritmoGenetico:
    # Constantes que podem ser alteradas
    TAMANHO_POPULACAO = 100
    GERACOES = 100
    TAXA_CROSSOVER = 0.65
    TAXA_MUTACAO = 0.08
    MAIS_ADAPTADOS = 10

    populacao = []
    populacoes = {}
    valor_minimo = -100
    valor_maximo = 100

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
        # return 0.5 - calc

    def gerar_populacao_inicial(self, size=TAMANHO_POPULACAO):
        """
        Gera a população inicial
        :param size: tamanho da população gerada
        :return: população inicial
        """
        acumulado = 0.0
        self.populacoes['0'] = {}
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
            # acumulado = float(format(acumulado, ".5f"))

            self.populacoes['0'][str(pos)] = {
                'individuo': individuo,
                'aptidao': aptidao,
                'acumulado': acumulado
            }

        aptidoes = {}
        aptidoes_f6 = []
        for i in range(0, size):
            aptidao = self.populacoes['0'][str(i)]['aptidao']
            aptidoes[str(i)] = {
                'posicao': i,
                'aptidao': aptidao
            }
            aptidoes_f6.append(aptidao)
        maior_aptidao = max(aptidoes_f6)
        self.populacoes['0']['mais_aptos'] = {}
        for i in range(0, self.MAIS_ADAPTADOS):
            mais_apto = max(aptidoes_f6)
            index = aptidoes_f6.index(mais_apto)
            aptidoes_f6[index] = -1
            self.populacoes['0']['mais_aptos'][str(index)] = self.populacoes['0'][str(index)]

        self.populacoes['0']['mais_apto'] = maior_aptidao
        self.populacoes['0']['ultimo_acumulado'] = acumulado

        return self.populacoes.get('0')

    def selecao_roleta(self, geracao):
        genitores = self.populacoes[geracao]['mais_aptos'].copy()
        while len(genitores) < int(self.TAMANHO_POPULACAO / 2):
            numero_aleatorio = random() * self.populacoes[geracao].get('ultimo_acumulado')
            for chave, populacao in self.populacoes.get(geracao).items():
                if numero_aleatorio <= populacao.get('acumulado'):
                    if not genitores.get(chave):
                        genitores[chave] = populacao.copy()
                    break

        return genitores

    def gerar_nova_populacao(self, geracao=1, size=TAMANHO_POPULACAO):
        genitores = self.selecao_roleta(str(geracao - 1))
        self.populacoes[str(geracao)] = {}

        chaves = []
        for chave in genitores.keys():
            chaves.append(chave)

        populacao_atual = 0
        acumulado = 0.0
        while populacao_atual < self.TAMANHO_POPULACAO:
            n1 = chaves[randint(0, len(genitores) - 1)]
            g1 = genitores.get(n1)
            n2 = chaves[randint(0, len(genitores) - 1)]
            g2 = genitores.get(n2)

            taxa_crossover = random()
            if taxa_crossover >= self.TAXA_CROSSOVER:
                # Aplica o Crossover e
                ponto_de_corte = randint(0, 44)
                d1 = g1.get('individuo')[0:ponto_de_corte] + g2.get('individuo')[ponto_de_corte:44]
                d2 = g2.get('individuo')[0:ponto_de_corte] + g1.get('individuo')[ponto_de_corte:44]
            else:
                d1 = g1.get('individuo')
                d2 = g2.get('individuo')

            for d in [d1, d2]:
                individuo = ''
                for i in range(0, 44):
                    numero_aleatorio = random()
                    if numero_aleatorio < self.TAXA_MUTACAO:
                        individuo += '0' if d[i] == 1 else '1'
                    else:
                        individuo += d[i]
                x_bin = individuo[0:22]
                y_bin = individuo[22:44]

                x10 = int(x_bin, 2)
                y10 = int(y_bin, 2)

                x = x10 * (200 / (pow(2, 22) - 1)) + self.valor_minimo
                y = y10 * (200 / (pow(2, 22) - 1)) + self.valor_minimo

                aptidao = self.f6(x, y)
                acumulado += aptidao
                acumulado = float(format(acumulado, ".5f"))

                self.populacoes[str(geracao)][str(populacao_atual)] = {
                    'individuo': individuo,
                    'aptidao': aptidao,
                    'acumulado': acumulado
                }
                populacao_atual += 1

        aptidoes = []
        for i in range(0, size):
            aptidoes.append(self.populacoes[str(geracao)][str(i)]['aptidao'])

        aptidoes = {}
        aptidoes_f6 = []
        for i in range(0, size):
            aptidao = self.populacoes[str(geracao)][str(i)]['aptidao']
            aptidoes[str(i)] = {
                'posicao': i,
                'aptidao': aptidao
            }
            aptidoes_f6.append(aptidao)

        self.populacoes[str(geracao)]['mais_aptos'] = {}
        maior_aptidao = max(aptidoes_f6)
        for i in range(0, self.MAIS_ADAPTADOS):
            mais_apto = max(aptidoes_f6)
            index = aptidoes_f6.index(mais_apto)
            aptidoes_f6[index] = -1
            self.populacoes[str(geracao)]['mais_aptos'][str(index)] = self.populacoes[str(geracao)][str(index)].copy()

        # self.populacoes[str(geracao)]['mais_apto'] = max(aptidoes_f6)
        self.populacoes[str(geracao)]['mais_apto'] = maior_aptidao
        self.populacoes[str(geracao)]['ultimo_acumulado'] = acumulado

        return self.populacoes.get(str(geracao))