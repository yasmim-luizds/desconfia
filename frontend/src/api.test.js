import { afterEach, expect, it, vi } from 'vitest';
import { request } from './api';
afterEach(() => vi.unstubAllGlobals());
it('normaliza erros de validação sem renderizar objetos', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 422, json: async () => ({ detail: [{ msg: 'Invalid' }] }) }));
  await expect(request('/test')).rejects.toThrow('Confira os campos');
});
it('preserva o status de autenticação para encerrar a sessão', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 401, json: async () => ({ detail: 'Token inválido' }) }));
  await expect(request('/test')).rejects.toMatchObject({ status: 401 });
});
it('trata falta de conexão', async () => {
  vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Network')));
  await expect(request('/test')).rejects.toThrow('Não foi possível conectar');
});
it('informa indisponibilidade quando o servidor falha sem responder em JSON', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 502, json: async () => { throw new Error('não é JSON'); } }));
  await expect(request('/test')).rejects.toThrow('O serviço está indisponível');
});
it('mantém resposta inesperada quando uma resposta sem erro de servidor não é JSON', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: true, status: 200, json: async () => { throw new Error('não é JSON'); } }));
  await expect(request('/test')).rejects.toThrow('O serviço retornou uma resposta inesperada');
});
it('usa mensagem clara de login quando o servidor não envia texto', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 401, json: async () => ({}) }));
  await expect(request('/test')).rejects.toThrow('E-mail ou senha incorretos');
});
it('orienta a aguardar quando há excesso de solicitações', async () => {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue({ ok: false, status: 429, json: async () => ({}) }));
  await expect(request('/test')).rejects.toThrow('Aguarde um instante');
});