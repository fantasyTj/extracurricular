points = [[x,y] for x in range(20) for y in range(21)]
s = set()

for i in range(len(points)):
# 这里 i 返回一个列表，如[0,0]
    x1,y1 = points[i][0], points[i][1]
    for j in range(i + 1, len(points)):
        x2,y2 = points[j][0], points[j][1]
        if x1 == x2:
            continue

        k = (y2-y1)/(x2-x1)
        # b1 = (x2*y1-x1*y2)/(x2-x1)
        b2 = y2-k*x2
        b2 = round(b2, 8)
        # if b1 != b2:
        #     print('b1 =', b1, 'b2 =', b2)
        #b = y2-k*x2:这个截距算出来的有问题
        if (k,b2) not in s:
            s.add((k,b2))
        # if 不要也可以
# 一定要用（），而不能用[]，不然数不出 

c = len(s) + 20
print(c)