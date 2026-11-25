
import re

PLACA_ANTIGA = re.compile(r"^[A-Z]{3}[0-9]{4}$")
PLACA_MERCOSUL = re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$")


def somente_digitos(texto):
    return re.sub(r"\D", "", texto or "")


# ---------- CPF ----------

def _digito_cpf(numeros):
    peso = len(numeros) + 1
    soma = sum(int(n) * (peso - i) for i, n in enumerate(numeros))
    resto = (soma * 10) % 11
    return "0" if resto == 10 else str(resto)


def validar_cpf(cpf):
    """Retorna o CPF só com dígitos. Lança ValueError se for inválido."""
    numeros = somente_digitos(cpf)

    if len(numeros) != 11:
        raise ValueError("O CPF deve ter 11 dígitos.")

    if numeros == numeros[0] * 11:
        raise ValueError("CPF inválido.")

    primeiro = _digito_cpf(numeros[:9])
    segundo = _digito_cpf(numeros[:9] + primeiro)

    if numeros[9:] != primeiro + segundo:
        raise ValueError("CPF inválido.")

    return numeros


def formatar_cpf(cpf):
    n = somente_digitos(cpf)
    if len(n) != 11:
        return cpf
    return f"{n[:3]}.{n[3:6]}.{n[6:9]}-{n[9:]}"


def mascara_cpf(texto):
    n = somente_digitos(texto)[:11]
    partes = [n[:3], n[3:6], n[6:9]]
    resultado = ".".join(p for p in partes if p)
    if len(n) > 9:
        resultado += "-" + n[9:]
    return resultado


# ---------- Telefone ----------

def validar_telefone(telefone):
    """Aceita fixo (10 dígitos) ou celular (11 dígitos, começa com 9)."""
    numeros = somente_digitos(telefone)

    if len(numeros) not in (10, 11):
        raise ValueError(
            "O telefone deve ter DDD + número (10 ou 11 dígitos)."
        )

    if int(numeros[:2]) < 11:
        raise ValueError("DDD inválido.")

    if len(numeros) == 11 and numeros[2] != "9":
        raise ValueError("Celular deve começar com 9 após o DDD.")

    return numeros


def formatar_telefone(telefone):
    n = somente_digitos(telefone)
    if len(n) == 11:
        return f"({n[:2]}) {n[2:7]}-{n[7:]}"
    if len(n) == 10:
        return f"({n[:2]}) {n[2:6]}-{n[6:]}"
    return telefone


def mascara_telefone(texto):
    n = somente_digitos(texto)[:11]
    if not n:
        return ""
    if len(n) <= 2:
        return f"({n}"

    corte = 7 if len(n) == 11 else 6
    resultado = f"({n[:2]}) {n[2:corte]}"
    if len(n) > corte:
        resultado += "-" + n[corte:]
    return resultado


# ---------- Placa ----------

def normalizar_placa(placa):
    return re.sub(r"[^A-Za-z0-9]", "", placa or "").upper()


def tipo_placa(placa):
    """Retorna 'Mercosul', 'Antiga' ou None."""
    p = normalizar_placa(placa)
    if PLACA_MERCOSUL.match(p):
        return "Mercosul"
    if PLACA_ANTIGA.match(p):
        return "Antiga"
    return None


def validar_placa(placa):
    """Retorna a placa normalizada (7 caracteres, sem hífen)."""
    p = normalizar_placa(placa)

    if tipo_placa(p) is None:
        raise ValueError(
            "Placa inválida.\n"
            "Use o padrão Mercosul (ABC1D23) "
            "ou o modelo antigo (ABC-1234)."
        )

    return p


def formatar_placa(placa):
    p = normalizar_placa(placa)
    if tipo_placa(p) == "Antiga":
        return f"{p[:3]}-{p[3:]}"
    return p


def mascara_placa(texto):
    p = normalizar_placa(texto)[:7]
    if len(p) == 7 and PLACA_ANTIGA.match(p):
        return f"{p[:3]}-{p[3:]}"
    return p
