"""API da aplicação Consulta CNPJ."""

from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from .brasilapi import (
    CnpjNaoEncontrado,
    ProvedorIndisponivel,
    buscar_cnpj,
    normalizar_empresa,
)
from .cnpj import formatar_cnpj, normalizar_cnpj, validar_cnpj
from .db import get_db
from .models import Consulta

app = FastAPI(title="Consulta CNPJ", version="1.0.0")


def _serializar(registro: Consulta) -> dict:
    return {
        "id": registro.id,
        "cnpj": formatar_cnpj(registro.cnpj),
        "cnpj_digitos": registro.cnpj,
        "razao_social": registro.razao_social,
        "nome_fantasia": registro.nome_fantasia,
        "situacao": registro.situacao,
        "municipio": registro.municipio,
        "uf": registro.uf,
        "total_consultas": registro.total_consultas,
        "ultima_consulta": registro.ultima_consulta.isoformat()
        if registro.ultima_consulta
        else None,
    }


def _registrar_consulta(db: Session, digitos: str, empresa: dict) -> Consulta:
    registro = db.scalar(select(Consulta).where(Consulta.cnpj == digitos))
    if registro is None:
        registro = Consulta(cnpj=digitos)
        db.add(registro)
    else:
        registro.total_consultas += 1

    registro.razao_social = empresa["razao_social"]
    registro.nome_fantasia = empresa["nome_fantasia"]
    registro.situacao = empresa["situacao"]
    registro.municipio = empresa["endereco"]["municipio"]
    registro.uf = empresa["endereco"]["uf"]
    registro.ultima_consulta = datetime.now(timezone.utc)

    db.commit()
    db.refresh(registro)
    return registro


@app.get("/api/cnpj/{cnpj}")
async def consultar_cnpj(cnpj: str, db: Session = Depends(get_db)) -> dict:
    digitos = normalizar_cnpj(cnpj)
    if not validar_cnpj(digitos):
        raise HTTPException(status_code=400, detail="CNPJ inválido. Informe 14 dígitos.")

    try:
        payload = await buscar_cnpj(digitos)
    except CnpjNaoEncontrado:
        raise HTTPException(
            status_code=404, detail="CNPJ não encontrado na base da Receita Federal."
        )
    except ProvedorIndisponivel as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Não foi possível consultar a base pública de CNPJ ({exc}).",
        ) from exc

    empresa = normalizar_empresa(payload)
    registro = _registrar_consulta(db, digitos, empresa)

    return {
        **empresa,
        "id": registro.id,
        "total_consultas": registro.total_consultas,
        "ultima_consulta": registro.ultima_consulta.isoformat()
        if registro.ultima_consulta
        else None,
    }


@app.get("/api/historico")
def listar_historico(
    limit: int = Query(default=10, ge=1, le=50), db: Session = Depends(get_db)
) -> list[dict]:
    registros = db.scalars(
        select(Consulta).order_by(Consulta.ultima_consulta.desc()).limit(limit)
    ).all()
    return [_serializar(registro) for registro in registros]


@app.delete("/api/historico/{consulta_id}", status_code=204)
def remover_historico(consulta_id: int, db: Session = Depends(get_db)) -> None:
    registro = db.get(Consulta, consulta_id)
    if registro is None:
        raise HTTPException(status_code=404, detail="Consulta não encontrada.")
    db.delete(registro)
    db.commit()
