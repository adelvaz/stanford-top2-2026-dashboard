import re
# patrones -> nombre normalizado (solo universidades; se excluyen hospitales, CSIC mixtos, institutos)
U = {
 'Universidad Pablo de Olavide':r'Pablo de Olavide',
 'Universidad de Sevilla':r'^(Facultad de .*)?Universidad de Sevilla',
 'Universidad de Granada':r'^Universidad de Granada',
 'Universidad de Córdoba':r'^Universidad de C[oó]rdoba',
 'Universidad de Málaga':r'^Universidad de M[aá]laga',
 'Universidad de Cádiz':r'^Universidad de C[aá]diz',
 'Universidad de Huelva':r'^Universidad de Huelva',
 'Universidad de Jaén':r'^Universidad de Ja[eé]n',
 'Universidad de Almería':r'^Universidad de Almer[ií]a',
 'Universidad Loyola Andalucía':r'Loyola',
 'Universidad Internacional de Andalucía':r'Internacional de Andaluc',
}
AND = list(U)
def norm_es(x):
    if not isinstance(x,str): return None
    for k,p in U.items():
        if re.search(p,x,flags=re.I): return k
    if re.search(r'hospital|instituto|institut |csic|cl[ií]nica|centro|fundaci|ciber|facultad|escuela',x,re.I) and not re.match(r'^Univ',x,re.I):
        return None
    if re.match(r'^(Universi|Mondragon)',x,re.I) or re.search(r'Universitat Pompeu',x):
        n=x.split(',')[0].strip()
        n=re.sub(r'\s*-\s*Euskal Herriko Unibertsitatea','',n)
        n=re.sub(r'\s*\(UPNA\)','',n)
        n=n.replace('Universidad del Pais Vasco','Universidad del País Vasco')
        return n
    return None

FIX = {'Universitat de Valencia':'Universitat de València','Universitat Politécnica de Catalunya':'Universitat Politècnica de Catalunya',
 'Universidad de Castilla La Mancha':'Universidad de Castilla-La Mancha','Universidad Rey Juan Caros':'Universidad Rey Juan Carlos',
 'Universidad Complutense de Madrid Instituto Pluridisciplinar':'Universidad Complutense de Madrid','Universidad de Murcia Laboratorio de Optica':'Universidad de Murcia',
 'Universidad Autonoma':None,'University Center of Defense':None}
def norm_es2(x):
    if not isinstance(x,str): return None
    n = norm_es(x)
    if n is None and not re.search(r'hospital|cl[ií]nica|csic|ciber|osakidetza|complejo|complexo',x,re.I):
        m = re.search(r'(Universi(?:dad|tat|dade)[^,()]*)$', x.strip()) or re.search(r', (Universi(?:dad|tat|dade)[^,()]*)', x)
        if m: n = norm_es(m.group(1).strip())
    if n in FIX: n = FIX[n]
    return n
