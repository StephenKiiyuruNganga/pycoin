from functools import reduce

name = "Steve"
age = 28

text = 'My name is {} and I am {} years old'
print(text.format(name, age))

coins = 150.2234

text = 'Funds: {:_>20.1f}'
print(text.format(coins))

bank = "Stanchat"
amount = 480000

text = f'I bank with {bank} and I have saved Ksh {amount:.4f}'
print(text)


def multi(el):
    return el*2


a = [1, 2, 3, 4]

b = list(map(multi, a))
print(b)

c = list(map(lambda el: el*2 if el % 2 == 0 else 0, a))
print(c)

# reduce arguments: fn, list, initial_value
# the fn gets access to last_value and current_value of the operation. Eg sum and current list item
d = reduce(lambda last_value, current_value: current_value + last_value, a, 0)
print(d)


def unlimited(*args):
    print(f"normal args: {str(args)}")
    for argument in args:
        print(argument)


unlimited(1, 2, 3, 4)


def unlimited_2(**keyword_args):
    print(f"keyword args: {str(keyword_args)}")
    for k, v in keyword_args.items():
        print(k, v)


unlimited_2(email="g@mail.com", password="1234")


def write():
    my_file = open("demo_file.txt", mode="w")
    my_file.write("Wrote the first line\n")
    my_file.close()


def write_v2():
    with open("demo.txt", mode="w") as my_file:
        my_file.write("Wrote the first line using version 2\n")


def read():
    my_file = open("demo_file.txt", mode="r")
    # read() returns 1 string with all the content of the file
    content = my_file.read()
    my_file.close()
    print(content)


def read_v2():
    with open("demo.txt", mode="r") as my_file:
        content = my_file.read()
        print(content)


def add_content():
    my_file = open("demo_file.txt", mode="a")
    my_file.write("Added this line\n")
    my_file.close()


def read_line_by_line():
    my_file = open("demo_file.txt", mode="r")
    line = my_file.readline()
    while line:
        print(line)
        # python will automatically go to the next line when you call readline again
        line = my_file.readline()


# there is also readlines which returns a list of all the lines

# write()
# read()
# print("-"*20)
# add_content()
# add_content()
# read()
# read_line_by_line()

write_v2()
read_v2()
