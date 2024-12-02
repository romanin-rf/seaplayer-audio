import os

# ! Main Paths
LOCAL_DIRPATH           = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SAMPLES_DIRPATH         = os.path.join(LOCAL_DIRPATH, 'samples')

# ! Other Paths
SAMPLES_FILEPATHS = {
    "sample0": os.path.join(SAMPLES_DIRPATH, 'sample0.mp3')
}