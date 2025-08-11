class ContentAI:
    def propose_route(
        self,
        *,
        city: str,
        start: tuple[float, float] | None,
        duration_min: int,
        transport_mode: str,
        interest_tags: list[str],
    ) -> list[dict]:
        """Возвращает список точек: [{id, name, lat, lng, poi_type, draft_text}]"""
        raise NotImplementedError

    def finalize_story(
        self,
        *,
        poi_id: str,
        draft_text: str,
        language: str,
    ) -> str:
        """Возвращает финальный markdown-текст истории"""
        raise NotImplementedError
