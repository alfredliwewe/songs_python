def file_put_contents(filename, data):
    file = open(filename, 'w')
    file.write(data)


def file_get_contents(filename):
    f = open(filename, "r")
    return f.read()
