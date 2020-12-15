if __name__ == '__main__':
    first = 2020
    second = 30000000

    data = [2, 20, 0, 4, 1, 17]
    history = {}

    for i, num in enumerate(data[:-1]):
        history.update(**{str(num): i})

    next_number = data[-1]

    for i in range(len(data) - 1, second - 1):
        age = i - history.get(str(next_number), i)
        history.update(**{str(next_number): i})
        next_number = age

    print(next_number)
