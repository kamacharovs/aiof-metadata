from pydantic import BaseSettings


class Settings(BaseSettings):
    aiof_portal_url: str = "http://localhost:4100"
