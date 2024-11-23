import mutagen
from typing_extensions import Optional

# ! File Works Methods

def get_mutagen_info(filepath: str) -> Optional[mutagen.FileType]:
    try: return mutagen.File(filepath)
    except: return

# ! Formatiing Methods

def check_string(value: Optional[str]) -> Optional[str]:
    if value is not None:
        if (len(value.replace(' ', '')) == 0):
            return None
    return value