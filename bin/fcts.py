# checkers on hexagonal grid
# for details see readme.md
#
# Dourov Maxime
# Cruquenaire Achille
# Gendbeien Jonas
#

from math import sqrt, ceil, pi, floor


def screen_to_board(x: int, y: int, tile_height: float):
    """ translate the coord on screen to x,y,z hexagonal axis
    :x: the x value in pixel of the click position
    :y: the y value in pixel of the click position
    :tile_height: the height of a tile on the board in pixel
    """
    if not isinstance(x, int) or not isinstance(y, int):
        raise TypeError

    x -= sqrt(3) * tile_height * 1.25
    y -= tile_height / 2
    board_x = ((2 * y) / 3) / (tile_height / 2)
    board_z = ((x * sqrt(3) - y) / 3) / (tile_height / 2)
    board_y = - board_x - board_z
    return (round(board_x), round(board_y), round(board_z))


def board_to_screen(x: int, y: int, tile_height: float):
    """ translate the coords of hex tiles to their screen coords

    :x, y: valid board coordonate (Z is not needed)
    :tile_height: the height of a tile on the board in pixel
    """
    if type(tile_height) != float and type(tile_height) != int:
        raise TypeError
    if type(x) != int or type(y) != int:
        raise TypeError
    if tile_height == 0:
        raise ValueError

    screen_x = (-((sqrt(3) * y) + (sqrt(3) * x / 2)) *
                tile_height / 2) + (sqrt(3) * tile_height * 1.25)
    screen_y = ((3 / 2) * x * tile_height / 2) + (tile_height / 2)

    return (round(screen_x), round(screen_y))


def vector_add(a: tuple, b: tuple):
    """ add 2 vectors together
    :a b: the vectors must have the same number of dimensions
    """
    if not isinstance(a, tuple) or not isinstance(b, tuple):
        raise TypeError
    if len(a) != len(b):
        raise IndexError

    out = []
    for i in range(len(a)):
        if (type(a[i]) != int and type(a[i]) != float) or (type(b[i]) != int and type(b[i]) != float):
            raise TypeError
        out.append(a[i]+b[i])
    return tuple(out)


def vector_sub(a: tuple, b: tuple):
    """ subtract 2 vectors together
    :a b: the vectors must have the same number of dimensions
    """
    if not isinstance(a, tuple) or not isinstance(b, tuple):
        raise TypeError
    if len(a) != len(b):
        raise IndexError
    out = []
    for i in range(len(a)):
        if (type(a[i]) != int and type(a[i]) != float) or (type(b[i]) != int and type(b[i]) != float):
                raise TypeError
        out.append(a[i]-b[i])
    return tuple(out)


def vector_cross_product(a: tuple, b: tuple):
    """ find the cross product of 2 vectors
    :a b: the vectors must have 3 dimensions
    """
    if not (isinstance(a, tuple) and isinstance(b, tuple)):
        raise TypeError
    if len(a) != 3 or len(b) != 3:
        raise IndexError
    if not ((isinstance(a[0],int) or isinstance(a[0],float)) and ((isinstance(a[1],int) or isinstance(a[1],float))) and (isinstance(a[2],int) or isinstance(a[2],float))):
        raise TypeError
    if not ((isinstance(b[0],int) or isinstance(b[0],float)) and ((isinstance(b[1],int) or isinstance(b[1],float))) and (isinstance(b[2],int) or isinstance(b[2],float))):
        raise TypeError
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def is_the_right_parallel(a: tuple, b: tuple):
    """ determines if a vector is the parallel we are looking for

    a and b must be of same lenght
    """
    if not isinstance(a, tuple) or not isinstance(b, tuple):
        raise TypeError
    if len(a) != len(b):
        raise ValueError
    for i in range(len(a)):
        if a[i] < 0 < b[i] or b[i] < 0 < a[i]:
            return False
    return True  # if you can't prove it's False it's True


def other_player(player: str):
    """
    :return: the opposite player
    """
    if player == "black":
        return "white"
    elif player == "white":
        return "black"
    else:
        if isinstance(player,str):
            raise ValueError
        else:
            raise TypeError


def get_starting_pos(player):
    """ generate a list of starting locations for given player

    :player: 'white' or 'black', corresponds to the current player
    """

    if isinstance(player,str) and player not in ["white", "black"]:
        raise ValueError
    elif not isinstance(player,str):
        raise TypeError

    out = []

    for i in range(8):
        if player == "white":
            out.append((0, -i, i))
            out.append((1, -i, i - 1))
        elif player == "black":
            out.append((6, -i - 3, i - 3))
            out.append((7, -i - 3, i - 4))

    return out


def get_starting_pos_test(player):
    """ made for testing/debugging purpose only 

    :player: 'white' or 'black', corresponds to the current player 
    """
    if isinstance(player,str) and player not in ["white", "black"]:
        raise ValueError
    elif not isinstance(player,str):
        raise TypeError
    
    if player == "white":
        return [(4, -5, 1)]
    elif player == "black":
        return [(4, -4, 0), (4, -6, 2), (5, -5, 0), (5, -6, 1), (3, -4, 1), (3, -5, 2),
                (2, -6, 4), (5, -8, 3), (2, -2, 0), (3, -
                                                     2, -1), (3, -7, 4), (6, -8, 2), (1, -3, 2),
                (1, -4, 3), (5, -3, -2), (6, -4, -2)]
    return []


def get_starting_pos_test2(player):
    """ made for testing/debugging purpose only 

    :player: 'white' or 'black', corresponds to the current player 
    """
    if isinstance(player,str) and player not in ["white", "black"]:
        raise ValueError
    elif not isinstance(player,str):
        raise TypeError
    
    if player == "white":
        return [(4, -5, 1)]
    elif player == "black":
        return [(6, -6, 0)]
    return []


def validate_coords(coords: tuple) -> bool:
    """ True if the coordinate are valid, False if not

:coords: (x,y,z) valid coordinates of the board

            usable tiles coords follow a pattern like that:
            if x = 0 -> y = -8 to 2
            if x = 1 | 2 -> y = -9 to 1
            if x = 3 | 4 -> y = -10 to 0
            if x = 5 | 6 -> y = -11 to -1
            if x = 7 -> y = -12 to -2
            z isn't relevant since it depends on the value of x and y at the same time
    """
    if not isinstance(coords,tuple):
        raise TypeError
    if len(coords) != 3:
        raise IndexError

    if coords[0] < 0 or coords[0] > 7:
        return False
    return True


def warp(coords):
    """ gives the coordinates of the tile they can warp to
        see readme.md for rules on teleportation
    :coords: (x,y,z) valid coordinates of the board

    :return: warped coordinates, none if cannot warp
    """
    if not isinstance(coords, tuple):
        raise TypeError
    tmp = (0, coords[1] + ceil(coords[0] / 2),
           coords[2] + floor(coords[0] / 2))
    if tmp[1] <= -9 and tmp[2] >= 9:
        return vector_add(coords, (0, 11, -11))
    elif tmp[1] >= 3 and tmp[2] <= -3:
        return vector_add(coords, (0, -11, 11))
    return coords


def takes_score(pieces_taken):
    """
        returns the score to add for x takes
        it's functionally the same as doing 100*2**(x-1) but it makes you look smarter
    """
    if pieces_taken <= 0:
        raise ValueError
    return 100 << (pieces_taken - 1)


def get_pieces_bonus(pieces_left, queens):
    """
        gives bonus points based on pieces left and queens
    """
    if pieces_left <= 0 or queens < 0:
        raise ValueError
    return 100 << (queens ^ pieces_left) if (queens ^ pieces_left) > queens else 100 << queens


# def get_time_bonus(time_spent):
# """
# calculates the bonus points for time spent before playing
# """
# return ceil(time_spent ** pi) if time_spent <= 10 else ceil(pi * time_spent)
