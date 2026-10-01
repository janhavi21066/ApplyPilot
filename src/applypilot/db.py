from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from applypilot.config import settings
engine = create_engine(settings.database_url)
echo = True
SessionLocal = sessionmaker(bind=engine)
class Base(DeclarativeBase):
    pass

