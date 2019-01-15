def rescale(x, range, newrange=(0,1)):
    mina, maxa = range
    minb, maxb = newrange
    return ((x-mina)/(maxa-mina) * (maxb-minb)) + minb


