def application_marge(prix):
    if prix <= 5:
        return prix * 2.5
    if prix <= 10:
        return prix * 2
    if prix <= 20:
        return prix * 1.75
    return prix * 1.5

