class State:
    def __init__(self, tile_seq=None, depth=0, weight=0, parent=None):
        if tile_seq is None:
            tile_seq = []
        self.tile_seq = tile_seq
        self.depth = depth
        self.weight = weight
        self.parent = parent

    def __eq__(self, other):
        return self.tile_seq == other.tile_seq
