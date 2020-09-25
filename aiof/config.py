from pydantic import BaseSettings


class Settings(BaseSettings):
    cors_origins: list = [
        "http://localhost:4100"
    ]
    cors_allowed_methods: list = [
        "*"
    ]
    cors_allowed_headers: list = [
        "*"
    ]

