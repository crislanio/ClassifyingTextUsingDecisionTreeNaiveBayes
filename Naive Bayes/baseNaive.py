# -*- coding: utf-8  -*-

import sys
import stopwords


simbolos = [',','.', '~', '^', '´', '`', '[', ']', '-', '_', '=', '+', ';', ':', '(', ')', '{', '}', '/', '?', '!', '"' ]
classes = ['ham', 'spam']


def retirar_pontuacao(linha):

	for s in simbolos:
		i = 1
		nova = ""
		if s in linha[1]:
			while i < (len(linha)):
				nova += linha[i].replace(s,"")
				i += 1
			linha[1] = nova

	return linha

def retirar_pontuacao_palavra(palavra):
	nova_palavra = ""
	for s in simbolos:
		if s in palavra:
			i = 0
			while i < len(palavra):
				if palavra[i] != s:
					nova_palavra += palavra[i]
				i+=1
	return nova_palavra

def read_arquivo(linhas):
	ln = []
	for l in linhas:
		l = l[0:-1].split(",")
		l = retirar_pontuacao(l)
		ln.append(l)
	j = 0
	while j < len(ln):
		aux = ln[j][1] 
		i = 0
		nova = " "
		while i < (len(aux)):
			nova += aux[i]
			i += 1
		ln[j][1] = nova
		j += 1

	return ln

def getPalavras(linhas):

	classe_ham = []
	classe_spam = []
	palavras = []

	for linha in linhas:
		#pegando as palavras
		aux = linha[1].split(' ')
		#removendo os espaços
		aux.remove('')
		for palavra in aux:
			for s in simbolos:
				if s in palavra:
					palavra = retirar_pontuacao_palavra(palavra)
			# Lista com todas as palavras
			palavras.append(palavra)

			if linha[0] == 'ham':
				classe_ham.append(palavra)

			if linha[0] == 'spam':
				classe_spam.append(palavra)

	return palavras, classe_ham, classe_spam



def getPalavrasDistintas(lista_palavras):
	distintas = []
	naoDist = []
	i = 0
	while i < len(lista_palavras):
		if not lista_palavras[i] in lista_palavras[(i+1):]:
			distintas.append(lista_palavras[i])
		else:
			naoDist.append(lista_palavras[i])
		i += 1

	for p in distintas:
		if p in naoDist:
			distintas.remove(p)

	return distintas

# Retorna uma lista das palavras que não estão no stopwords
def naoStopwords(lista_palavras):
	for palavra in lista_palavras:
		if palavra in stopwords.lista:
			lista_palavras.remove(palavra)

	return lista_palavras

# Retorna a frequencia da palavra na lista
def calcularFrequencia(palavra, lista_palavras):
	cont = 0
	for word in lista_palavras:
		if word == palavra:
			cont += 1
	return cont

def getProbClasse(palavra, listaProbabilidades):
	probabilidade = 0
	i = 0
	while i < len(listaProbabilidades):
		if listaProbabilidades[i][0] == palavra:
			probabilidade = listaProbabilidades[i][1]
			break
		i += 1 
	return probabilidade



def classificador(linhas):

	f_ham = calcularFrequencia('ham', classes)
	f_spam = calcularFrequencia('spam', classes)
	prob_ham = f_ham/(len(classes))
	prob_spam = f_spam/(len(classes))

	#Todas as palavras do arquivo
	palavras_arquivo, palavras_classeHam, palavras_classeSpam = getPalavras(linhas)
	lenHam = len(palavras_classeHam)
	lenSpam = len(palavras_classeSpam)

	# não stopwords
	nao_stopwordsHam = naoStopwords(palavras_classeHam)
	nao_stopwordsSpam = naoStopwords(palavras_classeSpam)
	nao_stopwords = nao_stopwordsHam + nao_stopwordsSpam


	# Frequencia das palavras da classe ham
	frequencia_ham = []
	for palavra in palavras_classeHam:
		frequencia_ham.append((palavra,calcularFrequencia(palavra, palavras_classeHam)))
	
	# Frequencia  das palavras da classe spam
	frequencia_spam = []
	for palavra in palavras_classeSpam:
		frequencia_spam.append((palavra,calcularFrequencia(palavra, palavras_classeSpam)))

	#Palavras distintas
	palavras_distintas = getPalavrasDistintas(palavras_arquivo)
	# Probabilidades condicionais
	prob_palavras_ham = [] # probabilidade condicional de palavras da classe Ham = count(w, c)
	tamanho_V = len(palavras_distintas)  # Tamanho do conjunto de palavras do documento
	i = 0
	while i < len(frequencia_ham):
		prob_palavras_ham.append((frequencia_ham[i][0],(frequencia_ham[i][1]+1)/(lenHam + tamanho_V)))
		i += 1

	prob_palavras_spam = [] # probabilidade condicional de palavras da classe Spam = count(w, c)
	j = 0
	while j < len(frequencia_spam):
		prob_palavras_spam.append((frequencia_spam[j][0],(frequencia_spam[j][1]+1)/(lenSpam + tamanho_V)))
		j += 1
	

	#Probabilidades
	probabilidades = []
	for palavra in nao_stopwords:
		if palavra in palavras_classeHam:
			prob = [('ham',palavra, (prob_ham * getProbClasse(palavra,prob_palavras_ham) * getProbClasse(palavra,prob_palavras_spam) * prob_spam))]
		else:
			prob = [('spam',palavra, (prob_spam * getProbClasse(palavra,prob_palavras_spam) * getProbClasse(palavra,prob_palavras_ham) * prob_ham))]
		probabilidades.append(prob)

	return probabilidades
	
'''
P(classe) = Número de ocorrências da classe / Quantidade de classes

count(w, c) = Quantidade de vezes que w aparece em c
count(c) = Quantidade de elementos em c

P(w|c) =	( count(w, c)+1 ) / ( count(c)+ |V | )

|V| = Número de palavras distintas no documento

'''
# Divide o arquivo em dois para poder efetuar o cálculo das probabilidades dos mesmo e escolher as melhores de 
# ambos os arquivos, cria uma lista com elas da seguinte forma, [classe, palavra, probabilidade]

def getProbabilidade(elementoLista):
	return elementoLista[0][2]


def main(args):
	arq = args
	arquivo = open(arq, 'r')
	linhas =  read_arquivo(arquivo.readlines())
	lenLinhas = len(linhas)
	divisor = int(0.70 * lenLinhas)
	treinar_1 = linhas[0:divisor]
	treinar_2 = linhas[divisor:]
	#Base de treinamento 70%
	base_1 = classificador(treinar_1)
	#Base de treinamento 30%
	base_2 = classificador(treinar_2)
	#Ordena as duas bases pela probabilidade de suas palavras
	base_1.sort(key=getProbabilidade)
	base_2.sort(key=getProbabilidade)
	#'Capturar os melhores da duas bases e retornar'
	contMelhorB1 = 0
	contMelhorB2 = 0
	for elem_b1 in base_1:
		for elem_b2 in base_2:
			if getProbabilidade(elem_b1) > getProbabilidade(elem_b2):
				contMelhorB1 += 1
			elif getProbabilidade(elem_b1) == getProbabilidade(elem_b2):
				contMelhorB1 += 1
				contMelhorB2 += 1
			else:
				contMelhorB2 += 1

	# Base de conhecimento para os testes
	base_treinamento = []

	if contMelhorB1 > contMelhorB2:
		base_treinamento = base_1
	elif contMelhorB1 == contMelhorB2:  #pode ser qualquer um
		base_treinamento = contMelhorB1
	else:
		base_treinamento = base_2

	return base_treinamento


	



if __name__ == '__main__':
	main(sys.argv[1:])


