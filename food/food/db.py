import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://fooduser:foodpass@localhost:5432/fooddb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
