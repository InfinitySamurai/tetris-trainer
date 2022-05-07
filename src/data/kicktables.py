from data.tetronimoData import Rotation

kick_tables_I = {
    (Rotation.START, Rotation.CW): [[-2,0],[1,0],[-2,-1],[1,2]],
    (Rotation.CW, Rotation.START): [[2,0],[-1,0],[2,1],[-1,-2]],
    (Rotation.CW, Rotation.UPSIDEDOWN): [[-1,0],[2,0],[-1,2],[2,-1]],
    (Rotation.UPSIDEDOWN, Rotation.CW): [[1,0],[-2,0],[1,-2],[-2,1]],
    (Rotation.UPSIDEDOWN, Rotation.CCW): [[2,0],[-1,0],[2,1],[-1,-2]],
    (Rotation.CCW, Rotation.UPSIDEDOWN): [[-2,0],[1,0],[-2,-1],[1,2]],
    (Rotation.CCW, Rotation.START): [[1,0],[-2,0],[1,-2],[-2,1]],
    (Rotation.START, Rotation.CCW): [[-1,0],[2,0],[-1,2],[2,-1]]
    # "0>>2": [[0,1],[1,1],[-1,1],[1,0],[-1,0]],
    # "2>>0": [[0,-1],[-1,-1],[1,-1],[-1,0],[1,0]],
    # "1>>3": [[1,0],[1,2],[1,1],[0,2],[0,1]],
    # "3>>1": [[-1,0],[-1,2],[-1,1],[0,2],[0,1]]
}

kick_tables = {
    (Rotation.START, Rotation.CW): [[-1,0],[-1,1],[0,-2],[-1,-2]],
    (Rotation.CW, Rotation.START): [[1,0],[1,-1],[0,2],[1,2]],
    (Rotation.CW, Rotation.UPSIDEDOWN): [[1,0],[1,-1],[0,2],[1,2]],
    (Rotation.UPSIDEDOWN, Rotation.CW): [[-1,0],[-1,1],[0,-2],[-1,-2]],
    (Rotation.UPSIDEDOWN, Rotation.CCW): [[1,0],[1,1],[0,-2],[1,-2]],
    (Rotation.CCW, Rotation.UPSIDEDOWN): [[-1,0],[-1,-1],[0,2],[-1,2]],
    (Rotation.CCW, Rotation.START): [[-1,0],[-1,-1],[0,2],[-1,2]],
    (Rotation.START, Rotation.CCW): [[1,0],[1,1],[0,-2],[1,-2]]
    # "0>>2": [[0,1],[1,1],[-1,1],[1,0],[-1,0]],
    # "2>>0": [[0,-1],[-1,-1],[1,-1],[-1,0],[1,0]],
    # "1>>3": [[1,0],[1,2],[1,1],[0,2],[0,1]],
    # "3>>1": [[-1,0],[-1,2],[-1,1],[0,2],[0,1]]
}
