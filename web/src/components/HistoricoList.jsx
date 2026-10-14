import { formatarDataHora } from '../utils'

export default function HistoricoList({ itens, onSelecionar, onRemover }) {
  return (
    <section className="historico">
      <h2 className="historico__titulo">Consultas recentes</h2>

      {itens.length === 0 ? (
        <p className="historico__vazio">
          Nenhuma consulta ainda. Busque um CNPJ para começar.
        </p>
      ) : (
        <ul className="historico__lista">
          {itens.map((item) => (
            <li key={item.id} className="historico__item">
              <button
                type="button"
                className="historico__principal"
                onClick={() => onSelecionar(item)}
                title={`Consultar ${item.cnpj} novamente`}
              >
                <span className="historico__razao">
                  {item.razao_social || 'Razão social não informada'}
                </span>
                <span className="historico__cnpj">{item.cnpj}</span>
                <span className="historico__meta">
                  {item.total_consultas}x · {formatarDataHora(item.ultima_consulta)}
                </span>
              </button>
              <button
                type="button"
                className="historico__remover"
                aria-label={`Remover ${item.cnpj} do histórico`}
                onClick={() => onRemover(item.id)}
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  )
}
