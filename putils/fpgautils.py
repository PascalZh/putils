import numpy as np
from numpy.lib.function_base import iterable


def gen_mif(vec: iterable, file, depth: int, width=8):
    """Generate mif binary data file

    Args:
          vec (np.ndarray or iterable): Data vector.
          depth (int): Length of vec.
          width (int, optional): Bit width of the number in the vector. Defaults to 8.
    """

    def clip(x, x_min, x_max):
        if x < x_min:
            return x_min
        elif x > x_max:
            return x_max
        else:
            return x

    vec_clipped = None
    if (type(vec) == np.ndarray):
      vec_clipped = np.clip(vec, 0, 2**depth - 1)
    else:
      vec_clipped = [clip(x, 0, 2**depth - 1) for x in vec]

    def print_file(*arg):
        print(*arg, file=file)

    print_file('WIDTH=%i;' % width)
    print_file('DEPTH=%i;\n' % depth)
    print_file('ADDRESS_RADIX=UNS;\nDATA_RADIX=UNS;\n')
    print_file('CONTENT BEGIN')
    for i in range(depth):
        print_file('  %i\t:\t%i;' % (i, vec_clipped[i]))
    print_file('END;')
