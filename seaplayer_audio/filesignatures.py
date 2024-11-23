from typing_extensions import Set, Iterable, Callable, Optional

# ^ Signature Class

class FileSignature:
    def __init__(
        self,
        name: str,
        max_size: int,
        expansions: Optional[Iterable[str]]=None,
        *,
        choice: Optional[Iterable[bytes]]=None,
        methods: Optional[Iterable[Callable[[bytes], bool]]]=None
    ) -> None:
        self.name = name.upper()
        self.max_size = max_size
        self.expansions = \
            set(map((lambda v: v.lower()), expansions)) \
            if expansions is not None else set()
        self.choice = set(choice) if choice is not None else None
        self.methods = list(methods)
        
        assert (self.methods is not None) or (self.choice is not None)
    
    def __str__(self) -> None:
        return f"{self.__class__.__name__}(name={self.name!r}, max_size={self.max_size!r})"
    
    def __repr__(self) -> None:
        return self.__str__()
    
    def check(self, data: bytes) -> bool:
        data = data[:self.max_size]
        if self.choice is None:
            return data in self.choice
        if self.methods is not None:
            for method in self.methods:
                if method(data):
                    return True
        return False

# ^ Signatures Class

class FileSignatures:
    def __init__(self, *signatures: FileSignature) -> None:
        self._signatures = { signature.name: signature for signature in signatures }
        self.max_size = max({signature.max_size for signature in self._signatures.values()})
    
    def __str__(self) -> None:
        return f"{self.__class__.__name__}({repr(self._signatures)})"
    
    def __repr__(self) -> None:
        return self.__str__()
    
    def __getitem__(self, key: str) -> FileSignature:
        return self._signatures[key]
    
    def __setitem__(self, key: str, value: FileSignature) -> None:
        assert isinstance(value, FileSignature)
        if value.max_size > self.max_size:
            self.max_size = value.max_size
        self._signatures[key] = value
    
    def exist(self, name: str) -> bool:
        return self._signatures.get(name.upper(), None) is not None
    
    def check(self, data: bytes) -> Optional[FileSignature]:
        for signature in self._signatures.values():
            if len(data) >= signature.max_size:
                if signature.check(data[:self.max_size]):
                    return signature
        return None

# ^ Audio File Signatures

SUPPORTED_AUDIOFILE_SIGNATURES = FileSignatures(
    FileSignature(
        'OGG', 4, { 'ogg', 'oga' },
        choice={ b'OggS' }
    ),
    FileSignature(
        'MP3', 3, { 'mp3' },
        choice={ b'\xFF\xFB', b'\xFF\xF3', b'\xFF\xF2', b'ID3' }
    ),
    FileSignature(
        'FLAC', 4, { 'flac' },
        choice={ b'fLaC' }
    ),
    FileSignature(
        'AU', 4, { 'au', 'snd' },
        choice={ b'\x2E\x73\x6E\x64' }
    ),
    FileSignature(
        'VOC', 22, { 'voc' },
        choice={ b'\x43\x72\x65\x61\x74\x69\x76\x65\x20\x56\x6F\x69\x63\x65\x20\x46\x69\x6C\x65\x1A\x1A\x00' }
    ),
    FileSignatures(
        'CAF', 4, { 'caf' },
        choice={ b'caff' }
    ),
    FileSignature(
        'WAV', 12, { 'wav' },
        methods=[ lambda v: (v[0:4]+v[8:12])==b'RIFFWAVE' ]
    ),
    FileSignature(
        'AIFF', 12, { 'aiff', 'aif', 'aifc', 'snd', 'iff' },
        methods=[ lambda v: (v[0:4]+v[8:12])==b'FORMAIFF' ]
    )
)

