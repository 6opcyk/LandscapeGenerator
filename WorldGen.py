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
import MapsGenerator

loadPrcFileData("", "window-type none")

class WorldGenerator(ShowBase):
    def __init__(self, rend, seed, rough, size):
        self.rend = rend
        self.cam = base.camera
        self.highMap = MapsGenerator.HighMap(size, seed)
        self.size = size
        self.flag = False
        
        array = GeomVertexArrayFormat()
        array.addColumn("vertex", 3, Geom.NTFloat32, Geom.C_point)
        array.addColumn("normal", 3, Geom.NTFloat32, Geom.C_normal)
        array.addColumn("color", 4, Geom.NTFloat32, Geom.C_color)

        format = GeomVertexFormat()
        format.addArray(array)
        format = GeomVertexFormat.registerFormat(format)

        vdata = GeomVertexData('Ground', format, Geom.UHStatic)
        vertex = GeomVertexWriter(vdata, 'vertex')
        normal = GeomVertexWriter(vdata, 'normal')
        color = GeomVertexWriter(vdata, 'color')

        vdata_water = GeomVertexData('Water', format, Geom.UHStatic)
        vertex_water = GeomVertexWriter(vdata_water, 'vertex')
        normal_water = GeomVertexWriter(vdata_water, 'normal')
        color_water = GeomVertexWriter(vdata_water, 'color')

        self.avr = 0
        i = 0
        for x in range(0, self.size):
            for y in range(0, self.size):
                h = self.highMap.hightMapArray[x][y]
                n = self.highMap.normalMapArray[x][y]
                vertex.addData3f(x*10, y*10, h*rough)
                normal.addData3f(n[0], n[1], n[2])
                color.addData4f(0.55, 0.75, 0.28, 1)
                self.avr+=h*rough
                i+=1
        self.avr=self.avr/i
        
        prim = GeomTriangles(Geom.UHStatic)
        for x in range(self.size-1):
            for y in range(self.size-1):
                prim.addVertices((x+1)*self.size+y, y+x*self.size+1, y+x*self.size)
                prim.addVertices(y+x*self.size+1, (x+1)*self.size+y, (x+1)*self.size+y+1)

        for x in range(0, self.size):
            for y in range(0, self.size):
                n = self.highMap.normalMapArray[x][y]
                vertex_water.addData3f(x*10, y*10, self.avr)
                normal_water.addData3f(n[0], n[1], n[2])
                color_water.addData4f(0, 0.5, 0.8, 1)
              
        prim_water = GeomTriangles(Geom.UHStatic)
        for x in range(self.size-1):
            for y in range(self.size-1):
                prim_water.addVertices((x+1)*self.size+y, y+x*self.size+1, y+x*self.size)
                prim_water.addVertices(y+x*self.size+1, (x+1)*self.size+y, (x+1)*self.size+y+1)
                
        geom = Geom(vdata)
        geom.addPrimitive(prim)
        node = GeomNode('gnode')
        node.addGeom(geom)
        ground_obj = rend.attachNewNode(node)

        geom_water = Geom(vdata_water)
        geom_water.addPrimitive(prim_water)
        water_node = GeomNode('wnode')
        water_node.addGeom(geom_water)
        water_obj = rend.attachNewNode(water_node)
        
        dlight = DirectionalLight('my dlight')
        dlnp = rend.attachNewNode(dlight)
        dlnp.setPos(0, 0, 400)
        dlnp.setHpr(0,280,0)
        ground_obj.setLight(dlnp)

        waterLightObj = DirectionalLight('waterLight')
        self.wlnp = rend.attachNewNode(waterLightObj)
        self.wlnp.setPos(0, 0, 400)
        self.wlnp.setHpr(0,280,0)
        water_obj.setLight(self.wlnp)
        
        taskMgr.add(self.waterLight, "waterLight")
        base.disableMouse()
    
        
    def bindToWindow(self, windowHandle, windowSize):
        wp = WindowProperties().getDefault()
        wp.setOrigin(0,0)
        wp.setSize(windowSize.width(), windowSize.height())
        wp.setParentWindow(windowHandle)
        self.win = base.openWindow(props=wp)
        self.wp = wp
        self.cam = base.camList[-1]
        self.cam.reparentTo(self.rend)
        self.cam.setPos(-760.383, -641.568, self.avr+500)
        self.cam.setHpr(-47.682, -26.2394, 0.591088)
        
        
    def waterLight(self, task):
        hpr = self.wlnp.getHpr()
        if self.flag == False:
            self.wlnp.setHpr(0,hpr.y-0.4,0)
            if hpr.y<=250:
                self.flag = True
        else:
            self.wlnp.setHpr(0,hpr.y+0.4,0)
            if hpr.y>290:
                self.flag = False
        return task.cont
    
    @classmethod    
    def initPanda(cls):
        ShowBase()

