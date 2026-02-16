from app.db.base import Base
from app.db.session import engine
from app.models import task  # Import models to ensure they are registered with Base

def init_db():
    """
    Initializes the database by creating all tables defined in Base.
    """
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
