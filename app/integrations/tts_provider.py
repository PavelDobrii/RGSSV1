class TTSProvider:
    def synthesize(
        self,
        *,
        text: str,
        language_code: str,
        voice_name: str | None = None,
        speaking_rate: float = 1.0,
        pitch: float = 0.0,
    ) -> bytes:
        """Возвращает MP3-байты"""
        raise NotImplementedError
