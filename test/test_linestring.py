import math

from shapely.geometry import LineString

def segments(curve):
    return list(map(LineString, zip(curve.coords[:-1], curve.coords[1:])))

line = LineString([(843650.005531, 6519894.817855), (843653.047059, 6519859.886444), (843655.723635, 6519851.521790), (843657.872405, 6519829.891332)])
line_segments = segments(line)

# for line in line_segments:    # d=math.pow(line[0]-line[1],2)    print (line[0])











 # data
l=[(843650.005531, 6519894.817855), (843653.047059, 6519859.886444), (843655.723635, 6519851.521790), (843657.872405, 6519829.891332)]
l=[(1.5,1.5),(1.5,2.6),(1.5,4.5),(1.5,8.0)]
split=10

lines=[]    # list of lines
dist=[]     # length of lines
len_tot=0   # length of lines
av_len=0
pos_split=[]# position of the segment where we have a split
list_points=[]

# get list of lines
for i in range(len(l)-1):
    lines.append([l[i],l[i+1]])

# get list of length of lines
for i in range(len(lines)):
    x=math.pow(lines[i][0][0]-lines[i][1][0],2)
    y=math.pow(lines[i][0][1]-lines[i][1][1],2)
    d=math.pow(x+y,0.5)
    dist.append(d)

# get length tot
len_tot=sum(dist)

# get av len
av_len=len_tot/split

# get pos segment of split
i=1
pos=1
len_cum=av_len
for p in range(1,split):
    len_seg=p*av_len
    len_cum=i*av_len
    if len_cum<dist[pos-1]:
        i+=1
    else:
        i=1
        pos+=1
    pos_split.append(pos)

# get list points
old=1
up=0
flag=False
len_calc_old=av_len
for p in range (0,len(pos_split)):
    if old==pos_split[p]:
        up+=1
        flag=True
    else:
        flag=False
        up,old=1,old+1
    start_point=l[pos_split[p]-1]
    end_line=l[pos_split[p]]
    end_line_y=l[pos_split[p]]
    if flag==False:
        len_calc=dist[pos_split[p]-2]-up*av_len
    else:
        len_calc=av_len
    print (dist[pos_split[p]-1],up*av_len,flag,len_calc)

    # len_calc_old=dist[pos_split[p]-1]-up*av_len
    # if len_calc_old>av_len: len_calc=av_len
    # else: len_calc=dist[pos_split[p]-1]-up*av_len
    x_t=float(start_point[0]+(len_calc+(up-1)*av_len)/dist[pos_split[p]-1]*( end_line[0]-start_point[0]   ))
    y_t=float(start_point[1]+(len_calc+(up-1)*av_len)/dist[pos_split[p]-1]*( end_line[1]-start_point[1]   ))
    print (y_t)
    list_points.append((x_t,y_t))

# create line

count=[]
nodup=list(dict.fromkeys(pos_split))
for i in nodup:count.append(pos_split.count(i))
print (count)

new_line=[]
new_line.append(l[0])
pos=0
i=0
while i<len(count):
    for a in range(pos,pos+count[i]):
        new_line.append(list_points[a])
        pos+=1
    new_line.append(l[i+1])
    i+=1

for i in range (9): print (1.5+i*0.65)
# test=1
# i=0
# while i<len(pos_split):
#     # print ("i =",i,", test =",test)
#     if pos_split[i]==test:
#         a=list_points[i]
#         print ("append the point in list_points",a)
#         i+=1
#     else:
#         a=l[pos_split[i]]
#         # print("append end segment",a)
#         test+=1
#     new_line.append(a)





print ("{:<20}".format("list of lines: "),lines)
print ("{:<20}".format("length of liens: "), dist)
print ("{:<20}".format("length tot: "),len_tot)
print ("{:<20}".format("av len: "),av_len )
print ("{:<20}".format("pos split: "),pos_split,len(pos_split) )
print ("{:<20}".format("points: "),list_points,len(list_points) )
print ("{:<20}".format("new line: "),new_line,len(new_line) )

