import random
import secrets
import math
from itertools import permutations
import secrets
from numpy import random, char, unique, array, append, insert
from scipy import stats

class Permutation:#класс для генерации подстановок

    def __init__ (self, length):
        self._length = length 
        self.perm = [0]*self._length
        i=0
        while (i<self._length):
            self.perm[i] = i+1
            i=i+1
         
    def inverse (self, j):
        n = self._length-1
        i=0 
        while i<(n-j+1)/2:
            buffer = self.perm[j]
            self.perm[j] = self.perm[n-i]
            self.perm[n-i] = buffer
            j = j+1
            i = i+1


    def generate (self):
        i = self._length - 1
        while self.perm[i]<self.perm[i-1] and i!=0:
            i=i-1
        if i==0:
           return False
        j = self._length - 1
        while self.perm[j]<self.perm[i-1]:
           j=j-1
        buf = self.perm[j]
        self.perm[j] = self.perm[i-1]
        self.perm[i-1] = buf
        self.inverse(i)
        return True


    def print (self):
        print (self.perm)


    def get_perm (self):
        return self.perm

    

class state_table:# класс таблица состояний
    def __init__(self, n, init_state):
        self._n = n
        self._init_state = init_state
        self.table = {}

    def copy (self, obj2):
        self._init_tate = obj2._init_state
        self.table = obj2.table.copy()

    def combine (self, list_of_perm, part_perm):# функция класса формирует из подстановок таблицу состояний
        i=1
        for j in part_perm:
           self.table[i] = list_of_perm[j-1].copy()
           i=i+1

    def get_table(self):
        return self.table

    


    def change_state (self, string):# функция переходов автомата под действием входной последовательности
        res = str(self._init_state)
        state = self._init_state
        for j in string:
            res = res[0:] + str(self.table[state][ord(j)-49])
            state = self.table[state][ord(j)-49]
        return (res)


        

        
class encrypted_authomata:# класс автоматов на подстановках(всех возможных таблиц состояний)
    def __init__ (self, length, state):
        self._length = length 
        self._state = state
        self.list_of_tables = {}

        
    def generate (self):
        list_of_perm = self.form_perm()#формирование списка всех подстановок
        self.form_comb(list_of_perm)#составление из подстановок таблиц переходов
        #for i in self.list_of_tables:
            #print (i,self.list_of_tables[i].table)
        
        
    def form_perm (self):
       a = Permutation (self._length)
       fact = math.factorial(self._length)
       list_of_perm = [0]*fact
       i=0
       list_of_perm[i] = a.get_perm().copy()
       i=i+1
       while (a.generate()):
         list_of_perm[i] = a.get_perm().copy()
         i=i+1
       print (list_of_perm)
       return list_of_perm

    def form_comb(self, list_of_perm):
        number = []
        j=0
        while (j < math.factorial(self._length)):
            number.append(j+1)
            j+=1
        c = state_table(self._length, self._state)
        i=0
        # в цикле создаются всевозможные размещения из |s| по |s|!
        # каждому числу в размещении соответсвует номер определнной подстановки
        for part_perm in permutations(number, self._length):
           c.combine (list_of_perm, part_perm)
           self.list_of_tables[i] = state_table(self._length, self._state)
           self.list_of_tables[i].copy(c)
           i=i+1


    def test_period (self):#функция тестирования последовательности состояний на периодичность
        period=input()
        string = d.periodic_string(period)
        print(string)
        c = state_table(self._length, self._state)
        print ('')
        for i in self.list_of_tables:
            c = self.list_of_tables[i]

            bijection = True
            for j in range(self._length):
                for k in range (1, self._length+1):
                    for t in range(k+1, self._length+1):
                        if c.table[k][j]==c.table[t][j]:
                           bijection=False

            print (c.table)
            if bijection==True: print("биекция")
            output = c.change_state(string)
            print(output)
            self.period(output)

    def test_probability(self):#функция тестирования последовательности состояний на вероятности
        length = int(input())
        probabilities = [float(x) for x in input().split()]
        string = d.prob_string(length, probabilities)

        inp = array([ord(j)-48 for j in string], dtype = int)
        elemnets, frequency = unique(inp, return_counts = True)
        probabilities = frequency/len(inp) 
        print('\n'+ string)
        print(probabilities, '\n')
       

        j=0
        for i in self.list_of_tables:
            c = self.list_of_tables[i]
            print (i, c.table)

            row=[]
            for k in range(0, self._length):
                  elements, frequency = unique([c.table[j][k] for j in c.table], return_counts = True)
                  row.append(frequency.tolist())
                  count=1
                  for j in range(len(elements)):
                      if elements[j]!=j+count:
                         row[len(row)-1].insert(j, 0)
                         count+=1
                  while (j+count!=self._length):
                     row[len(row)-1].append(0)
                     j+=1


            estimateprob=[0]*self._length
            for j in range(self._length):
                for k in range(self._length):
                   estimateprob[j]+=probabilities[k]*(row[k][j]/self._length)
           
            output = c.change_state(string)
            print(output)
            print(estimateprob)
            self.probabilities(output)
            print()

    def test_uniformity (self):#функция тестирования последовательности состояний на равномерность распределения
        length = int(input())
        string = d.true_random_string(length)
        print(string)
        inseq = array([ord(j)-48 for j in string], dtype = int)
        elements, frequency = unique(inseq, return_counts = True)
        print(frequency/len(inseq))
        print(stats.chisquare(frequency))
        for i in self.list_of_tables:
            c = self.list_of_tables[i]
            print(i+1)
            print (c.table)
            output = c.change_state(string)
            print(output)
            self.uniformity(output)



    def period(self, res):
        
        j=0
        flag = False
        while j!=len(res)-1 and flag!=True:#тестируем последовательности с началом во всех позициях
            i=1
            while (i!=len(res) - 1 and flag!=True):#i-длина проверяемой последовтельности
               coincident = 0
               begin = j+i
               end = j+2*i
               while (begin<len(res) and end<len(res)+1 and res[j:j+i]==res[begin:end]):# последовательно проверяем равенство всех частей длины i
                  begin = end
                  end = end+i
                  coincident+=1
               if (begin>=len(res) or end>=len(res)) and coincident>0:#если совпадения проследовали до конца последовательности, считаем период найденным
                 flag = True
                 print (i, j)
               else:
                 i=i+1#иначе увеличиваем длину
            j+=1#иначе увеличиваем позицию старта (длина снова равна 2)        

    def probabilities(self, res):#подсчет вероятностей
        output = array([ord(j)-48 for j in res], dtype = int)
        elements, frequency = unique(output, return_counts = True)
        count=1
        for j in range(len(elements)):
            if elements[j]!=j+count:
                frequency=insert(frequency, j, 0)
                count+=1
        while (j+count!=self._length):
                frequency = append(frequency, 0)
                j+=1
        print(frequency/len(res))


    def uniformity (self, res):#проверка гипотезы равномерности распределения (критерий хи-квадрат)
        output = array([ord(j)-48 for j in res], dtype = int)
        elemnets, frequency = unique(output, return_counts = True)
        print(frequency/len(res))
        print(stats.chisquare(frequency))
        print()

    def prob_string (self, length, probabilities):#формирование строки с заданными веротностными характеристиками
        values = [i for i in range(1, self._length+1)]
        numbers = [i for i in range(self._length+1)]
        discrete = stats.rv_discrete(
        name='some_distribution', 
        values=(values, probabilities))
        distribution = discrete.rvs(size=length)
        #uniform= random.randint(1, self._lenght+1, lenght)
        distribution = char.mod('%d', distribution)
        string = ''
        for j in distribution:
            string +=j 
        return (string)

    def random_string(self, length):
        values = [chr(i+48) for i in range(1, self._length+1)]
        print(values)
        string = ''.join(secrets.choice(values) for i in range(length))
        return(string)

    def periodic_string(self, string):
        result = string*(self._length*len(string)+(self._length-1)*len(string))
        return(result)

    
d = encrypted_authomata(4, 1)
d.generate()
d.test_uniformity()
#d.test(input, 1)















        

