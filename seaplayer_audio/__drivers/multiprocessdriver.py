from numpy import ndarray
from ..base.driver import DriverBase

# ! Main Class
class SoundDeviceMultiprocessingDriver(DriverBase[ndarray]):
    __driver_name__: str        = 'sounddevice-multiprocessing'
    __driver_version__: str     = '0.1.0'

    