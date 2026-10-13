from datetime import datetime, timedelta

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import Analysis, AnalysisIndicator, IndicatorCategory, User
from app.security import hash_password

DEMO_EMAIL = 'aluno@example.com'
DEMO_PASSWORD = 'Desconfia123!'


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        user = db.scalar(select(User).where(User.email == DEMO_EMAIL))
        if not user:
            user = User(full_name='Usuário de Teste', email=DEMO_EMAIL, password_hash=hash_password(DEMO_PASSWORD))
            db.add(user)
            db.flush()
        else:
            user.full_name = 'Usuário de Teste'
            user.password_hash = hash_password(DEMO_PASSWORD)
            user.is_active = True

        if not db.scalar(select(Analysis).where(Analysis.user_id == user.id)):
            first = Analysis(user_id=user.id, message_text='Seu cadastro foi bloqueado. Faça um Pix urgente para regularizar.', risk_level='high', explanation='A mensagem combina urgência, ameaça de bloqueio e solicitação financeira.', recommendation='Não faça o Pix. Confirme a informação em um canal oficial.', ai_provider='local-seed', ai_model='rules-v0', created_at=datetime.utcnow() - timedelta(days=1), completed_at=datetime.utcnow() - timedelta(days=1))
            first.indicators = [
                AnalysisIndicator(category=IndicatorCategory.URGENCY.value, description='Senso de urgência', evidence='Uso da palavra urgente.'),
                AnalysisIndicator(category=IndicatorCategory.FINANCIAL_REQUEST.value, description='Solicitação financeira', evidence='Pedido explícito de Pix.'),
                AnalysisIndicator(category=IndicatorCategory.THREAT.value, description='Ameaça de bloqueio', evidence='A mensagem afirma que o cadastro foi bloqueado.'),
            ]
            second = Analysis(user_id=user.id, message_text='A reunião de amanhã foi confirmada para as 14h. Até lá.', risk_level='low', explanation='Nenhum sinal básico de golpe foi encontrado no texto.', recommendation='Confirme o remetente se a mensagem causar dúvida.', ai_provider='local-seed', ai_model='rules-v0', created_at=datetime.utcnow() - timedelta(hours=3), completed_at=datetime.utcnow() - timedelta(hours=3))
            db.add_all([first, second])
        db.commit()
        print(f'Banco pronto. Usuário de teste: {DEMO_EMAIL} / {DEMO_PASSWORD}')
    finally:
        db.close()


if __name__ == '__main__':
    seed()
