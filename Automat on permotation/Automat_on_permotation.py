
import math

class Permutation:

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

    

class Combination:

    def __init__ (self, m, n):
        self._m = m
        self._n = n
        i=0
        self.comb = [0]*m
        while i<m:
            self.comb[i]=i+1
            i=i+1

    def generate (self):
        for i in range (self._m - 1, -1, -1):
            if (self.comb[i] < self._n - self._m + i + 1):
                self.comb[i] = self.comb[i]+1
                for j in range (i, self._m - 1):
                    self.comb[j+1] = self.comb[j]+1
                return True   
        return False

    def print(self):
        print(self.comb)

    def get_comb(self):
        return self.comb



class state_table:
    def __init__(self, n, init_state):
        self._n = n
        self._init_state = init_state
        self.table = {}

    def copy (self, obj2):
        self._init_tate = obj2._init_state
        self.table = obj2.table.copy()

    def combine (self, list_of_perm, combination):
        i=97
        for j in combination.get_comb():
            self.table[chr(i)] = list_of_perm[j-1].copy()
            i=i+1
        print (self.table)

    def get_table(self):
        return self.table

    def change_state (self, string):
        res = str(self._init_state)
        for j in string:
            res = res[0:] + str(self.table[j][self._init_state - 1])
            self._init_state = self.table[j][self._init_state - 1]
        print (res)

       


class encrypted_authomates:
    def __init__ (self, lenght, state):
        self._lenght = lenght 
        self._state = state
        self.list_of_tables = {}

        

    def generate (self):
        list_of_perm = self.form_perm()
        self.form_comb(list_of_perm)
        for i in self.list_of_tables:
            print (i,self.list_of_tables[i].table)
        
        
       
    def form_perm (self):
       a = Permutation (self._lenght)
       fact = math.factorial(self._lenght)
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
        c = state_table(self._lenght, self._state)
        fact = math.factorial(self._lenght)
        b = Combination (self._lenght, fact)
        i=0
        c.combine(list_of_perm, b)
        self.list_of_tables[i] = state_table(self._lenght, self._state)
        self.list_of_tables[i].copy(c)
        i=i+1
        while (b.generate()):
           c.combine (list_of_perm, b)
           self.list_of_tables[i] = state_table(self._lenght, self._state)
           self.list_of_tables[i].copy(c)
           i=i+1

    def test (self, string):
        c = state_table(self._lenght, self._state)
        print ('')
        for i in self.list_of_tables:
            c = self.list_of_tables[i]
            print (c.table)
            c.change_state(string)


d = encrypted_authomates(3, 1)
d.generate()
d.test('bcbc')









        

