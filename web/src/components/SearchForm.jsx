import { formatarCnpj } from '../utils'

export default function SearchForm({ valor, onChange, onSubmit, carregando }) {
  function aoDigitar(evento) {
    onChange(formatarCnpj(evento.target.value))
  }

  function aoEnviar(evento) {
    evento.preventDefault()
    onSubmit()
  }

  return (
    <form className="busca" onSubmit={aoEnviar} noValidate>
      <label className="busca__label" htmlFor="cnpj">
        CNPJ da empresa
      </label>
      <div className="busca__linha">
        <input
          id="cnpj"
          className="busca__input"
          type="text"
          inputMode="numeric"
          autoComplete="off"
          placeholder="00.000.000/0000-00"
          value={valor}
          onChange={aoDigitar}
        />
        <button className="busca__botao" type="submit" disabled={carregando}>
          {carregando ? 'Consultando…' : 'Consultar'}
        </button>
      </div>
    </form>
  )
}
