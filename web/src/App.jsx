import { useCallback, useEffect, useState } from 'react'

import CompanyCard from './components/CompanyCard'
import HistoricoList from './components/HistoricoList'
import SearchForm from './components/SearchForm'
import { consultarCnpj, listarHistorico, removerDoHistorico } from './api'
import { apenasDigitos, formatarCnpj } from './utils'

export default function App() {
  const [cnpj, setCnpj] = useState('')
  const [empresa, setEmpresa] = useState(null)
  const [erro, setErro] = useState('')
  const [carregando, setCarregando] = useState(false)
  const [historico, setHistorico] = useState([])

  const carregarHistorico = useCallback(async () => {
    try {
      const dados = await listarHistorico()
      setHistorico(dados || [])
    } catch {
      // histórico é secundário: falha silenciosa
    }
  }, [])

  useEffect(() => {
    carregarHistorico()
  }, [carregarHistorico])

  async function consultar(valor) {
    const digitos = apenasDigitos(valor ?? cnpj)
    setErro('')

    if (digitos.length !== 14) {
      setEmpresa(null)
      setErro('Informe um CNPJ com 14 dígitos.')
      return
    }

    setCarregando(true)
    try {
      const dados = await consultarCnpj(digitos)
      setEmpresa(dados)
      await carregarHistorico()
    } catch (e) {
      setEmpresa(null)
      setErro(e.message)
    } finally {
      setCarregando(false)
    }
  }

  async function remover(id) {
    try {
      await removerDoHistorico(id)
      await carregarHistorico()
    } catch (e) {
      setErro(e.message)
    }
  }

  function selecionarDoHistorico(item) {
    setCnpj(formatarCnpj(item.cnpj))
    consultar(item.cnpj)
  }

  return (
    <div className="app">
      <header className="topo">
        <h1 className="topo__titulo">Consulta CNPJ</h1>
        <p className="topo__subtitulo">
          Dados públicos de empresas brasileiras direto da base da Receita Federal.
        </p>
      </header>

      <main className="conteudo">
        <div className="coluna-principal">
          <div className="cartao">
            <SearchForm
              valor={cnpj}
              onChange={setCnpj}
              onSubmit={() => consultar()}
              carregando={carregando}
            />
            {erro ? (
              <p className="alerta" role="alert">
                {erro}
              </p>
            ) : null}
          </div>

          {empresa ? (
            <CompanyCard empresa={empresa} />
          ) : (
            !erro && (
              <p className="dica">
                Digite o CNPJ de uma empresa para ver razão social, situação
                cadastral, endereço, atividade e quadro societário.
              </p>
            )
          )}
        </div>

        <aside className="coluna-lateral">
          <HistoricoList
            itens={historico}
            onSelecionar={selecionarDoHistorico}
            onRemover={remover}
          />
        </aside>
      </main>

      <footer className="rodape">
        Dados de <a href="https://brasilapi.com.br/docs#tag/CNPJ" target="_blank" rel="noreferrer">BrasilAPI</a> ·
        uso informativo, sem valor de certificação oficial.
      </footer>
    </div>
  )
}
