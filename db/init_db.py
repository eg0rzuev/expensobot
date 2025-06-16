from db.models import Base
from db.db import engine

Base.metadata.create_all(engine)
print('Database initialized!')
