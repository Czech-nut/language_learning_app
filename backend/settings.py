from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_user: str
    db_pass: str
    db_name: str

    secret_key: str
    refresh_secret_key: str

    def db_url(self):
        return f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"  # noqa: E501

    class Config:
        env_file = ".env"
