"""Cliente da BrasilAPI (dados públicos de CNPJ da Receita Federal).

Não exige chave/token: https://brasilapi.com.br/docs#tag/CNPJ
"""

import os
import re
from typing import Any

import httpx

from .cnpj import formatar_cnpj, normalizar_cnpj

BASE_URL = os.getenv("BRASILAPI_BASE_URL", "https://brasilapi.com.br/api")


class CnpjNaoEncontrado(Exception):
    """O CNPJ não existe na base consultada."""


class ProvedorIndisponivel(Exception):
    """A base pública não respondeu ou respondeu com erro."""


async def buscar_cnpj(digitos: str) -> dict[str, Any]:
    url = f"{BASE_URL}/cnpj/v1/{digitos}"
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(url, headers={"Accept": "application/json"})
    except httpx.HTTPError as exc:
        raise ProvedorIndisponivel(str(exc)) from exc

    if response.status_code == 404:
        raise CnpjNaoEncontrado(digitos)
    if response.status_code >= 400:
        raise ProvedorIndisponivel(f"HTTP {response.status_code}")

    return response.json()


def _formatar_cep(valor: str | None) -> str | None:
    digitos = re.sub(r"\D", "", valor or "")
    if len(digitos) != 8:
        return valor or None
    return f"{digitos[:5]}-{digitos[5:]}"


def _formatar_telefone(valor: str | None) -> str | None:
    digitos = re.sub(r"\D", "", valor or "")
    if len(digitos) < 10:
        return valor or None
    ddd, resto = digitos[:2], digitos[2:]
    corte = 5 if len(resto) == 9 else 4
    return f"({ddd}) {resto[:corte]}-{resto[corte:]}"


def normalizar_empresa(payload: dict[str, Any]) -> dict[str, Any]:
    """Converte o payload da BrasilAPI no formato usado pela interface."""
    logradouro = " ".join(
        parte
        for parte in (
            payload.get("descricao_tipo_de_logradouro"),
            payload.get("logradouro"),
        )
        if parte
    )

    socios = [
        {
            "nome": socio.get("nome_socio"),
            "qualificacao": socio.get("qualificacao_socio"),
            "entrada": socio.get("data_entrada_sociedade"),
            "faixa_etaria": socio.get("faixa_etaria"),
        }
        for socio in (payload.get("qsa") or [])
    ]

    capital = payload.get("capital_social")
    try:
        capital = float(capital) if capital is not None else None
    except (TypeError, ValueError):
        capital = None

    return {
        "cnpj": formatar_cnpj(normalizar_cnpj(payload.get("cnpj"))),
        "cnpj_digitos": normalizar_cnpj(payload.get("cnpj")),
        "razao_social": payload.get("razao_social"),
        "nome_fantasia": payload.get("nome_fantasia") or None,
        "situacao": payload.get("descricao_situacao_cadastral"),
        "data_situacao": payload.get("data_situacao_cadastral"),
        "data_inicio_atividade": payload.get("data_inicio_atividade"),
        "natureza_juridica": payload.get("natureza_juridica"),
        "porte": payload.get("porte"),
        "capital_social": capital,
        "cnae": payload.get("cnae_fiscal_descricao"),
        "cnae_codigo": payload.get("cnae_fiscal"),
        "email": payload.get("email") or None,
        "telefone": _formatar_telefone(payload.get("ddd_telefone_1")),
        "endereco": {
            "logradouro": logradouro,
            "numero": payload.get("numero"),
            "complemento": payload.get("complemento"),
            "bairro": payload.get("bairro"),
            "municipio": payload.get("municipio"),
            "uf": payload.get("uf"),
            "cep": _formatar_cep(payload.get("cep")),
        },
        "socios": socios,
        "optante_simples": payload.get("opcao_pelo_simples"),
        "optante_mei": payload.get("opcao_pelo_mei"),
    }
