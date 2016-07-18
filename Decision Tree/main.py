# -*- coding: utf-8 -*-
import sys
import math
import stopwords
import dt

pontuations = [',','.', '~', '^', '´', '`', '[', ']', '-', '_', '=', '+', ';', ':', '(', ')', '{', '}', '/', '?', '!']

def first_comma(s):
    i = 0
    while i < len(s):
        if s[i] == ',':
            break
        i+=1
    return i

def remove_aspas(s):
    i = 0
    s2 = ''
    while i < len(s):
        if s[i] != '"' and s[i] != "'":
            s2 += s[i]
        i += 1
    return s2

def split_things(s):
    kkk = []
    i = 0
    last = 0
    while i < len(s):
        if s[i] in pontuations:
            word = s[last:i]
            if len(word) > 0:
                kkk.append(word.lower())
            last = i + 1
        i += 1
    word = remove_aspas(s[last:i])
    if len(word) > 0:
        kkk.append(word.lower())
    return kkk

def separate_first_comma(s):
    i = first_comma(s)
    return [s[0:i], s[i+1:]]

def process_data1(data):
    #Primeiro processador dos dados
    #pega os dados NÚS: "ham,ashda sjdak\nham,ahdgnbf hnvjadf\nspam,ashdkhasb dja"
    #e transforma em lista de listas: [['ham', 'ashdkja', 'shd'], ['spam', 'asud', 'haksj']]

    d = [separate_first_comma(i) for i in data]
    i = 0
    while i < len(d):
        li = [remove_aspas(k) for k in d[i][1].split()]
        li2 = []
        for k in li:
            li2 += split_things(k)
        li = li2
        d[i][1] = li
        i += 1
    return d

def create_bag_of_words(data):
    #pega os dados vindo do process_data1
    #cria uma lista de palavras contento todas as 
    #palavras que estão nos dados nús e que não são stopwords
    bag = set()
    for i in data:
        for j in i[1]:
            if not j in stopwords.lista and len(j) > 0:
                bag.add(j.lower())
    bag = list(bag)
    bag.sort()
    return bag

def process_data2(data, bag):
    #pega os dados vindo do process_data1
    #cria uma lista de listas
    #cada sublista l: l[0] => "ham" or "spam"
    #cada sublista l: l[i] => 1 se a palavra i existe
    data_final = []
    for i in data:
        line = []
        for j in bag:
            line.append( j.lower() in i[1])
        line.append(i[0])
        data_final.append(line)
    return data_final

def main(arg):
    dataf = open(arg[0])
    data = process_data1(dataf.readlines()[1:])
    bag = create_bag_of_words(data)
    data_final = process_data2(data, bag)

    k = 10
    sg_length = len(data_final)/k
    small_groups = [ data_final[ i*sg_length : (i+1)*sg_length ] for i in range(k)]

    for i in xrange(k):

        dados_de_treino = []
        for j in xrange(k):
            if j != i:
                dados_de_treino += small_groups[j]

        d = dt.DecisionTree(dados_de_treino)
        print "\n###################################\nTeste " + str(i + 1)
        print "Treinando árvore"
        print "escolhendo atributos"
        d.train()
        print "Treino terminado"
        print "\nTestando árvore com "+str(len(small_groups[i])) + " mensagens"

        mc, ph, ch, fh, ps, cs, fs = d.teste(small_groups[i])
        print "matriz de confusão: "
        for i in mc:
            print "    ", i

        print "teste terminado, a seguir, resultados:"
        print "Para Hams:"
        print "----precisão: " + str(ph)
        print "----cobertura: " + str(ch)
        print "----f-score: " + str(fh)
        print "Para Spams:"
        print "----precisão: " + str(ps)
        print "----cobertura: " + str(cs)
        print "----f-score: " + str(fs)
        

if __name__ == "__main__":
    main(sys.argv[1:])