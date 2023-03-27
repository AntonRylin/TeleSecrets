book = {
    "817982673": "Никита"
}


def name(id):
    if book.get(id):
        return book[id]
    else:
        return id
