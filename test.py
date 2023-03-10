x = 5
y = 2 if x > 4 else 6
print(y)

def simplified():
    if x > 4:
       return 2
    else:
        return 6

u = [1, 2, 3]
v = [i * i for i in u]
print(v)

v = []
for i in u:
    v.append(i * i)

print([[i*j for i in range(3)] for j in range(10)])

result = []
for j in range(10):
    x = []
    for i in range(3):
        x.append(i*j)
    result.append(x)
print(result)

xyz = {'a':3}
xyz['b']=4
print(xyz)

xzz = {2,3}

x= ['abc', 'def', 'ghi']
print('uvs'.join(x))
