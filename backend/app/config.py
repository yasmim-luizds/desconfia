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
if PRODUCTION and not os.getenv('GROQ_API_KEY', '').strip():
    raise RuntimeError('Configure GROQ_API_KEY antes de iniciar em produção.')


def positive_int(name: str, default: int) -> int:
    try:
        value = int(os.getenv(name, str(default)))
    except ValueError:
        raise RuntimeError(f'{name} deve ser um inteiro positivo.') from None
    if value < 1:
        raise RuntimeError(f'{name} deve ser um inteiro positivo.')
    return value


# Application budgets, not a claim about the provider's plan or token allowance.
AI_GLOBAL_PER_MINUTE = positive_int('AI_GLOBAL_PER_MINUTE', 20)
AI_GLOBAL_PER_DAY = positive_int('AI_GLOBAL_PER_DAY', 200)
