from random import randint

#all books, libraries num, num of days

#library defined by:
#books in lib, sign up days, books per day

def books_by_importance():
    return

def libraries_by_capacity():
    return

def libraries_by_timeToStart ():
    return

def delete_read_books(books, libraries):
    return

def next_best (remaining_days, libraries, books):
    best_lib = -1
    best_score = 0

    for i in range(len(libraries)):
        score = 0
        capacity = remaining_days * libraries[i].books_per_day
        for j in range(capacity):
            if j >= len(libraries[i].books):
                break
            if books.has_key(libraries[i].books[j].id):
                continue
            score += libraries[i].books[j].score
        if (score > best_score):
            best_lib = i
            best_score = score

    if best_score == 0:
        return [0,0,0,0]

    ret = []
    for book in libraries[best_lib].books:
        ret.append (book.id)

    return [ best_lib,[ libraries[best_lib].id, len(ret) ], ret, remaining_days - libraries[best_lib].signup_days ]

def randomized (number_of_books, libraries_num, days, scores_of_books, libraries):
    libs_to_sign = libraries_num
    ret = []

    read_books = []
    remaining_days = int(days)

    for x in range(int(libraries_num)):
        books_to_read = []
        capacity = (remaining_days - int(libraries[x][0][2])) * int(libraries[x][0][3])
        for i in range(capacity):
            if i >= len(libraries[x][1]):
                continue
            if libraries[x][1][i] not in read_books:
                books_to_read.append (libraries[x][1][i])
        if (len(books_to_read) == 0):
            continue
        remaining_days -= int(libraries[x][0][2])
        read_books = read_books + books_to_read
        ret.append ( [libraries[x][0][0], len(books_to_read)] )
        ret.append ( books_to_read )
        print(str(x) + "/" + libraries_num)
    ret.insert (0, [len(ret) / 2])
    return ret


def solve (days, libraries):
    # libraries.sort(key=lambda x: x.signup_days) #, reverse=True)
    # libraries.sort(key=lambda x: x.books_per_day, reverse=True)

    remaining_days = days
    ret = []
    read_books = {}

    while True:
        lib, line1, line2, remaining_days = next_best (remaining_days, libraries, read_books)
        if remaining_days == 0:
            break
        ret.append (line1)
        ret.append (line2)
        del libraries[lib]
        if len(libraries) == 0:
            break

        for book in line2:
            read_books[book] = 1

    ret.insert (0, [len(ret) / 2])

    return ret

    #lib = []
    #for x in libraries:
    #    lib.append ([ [x.id, x.books_num, x.signup_days, x.books_per_day], x.books ])

    # print (lib)

    #return randomized (number_of_books, libraries_num, days, scores_of_books, lib)
#    return random_slices (pizzas_to_order, slices_in_each_type)
