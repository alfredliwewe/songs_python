import numpy

data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
q1 = numpy.percentile(data, 25)
new_series = [x for x in data if x >= q1]

print(new_series)
