Transform = tuple[tuple[float, float, float, float], tuple[float, float, float, float], tuple[float, float, float, float], tuple[float, float, float, float]]

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
    return ((2.0 * (w**2 + x**2) - 1, 2.0 * (x * y - w * z), 2.0 * (x * z + w * y), 0.0), 
            (2.0 * (x * y + w * z), 2.0 * (w**2 + y**2) - 1, 2.0 * (y * z - w * x), 0.0), 
            (2.0 * (x * z - w * y), 2.0 * (y * z + w * x), 2.0 * (w**2 + z**2) - 1.0, 0.0), 
            (0.0, 0.0, 0.0, 1.0))

def get_scale_matrix(x: float, y: float, z: float) -> Transform:
    return ((x, 0.0, 0.0, 0.0),
            (0.0, y, 0.0, 0.0),
            (0.0, 0.0, z, 0.0),
            (0.0, 0.0, 0.0, 1.0))

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
