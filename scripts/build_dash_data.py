import pandas as pd, numpy as np, re, json, sys
sys.path.insert(0,'/home/claude/scripts')
import pycountry, pycountry_convert as pc
from univ import norm_es2

FIELD_ES={'Clinical Medicine':'Medicina clínica','Biomedical Research':'Investigación biomédica','Chemistry':'Química','Physics & Astronomy':'Física y astronomía',
'Enabling & Strategic Technologies':'Tecnologías estratégicas','Engineering':'Ingeniería','Information & Communication Technologies':'TIC',
'Biology':'Biología','Agriculture, Fisheries & Forestry':'Agricultura, pesca y forestal','Earth & Environmental Sciences':'Ciencias de la Tierra y medio ambiente',
'Psychology & Cognitive Sciences':'Psicología y ciencias cognitivas','Economics & Business':'Economía y empresa','Mathematics & Statistics':'Matemáticas y estadística',
'Social Sciences':'Ciencias sociales','Public Health & Health Services':'Salud pública','Built Environment & Design':'Arquitectura y diseño',
'Historical Studies':'Historia','Communication & Textual Studies':'Comunicación y estudios textuales','Philosophy & Theology':'Filosofía y teología',
'Visual & Performing Arts':'Artes visuales y escénicas','General Science & Technology':'Ciencia y tecnología general','General Arts, Humanities & Social Sciences':'Artes, humanidades y CC. sociales (general)'}
CONT_ES={'EU':'Europa','NA':'América del Norte','SA':'América del Sur','AS':'Asia','AF':'África','OC':'Oceanía','AN':'Antártida'}

def country(code):
    if not isinstance(code,str): return ('Sin país','—',None)
    c=code.upper()
    if c=='EUE': return ('Europa (sin país)','Europa',None)
    if c=='CSK': return ('Checoslovaquia','Europa',None)
    p=pycountry.countries.get(alpha_3=c)
    if not p: return (c,'—',None)
    try: cont=CONT_ES[pc.country_alpha2_to_continent_code(p.alpha_2)]
    except Exception: cont={'TLS':'Asia','VAT':'Europa','SXM':'América del Norte','ESH':'África','ATA':'Antártida','PCN':'Oceanía','UMI':'Oceanía','ATF':'África'}.get(c,'—')
    name=getattr(p,'common_name',None) or p.name
    return (name,cont,int(p.numeric))

COMP=r"\b(meta|meta ai|inc|corp|corporation|ltd|llc|gmbh|plc|s\.?a\.?|co\.|company|pharmaceuticals?|google|microsoft|ibm|pfizer|novartis|roche|merck|genentech|amgen|siemens|samsung|huawei|intel|nokia|philips|bayer|astrazeneca|glaxosmithkline|gsk|sanofi|eli lilly|johnson & johnson|meta platforms|facebook|amazon|apple|tencent|alibaba|baidu|nvidia|bell lab|at&t|boeing|deepmind|openai|bristol-myers|abbvie|regeneron|gilead|biogen|novo nordisk|takeda|toshiba|hitachi|nec |fujitsu|sony|panasonic|xerox|hp labs|hewlett|exxon|shell|bp |chevron|dupont|basf)\b"
HOSP=r"hospital|hopitaux|hôpitaux|langone|erasmus mc|\bumc\b|medical centre|hôpital|hospitalier|ospedale|klinik|clinic|clínica|medical cent|health system|healthcare|health care|nhs|mayo|cancer cent|kaiser|hospices|policlinico|irccs|charité|sloan kettering|md anderson"
UNIV=r"univers|institutet|advanced institute of science|institut für technologie|tudományegyetem|egyetem|ülikool|haskoli|yliopisto|universiti|hochschule|yliopisto|üniversitesi|universitesi|univerza|politechnika|unsw|tu wien|akademin|fakultet|fakultät|tiedekunta|scuola|ucl|uclouvain|medicine$|engineering$|department|weill cornell|penn medicine|michigan medicine|uconn|nyu |universit|universid|universidade|università|universität|universiteit|uniwersytet|univerzita|universitet|college|école|ecole|school|polytechn|politecnic|polytechnique|eth |eth$|epfl|kth|caltech|massachusetts institute of technology|institute of technology|technische|hochschule|ku leuven|sorbonne|faculty|faculdade|facultad|faculté|daigaku|academy of medical sciences|medical university"
RES=r"cnrs|consiglio|administration|department of agriculture|environment and climate|fundacao|fundação|csic|max planck|max-planck|helmholtz|fraunhofer|inserm|inrae|inra\b|cnr\b|academy of sciences|chinese academy|national institute|national lab|laborator|nih\b|nasa|cern|embl|pasteur|institute|instituto|institut|istituto|centre|center|centro|zentrum|agency|survey|ministry|observatory|observatorio|museum|foundation|fundación|riken|csiro|usda|cdc\b|council|organisation|organization|world health|consejo|agencia|research"
def itype(n):
    if not isinstance(n,str) or not n.strip(): return 'Sin institución'
    s=n.lower()
    if re.search(COMP,s) and not re.search(r'univers|hospital|forschung|zentrum|institut|centre|center',s): return 'Empresa'
    if re.search(HOSP,s): return 'Hospital / centro sanitario'
    if re.search(GOV,s) and not re.search(r'univers',s): return 'Centro de investigación / organismo público'
    if re.search(UNIV,s): return 'Universidad'
    if re.search(RES,s): return 'Centro de investigación / organismo público'
    return 'Otra'
GOV=r"consiglio|administration|department of agriculture|department of energy|environment and climate|cnrs|csic|max planck|max-planck|helmholtz|fraunhofer|inserm|inrae|academy of sciences|riken|csiro|nasa|cern|national laborator|forschungszentrum|national institutes of health|centers for disease"
GENERIC=r"^(college|school|faculty|department|institute|division) of [a-z &]+$"

def load(path):
    d=pd.read_parquet(path)
    d.columns=[re.sub(r'(9625|2525|9624|2424)','XX',re.sub(r'h(25|24)','hYY',c)) for c in d.columns]
    d['pct']=d['rank sm-subfield-1']/d['sm-subfield-1 count']*100
    return d

out={'meta':{}}
CTRY={}; FIELDS=sorted(FIELD_ES.values()); TYPES=['Universidad','Hospital / centro sanitario','Centro de investigación / organismo público','Empresa','Otra','Sin institución']
fidx={f:i for i,f in enumerate(FIELDS)}; tidx={t:i for i,t in enumerate(TYPES)}
cube=[]; inst={}; ctry_v8={}
for ti,(tab,p9,p8) in enumerate([('career','data/career.parquet','data/v8/career.parquet'),('single','data/single.parquet','data/v8/single.parquet')]):
    d=load(p9)
    d['type']=d.inst_name.map(itype)
    d['field']=d['sm-field'].map(FIELD_ES).fillna('Ciencia y tecnología general')
    d['top10k']=(d['rank']<=10000).astype(int)
    d['rw']=(d['np6025_rw'].fillna(0)>0).astype(int) if 'np6025_rw' in d else 0
    d['hi_self']=(d['self%']>0.25).astype(int)
    out['meta'][tab]={'n':len(d)}
    for code in d.cntry.dropna().unique():
        if code not in CTRY: CTRY[code]=country(code)
    g=d.groupby(['cntry','field','type'],dropna=False).agg(n=('authfull','size'),top=('top10k','sum'),rw=('rw','sum'),hs=('hi_self','sum'),selfsum=('self%','sum')).reset_index()
    for r in g.itertuples():
        cube.append([ti, r.cntry if isinstance(r.cntry,str) else 'zzz', fidx[r.field], tidx[r.type], int(r.n), int(r.top), int(r.rw), int(r.hs), round(float(r.selfsum),2)])
    gi=d[d.inst_name.notna()].groupby(['inst_name','cntry']).agg(n=('authfull','size'),top=('top10k','sum'),field=('field',lambda s:s.value_counts().index[0])).reset_index()
    for r in gi.itertuples():
        k=(r.inst_name,r.cntry)
        e=inst.setdefault(k,{'n':[0,0],'top':[0,0],'f':r.field,'t':itype(r.inst_name)})
        e['n'][ti]=int(r.n); e['top'][ti]=int(r.top)
        if ti==0: e['f']=r.field
    d8=pd.read_parquet(p8)
    ctry_v8[tab]=d8.cntry.value_counts().to_dict()
    # subcampos globales
    out.setdefault('subfields',{})[tab]=d.groupby(['field','sm-subfield-1']).size().reset_index().values.tolist()
CTRY['zzz']=('Sin país','—',None)
codes=sorted(CTRY)
out['countries']=[[c,CTRY[c][0],CTRY[c][1],CTRY[c][2],int(ctry_v8['career'].get(c,0)),int(ctry_v8['single'].get(c,0))] for c in codes]
out['fields']=FIELDS; out['types']=TYPES
out['cube']=cube
insts=[[k[0],k[1],v['t'],v['f'],v['n'][0],v['n'][1],v['top'][0],v['top'][1]] for k,v in inst.items() if max(v['n'])>=5 and not re.match(GENERIC,k[0].lower())]
out['institutions']=sorted(insts,key=lambda x:-(x[4]+x[5]))
out['meta']['generic_excluded']=sorted({k[0] for k in inst if re.match(GENERIC,k[0].lower())})[:30]
# ---- España
es={}
uni9={}
for tab,p in [('career','data/career.parquet'),('single','data/single.parquet')]:
    d=load(p); e=d[d.cntry=='esp'].copy()
    e['field']=e['sm-field'].map(FIELD_ES); e['type']=e.inst_name.map(itype); e['uni']=e.inst_name.map(norm_es2)
    es[tab]=e
# simpler explicit build
res=[]
for tab,e in es.items():
    t=0 if tab=='career' else 1
    for _,r in e.iterrows():
        res.append([t,r.authfull,r.inst_name if isinstance(r.inst_name,str) else '',r.uni if isinstance(r.uni,str) else '',r.type,r.field,r['sm-subfield-1'],int(r['rank']),round(float(r.pct),2),round(float(r['self%'])*100,1),int(r['hYY']),int(r.firstyr)])
out['spain_researchers']=res
norm=pd.read_csv('data/normalizado_pdi.csv')
ar_c=pd.read_csv('data/ajuste_rama_career.csv').set_index('Universidad'); ar_s=pd.read_csv('data/ajuste_rama_single.csv').set_index('Universidad')
su=[]
for _,r in norm.iterrows():
    u=r.Universidad
    su.append([u,int(r.n_career),int(r.n_single),round(float(r.etc),1),
               round(float(ar_c.loc[u,'ratio']),3) if u in ar_c.index else None, round(float(ar_s.loc[u,'ratio']),3) if u in ar_s.index else None,
               round(float(ar_c.loc[u,'esp']),2) if u in ar_c.index else None, round(float(ar_s.loc[u,'esp']),2) if u in ar_s.index else None,
               i<48 if (i:=list(norm.Universidad).index(u)) is not None else False])
out['spain_universities']=su
json.dump(out,open('/home/claude/dash/data.json','w'),ensure_ascii=False,separators=(',',':'))
import os; print('bytes',os.path.getsize('/home/claude/dash/data.json'),'cube',len(cube),'insts',len(insts),'es',len(res))
print(pd.Series([x[2] for x in insts]).value_counts())
