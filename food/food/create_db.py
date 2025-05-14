from models import Base
from db import engine

def main():
    Base.metadata.create_all(engine)
    print("✅ Database schema created.")

if __name__ == "__main__":
    main()
