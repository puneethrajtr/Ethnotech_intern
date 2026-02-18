def person_lister(func):
    def wrapper(people):
        # sort people by age (index 2)
        people.sort(key=lambda x: int(x[2]))
        return func(people)
    return wrapper


@person_lister
def name_format(people):
    formatted = []
    for person in people:
        title = "Mr." if person[3] == "M" else "Ms."
        formatted.append(f"{title} {person[0]} {person[1]}")
    return formatted


# Input handling
n = int(input())
people = []

for _ in range(n):
    people.append(input().split())

# Call function and print output
result = name_format(people)

for name in result:
    print(name)
