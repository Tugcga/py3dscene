import math

Transform = tuple[tuple[float, float, float, float], tuple[float, float, float, float], tuple[float, float, float, float], tuple[float, float, float, float]]

'''Transform matrix stored in column form
It means that the first column contains coordinates of the first transformed axis,
the second column - the second axis, the third column - the third axis and the last column - position of the origin
Last row is always (0.0, 0.0, 0.0, 1.0)

In this form transformed coordinates of the point (x, y, z) can be found:
(x_new, y_new, z_new)^t = T * (x, y, z)^t
Coordinates are columns
'''

def length(x: float, y: float, z: float):
    '''Return the length of the vector (x, y, z)
    '''
    return math.sqrt(x**2 + y**2 + z**2)

def get_identity() -> Transform:
    return ((1.0, 0.0, 0.0, 0.0),
            (0.0, 1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0, 0.0),
            (0.0, 0.0, 0.0, 1.0))

def get_translation_matrix(x: float, y: float, z: float) -> Transform:
    return ((1.0, 0.0, 0.0, x),
            (0.0, 1.0, 0.0, y),
            (0.0, 0.0, 1.0, z),
            (0.0, 0.0, 0.0, 1.0))

def get_rotation_matrix(x: float, y: float, z: float, w: float) -> Transform:
    return ((-1.0 + 2.0 * (w**2 + x**2), 2.0 * (x * y - w * z), 2.0 * (x * z + w * y), 0.0), 
            (2.0 * (x * y + w * z), -1.0 + 2.0 * (w**2 + y**2), 2.0 * (y * z - w * x), 0.0), 
            (2.0 * (x * z - w * y), 2.0 * (y * z + w * x), -1.0 + 2.0 * (w**2 + z**2), 0.0), 
            (0.0, 0.0, 0.0, 1.0))

def get_scale_matrix(x: float, y: float, z: float) -> Transform:
    return ((x, 0.0, 0.0, 0.0),
            (0.0, y, 0.0, 0.0),
            (0.0, 0.0, z, 0.0),
            (0.0, 0.0, 0.0, 1.0))

def get_srt_matrix(translation: tuple[float, float, float],
                   rotation: tuple[float, float, float, float],
                   scale: tuple[float, float, float]) -> Transform:
    translation_tfm: Transform = get_translation_matrix(*translation)
    rotation_tfm: Transform = get_rotation_matrix(*rotation)
    scale_tfm: Transform = get_scale_matrix(*scale)
    return multiply(translation_tfm, multiply(rotation_tfm, scale_tfm))

def multiply(a: Transform, b: Transform) -> Transform:
    '''Return A * B
    '''
    result = [[0.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 0.0]]
    for i in range(4):
        for j in range(4):
            for s in range(4):
                result[i][j] += a[i][s] * b[s][j]
    return ((result[0][0], result[0][1], result[0][2], result[0][3]),
            (result[1][0], result[1][1], result[1][2], result[1][3]),
            (result[2][0], result[2][1], result[2][2], result[2][3]),
            (result[3][0], result[3][1], result[3][2], result[3][3]))

def tfm_to_translation(tfm: Transform) -> tuple[float, float, float]:
    return (tfm[0][3], tfm[1][3], tfm[2][3])

def tfm_to_rotation(tfm: Transform) -> tuple[float, float, float, float]:
    trace = tfm[0][0] + tfm[1][1] + tfm[2][2]
    if trace > 0.0:
        k = 0.5 / math.sqrt(1.0 + trace)
        return (k * (tfm[2][1] - tfm[1][2]), k * (tfm[0][2] - tfm[2][0]), k * (tfm[1][0] - tfm[0][1]), 0.25 / k)
    elif (tfm[0][0] > tfm[1][1]) and (tfm[0][0] > tfm[2][2]):
        k = 0.5 / math.sqrt(1.0 + tfm[0][0] - tfm[1][1] - tfm[2][2])
        return(0.25 / k, k * (tfm[0][1] + tfm[1][0]), k * (tfm[0][2] + tfm[2][0]), k * (tfm[2][1] - tfm[1][2]))
    elif tfm[1][1] > tfm[2][2]:
        k = 0.5 / math.sqrt(1.0 + tfm[1][1] - tfm[0][0] - tfm[2][2])
        return (k * (tfm[0][1] + tfm[1][0]), 0.25 / k, k * (tfm[1][2] + tfm[2][1]), k * (tfm[0][2] - tfm[2][0]))
    else:
        k = 0.5 / math.sqrt(1.0 + tfm[2][2] - tfm[0][0] - tfm[1][1])
        return (k * (tfm[0][2] + tfm[2][0]), k * (tfm[1][2] + tfm[2][1]), 0.25 / k, k * (tfm[1][0] - tfm[0][1]))

def tfm_to_scale(tfm: Transform) -> tuple[float, float, float]:
    return (length(tfm[0][0], tfm[1][0], tfm[2][0]),
            length(tfm[0][1], tfm[1][1], tfm[2][1]),
            length(tfm[0][2], tfm[1][2], tfm[2][2]))
