const BASE = '/api'

async function requester(path, options) {
  let response
  try {
    response = await fetch(`${BASE}${path}`, options)
  } catch {
    throw new Error('Não foi possível falar com o servidor. Tente novamente.')
  }

  if (response.status === 204) return null

  const data = await response.json().catch(() => null)
  if (!response.ok) {
    throw new Error(data?.detail || 'Não foi possível concluir a consulta.')
  }
  return data
}

export function consultarCnpj(cnpj) {
  return requester(`/cnpj/${cnpj}`)
}

export function listarHistorico() {
  return requester('/historico')
}

export function removerDoHistorico(id) {
  return requester(`/historico/${id}`, { method: 'DELETE' })
}
