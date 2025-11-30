def my_generator():
    yield 1
    yield 2
    yield 3
    return "Done"

# Using the generator
gen = my_generator()
for value in gen:
    print(value)


# Catching the StopIteration to get the return value
try:
    next(gen)
except StopIteration as e:
    print(f"Generator returned: {e.value}")