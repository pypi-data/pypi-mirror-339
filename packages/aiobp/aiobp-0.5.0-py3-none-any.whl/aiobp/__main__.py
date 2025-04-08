from aiobp.config.conf import loader

class SubConfig:
    port: int = 1234

class Config:
    sub: SubConfig
    users: dict[str, str] = {}
    ports: dict[str, bool] = {"http": 80}


config = loader(Config, "config.conf")
print(config.sub.port)
print(config.users)
print(config.ports)
