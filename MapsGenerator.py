# -*- coding: utf-8-*-
from panda3d.core import * 
from direct.showbase.ShowBase import ShowBase
from direct.task import Task   
from direct.actor import Actor
from direct.interval.IntervalGlobal import *
import math
import sys
from PIL import Image, ImageDraw
import random
import numpy as np
loadPrcFileData("", "window-type none")
    
class HighMap:
    def __init__(self, size, seed):
        self.size = size
        self.seed = 0
        if len(seed) > 0:
            self.seed = int(seed)
        else:
            self.seed = random.randint(10000,99999)
        random.seed(self.seed)
        
        self.hightMapArray = np.ones((self.size+1,self.size+1))
        self.normalMapArray = np.ones((self.size+1, self.size+1, 3))
        
        self.hightMapArray[0, 0] = random.uniform(0,1)
        self.hightMapArray[self.size, 0] = random.uniform(0,1)
        self.hightMapArray[0, self.size] = random.uniform(0,1)
        self.hightMapArray[self.size, self.size] = random.uniform(0,1)
        
        self.makeMap(self.size)
        
        self.hightMap = Image.new( 'RGB', (self.size+1,self.size+1))
        self.hightPixels = self.hightMap.load()
        
        for i in range(self.hightMap.size[0]):    
            for j in range(self.hightMap.size[1]):
                x = 256/(1.5/self.hightMapArray[i,j])
                self.hightPixels[i,j] = (int(x), int(x), int(x))
        self.calculateNormal()
        self.normalMap = Image.new( 'RGB', (self.size+1,self.size+1))
        self.normalPixels = self.normalMap.load()
        for i in range(self.normalMap.size[0]):    
            for j in range(self.normalMap.size[1]):
                x = self.normalMapArray[i][j]
                self.normalPixels[i,j] = (int(x[0]*256), int(x[1]*256), int(x[2]*256))

        
    def makeMap (self, step):
        for x in range(0, self.size, step):
            for y in range(0, self.size, step):
                self.square((x,y), step)
                
        for x in range(0, self.size, step):
            for y in range(0, self.size, step):
                self.diamond((x, y+step/2), step/2)
                self.diamond((x+step/2, y), step/2)
                self.diamond((x+step, y+step/2), step/2)
                self.diamond((x+step/2, y+step), step/2)
                
        if step > 2:      
            self.makeMap(int(step/2))
                
    def square(self, point, step):
        x, y = int(point[0]), int(point[1])
        average = (self.hightMapArray[x][y]+self.hightMapArray[x+step][y]+self.hightMapArray[x][y+step]+self.hightMapArray[x+step][y+step])/4
        coef = step/self.size
        self.hightMapArray[x+int(step/2)][y+int(step/2)] = average + random.uniform(0,1)*coef-coef/2
    
    def diamond(self, point, step):
        x, y = int(point[0]), int(point[1])
        tm = self.checkIfEdge(x, y-step, step)
        dm = self.checkIfEdge(x, y+step, step)
        rm = self.checkIfEdge(x+step, y, step)
        lm = self.checkIfEdge(x-step, y, step)
        average =(self.hightMapArray[tm]+self.hightMapArray[dm]+self.hightMapArray[rm]+self.hightMapArray[lm])/4
        coef = (step*2)/self.size
        self.hightMapArray[x, y] = average + random.uniform(0,1)*coef-coef/2
        
        
    def checkIfEdge(self,x, y, step):
        if x < 0: x = self.size - step
        if x > self.size: x = 0 + step
        if y < 0: y = self.size - step
        if y > self.size: y = 0 + step
        return (int(x),int(y))
    
    def calculateNormal(self):
        for x in range(0, self.size):
            for y in range(0, self.size):
                n1 = self.getNormal((x+1,y, self.hightPixels[x+1,y][0]),(x,y+1, self.hightPixels[x,y+1][0]), (x,y, self.hightPixels[x,y][0]))
                n2 = self.getNormal((x,y+1, self.hightPixels[x,y+1][0]),(x+1,y, self.hightPixels[x+1,y][0]),(x+1,y+1, self.hightPixels[x+1,y+1][0]))

                self.normalMapArray[x,y] += n1
                self.normalMapArray[x+1,y] += n1 + n2
                self.normalMapArray[x,y+1] += n1 + n2
                self.normalMapArray[x+1,y+1] += n2
                
        for x in range(0, self.size):
            for y in range(0, self.size):
                self.normalMapArray[x,y] = self.normalized(self.normalMapArray[x,y])
        
    def getNormal(self, p1, p2, p3):
        a = (p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2])
        b = (p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2])
        c = np.array([a[1]*b[2]-b[1]*a[2], a[2]*b[0]-b[2]*a[0], a[0]*b[1]-b[0]*a[1]])
        return self.normalized(c)
    
    def normalized(self, vect): 
        cLen = math.sqrt(math.pow(vect[0], 2)+math.pow(vect[1], 2)+math.pow(vect[2], 2))
        vect = np.array([vect[0]/cLen, vect[1]/cLen, vect[2]/cLen])
        return vect
