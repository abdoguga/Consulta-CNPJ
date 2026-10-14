"""Normalização, formatação e validação de CNPJ."""

import re

_PESOS_DV1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
_PESOS_DV2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]


def normalizar_cnpj(valor: str | None) -> str:
    """Remove tudo que não for dígito."""
    return re.sub(r"\D", "", valor or "")


def formatar_cnpj(digitos: str) -> str:
    """14 dígitos -> 00.000.000/0000-00."""
    if len(digitos) != 14:
        return digitos
    return (
        f"{digitos[:2]}.{digitos[2:5]}.{digitos[5:8]}/"
        f"{digitos[8:12]}-{digitos[12:]}"
    )


def _digito_verificador(sequencia: str, pesos: list[int]) -> int:
    total = sum(int(digito) * peso for digito, peso in zip(sequencia, pesos))
    resto = total % 11
    return 0 if resto < 2 else 11 - resto


def validar_cnpj(valor: str | None) -> bool:
    """Valida tamanho e dígitos verificadores."""
    digitos = normalizar_cnpj(valor)
    if len(digitos) != 14 or len(set(digitos)) == 1:
        return False

    primeiro = _digito_verificador(digitos[:12], _PESOS_DV1)
    segundo = _digito_verificador(digitos[:12] + str(primeiro), _PESOS_DV2)
    return digitos[12] == str(primeiro) and digitos[13] == str(segundo)
