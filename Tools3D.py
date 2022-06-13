import matrixMath as mMath
import matrix as m
import math

X_rotation = []
Y_rotation = []
Z_rotation = []

def calculateRotationMatrix(angle):
    global X_rotation, Y_rotation, Z_rotation
    X_rotation = m.Matrix([
        [1, 0, 0],
        [0, math.cos(angle), -math.sin(angle)],
        [0, math.sin(angle), math.cos(angle)]
    ])
    Y_rotation = m.Matrix([
        [math.cos(angle), 0, -math.sin(angle)],
        [0, 1, 0],
        [math.sin(angle),0, math.cos(angle)]
    ])
    Z_rotation = m.Matrix([
        [math.cos(angle), -math.sin(angle), 0],
        [math.sin(angle), math.cos(angle), 0],
        [0, 0, 1]
    ])

def rotatePoints(points, angle, axis):
    rPoints = []
    calculateRotationMatrix(angle)
    for i in range(len(points)):
        rotatedPoint = points[i].copy()
        if axis[1]:
            rotatedPoint = mMath.multiply(Y_rotation, rotatedPoint)
        if axis[0]:
            rotatedPoint = mMath.multiply(X_rotation, rotatedPoint)
        if axis[2]:
            rotatedPoint = mMath.multiply(Z_rotation, rotatedPoint)
        rPoints.append(rotatedPoint)
    return rPoints

def getZBuffer(faces, points):
    zBuffer = []
    for face in faces:
        p = 0
        for point in face[0]:
            p+=points[point].mat[2][0]
        p/=len(face[0])
        zBuffer.append([p, face])
    zBuffer = sorted(zBuffer, key=lambda x: x[0])
    bufferedFaces = []
    for face in zBuffer:
        bufferedFaces.append(face[1])
    return bufferedFaces