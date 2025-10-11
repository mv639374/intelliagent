from sqlalchemy.orm import declarative_base

# This is the single source of truth for the declarative base.
# All models will inherit from this Base.
Base = declarative_base()