"""Acompanha a apuração do 2º turno 2026 (TSE). Uso: python apuracao.py [UF]
Ex.: python apuracao.py        -> Presidente (BR)
     python apuracao.py ma     -> Presidente (BR) + Governador (MA)
"""
import json, sys, time, urllib.request
from datetime import datetime

BASE = "https://resultados.tse.jus.br/oficial"
INTERVALO = 60  # segundos

def url_pres():
    return f"{BASE}/ele2026/6258/dados/br/br-c0001-e006258-u.json"

def url_gov(uf):
    return f"{BASE}/ele2026/6260/dados/{uf}/{uf}-c0003-e006260-u.json"

def baixar(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)

def achar(obj, chave):
    """Busca recursiva do 1º valor de uma chave."""
    if isinstance(obj, dict):
        if chave in obj:
            return obj[chave]
        for v in obj.values():
            r = achar(v, chave)
            if r is not None:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = achar(v, chave)
            if r is not None:
                return r
    return None

def candidatos(obj):
    """Acha a lista de candidatos (dicts com 'nm' e 'vap')."""
    if isinstance(obj, list) and obj and isinstance(obj[0], dict) and "nm" in obj[0] and "vap" in obj[0]:
        return obj
    if isinstance(obj, dict):
        obj = list(obj.values())
    if isinstance(obj, list):
        for v in obj:
            r = candidatos(v)
            if r:
                return r
    return []

def mostrar(titulo, url, salvar):
    try:
        d = baixar(url)
    except Exception as e:
        print(f"{titulo}: erro -> {e}")
        return
    with open(salvar, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    pst = achar(d, "pst")
    print(f"\n{titulo}  |  seções totalizadas: {pst}%")
    for c in sorted(candidatos(d), key=lambda c: int(str(c.get("vap", 0)).replace(".", "") or 0), reverse=True):
        eleito = "  << ELEITO" if str(c.get("e", "")).lower() == "s" else ""
        print(f"  {c.get('nm', '?'):<30} {c.get('pvap', '?'):>7}%  {c.get('vap', '?'):>12} votos{eleito}")

def main():
    uf = sys.argv[1].lower() if len(sys.argv) > 1 else None
    while True:
        print("\n" + "=" * 60 + f"\n{datetime.now():%H:%M:%S}")
        mostrar("PRESIDENTE (BR)", url_pres(), "presidente.json")
        if uf:
            mostrar(f"GOVERNADOR ({uf.upper()})", url_gov(uf), f"governador_{uf}.json")
        time.sleep(INTERVALO)

if __name__ == "__main__":
    main()
