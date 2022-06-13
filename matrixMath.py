import matrix

def multiply(m1, m2):
    m1 = m1.copy()
    m2 = m2.copy()
    if(m1.columns == m2.rows):
        res = []
        for i in range(m1.rows):
            row = []
            for j in range(m2.columns):
                row.append(getMult(m1, m2, i, j))
            res.append(row)
        return matrix.Matrix(res)
    else:
        raise Exception("The size of the matrix does not match")

def sum(m1, m2):
    m1 = m1.copy()
    m2 = m2.copy()
    if(m1.rows == m2.rows and m1.columns == m2.columns):
        for i in range(m1.rows):
            for j in range(m2.columns):
                m1.mat[i][j] += m2.mat[i][j]
        return m1
    else:
        raise Exception("The size of the matrix does not match")

def rest(m1, m2):
    m1 = m1.copy()
    m2 = m2.copy()
    return sum(m1, cmultiply(m2, -1))
    

def cmultiply(m1, a):
    m1 = m1.copy()
    res = []
    for i in range(m1.rows):
        row = []
        for j in range(m1.columns):
            row.append(m1.mat[i][j]*a)
        res.append(row)
    return matrix.Matrix(res)

def getSubMatrix(m1, r, c):
    m1 = m1.copy()
    res = []
    for i in range(m1.rows):
        if i != r:
            aux = []
            for j in range(m1.columns):
                if j != c:
                    aux.append(m1.mat[i][j])
            res.append(aux)
    return matrix.Matrix(res)
            
def determinant(m):
    m = m.copy()
    if(m.columns == m.rows):
        if(m.columns == 2):
            return m.mat[0][0]*m.mat[1][1] - m.mat[0][1]*m.mat[1][0]
        else:
            res = 0
            for i in range (m.columns):
                res += m.mat[0][i] * determinant(getSubMatrix(m, 0, i)) * (1 if (i%2 == 0) else -1)
                    
                
            return res
    else:
        raise Exception("The matrix is not square")

def getMult(m1, m2, row, col):
    m1 = m1.copy()
    m2 = m2.copy()
    res = 0
    for i in range (m2.rows):
        res += m1.mat[row][i] * m2.mat[i][col]
    return res

def gaussJordanOperation(m, v, r, mult):
    m = m.copy()
    v = v.copy()
    for i in range(m.columns):
        m.mat[r][i] *= mult
    v.mat[r][0] *= mult
    return m, v

def gaussJordanRowSum(m, v, r1, r2, mult):
    m = m.copy()
    v = v.copy()
    for i in range(m.columns):
        m.mat[r1][i] += mult*m.mat[r2][i]
    v.mat[r1][0] += mult * v.mat[r2][0]
        
    return m , v
    
def gaussJordan(m, r):
    m = m.copy()
    r = r.copy()
    if r.columns == 1 and r.rows == m.rows:
        for i in range (m.columns):
            if i > m.columns:
                break
            if(m.mat[i][i] == 0):
                for j in range (r.rows):
                    if(m.mat[j][i] != 0):
                        m,r = gaussJordanRowSum(m, r, i, j, 1)
            if(m.mat[i][i] != 0):
                m,r = gaussJordanOperation(m, r, i, 1/m.mat[i][i])   
            for j in range (r.rows):
                if j != i:
                    m,r = gaussJordanRowSum(m, r, j, i, -m.mat[j][i])
        return m,r              
    else:
        raise Exception("The matrix and the answer matrix do not match")

def replaceColumn(m,r,c):
    m = m.copy()
    r = r.copy()
    mx = []
    for i in range(m.rows):
        mx.append(m.mat[i][:])
    for j in range(r.rows):
        mx[j][c] = r.mat[j][0]
    return matrix.Matrix(mx)

def cramer(m, r):
    m = m.copy()
    r = r.copy()
    if(m.rows == m.columns):
        res = []
        det = determinant(m)
        if det != 0:
            for i in range(m.columns):
                res.append([determinant(replaceColumn(m,r,i))/det])
            return matrix.Matrix(res)
    raise Exception("The linear system does not have a solution using Krammer methode")