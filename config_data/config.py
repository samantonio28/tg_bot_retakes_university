from dataclasses import dataclass
from dotenv import dotenv_values

@dataclass
class DatabaseConfig:
    database: str
    db_host: str
    db_user: str
    db_password: str

@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    tutor_ids: list[int]
    student_ids: list[int]

@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig

def load_config(path: str | None = None) -> Config:
    env = dotenv_values(path)
    
    if env['ADMIN_IDS'] == '' or env['ADMIN_IDS'] is None:
        admin_ids = []
    else:
        admin_ids = list(map(int, env['ADMIN_IDS'].rstrip(',').split(',')))
    
    if env['STUDENT_IDS'] == '' or env['STUDENT_IDS'] is None:
        student_ids = []
    else:
        student_ids = list(map(int, env['STUDENT_IDS'].rstrip(',').split(',')))

    if env['TUTOR_IDS'] == '' or env['TUTOR_IDS'] is None:
        tutor_ids = []
    else:
        tutor_ids = list(map(int, env['TUTOR_IDS'].rstrip(',').split(',')))

    return Config(
        tg_bot=TgBot(
            token=env['BOT_TOKEN'],
            admin_ids=admin_ids,
            tutor_ids=tutor_ids,
            student_ids=student_ids
        ),
        db=DatabaseConfig(
            database=env['DATABASE'],
            db_host=env['DB_HOST'],
            db_user=env['DB_USER'],
            db_password=env['DB_PASSWORD']
        )
    )