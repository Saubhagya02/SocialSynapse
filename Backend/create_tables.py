# create_tables.py
from app.database import engine, Base
from app.models import user, post, analytics  # Ensure all models are imported

Base.metadata.create_all(bind=engine)
print("All tables created!")
