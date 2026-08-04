from app.database.connection import engine
from app.database.base import Base

# IMPORTANT: import models so they register
from app.models.stock_price import StockPrice


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("DONE: Tables created")
