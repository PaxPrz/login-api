from dataclasses import dataclass, field


@dataclass
class AppSettings:
    database: str
    jwt_secret: str
    jwt_algo: str


def create_app_settings(
    database: str,
    jwt_secret: str,
    jwt_algo: str = "HS256",
):
    return AppSettings(
        database=database,
        jwt_secret=jwt_secret,
        jwt_algo=jwt_algo,
    )
