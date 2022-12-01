def cakes(recipe, available):
    try:
        for i, (key, value) in enumerate(recipe.items()):
            multiple = available[key] // value
            if i == 0:
                number_of_cakes = multiple
            else:
                number_of_cakes = min(number_of_cakes, multiple)
        return number_of_cakes
    except KeyError:
        return 0