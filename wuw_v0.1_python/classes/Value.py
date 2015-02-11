#coding=utf-8

#共享变量定义

import SizeR
import math
import PointR

class Value:
    NumResamplePoints = 64
    DX = 250.0
    ResampleScale = SizeR.SizeR(DX,DX)
    Diagonal = math.sqrt(DX*DX+DX*DX)
    HalfDiagonal = 0.5 * Diagonal
    ResampleOrigin = PointR.PointR(0,0)
    Phi = 0.5 * (-1 + math.sqrt(5))

    tolerance = 0.75

    WuwWidth = 1000
    WuwHeight = 800

