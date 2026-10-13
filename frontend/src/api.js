export async function request(path, { token, method = 'GET', body, signal } = {}) {
  let response;
  try {
    response = await fetch(path, { method, signal, headers: { ...(body ? { 'Content-Type': 'application/json' } : {}), ...(token ? { Authorization: `Bearer ${token}` } : {}) }, ...(body ? { body: JSON.stringify(body) } : {}) });
  } catch (error) {
    if (error.name === 'AbortError') throw error;
    throw new Error('Não foi possível conectar. Verifique sua conexão e tente novamente.');
  }
  if (response.status === 204) return null;
  let data;
  try { data = await response.json(); } catch { throw new Error('O serviço retornou uma resposta inesperada. Tente novamente.'); }
  if (!response.ok) {
    const error = new Error(typeof data.detail === 'string' ? data.detail : 'Confira os campos preenchidos e tente novamente.');
    error.status = response.status;
    throw error;
  }
  return data;
}
