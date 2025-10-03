import pathlib

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = pathlib.Path(__file__).parent.parent.parent / ".env"


class DBSettings(BaseModel):
    HOST: str
    PORT: int
    NAME: str
    USER: str
    PASSWORD: str

    @property
    def url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                host=self.HOST,
                port=self.PORT,
                username=self.USER,
                password=self.PASSWORD,
                path=self.NAME,
            )
        )


class Settings(BaseSettings):
    db: DBSettings

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="_",
        env_nested_max_split=1,
    )


settings = Settings()
