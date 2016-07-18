# -*- coding: utf-8 -*-
import math
from iris import iris_data
import stopwords
import copy
from main import *

def entropy(data):
    # data é algo como: [2/9 , 3/9 , 4/9] .. 9 pois 2+3+4 = 9
    e = 0
    for i in data:
        if i != 0:
            e += -i*math.log(i,len(data))
    return e

def info(data):
    # data é algo como: [2 , 3 , 4]
    s = float(sum(data))
    if s == 0:
        return 0
    return entropy([i/s for i in data])

def avg_info(data):
    # data é algo com: [[2, 3 ], [4, 0 ], [3, 2 ]]
    l = len(data)
    sums = [sum(d) for d in data]
    total_sum = float(sum(sums))
    info_data = []
    information = 0
    i = 0
    while i < l:
        info_data.append(info(data[i]))
        information += (sums[i]/total_sum)*info_data[i]
        i += 1
    return information


class DecisionTree:
    def __init__(self, data, class_index = -1):
        self.data = data
        self.class_index = 0
        if class_index == -1:
            self.class_index = len(data[1]) - 1
        else:
            self.class_index = class_index
        self.classes = set()
        for i in self.data:
            self.classes.add(i[self.class_index])

        distribuition = {i:0 for i in self.classes}
        for i in self.data:
            distribuition[i[self.class_index]] += 1
        dist_list = [distribuition[i] for i in distribuition]
        self.initial_info = info(dist_list)
        self.current_info = self.initial_info
        self.root = 0
        self.remaining_attr = [i for i in range(len(self.data[1])) if i != self.class_index]
        self.data_per_attr = {'root':range(len(data))}
        self.tree = dict() #ISSO É UM DICIONARIO DE DICIONARIOS # { 0:{false:3, true:2, info:[0.31, 0.1]},  }
        #CADA ELEMENTO DO DICIONARIO MAIOR È UM NÓ
        #Dependendo do valor que um dado tiver sobre o atributo
        #correspondente ao NÓ, este dado vai ser jogado para
        #um NÓ diferente, que pode ser um NÓ folha.

        print "Dados preparados.\nChame o método train() para construir a árvore de decisão."

    def getInfoFromData(self, data):
        dist = {'ham':0, 'spam':0}
        for i in data:
            dist[self.data[i][-1]] += 1
        dist = [dist[k] for k in dist]
        return info(dist)

    def train(self, subdata=False):

        attr, splited_data, dist = self.choose_attr(subdata)
        if len(self.tree) == 0:  
            self.root = attr

        print attr
        self.remaining_attr.remove(attr)
        self.tree[attr] = dict()

        dist2 = [[k[l] for l in k] for k in dist]

        self.tree[attr]['info'] = avg_info(dist2)
        
        if len(splited_data[0]) > 0 and info(dist2[0]) > 0.4:
            child = self.train(splited_data[0])
            self.tree[attr][False] = child
            self.tree[child]['parent'] = attr
        else:
            self.tree[attr][False] = dist[0]

        if len(splited_data[1]) > 0 and info(dist2[1]) > 0.4:
            child = self.train(splited_data[1])
            self.tree[attr][True] = child
            self.tree[child]['parent'] = attr
        else:
            self.tree[attr][True] = dist[1]

        return attr
    '''
        qtd_list = [0 for i in classes]
        i = 0
        l = len(data)
        while i < l:
            qtd_list[classes.index(data[i][-1])] += 1
            i += 1

        initial_info = info(qtd_list)
        qtd_attr = len(data[0]) - 1
        min_v = [data[0][j] for j in range(qtd_attr)]
        max_v = [data[0][j] for j in range(qtd_attr)]

        for i in data:
            j = 0
            while j < qtd_attr:
                if min_v[j] > i[j]:
                    min_v[j] = i[j]
                if max_v[j] < i[j]:
                    max_v[j] = i[j]
                j += 1
        medio_v = [(min_v[i] + max_v[i])/2.0 for i in range(qtd_attr)]
        print medio_v
    '''

    def choose_attr(self, subdata=False):
        if not subdata:
            subdata = range(len(self.data))

        prev_info = self.getInfoFromData(subdata)

        i = 0
        lim = len(self.data[0])

        maior_ganho = 0
        maior_ganho_index = 0
        maior_dist = []
        while i < lim:
            if i != self.class_index and i in self.remaining_attr:
                dist = self.split_data_t_attr(subdata, i, 'bool', 'dist')

                dist2 = [[k[l] for l in k] for k in dist]

                i_ganho =  prev_info - avg_info(dist2)
                if i_ganho > maior_ganho:
                    maior_ganho = i_ganho
                    maior_ganho_index = i
                    maior_dist = dist
            i += 1
        splited_data = self.split_data_t_attr(subdata, maior_ganho_index, 'bool', 'data')
        return maior_ganho_index, splited_data, maior_dist


    def split_data_t_attr(self, data, attr_index, attr_type, r):
        # dividir os dados atraves de um atributo
        # pega todos os dados e depedendo do valor
        # de um dado I no atributo J, o dado I vai
        # para uma caixinha diferente.
        # Esse método retorna as caixinhas
        # ou (dependendo do valor do argumento r)
        # retorna a distribuição das CLASSES nas caixinhas

        #data é uma lista de indices, que vão servir como
        #referência para os dados em self.data

        if attr_type == 'bool':
            data_f = [] #Guarda apenas os indices para os dados
            data_t = [] # ^^^
            distribution_t = {'ham':0, 'spam':0}
            distribution_f = {'ham':0, 'spam':0}

            i = 0
            while i < len(data):
                line = self.data[data[i]]
                if line[attr_index] == True:
                    data_t.append(data[i])
                    if distribution_t.has_key(line[self.class_index]):
                        distribution_t[line[self.class_index]] += 1
                    else:
                        distribution_t[line[self.class_index]] = 0
                else:
                    data_f.append(data[i])
                    if distribution_f.has_key(line[self.class_index]):
                        distribution_f[line[self.class_index]] += 1
                    else:
                        distribution_f[line[self.class_index]] = 0

                i += 1

            if r == 'data':
                return [data_f, data_t]
            else:
                return [distribution_f, distribution_t]

    def classificar(self, msg):
        next_attr = self.tree[self.root][msg[self.root]]
        while type(next_attr) == int:
            next_attr = self.tree[next_attr][msg[next_attr]]    
        if next_attr['ham'] > next_attr['spam']:
            return 'ham'
        else:
            return 'spam'

    def teste(self, dados_de_teste):
        positivos = 0
        negativos = 0
        falso_positivos = 0
        falso_negativos = 0

        qtd = len(dados_de_teste)
        count = 0

        for i in dados_de_teste:
            classe = self.classificar(i)
            if i[-1] == classe:
                if i[-1] == 'ham':
                    positivos += 1
                else:
                    negativos += 1
            else:
                if i[-1] == 'ham':
                    falso_negativos += 1
                else:
                    falso_positivos += 1

            count += 1
            if count % 6 == 0:
                print str((count*100)/qtd) + "%"
        matriz_confusao = [[positivos, falso_positivos], [falso_negativos, negativos]]
        precisao_h = float(positivos)/(positivos + falso_positivos)
        cobertura_h = float(positivos)/(positivos + falso_negativos)
        f_score_h = 2*(precisao_h*cobertura_h)/(precisao_h + cobertura_h)

        precisao_s = float(negativos)/(negativos + falso_negativos)
        cobertura_s = float(negativos)/(negativos + falso_positivos)
        f_score_s = 2*(precisao_s*cobertura_s)/(precisao_s + cobertura_s)
        return matriz_confusao, precisao_h, cobertura_h, f_score_h, precisao_s, cobertura_s, f_score_s


            
