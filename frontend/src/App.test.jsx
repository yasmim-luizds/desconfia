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
  }, 15000);
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
  it.each([429, 503, 504])('preserva o texto digitado quando a análise falha com erro %s', async status => {
    mockRequests({ '/analyses': () => Promise.reject(Object.assign(new Error('O serviço está indisponível no momento. Tente novamente em instantes.'), { status })) });
    const user = userEvent.setup(); render(<App/>); await login(user);
    const campo = screen.getByLabelText('Qual mensagem você recebeu?');
    await user.type(campo, 'Mensagem importante que não pode sumir');
    await user.click(screen.getByLabelText(/Entendo que o texto/));
    await user.click(screen.getByRole('button', { name: 'Analisar mensagem' }));
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('O serviço está indisponível'));
    expect(campo).toHaveValue('Mensagem importante que não pode sumir');
  }, 15000);
  it('encerra a sessão ao receber erro 401 durante uma ação autenticada', async () => {
    mockRequests({ '/analyses': () => Promise.reject(Object.assign(new Error('Token expirado'), { status: 401 })) });
    const user = userEvent.setup(); render(<App/>); await login(user);
    await user.type(screen.getByLabelText('Qual mensagem você recebeu?'), 'Teste de sessão');
    await user.click(screen.getByLabelText(/Entendo que o texto/));
    await user.click(screen.getByRole('button', { name: 'Analisar mensagem' }));
    await waitFor(() => expect(screen.getByRole('alert')).toHaveTextContent('Sua sessão expirou. Entre novamente.'));
    expect(screen.getByRole('heading', { name: /Que bom ter você aqui/ })).toBeInTheDocument();
  }, 15000);
  it('mantém o registro no histórico quando a exclusão é cancelada', async () => {
    mockRequests(); const user = userEvent.setup(); render(<App/>); await login(user);
    await user.click(screen.getByRole('button', { name: 'Histórico', exact: true }));
    await screen.findByText('Texto original não armazenado');
    await user.click(screen.getByRole('button', { name: 'Excluir análise' }));
    await user.click(screen.getByRole('button', { name: 'Cancelar', exact: true }));
    expect(screen.getByText('Texto original não armazenado')).toBeInTheDocument();
    expect(request.mock.calls.some(([, options]) => options?.method === 'DELETE')).toBe(false);
  }, 15000);
  it('abre o resultado mesmo se o carregamento do feedback falhar', async () => {
    mockRequests({ '/analyses/a/feedback': () => Promise.reject(new Error('Falha no feedback')) });
    const user = userEvent.setup(); render(<App/>); await login(user);
    await user.click(screen.getByRole('button', { name: 'Histórico', exact: true }));
    await user.click(await screen.findByText('Texto original não armazenado'));
    await screen.findByText('Pare e confirme antes de agir.');
    expect(screen.getByText('Não foi possível carregar o status do feedback agora.')).toBeInTheDocument();
  }, 15000);
  it('encerra a sessão quando a consulta de feedback retorna 401', async () => {
    mockRequests({ '/analyses/a/feedback': () => Promise.reject(Object.assign(new Error('Token expirado'), { status: 401 })) });
    const user = userEvent.setup(); render(<App/>); await login(user);
    await user.click(screen.getByRole('button', { name: 'Histórico', exact: true }));
    await user.click(await screen.findByText('Texto original não armazenado'));
    await screen.findByText('Sua sessão expirou. Entre novamente.');
    expect(screen.getByRole('heading', { name: /Que bom ter você aqui/ })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: 'Sair' })).not.toBeInTheDocument();
  }, 15000);
  it('permite tentar carregar o feedback novamente após uma falha temporária', async () => {
    let attempts = 0;
    mockRequests({ '/analyses/a/feedback': async () => {
      attempts++;
      if (attempts === 1) throw Object.assign(new Error('Indisponível'), { status: 503 });
      return { is_helpful: true };
    } });
    const user = userEvent.setup(); render(<App/>); await login(user);
    await user.click(screen.getByRole('button', { name: 'Histórico', exact: true }));
    await user.click(await screen.findByText('Texto original não armazenado'));
    await user.click(await screen.findByRole('button', { name: 'Tentar carregar feedback novamente' }));
    await screen.findByText('Obrigado! Seu feedback foi registrado.');
    expect(attempts).toBe(2);
    expect(screen.queryByRole('button', { name: 'Enviar feedback' })).not.toBeInTheDocument();
  }, 15000);
  it('recupera o feedback salvo depois de um conflito sem repetir o envio', async () => {
    mockRequests({ '/analyses/a/feedback': async options => {
      if (options?.method === 'POST') throw Object.assign(new Error('Já recebido'), { status: 409 });
      return { is_helpful: true };
    } });
    const user = userEvent.setup(); render(<App/>); await login(user);
    await user.click(screen.getByRole('button', { name: 'Usar um exemplo' }));
    await user.click(screen.getByLabelText(/Entendo que o texto/));
    await user.click(screen.getByRole('button', { name: 'Analisar mensagem' }));
    await screen.findByText('Pare e confirme antes de agir.');
    await user.click(screen.getByRole('button', { name: 'Sim', exact: true }));
    await user.click(screen.getByRole('button', { name: 'Enviar feedback' }));
    await screen.findByText('Obrigado! Seu feedback foi registrado.');
    expect(request.mock.calls.filter(([path, options]) => path === '/analyses/a/feedback' && options?.method === 'POST')).toHaveLength(1);
  }, 15000);
  it.each([401, 503])('trata erro %s ao consultar o feedback após conflito', async status => {
    mockRequests({ '/analyses/a/feedback': async options => {
      throw Object.assign(new Error('Feedback indisponível'), { status: options?.method === 'POST' ? 409 : status });
    } });
    const user = userEvent.setup(); render(<App/>); await login(user);
    await user.click(screen.getByRole('button', { name: 'Usar um exemplo' }));
    await user.click(screen.getByLabelText(/Entendo que o texto/));
    await user.click(screen.getByRole('button', { name: 'Analisar mensagem' }));
    await screen.findByText('Pare e confirme antes de agir.');
    await user.click(screen.getByRole('button', { name: 'Sim', exact: true }));
    await user.click(screen.getByRole('button', { name: 'Enviar feedback' }));
    if (status === 401) {
      await screen.findByText('Sua sessão expirou. Entre novamente.');
    } else {
      await screen.findByRole('button', { name: 'Tentar carregar feedback novamente' });
      expect(screen.queryByText('Obrigado! Seu feedback foi registrado.')).not.toBeInTheDocument();
    }
  }, 15000);
});
