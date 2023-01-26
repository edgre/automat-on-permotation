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



class Combinations:

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


a = Permutation(3)
print (a.perm) 
while (a.generate()): print (a.perm)

print ('\n')

b = Combinations (3, 5)
print (b.comb)
while (b.generate()): print (b.comb)








        

