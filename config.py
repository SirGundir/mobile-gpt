from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    jwt_secret: str
    password: str

    api_link: str
    openai_api_link: str
    openai_api_key: str
    default_model: str
    files_dir: str = 'assets/images'
    upload_dir: str = 'static'
    date_format: str = '%Y-%m-%d'
    date_time_format: str = '%Y-%m-%d %H:%M'

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
