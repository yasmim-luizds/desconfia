from datetime import datetime
from pathlib import Path
import os
import logging

from fastapi import Depends, FastAPI, HTTPException, status, Request, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, text
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session, selectinload

from .database import Base, engine, get_db
from .models import Analysis, AnalysisIndicator, Feedback, IndicatorCategory, RiskLevel, User
from .schemas import (
    AnalysisCreateRequest,
    AnalysisResponse,
    FeedbackRequest,
    FeedbackResponse,
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from .security import create_access_token, get_current_user, hash_password, normalize_email, verify_password
from . import ai
from .config import AI_MODE, GROQ_MODEL
from .limits import check_limit

logging.basicConfig(level=logging.INFO)
Base.metadata.create_all(bind=engine)
app = FastAPI(title='Desconfia API', version='0.1.0', description='API local para análise de mensagens suspeitas.')
app.add_middleware(CORSMiddleware, allow_origins=os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173').split(','), allow_methods=['GET', 'POST', 'DELETE'], allow_headers=['Authorization', 'Content-Type'])


@app.middleware('http')
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['X-Frame-Options'] = 'DENY'
    if not request.url.path.startswith('/assets/'):
        response.headers['Cache-Control'] = 'no-store'
    return response


@app.get('/config')
def public_config():
    return {'ai_mode': AI_MODE, 'max_message_length': 2000}

FRONTEND_DIST = Path(__file__).resolve().parents[2] / 'frontend' / 'dist'


def serialize_analysis(analysis: Analysis) -> AnalysisResponse:
    return AnalysisResponse.model_validate(analysis)


def local_analyze(message: str) -> tuple[RiskLevel, str, str, list[tuple[IndicatorCategory, str, str]]]:
    lower = message.lower()
    rules = [
        (('pix', 'transferência', 'transferencia', 'pagamento', 'depósito', 'deposito'), IndicatorCategory.FINANCIAL_REQUEST, 'Solicitação de pagamento ou transferência', 'A mensagem menciona uma movimentação financeira.'),
        (('urgente', 'agora', 'imediatamente', 'última chance', 'ultima chance'), IndicatorCategory.URGENCY, 'Senso de urgência', 'A mensagem tenta acelerar a decisão do destinatário.'),
        (('senha', 'código', 'codigo', 'token', 'login'), IndicatorCategory.CREDENTIAL_REQUEST, 'Pedido de credencial ou código', 'A mensagem pode tentar obter um dado de autenticação.'),
        (('bloqueado', 'bloqueada', 'cancelada', 'suspensa'), IndicatorCategory.THREAT, 'Ameaça de bloqueio ou suspensão', 'A mensagem usa uma consequência negativa para pressionar a pessoa.'),
        (('prêmio', 'premio', 'sorteio', 'ganhou', 'benefício', 'beneficio'), IndicatorCategory.PRIZE_OR_BENEFIT, 'Promessa inesperada de benefício', 'A mensagem anuncia vantagem ou prêmio sem contexto confirmado.'),
        (('clique', 'http://', 'https://', 'link'), IndicatorCategory.SUSPICIOUS_LINK, 'Possível link suspeito', 'A mensagem orienta o destinatário a acessar um link ou clicar.'),
    ]
    indicators = [(category, description, evidence) for keywords, category, description, evidence in rules if any(word in lower for word in keywords)]
    if len(indicators) >= 2:
        risk = RiskLevel.HIGH
        explanation = 'A mensagem combina sinais de engenharia social que podem indicar uma tentativa de golpe.'
        recommendation = 'Não faça pagamentos nem informe códigos. Confirme a solicitação por um canal oficial e independente.'
    elif indicators:
        risk = RiskLevel.MEDIUM
        explanation = 'A mensagem contém pelo menos um sinal que merece verificação antes de qualquer ação.'
        recommendation = 'Verifique a origem da mensagem por outro canal antes de clicar, responder ou compartilhar dados.'
    else:
        risk = RiskLevel.LOW
        explanation = 'Nenhum dos sinais básicos configurados no protótipo foi identificado.'
        recommendation = 'Mesmo assim, confirme o remetente e evite compartilhar dados pessoais sem necessidade.'
    return risk, explanation, recommendation, indicators


@app.get('/health')
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text('SELECT 1'))
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503, detail='Banco de dados indisponível') from exc
    return {'status': 'ok', 'database': 'connected'}


@app.post('/auth/register', response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    check_limit('auth:' + (request.client.host if request.client else 'unknown'), 20)
    email = normalize_email(str(payload.email))
    if db.scalar(select(User).where(User.email == email)):
        raise HTTPException(status_code=409, detail='E-mail já cadastrado')
    user = User(full_name=payload.full_name.strip(), email=email, password_hash=hash_password(payload.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail='E-mail já cadastrado') from exc
    db.refresh(user)
    return TokenResponse(access_token=create_access_token(user.id), user=user)


@app.post('/auth/login', response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)) -> TokenResponse:
    check_limit('auth:' + (request.client.host if request.client else 'unknown'), 20)
    user = db.scalar(select(User).where(User.email == normalize_email(str(payload.email))))
    if not user or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='E-mail ou senha inválidos')
    return TokenResponse(access_token=create_access_token(user.id), user=user)


@app.get('/me', response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@app.post('/analyses', response_model=AnalysisResponse, status_code=status.HTTP_201_CREATED)
def create_analysis(payload: AnalysisCreateRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Analysis:
    check_limit('analysis:' + current_user.id, 10)
    if AI_MODE == 'demo':
        risk, explanation, recommendation, indicators = local_analyze(payload.message_text)
    else:
        try:
            result = ai.analyze(payload.message_text)
        except ai.AIError as exc:
            raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
        risk, explanation, recommendation = result.risk_level, result.explanation, result.recommendation
        indicators = [(item.category, item.description, item.evidence) for item in result.indicators]
    analysis = Analysis(user_id=current_user.id, message_text=payload.message_text if payload.store_message else '', risk_level=risk.value, explanation=explanation, recommendation=recommendation, ai_provider='local-demo' if AI_MODE == 'demo' else 'groq', ai_model='rules-v0' if AI_MODE == 'demo' else GROQ_MODEL, completed_at=datetime.utcnow())
    for category, description, evidence in indicators:
        analysis.indicators.append(AnalysisIndicator(category=category.value, description=description, evidence=evidence if payload.store_message else None))
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return db.scalar(select(Analysis).options(selectinload(Analysis.indicators)).where(Analysis.id == analysis.id))


@app.get('/analyses', response_model=list[AnalysisResponse])
def list_analyses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db), limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)) -> list[Analysis]:
    return list(db.scalars(select(Analysis).options(selectinload(Analysis.indicators)).where(Analysis.user_id == current_user.id).order_by(Analysis.created_at.desc(), Analysis.id).offset(offset).limit(limit)).unique().all())


@app.get('/analyses/{analysis_id}', response_model=AnalysisResponse)
def get_analysis(analysis_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Analysis:
    analysis = db.scalar(select(Analysis).options(selectinload(Analysis.indicators)).where(Analysis.id == analysis_id, Analysis.user_id == current_user.id))
    if not analysis:
        raise HTTPException(status_code=404, detail='Análise não encontrada')
    return analysis


@app.post('/analyses/{analysis_id}/feedback', response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def create_feedback(analysis_id: str, payload: FeedbackRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> Feedback:
    analysis = db.scalar(select(Analysis).where(Analysis.id == analysis_id, Analysis.user_id == current_user.id))
    if not analysis:
        raise HTTPException(status_code=404, detail='Análise não encontrada')
    if db.scalar(select(Feedback).where(Feedback.analysis_id == analysis_id, Feedback.user_id == current_user.id)):
        raise HTTPException(status_code=409, detail='Esta análise já recebeu feedback')
    feedback = Feedback(analysis_id=analysis_id, user_id=current_user.id, is_helpful=payload.is_helpful, comment=payload.comment)
    db.add(feedback)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail='Esta análise já recebeu feedback') from exc
    db.refresh(feedback)
    return feedback


@app.delete('/analyses/{analysis_id}', status_code=204)
def delete_analysis(analysis_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    analysis = get_analysis(analysis_id, current_user, db)
    db.delete(analysis)
    db.commit()
    return Response(status_code=204)


@app.get('/analyses/{analysis_id}/feedback', response_model=FeedbackResponse | None)
def get_feedback(analysis_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    get_analysis(analysis_id, current_user, db)
    return db.scalar(select(Feedback).where(Feedback.analysis_id == analysis_id, Feedback.user_id == current_user.id))


if FRONTEND_DIST.exists():
    app.mount('/', StaticFiles(directory=FRONTEND_DIST, html=True), name='frontend')
