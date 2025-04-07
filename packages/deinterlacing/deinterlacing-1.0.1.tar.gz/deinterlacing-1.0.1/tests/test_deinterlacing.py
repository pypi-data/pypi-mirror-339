from deinterlacing.processing import deinterlace, DeinterlaceParameters
import numpy as np
from pathlib import Path


def test_deinterlacing():
    images = np.load(Path("./tests/artifact_512.npy"))
    images = np.vstack([np.reshape(images, (1, 512, 512)) for _ in range(2000)])
    deinterlace(images)
