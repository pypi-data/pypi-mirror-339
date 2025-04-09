from typing import List, Optional, Tuple
import numpy as np
import numpy.typing as npt

def dummy_func() -> int: ...

def reconstruct_mask(
    bytes: bytes,
    width: int,
    height: int,
    scale: Optional[Tuple[float, str]] = None
) -> npt.NDArray[np.float32]: ...

def a2ev1_melspectrogram(
    wav: npt.NDArray[np.float32],
    sample_rate: int
) -> List[bytes]: ...

def a2ev2_melspectrogram(
    wav: npt.NDArray[np.float32],
    sample_rate: int
) -> List[bytes]: ...

class RTMelV2:
    def __init__(self, sample_rate: int) -> None: ...
    def clear(self) -> None: ...
    def transform(self, wav: npt.NDArray[np.float32]) -> str: ...

