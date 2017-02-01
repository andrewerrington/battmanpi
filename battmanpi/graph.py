#!/usr/bin/env python3
"""BattMan Pi graph support"""

#
# Copyright 2007 Capable Computing, Inc. (CCI)
# Copyright 2017 Andrew Errington
#
# This file is part of BattMan Pi.
#
# BattMan Pi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# BattMan Pi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with BattMan Pi.  If not, see <http://www.gnu.org/licenses/>.
#


#/* Copyright (c) 2007, Capable Computing, Inc.
#   Please see "license.txt" file for licensing information. */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "Graph.h"
#include "Main.h"

#define HORIZONTAL_GRID_SIZE 60
#define VERTICAL_GRID_SIZE 50
#define TICK_SIZE 9

HORIZONTAL_GRID_SIZE = 60
VERTICAL_GRID_SIZE = 50
TICK_SIZE = 9

import tkinter.font
import math


def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

class graph:
    
    def __init__(self, yMin0, yMax0, canvas):
        

#Graph::Graph( double yMin0, double yMax0, TImage *image )
#{
#    canvas = image->Canvas;

#    canvas->Brush->Color = clBlack;
#    canvas->Pen->Color = TColor(0x66CC00);

        self.yMin0 = yMin0
        self.yMax0 = yMax0
        self.canvas = canvas
        
        self.font = tkinter.font.Font(size=8, weight='bold')  # Use the default font, size 10
        
        self.color = '#00CC66'
        self.plotcolor = '#00CC66'

#    canvas->Font->Assign(MainForm->Font);
#    canvas->Font->Name = "MS Line Draw";
#    canvas->Font->Color = canvas->Pen->Color;
#    canvas->Font->Style = TFontStyles() << fsBold;

#    xResolution = image->Width;
#    yResolution = image->Height;

        self.xResolution = self.canvas.winfo_reqwidth()
        self.yResolution = self.canvas.winfo_reqheight()

#    xLeft = canvas->TextWidth("99.99") + TICK_SIZE + 2;
#    yTop = 1 + (3 * abs(canvas->Font->Height)) / 2;
#    yBottom = yResolution - 3 * abs(canvas->Font->Height);

        self.xLeft = self.font.measure("99.99") + TICK_SIZE + 2
        self.yTop = 1 + (3 * abs(self.font.metrics("linespace")))
        self.yBottom = self.yResolution - 3 * abs(self.font.metrics("linespace"))


#    ClearArea(1,1,xResolution,yResolution);

        # Clear everything
        for item in self.canvas.find_all():
            self.canvas.delete(item)

#    numPoints = xResolution - xLeft + 1;
#    yList = new double[numPoints];
#    yCountList = new double[numPoints];
#    for( int i = 0; i < numPoints; ++i ) {
#	yList[i] = -1e9;
#	yCountList[i] = 0;
#    }

        self.numPoints = self.xResolution - self.xLeft + 1
        self.yList = [-1e9] * self.numPoints
        self.yCountList = [0] * self.numPoints

#    xStepSize = 60.0 / HORIZONTAL_GRID_SIZE;
#    scaleCount = 1;
#    redraw = 1;

        self.xStepSize = 60.0 / HORIZONTAL_GRID_SIZE
        self.scaleCount = 1
        self.redraw = 1

#    yMin = yMin0;
#    yMax = yMax0;

        self.yMin = yMin0
        self.yMax = yMax0

#    xLabelScale = 1;
#    xLabelOffset = 0;
#    xLabelMod = 0;

        self.xLabelScale = 1
        self.xLabelOffset = 0
        self.xLabelMod = 0


# Destructor.  FIXME do we need this?
#Graph::~Graph( )
#{
#        self.yCountList = []
#        self.yList = []
#}

    def axisLimitsAndSteps(self, min_, max_):
#static double axisLimitsAndSteps( double *min, double *max )
#{
#    double step = (*max - *min) / 7;
#    int iLog = (int) floor(log10(step) * 3 + 0.5);

        step = (max_ - min_) / 7
        iLog = int(math.floor(math.log10(step) * 3 + 0.5))

#    switch( (iLog + 300) % 3 ) {
#        case 0: step = 1; break;
#        case 1: step = 2; break;
#        case 2: step = 5; break;
#    }

        if ((iLog + 300) % 3) == 0:
            step = 1
        elif ((iLog + 300) % 3) == 1:
            step = 2
        elif ((iLog + 300) % 3) == 2:
            step = 5

#    while( iLog > 2 ) {
#	step *= 10;
#	iLog -= 3;
#    }

        while( iLog > 2 ):
            step *= 10
            iLog -= 3

#    while( iLog < 0 ) {
#	step /= 10;
#	iLog += 3;
#    }

        while( iLog < 0 ):
            step /= 10
            iLog += 3

#    *min = floor(*min/step) * step;
#    *max = ceil(*max/step) * step;

        min_ = math.floor(min_/step) * step
        max_ = math.ceil(max_/step) * step

        return (step, min_, max_)


    def Render(self, onlyX):
#void Graph::Render( int onlyX )
#{
#        int i, x, y, xFrom, xTo, xVal;
#        char num[20];
#        double yVal, yStep;

        if (onlyX < 0):
            # Clear graph area
            #self.ClearArea(1, self.yTop, self.xResolution, self.yBottom+TICK_SIZE/2)
            self.canvas.delete('xtick')
            self.canvas.delete('ytick')
            self.canvas.delete('xlabel')
            self.canvas.delete('ylabel')
            self.canvas.delete('xaxis')
            self.canvas.delete('yaxis')
            self.canvas.delete('xgraticule')
            self.canvas.delete('ygraticule')
            self.canvas.delete('plot')

        elif (self.redraw):
            # Clear graph area
            #self.ClearArea(1,self.yTop, self.xResolution, self.yBottom+TICK_SIZE/2)
            self.canvas.delete('xtick')
            self.canvas.delete('ytick')
            self.canvas.delete('xlabel')
            self.canvas.delete('ylabel')
            self.canvas.delete('xaxis')
            self.canvas.delete('yaxis')
            self.canvas.delete('xgraticule')
            self.canvas.delete('ygraticule')
            self.canvas.delete('plot')

            for x in range(self.xLeft, self.xResolution):
                if ((x - self.xLeft) % HORIZONTAL_GRID_SIZE == 0):
                    # Draw x-axis tick
                    self.canvas.create_line(x-1,self.yBottom-TICK_SIZE/2-1,x-1,self.yBottom+TICK_SIZE/2, fill=self.color, tag='xtick')
                    #canvas->MoveTo(x-1,yBottom-TICK_SIZE/2-1)
                    #canvas->LineTo(x-1,yBottom+TICK_SIZE/2)
                    xVal = (x - self.xLeft) * self.xStepSize * self.xLabelScale + self.xLabelOffset + 0.5
                    if self.xLabelMod != 0:
                        xVal %= self.xLabelMod
                    if (xVal % 60 == 0 and self.xLabelScale == 1):
                        num="%d"%(xVal/60)
                    else:
                        num="%d:%02d"%(xVal/60,xVal%60)
                    # Write x label
                    self.canvas.create_text(x, self.yBottom+TICK_SIZE/2, text=num, font=self.font, fill=self.color, anchor = 'n', tag='xlabel')
                    if( x != self.xLeft ):
                        # Draw vertical graticule
                        self.canvas.create_line(x-1, self.yBottom - TICK_SIZE/2 - 2, x-1, self.yTop, dash=(1,1), fill=self.color, tag='xgraticule')
                        #for y in frange(self.yTop, self.yBottom - TICK_SIZE/2 - 2, 2):
                        #    self.canvas.create_line(x-1,y-1,x,y-1, fill='green')
                            #plot canvas->Pixels[x-1][y-1] = canvas->Pen->Color

                else:
                    # Draw one pixel of x-axis FIXME Why?  Moved to outside loop
                    pass
                    #self.canvas.create_line(x-1,self.yBottom-1,x,self.yBottom-1, fill='green')
                    #canvas->Pixels[x-1][yBottom-1] = canvas->Pen->Color
                
            yStep, self.yMin, self.yMax = self.axisLimitsAndSteps(self.yMin, self.yMax)

            for yVal in frange(self.yMin, self.yMax + 0.1 * yStep, yStep):
                y = math.floor(self.yBottom - (yVal - self.yMin) * (self.yBottom - self.yTop) / (self.yMax - self.yMin) + 0.5)
                # Draw y-axis tick
                self.canvas.create_line(self.xLeft-TICK_SIZE/2-1,y-1,self.xLeft+TICK_SIZE/2,y-1, fill=self.color, tag='ytick')
                #canvas->MoveTo(xLeft-TICK_SIZE/2-1,y-1)
                #canvas->LineTo(xLeft+TICK_SIZE/2,y-1)
                num="%5.2f"%yVal
                # Write y-axis label
                self.canvas.create_text(self.xLeft-TICK_SIZE/2-3, y, text=num, font=self.font, fill=self.color, anchor = 'e', tag='ylabel')
                if (yVal != self.yMin):
                    # Draw horizontal graticule
                    self.canvas.create_line(self.xLeft + TICK_SIZE/2, y-1, self.xResolution, y-1, dash=(1,1), fill=self.color, tag='ygraticule')
                        
                    #for x in frange(self.xLeft + TICK_SIZE/2, self.xResolution, 2):
                    #    self.canvas.create_line(x-1,y-1,x,y-1, fill='green')
                        #plot canvas->Pixels[x-1][y-1] = canvas->Pen->Color;
                        
            
            # Draw x-axis
            self.canvas.create_line(self.xLeft-1,self.yBottom-1, self.xResolution,self.yBottom-1, fill=self.color, tag='xaxis')
            # Draw y-axis
            self.canvas.create_line(self.xLeft-1,self.yBottom, self.xLeft-1,self.yTop, fill=self.color, tag='yaxis')
            
            #/*
            #for( y = yBottom; y >= yTop; --y )
            #    canvas->Pixels[xLeft-1][y-1] = canvas->Pen->Color;
            #*/
            xFrom = 0
            xTo = self.numPoints
            self.redraw = 0

        else:
            xFrom = onlyX
            xTo = onlyX + 1

        # Plot data points
        for i in range(xFrom, xTo):
            yVal = self.yList[i]
            if ((yVal >= self.yMin) and (yVal <= self.yMax)):
                self.canvas.create_line(i + self.xLeft - 1, self.yBottom - (yVal - self.yMin) * (self.yBottom - self.yTop) / (self.yMax - self.yMin) - 0.5,
                                        i + self.xLeft, self.yBottom - (yVal - self.yMin) * (self.yBottom - self.yTop) / (self.yMax - self.yMin) - 0.5, tag='plot', fill=self.plotcolor)
                #plot point:
                #canvas->Pixels[i + xLeft - 1][yBottom - (yVal - yMin) * (yBottom - yTop) / (yMax - yMin) - 0.5] =
                #    canvas->Pen->Color;
        
        self.canvas.update()
        #MainForm->Update();


    def AddPoint(self, x, y):
#void Graph::AddPoint( int x, double y )
#{
#    int i;

#    if( x >= 0 ) {
#    while( (i = (int) (x / xStepSize)) >= numPoints )
#        Collapse();

#    if( yCountList[i] <= 0.1 ) {
#        yList[i] = y;
#        yCountList[i] = 1.0;
#    }
#    else {
#        yList[i] = (yList[i] * yCountList[i] + y)
#            / (yCountList[i] + 1.0);
#        yCountList[i] += 1.0;
#    }
#    if( y < yMin ) { yMin = y - (yMax - yMin) / 10; redraw = 1; }
#    if( y > yMax ) { yMax = y + (yMax - yMin) / 10; redraw = 1; }
#    Render(i);
#    }
#}


        if (x >= 0):
            i = int(x/self.xStepSize)
            while (i  >= self.numPoints):
                self.Collapse()
                i = int(x/self.xStepSize)

            if (self.yCountList[i] <= 0.1):
                self.yList[i] = y
                self.yCountList[i] = 1.0
            else:
                self.yList[i] = (self.yList[i] * self.yCountList[i] + y) / (self.yCountList[i] + 1.0)
                self.yCountList[i] += 1.0
                
            if (y < self.yMin):
                self.yMin = y - (self.yMax - self.yMin) / 10
                self.redraw = 1
                
            if (y > self.yMax):
                self.yMax = y + (self.yMax - self.yMin) / 10
                self.redraw = 1

            self.Render(i)


    def redraw(self):
        self.redraw = 1
        self.Render()


    
#void Graph::ClearArea( int x1, int y1, int x2, int y2 )
#{

#void Graph::WriteText( int x, int y, char *s, int leftRight, int aboveBelow )
#{

    def WriteTopLine(self, msg):
        self.canvas.delete('topline')
        self.canvas.create_text(self.xResolution/2, 1, text=msg,\
            font=self.font, fill=self.color, anchor='n', tag='topline')
        self.canvas.update()


    def WriteBottomLine(self, msg):
        self.canvas.delete('bottomline')
        self.canvas.create_text(self.xResolution/2, self.yResolution-4,\
            text=msg, font=self.font, fill=self.color, anchor='s',\
                tag='bottomline')       # FIXME: -4 because of canvas border
        self.canvas.update()


    def Collapse(self):
#void Graph::Collapse( )
#{
#    int i, old, np, i1, i2;
#    double y1, y2, c1, c2;

        old = self.scaleCount
        self.scaleCount +=1
        np = int(old * self.numPoints / self.scaleCount)

        for i in range(0, np):
            i1 = int(self.scaleCount * i / old)
            i2 = int((self.scaleCount * i + 1) / old)
            if (i1 == i2):
                self.yList[i] = self.yList[i1]
                self.yCountList[i] = self.yCountList[i1]
            else:
                y1 = self.yList[i1]
                y2 = self.yList[i2]
                if (y1 <= -1e9):
                    y1 = y2
                elif (y2 <= -1e9):
                    y2 = y1
                c1 = self.yCountList[i1]
                c2 = self.yCountList[i2]
                if( c1 + c2 > 0.1 ):
                    self.yList[i] = (y1 * c1 + y2 * c2) / (c1 + c2)
                else:
                    self.yList[i] = (y1 + y2) / 2
                self.yCountList[i] = c1 + c2

        while (i < self.numPoints):
            self.yList[i] = -1e9
            self.yCountList[i] = 0
            i += 1

        self.xStepSize = self.scaleCount * self.xStepSize / old
        self.redraw = 1


    def SaveToFile(self, filename):
        pass
#void Graph::SaveToFile( char *fileName )
#{
#    Graphics::TBitmap *bmp = new Graphics::TBitmap();
#    bmp->Width = xResolution;
#    bmp->Height = yResolution;
#    TRect rect(0,0,bmp->Width,bmp->Height);
#    bmp->Canvas->CopyRect(rect,canvas,rect);
#    bmp->PixelFormat = pf8bit;
#    bmp->SaveToFile(fileName);
#    delete bmp;
#}
