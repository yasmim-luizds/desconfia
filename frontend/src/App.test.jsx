import React from 'react';
import { describe, it, expect, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';
import { request } from './api';
vi.mock('./api', () => ({ request: vi.fn() }));
const session = { access_token: 'test', user: { full_name: 'Pessoa Teste' } };
const result = { id: 'a', risk_level: 'high', message_text: '', created_at: '2026-09-27T12:00:00', ai_provider: 'groq', explanation: 'Urgência e pagamento.', recommendation: 'Confirme por outro canal.', indicators: [{ description: 'Pedido financeiro' }] };
function mockRequests(overrides = {}) {
  request.mockImplementation(async (path, options) => {
    if (overrides[path]) return overrides[path](options);
    if (path === '/config') return { ai_mode: 'groq' };
    if (path === '/auth/login' || path === '/auth/register') return session;
    if (path === '/analyses') return result;
    if (path.startsWith('/analyses?')) return [result];
    if (path === '/analyses/a/feedback') return options?.method === 'POST' ? { is_helpful: true } : null;
    if (path === '/analyses/a') return result;
  });
}
async function login(user) {
  await user.click(screen.getByRole('button', { name: 'Entrar', exact: true }));
  await user.type(screen.getByLabelText('E-mail'), 'teste@example.com');
  await user.type(screen.getByLabelText('Senha', { exact: true }), 'Teste123!');
  await user.click(screen.getAllByRole('button', { name: 'Entrar', exact: true }).at(-1));
  await screen.findByText('Vamos olhar com calma.');
}
describe('Fluxos do Desconfia', () => {
  it('explica o produto e permite acessar cadastro', async () => {
    mockRequests(); const user = userEvent.setup(); render(<App/>);
    expect(screen.getByRole('heading', { name: /Antes de agir/ })).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Criar conta', exact: true }));
    expect(screen.getByLabelText('Confirme a senha')).toBeInTheDocument();
  });
  it('impede cadastro quando as senhas são diferentes', async () => {
    mockRequests(); const user = userEvent.setup(); render(<App/>);
    await user.click(screen.getByRole('button', { name: 'Criar conta', exact: true }));
    await user.type(screen.getByLabelText('Nome'), 'Pessoa Teste');
    await user.type(screen.getByLabelText('E-mail'), 'teste@example.com');
    await user.type(screen.getByLabelText('Senha', { exact: true }), 'Teste123!');
    await user.type(screen.getByLabelText('Confirme a senha'), 'Diferente123!');
    await user.click(screen.getAllByRole('button', { name: 'Criar conta', exact: true }).at(-1));
    expect(screen.getByRole('alert')).toHaveTextContent('As senhas precisam ser iguais');
    expect(request.mock.calls.some(([path]) => path === '/auth/register')).toBe(false);
  });
  it('analisa, mostra resultado, envia feedback e faz logout', async () => {
    mockRequests(); const user = userEvent.setup(); render(<App/>); await login(user);
    expect(screen.getByRole('button', { name: 'Analisar mensagem' })).toBeDisabled();
    await user.type(screen.getByLabelText('Qual mensagem você recebeu?'), 'Faça Pix agora');
    await user.click(screen.getByLabelText(/Entendo que o texto/));
    await user.click(screen.getByRole('button', { name: 'Analisar mensagem' }));
    await screen.findByText('Pare e confirme antes de agir.');
    expect(request).toHaveBeenCalledWith('/analyses', expect.objectContaining({ body: { message_text: 'Faça Pix agora', store_message: false } }));
    expect(screen.getByText('Confirme por outro canal.')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Sim', exact: true }));
    await user.click(screen.getByRole('button', { name: 'Enviar feedback' }));
    await screen.findByRole('status');
    await user.click(screen.getByRole('button', { name: 'Sair' }));
    expect(screen.getByRole('heading', { name: /Antes de agir/ })).toBeInTheDocument();
  });
  it('mostra carregamento e erro sem inventar resultado', async () => {
    let rejectRequest;
    mockRequests({ '/analyses': () => new Promise((resolve, reject) => { rejectRequest = reject; }) });
    const user = userEvent.setup(); render(<App/>); await login(user);
    await user.click(screen.getByRole('button', { name: 'Usar um exemplo' }));
    await user.click(screen.getByLabelText(/Entendo que o texto/));
    await user.click(screen.getByRole('button', { name: 'Analisar mensagem' }));
    expect(screen.getByRole('button', { name: /Analisando com cuidado/ })).toBeDisabled();
    rejectRequest(new Error('IA indisponível'));
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('IA indisponível'));
    expect(screen.queryByText('O que a mensagem indica')).not.toBeInTheDocument();
  });
  it('carrega histórico e exige confirmação para excluir', async () => {
    mockRequests(); const user = userEvent.setup(); render(<App/>); await login(user);
    await user.click(screen.getByRole('button', { name: 'Histórico', exact: true }));
    await screen.findByText('Texto original não armazenado');
    await user.click(screen.getByRole('button', { name: 'Excluir análise' }));
    expect(screen.getByText('Excluir esta análise e seu feedback?')).toBeInTheDocument();
    await user.click(screen.getByRole('button', { name: 'Excluir', exact: true }));
    await screen.findByText('Seu histórico começa aqui.');
    expect(request).toHaveBeenCalledWith('/analyses/a', expect.objectContaining({ method: 'DELETE' }));
  });
});
