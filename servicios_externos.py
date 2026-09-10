import httpx
from fastapi import HTTPException, status


async def obtener_tasa_cambio(moneda_origen: str, moneda_destino: str) -> float:
    """Consulta la cotización oficial en tiempo real con soporte de redirecciones y fallback."""
    origen = moneda_origen.strip().upper()
    destino = moneda_destino.strip().upper()

    if origen == destino:
        return 1.0

    cabeceras = {"User-Agent": "BancoCentral-API/1.0"}

    # 1. Intento primario: Frankfurter API (nueva URL v1 del Banco Central Europeo)
    try:
        url_frankfurter = f"https://api.frankfurter.dev/v1/latest?base={origen}&symbols={destino}"
        async with httpx.AsyncClient(
            timeout=7.0, follow_redirects=True, headers=cabeceras
        ) as cliente:
            respuesta = await cliente.get(url_frankfurter)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                tasa = datos.get("rates", {}).get(destino)
                if tasa:
                    return float(tasa)
    except Exception:
        # Si Frankfurter tiene latencia o caída, pasa silenciosamente al proveedor de respaldo
        pass

    # 2. Proveedor de respaldo (Fallback): Open Exchange Rates API
    try:
        url_fallback = f"https://open.er-api.com/v6/latest/{origen}"
        async with httpx.AsyncClient(
            timeout=7.0, follow_redirects=True, headers=cabeceras
        ) as cliente:
            respuesta = await cliente.get(url_fallback)
            if respuesta.status_code == 200:
                datos = respuesta.json()
                tasa = datos.get("rates", {}).get(destino)
                if tasa:
                    return float(tasa)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Servicios de divisas no disponibles temporalmente: {exc}",
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"No fue posible cotizar el par de divisas {origen} -> {destino}.",
    )