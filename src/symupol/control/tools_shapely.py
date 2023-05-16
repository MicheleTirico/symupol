from shapely.geometry import LineString, Point
import numpy as np
from shapely.ops import unary_union

def splitLineStringDistance(line, distance, lines):
    # Cuts a line in several segments at a distance from its starting point
    if distance <= 0.0 or distance >= line.length:
        #print (line.length,line)
        return [line]#[LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [LineString(coords[:i+1]),LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            lines.append(LineString(coords[:i] + [(cp.x, cp.y)]))
            line = LineString([(cp.x, cp.y)] + coords[i:])
            if line.length > distance:  splitLineStringDistance(line, distance, lines)
            else:                       lines.append(LineString([(cp.x, cp.y)] + coords[i:]))
            return lines

def splitLineStringNsplit(line,nSplit,lines):
    length = line.length
    return splitLineStringDistance(line,line.length/nSplit,lines)

def splitLineStringNsplit_test(line,n):
    length = line.length
    n=int(n)
    distances = np.linspace(0, line.length, n)
    # or alternatively without NumPy:
    # distances = (line.length * i / (n - 1) for i in range(n))
    points = [line.interpolate(distance) for distance in distances]
    multipoint = unary_union(points)  # or new_line = LineString(points)
    return LineString(multipoint)

def removeLastLine(lines,threshold):
    if lines[-1]<threshold: return lines[:-1]

def removeShortLines(lines,threshold):
    i=0
    while i<len(lines):
        if lines[i].length<threshold: lines.pop(i)
        i+=1
    return lines

