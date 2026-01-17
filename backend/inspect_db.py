from app.database import engine
from sqlalchemy import inspect

def inspect_db():
    inspector = inspect(engine)
    print("Tables found:", inspector.get_table_names())

if __name__ == "__main__":
    inspect_db()
