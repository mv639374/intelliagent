from app.db.session import get_db

# This file can be used for common dependencies across the application.
# For now, we are just re-exporting get_db for consistency.
__all__ = ["get_db"]
