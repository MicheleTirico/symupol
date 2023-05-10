from shapely.geometry import LineString, Point

line = LineString(([0, 0], [2, 1], [3, 2], [3.5, 1], [5, 2]))
line=LineString(([1.5,1.5],[1.5,2.6],[1.5,4.5],[1.5,8.0]))

length=line.length
print (length)
nSplit=10
distance=length/nSplit
# distance=1
def cut(line, distance, lines):
    # Cuts a line in several segments at a distance from its starting point
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [
                LineString(coords[:i+1]),
                LineString(coords[i:])
            ]
        if pd > distance:
            cp = line.interpolate(distance)
            lines.append(LineString(coords[:i] + [(cp.x, cp.y)]))
            line = LineString([(cp.x, cp.y)] + coords[i:])
            if line.length > distance:
                cut(line, distance, lines)
            else:
                lines.append(LineString([(cp.x, cp.y)] + coords[i:]))
            return lines

def removeLastLine(lines,threshold):
    if lines[-1]<threshold: return lines[:-1]

def removeShortLines(lines,threshold):
    i=0
    while i<len(lines):
        if lines[i].length<threshold:
            lines.pop(i)
        i+=1
    return lines
lines = cut(line, distance, list())

print (lines)

lines=removeShortLines(lines,0.001)
for line in lines:
    print (line, line.length)