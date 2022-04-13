from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_URL: str
    STOCK_PRICE_TIME_FRAME: int = 60  # the lowest/highest price so far in the day/hour (in minutes) the variable can be changed to set the timeframe at which highest/lowest stock prices could be monitored
    RETRY_TRANSACTION_COMMIT_TIME_FRAME: int = 60

settings = Settings()