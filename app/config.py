import os
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()

login_manager = LoginManager()


def get_supabase_client():
    """Return a Supabase client or None if not configured."""
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_ANON_KEY", "")
    if not url or not key or url.startswith("https://your-project"):
        return None
    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception:
        return None


def get_supabase_service_client():
    """Return a Supabase service-role client or None if not configured."""
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not url or not key or url.startswith("https://your-project"):
        return None
    try:
        from supabase import create_client
        return create_client(url, key)
    except Exception:
        return None


class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key-change-in-production")
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    WTF_CSRF_SSL_STRICT = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
