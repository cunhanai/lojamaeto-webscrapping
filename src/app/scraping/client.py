import httpx


class MaetoClient:
    def __init__(self, base_url: str, timeout: int, user_agent: str):
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={"User-Agent": user_agent},
            follow_redirects=True,
        )

    def get(self, path: str, params: dict | None = None) -> str:
        response = self._client.get(path, params=params)
        response.raise_for_status()
        return response.text

    def close(self) -> None:
        self._client.close()
