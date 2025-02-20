from random import choices

def weight_choices(given_list):
    spawns = []
    chances = []

    for item in given_list:
        spawns.append(given_list[item][0])
        chances.append(given_list[item][1])

    return choices(population=spawns, weights=chances)[0]