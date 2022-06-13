import matrix as m
import matrixMath as mMath
import math

def crossProduct(v1, v2):
    if(v1.columns ==1 and v2.columns==1 and v1.rows == 3 and v2.rows == 3):
        i = v1.mat[1][0] * v2.mat[2][0] - v1.mat[2][0] * v2.mat[1][0]
        j = v1.mat[2][0] * v2.mat[0][0] - v1.mat[0][0] * v2.mat[2][0]
        k = v1.mat[0][0] * v2.mat[1][0] - v1.mat[1][0] * v2.mat[0][0]
        return(m.Matrix([[i],[j],[k]]))
    
def dotProduct(v1, v2):
    return v1.mat[0][0] * v2.mat[0][0] + v1.mat[1][0] * v2.mat[1][0] + v1.mat[2][0] * v2.mat[2][0]
    
def magnitude(v):
    return math.sqrt(v.mat[0][0]*v.mat[0][0] + v.mat[1][0]*v.mat[1][0] + v.mat[2][0]* v.mat[2][0])

def normalizeVector(v):
    v = v.copy()
    m = magnitude(v)
    if m!=0:
        v.mat[0][0] /= m
        v.mat[1][0] /= m
        v.mat[2][0] /= m
    return v

def getVector(o, p):
    return mMath.rest(p, o)
