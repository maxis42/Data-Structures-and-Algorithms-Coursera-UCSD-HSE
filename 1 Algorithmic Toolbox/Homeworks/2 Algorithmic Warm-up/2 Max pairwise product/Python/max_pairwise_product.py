# Uses python3
n = int(input())
a = [int(x) for x in input().split()]
assert(len(a) == n)

max_ind1 = -1
for i in range(n):
    if max_ind1 == -1 or a[i] > a[max_ind1]:
        max_ind1 = i

max_ind2 = -1
for i in range(n):
    if i != max_ind1 and (max_ind2 == -1 or a[i] > a[max_ind2]):
        max_ind2 = i

result = a[max_ind1] * a[max_ind2]

print(result)
