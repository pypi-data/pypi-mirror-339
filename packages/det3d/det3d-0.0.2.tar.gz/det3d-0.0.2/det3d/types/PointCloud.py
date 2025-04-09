import numpy as np

class PointCloud:
    """
    General PointCloud class.
    Holds point cloud data as an (N, 4) numpy array: [x, y, z, intensity]
    """
    def __init__(self, points: np.ndarray):
        assert isinstance(points, np.ndarray), "points must be a numpy array"
        assert points.shape[1] == 4, "PointCloud expects shape (N, 4)"
        self.points = points.astype(np.float32)