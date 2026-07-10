from slowapi import Limiter
from slowapi.util import get_remote_address
from utils.config import settings

limiter = Limiter(key_func=get_remote_address, enabled=not settings.TESTING,)