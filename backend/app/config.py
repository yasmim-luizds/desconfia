import os
import secrets
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')
PRODUCTION = os.getenv('APP_ENV') == 'production'
SECRET_KEY = os.getenv('DESCONFIA_SECRET_KEY') or secrets.token_urlsafe(48)
if PRODUCTION and (not os.getenv('DESCONFIA_SECRET_KEY') or len(SECRET_KEY) < 32):
    raise RuntimeError('Configure DESCONFIA_SECRET_KEY com pelo menos 32 caracteres.')
AI_MODE = os.getenv('AI_MODE', 'groq')
if AI_MODE not in ('groq', 'demo') or (PRODUCTION and AI_MODE != 'groq'):
    raise RuntimeError('AI_MODE deve ser groq; demo somente em desenvolvimento.')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'openai/gpt-oss-20b')
