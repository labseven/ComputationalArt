"""
Mini Project 2: Recursive Art

@author: Adam Novotny
"""

import random
from PIL import Image
from math import pi, cos, sin


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """

    # If at end of chain
    if(max_depth == 1):
        return ['x', 'y'][random.randint(0, 1)]

    # Random cuts out early
    if(min_depth <= 0):
        if(random.randint(0, max_depth * 2) == 0):
            return ['x', 'y'][random.randint(0, 1)]
    possible_functions = [["sin_pi", ''], ["cos_pi", ''], ["prod", '', ''], ["avg", '', '']]

    function_num = random.randint(0, len(possible_functions) - 1)

    myfunction = []
    myfunction.append(possible_functions[function_num][0])

    for x in range(len(possible_functions[function_num]) - 1):
        myfunction.append(build_random_function(min_depth - 1, max_depth - 1))

    return myfunction


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """

    if(f[0] == 'x'):
        return x
    if(f[0] == 'y'):
        return y
    if(f[0] == 'prod'):
        return evaluate_random_function(f[1], x, y) * evaluate_random_function(f[2], x, y)
    if(f[0] == 'sin_pi'):
        return sin(pi * evaluate_random_function(f[1], x, y))
    if(f[0] == 'cos_pi'):
        return cos(pi * evaluate_random_function(f[1], x, y))
    if(f[0] == 'avg'):
        return (evaluate_random_function(f[1], x, y) + evaluate_random_function(f[2], x, y)) / 2
    else:
        raise(ValueError("Function not defined."))


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """

    if(val < input_interval_start):
        return output_interval_start
    if(val > input_interval_end):
        print("above input bounds")
        return output_interval_end
    if(input_interval_start == input_interval_end):
        return output_interval_start

    input_range = input_interval_end - input_interval_start
    output_range = output_interval_end - output_interval_start

    # Remap the values:
    return (((val - input_interval_start) * (output_range)) / (input_range)) + output_interval_start


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(0, 10)
    green_function = build_random_function(0, 10)
    blue_function = build_random_function(0, 10)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    generate_art("myart.png")
