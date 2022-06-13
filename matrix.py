class Matrix:
    mat = []
    rows = 0
    columns = 0

    def __init__(self, r, c):
        self.mat = []
        self.rows = r
        self.columns = c
        for i in range(r):
            aux = []
            for j in range (c):
                aux.append(1 if i == j else 0)
            self.mat.append(aux)

    def __init__(self, mat):
        self.rows = len(mat)
        self.columns = len(mat[0])
        self.mat = []
        for i in range(self.rows):
            self.mat.append(mat[i][:])
        
    def __str__(self):
        str = ""
        for i in range(self.rows):
            for j in range(self.columns):
                str += f"{self.mat[i][j]}\t"
            str += '\n'
        return str
    
    def copy(self):
        return self.__class__(self.mat)