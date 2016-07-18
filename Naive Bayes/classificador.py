# -*- coding: utf-8  -*-

import sys
import baseNaive


def getProb(classe, palavras, base):
	i = 0
	while i < len(base_conhecimento):
		if base_conhecimento[i][0] == 'ham':
			if palavra == base_conhecimento[i][1]:
				return base_conhecimento[i][2]
				break
		else:
			if palavra == base_conhecimento[i][1]:
				return base_conhecimento[i][2]
				break
		i+=1


def main(args):

	arquivo_treinamento = args[0] 
	arq_teste = args[1]
	arquivo_teste = open(arq_teste, 'r')
	# Base de treinamento
	base_conhecimento = baseNaive.main(arquivo_treinamento)

	# Processo de cálculo das probabilidades para os testes 
	linhas =  baseNaive.read_arquivo(arquivo.readlines())

	f_ham = baseNaive.calcularFrequencia('ham', baseNaive.classes)
	f_spam = baseNaive.calcularFrequencia('spam', baseNaive.classes)
	prob_ham = f_ham/(len(classes))
	prob_spam = f_spam/(len(classes))

	#Todas as palavras do arquivo
	palavras_arquivo, palavras_classeHam, palavras_classeSpam = baseNaive.getPalavras(linhas)

	# não stopwords
	nao_stopwordsHam = baseNaive.naoStopwords(palavras_classeHam)
	nao_stopwordsSpam = baseNaive.naoStopwords(palavras_classeSpam)
	nao_stopwords = nao_stopwordsHam + nao_stopwordsSpam
	# Probabilidades de ser ham ou spam
	probabilidades_ham = []
	probabilidades_spam = []
	for palavra in nao_stopwords:
		i = 0
		while i < len(base_conhecimento):
			if base_conhecimento[i][0] == 'ham':
				prob = [('ham',palavra,0)]
				if palavra == base_conhecimento[i][1]:
					prob = [('ham',palavra,(prob_ham * base_conhecimento[i][2] * getProb('spam',palavra, base_conhecimento) * prob_spam))]
				probabilidades_ham.append(prob)
			else:
				prob = [('spam',palavra,0)]
				if palavra == base_conhecimento[i][1]:
					prob = [('spam',palavra,(prob_spam * base_conhecimento[i][2] * getProb('ham',palavra, base_conhecimento) * prob_ham))]
				probabilidades_spam.append(prob)
			i += 1

	isHam = []
	isSpam = []
	falsoHam = []
	falsoSpam

	i = 0
	while i < len(base_conhecimento):
		if base_conhecimento[i][0] == 'ham':
			if base_conhecimento[i][2] >= getProb('spam', base_conhecimento[i][1], base_conhecimento):
				isHpam.append(base_conhecimento[i][1])
			else:
				falsoHam.append(base_conhecimento[i][1])
		else:
			if base_conhecimento[i][2] >= getProb('ham', base_conhecimento[i][1], base_conhecimento):
				isSpam.append(base_conhecimento[i][1])
			else:
				falsoSpam.append(base_conhecimento[i][1])
		i += 1

	positivo = len(isHam)
	falso_positivo = len(falsoHam)

	negativo = len(isSpam)
	falso_negativo = len(falsoSpam)

	matriz_confusao = [[positivo, falso_positivo],[negativo, falso_negativo]]

	#Opcional
	'''probabilidades = probabilidades_ham + probabilidades_spam
	
	for probabilidade in probabilidades:
		print probabilidade '''

	print "Matriz de Confusão: \n"
	print matriz_confusao



if __name__ == '__main__':
	main(sys.argv[1:3])
