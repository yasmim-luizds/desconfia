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
