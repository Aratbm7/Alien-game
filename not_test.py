lists = ['hello', 'ot', 'is']

for list in lists.copy():
    print(list)
    lists.remove(list)


print(lists)
if not lists:
    print('hello')