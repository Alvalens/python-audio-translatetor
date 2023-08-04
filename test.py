x = int(input())
y = int(input())
array = []
for i in range(x):
    array.append([])
    for j in range(y):
        array[i].append(int(input()))
print(array)