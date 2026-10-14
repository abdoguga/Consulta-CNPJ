import {
  classeSituacao,
  formatarData,
  formatarDataHora,
  formatarMoeda,
} from '../utils'

function Campo({ rotulo, valor }) {
  return (
    <div className="campo">
      <span className="campo__rotulo">{rotulo}</span>
      <span className="campo__valor">{valor || '—'}</span>
    </div>
  )
}

export default function CompanyCard({ empresa }) {
  if (!empresa) return null

  const { endereco = {}, socios = [] } = empresa

  const linhaEndereco = [
    [endereco.logradouro, endereco.numero].filter(Boolean).join(', '),
    endereco.complemento,
    endereco.bairro,
    [endereco.municipio, endereco.uf].filter(Boolean).join(' - '),
    endereco.cep,
  ]
    .filter(Boolean)
    .join(' · ')

  return (
    <article className="empresa">
      <header className="empresa__cabecalho">
        <div>
          <h2 className="empresa__razao">{empresa.razao_social || 'Razão social não informada'}</h2>
          {empresa.nome_fantasia ? (
            <p className="empresa__fantasia">{empresa.nome_fantasia}</p>
          ) : null}
          <p className="empresa__cnpj">{empresa.cnpj}</p>
        </div>
        <span className={classeSituacao(empresa.situacao)}>
          {empresa.situacao || 'Situação não informada'}
        </span>
      </header>

      <div className="empresa__grade">
        <Campo rotulo="Início de atividade" valor={formatarData(empresa.data_inicio_atividade)} />
        <Campo rotulo="Natureza jurídica" valor={empresa.natureza_juridica} />
        <Campo rotulo="Porte" valor={empresa.porte} />
        <Campo rotulo="Capital social" valor={formatarMoeda(empresa.capital_social)} />
        <Campo rotulo="Atividade principal" valor={empresa.cnae} />
        <Campo rotulo="Telefone" valor={empresa.telefone} />
        <Campo rotulo="E-mail" valor={empresa.email} />
        <Campo
          rotulo="Simples / MEI"
          valor={[empresa.optante_simples ? 'Simples Nacional' : null, empresa.optante_mei ? 'MEI' : null]
            .filter(Boolean)
            .join(' · ') || 'Não'}
        />
      </div>

      <section className="empresa__secao">
        <h3 className="empresa__titulo">Endereço</h3>
        <p className="empresa__texto">{linhaEndereco || 'Endereço não informado'}</p>
      </section>

      <section className="empresa__secao">
        <h3 className="empresa__titulo">Quadro societário</h3>
        {socios.length === 0 ? (
          <p className="empresa__texto">Nenhum sócio informado.</p>
        ) : (
          <ul className="socios">
            {socios.map((socio, indice) => (
              <li key={`${socio.nome}-${indice}`} className="socios__item">
                <span className="socios__nome">{socio.nome || 'Não informado'}</span>
                <span className="socios__qualificacao">{socio.qualificacao || '—'}</span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <footer className="empresa__rodape">
        {empresa.total_consultas > 1
          ? `Consultado ${empresa.total_consultas} vezes · `
          : ''}
        Última consulta em {formatarDataHora(empresa.ultima_consulta)}
      </footer>
    </article>
  )
}
