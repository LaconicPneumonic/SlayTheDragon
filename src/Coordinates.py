size = (2,2)


coordinates = {}


for i in xrange(size[0]/2 + 1):

    for j in xrange(size[1]/2 + 1):

        coordinates[(i,j)] = (size[0]/2 + i,size[1]/2 + j)


print coordinates
