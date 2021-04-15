from algoritmo_genetico import AlgoritmoGenetico

ag = AlgoritmoGenetico()
populacao = ag.gerar_populacao_inicial()

for geracao in range(1, ag.GERACOES):
    mais_apto = ag.populacoes[str(geracao - 1)].get('mais_apto')
    print(f"Mais apto da {geracao - 1}a geração: {mais_apto}")
    if mais_apto == 1.00:
        print(f"Solucão encontrada na {geracao - 1}a geração")
        break

    ag.gerar_nova_populacao(geracao=geracao, )
