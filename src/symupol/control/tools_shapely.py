from shapely.geometry import LineString, Point

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
def removeLastLine(lines,threshold):
    if lines[-1]<threshold: return lines[:-1]

def removeShortLines(lines,threshold):
    i=0
    while i<len(lines):
        if lines[i].length<threshold: lines.pop(i)
        i+=1
    return lines

