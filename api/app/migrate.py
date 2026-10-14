"""Cria as tabelas do banco (executado uma vez pela plataforma/compose)."""

import time

from sqlalchemy.exc import OperationalError

from .db import engine
from .models import Base


def main() -> None:
    for tentativa in range(1, 11):
        try:
            Base.metadata.create_all(engine)
            print("Banco de dados pronto: tabelas verificadas.")
            return
        except OperationalError as exc:
            print(f"Banco indisponível (tentativa {tentativa}/10): {exc}")
            time.sleep(2)

    raise SystemExit("Não foi possível conectar ao banco de dados.")


if __name__ == "__main__":
    main()
