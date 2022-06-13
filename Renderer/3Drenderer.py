import pygame
import sys
from pygame.locals import *
import matrixMath as mMath
import vectorMath as vMath
import matrix as m
import json
import Tools3D as tls

pygame.init()

screen = pygame.display.set_mode((900,750))
pygame.display.set_caption('3D Renderer')

FPS = 30
frames = pygame.time.Clock()

cubePoints = []
cubeEdges = []
cubeFaces = []

pyramidPoints = []
pyramidEdges = []
pyramidFaces = []

testModelPoints = []
testModelEdges = []
testModelFaces = []

ROTATION_AXIS = [True, True, True]
DISTANCE = 2.7

angle = 0

font = pygame.font.SysFont("Arial" , 18 , bold = True)

def fps_counter():
    fps = str(int(frames.get_fps()))
    fps_t = font.render(fps , 1, pygame.Color("WHITE"))
    screen.blit(fps_t,(0,0))

def loadModel(points, file, edges = [], faces = [], loadEdges = False, loadFaces = True, loadCalculations = False):
    with open(file, 'r') as f:
        modelData = json.load(f)
    for i in range(modelData["pointCount"]):
        points.append(m.Matrix([
            [modelData["points"][i]["x"]],
            [-modelData["points"][i]["y"]],
            [modelData["points"][i]["z"]]
        ]))
    if loadEdges:
        for i in range(modelData["edgeCount"]):
            edges.append([
                modelData["edges"][i]["p1"],
                modelData["edges"][i]["p2"] 
            ])

    if loadFaces:
        for i in range(modelData["faceCount"]):
            tmp = []
            tmp.append(modelData["faces"][i]["points"])
            tmp.append(modelData["faces"][i]["color"])
            if loadCalculations:
                tmp.append(m.Matrix(modelData["faces"][i]["normal"]))
                tmp.append(m.Matrix(modelData["faces"][i]["center"]))

            faces.append(tmp)    

def projectPoints(points, calculateRotation = True, rPoints = []):
    Ppoints = []
    SCALE = 500

    if calculateRotation:
        rPoints = tls.rotatePoints(points, angle, ROTATION_AXIS)
    
    for i in range(len(rPoints)): 
        rotatedPoint = rPoints[i]
        
        projection = m.Matrix([[1/(DISTANCE - rotatedPoint.mat[2][0]), 0, 0], [0, 1/(DISTANCE - rotatedPoint.mat[2][0]), 0]])
        projectedPoint = mMath.multiply(projection, rotatedPoint)
        Ppoints.append(mMath.cmultiply(projectedPoint, SCALE))
        
    return Ppoints
        
def drawModelWF(points, edges):
    w, h = pygame.display.get_surface().get_size()
    w = int(w/2)
    h = int(h/2)
    for edge in edges:
        pygame.draw.line(screen, [255,255,255], [points[edge[0]].mat[0][0]+w, points[edge[0]].mat[1][0]+h], [points[edge[1]].mat[0][0]+w, points[edge[1]].mat[1][0]+h])

def drawModelF(points, faces, ogpoints, outline = False, lightning = True, calculateNormal = True):
    orderedFaces = tls.getZBuffer(faces, ogpoints)
    w, h = pygame.display.get_surface().get_size()
    w = int(w/2)
    h = int(h/2)
    for face in orderedFaces:
        facePoints = []
        for point in face[0]:
            facePoints.append((points[point].mat[0][0] + w, points[point].mat[1][0] + h))
        fColor = [face[1][0], face[1][1], face[1][2]]
        if(lightning):
            normal = vMath.crossProduct(vMath.getVector(ogpoints[face[0][1]], ogpoints[face[0][2]]), vMath.getVector(ogpoints[face[0][1]], ogpoints[face[0][0]]))
            normal = vMath.normalizeVector(normal)
            if(calculateNormal):
                lightDirection = vMath.getVector(ogpoints[face[0][1]], m.Matrix([[0],[10],[-10]]))
            else:
                lightDirection = vMath.getVector(mMath.sum(face[3], ogpoints[face[0][0]]), m.Matrix([[0],[10],[-10]]))
            lightDirection = vMath.normalizeVector(lightDirection)
            brightness = max(vMath.dotProduct(normal, lightDirection),0.0)

            fColor[0]*=brightness
            fColor[1]*=brightness
            fColor[2]*=brightness 
            
        pygame.draw.polygon(screen, fColor, facePoints)
        if outline:
            pygame.draw.polygon(screen, [255-fColor[0], 255-fColor[1], 255-fColor[2]], facePoints, 1)
        
def drawModelFWF(points, faces):
    w, h = pygame.display.get_surface().get_size()
    w = int(w/2)
    h = int(h/2)
    for face in faces:
        for i in range(len(face[0])):
            x1 = points[face[0][i]].mat[0][0] + w
            y1 = points[face[0][i]].mat[1][0] + h
            x2 = points[face[0][(i+1)%len(face[0])]].mat[0][0] + w
            y2 = points[face[0][(i+1)%len(face[0])]].mat[1][0] + h
            pygame.draw.line(screen, [255,255,255], [x1, y1], [x2, y2])

loadModel(testModelPoints, "/Models/world.json", faces=testModelFaces, loadFaces=True, loadCalculations=True)

while True:
    pygame.display.update()
    mouse = pygame.mouse.get_pos() 
    pressed_keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill([0,0,0])
    
    angle += 0.03
    #drawModelF(projectPoints(cubePoints), cubeFaces, tls.rotatePoints(cubePoints, angle, ROTATION_AXIS))
    #drawModelFWF(projectPoints(cubePoints), cubeFaces) 
    #drawModelF(projectPoints(pyramidPoints), pyramidFaces, tls.rotatePoints(pyramidPoints, angle, ROTATION_AXIS))      
    #drawModelFWF(projectPoints(pyramidPoints), pyramidFaces) 
    rotatedPoints = tls.rotatePoints(testModelPoints, angle, ROTATION_AXIS)
    drawModelF(projectPoints(testModelPoints, calculateRotation = False, rPoints = rotatedPoints), testModelFaces, rotatedPoints, lightning = True, calculateNormal=False, outline = False)
    #drawModelFWF(projectPoints(testModelPoints), testModelFaces)
         
    
    fps_counter()
    frames.tick(FPS)
