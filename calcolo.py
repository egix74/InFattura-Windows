from decimal import Decimal, ROUND_HALF_UP

D = Decimal
def euro(x):
    return x.quantize(D('0.01'), rounding=ROUND_HALF_UP)

def calcola(onorario, esenti, spese, cassa, iva, ritenuta, forfait):
    generali = euro(onorario * forfait / 100)
    base = onorario + generali + spese
    previdenza = euro(base * cassa / 100)
    imposta = euro((base + previdenza) * iva / 100)
    trattenuta = euro(base * ritenuta / 100)
    return dict(onorario=onorario, generali=generali, spese=spese, cassa=previdenza,
                iva=imposta, esenti=esenti, ritenuta=trattenuta,
                netto=base + previdenza + imposta + esenti - trattenuta)

def scorpora(netto, esenti, spese, cassa, iva, ritenuta, forfait):
    def f(cents):
        return calcola(D(cents)/100, esenti, spese, cassa, iva, ritenuta, forfait)
    if f(0)['netto'] > netto:
        raise ValueError('Il netto è inferiore al totale delle spese e degli accessori.')
    lo, hi = 0, 1
    while f(hi)['netto'] < netto and hi < 10**14:
        hi *= 2
    if f(hi)['netto'] < netto:
        raise ValueError('Impossibile calcolare lo scorporo con queste percentuali.')
    while lo < hi:
        mid = (lo + hi)//2
        if f(mid)['netto'] < netto: lo = mid + 1
        else: hi = mid
    candidates = [f(max(0, lo-1)), f(lo)]
    return min(candidates, key=lambda x: abs(x['netto']-netto))
