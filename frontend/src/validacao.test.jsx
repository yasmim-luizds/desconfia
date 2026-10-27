import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';
import { request } from './api';
vi.mock('./api', () => ({ request: vi.fn() }));
beforeEach(() => {
  request.mockReset();
  request.mockImplementation(async path => (path === '/config' ? { ai_mode: 'groq' } : null));
});
describe('Validação dos campos de acesso', () => {
  it('mostra mensagens por campo ao tentar entrar sem preencher', async () => {
    const user = userEvent.setup(); render(<App/>);
    await user.click(screen.getByRole('button', { name: 'Entrar', exact: true }));
    await user.click(screen.getAllByRole('button', { name: 'Entrar', exact: true }).at(-1));
    expect(screen.getByText('Informe um e-mail válido, como voce@exemplo.com.')).toBeInTheDocument();
    expect(screen.getByText('Informe sua senha.')).toBeInTheDocument();
    expect(request.mock.calls.some(([path]) => path === '/auth/login')).toBe(false);
  });
  it('exige senha com pelo menos 8 caracteres no cadastro', async () => {
    const user = userEvent.setup(); render(<App/>);
    await user.click(screen.getByRole('button', { name: 'Criar conta', exact: true }));
    await user.type(screen.getByLabelText('Nome'), 'Pessoa Teste');
    await user.type(screen.getByLabelText('E-mail'), 'teste@example.com');
    await user.type(screen.getByLabelText('Senha', { exact: true }), 'curta');
    await user.type(screen.getByLabelText('Confirme a senha'), 'curta');
    await user.click(screen.getAllByRole('button', { name: 'Criar conta', exact: true }).at(-1));
    expect(screen.getByText('A senha precisa ter pelo menos 8 caracteres.')).toBeInTheDocument();
    expect(request.mock.calls.some(([path]) => path === '/auth/register')).toBe(false);
  });
});
it('mostra o erro de senhas diferentes abaixo do campo de confirmação', async () => {
  const user = userEvent.setup(); render(<App/>);
  await user.click(screen.getByRole('button', { name: 'Criar conta', exact: true }));
  await user.type(screen.getByLabelText('Nome'), 'Pessoa Teste');
  await user.type(screen.getByLabelText('E-mail'), 'teste@example.com');
  await user.type(screen.getByLabelText('Senha', { exact: true }), 'Teste1234!');
  await user.type(screen.getByLabelText('Confirme a senha'), 'Outra1234!');
  await user.click(screen.getAllByRole('button', { name: 'Criar conta', exact: true }).at(-1));
  expect(screen.getByLabelText('Confirme a senha')).toHaveAttribute('aria-invalid', 'true');
  expect(screen.getByRole('alert')).toHaveTextContent('As senhas precisam ser iguais');
  expect(request.mock.calls.some(([path]) => path === '/auth/register')).toBe(false);
});
it('permite mostrar e ocultar a senha', async () => {
  const user = userEvent.setup(); render(<App/>);
  await user.click(screen.getByRole('button', { name: 'Entrar', exact: true }));
  const senha = screen.getByLabelText('Senha', { exact: true });
  expect(senha).toHaveAttribute('type', 'password');
  await user.click(screen.getByLabelText('Mostrar senha'));
  expect(senha).toHaveAttribute('type', 'text');
  await user.click(screen.getByLabelText('Mostrar senha'));
  expect(senha).toHaveAttribute('type', 'password');
});
it('mostra o erro de login junto ao botão, e não no topo da página', async () => {
  request.mockImplementation(async path => {
    if (path === '/config') return { ai_mode: 'groq' };
    if (path === '/auth/login') throw Object.assign(new Error('E-mail ou senha inválidos.'), { status: 401 });
    return null;
  });
  const user = userEvent.setup(); render(<App/>);
  await user.click(screen.getByRole('button', { name: 'Entrar', exact: true }));
  await user.type(screen.getByLabelText('E-mail'), 'teste@example.com');
  await user.type(screen.getByLabelText('Senha', { exact: true }), 'SenhaErrada1!');
  await user.click(screen.getAllByRole('button', { name: 'Entrar', exact: true }).at(-1));
  const alerta = await screen.findByRole('alert');
  expect(alerta).toHaveTextContent('E-mail ou senha inválidos');
  expect(alerta.closest('form')).not.toBeNull();
});
