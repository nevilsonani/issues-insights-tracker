from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Import all models so that metadata.create_all works
import app.models.issue
import app.models.stats
import app.models.user
