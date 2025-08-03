from datetime import datetime, timedelta
import base64
import json
import gc

def getIdfromHash(msg:str)->str:
    now=datetime.now()
    modmsg=msg+" "+now.strftime('%Y-%m-%dT%H:%M:%S') 
    hz= modmsg.__hash__().__abs__()    
    return  str(hz)

def is_number(s: str) -> bool:
    """ Returns True if string is a number. """
    try:
        float(s)
        return True
    except ValueError:
        return False

def getNow():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getNowT():
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

def getFutureT(houres=0):
    now = datetime.now()
    future_time = now + timedelta(hours=houres)
    return future_time.strftime('%Y-%m-%dT%H:%M:%S')
    

def getHoursfromDate(strdate: str) -> int:
    now = datetime.now()
    tmk = datetime.strptime(strdate, '%Y-%m-%d %H:%M:%S')
    dtime = now-tmk
    return int(dtime.total_seconds()//3600)

def getHoursfromDateT(strdate: str) -> int:
    now = datetime.now()
    tmk = datetime.strptime(strdate, '%Y-%m-%dT%H:%M:%S')
    dtime = now-tmk
    return int(dtime.total_seconds()//3600)

b64u_lookup = {'/': '_', '_': '/', '+': '-', '-': '+', '=': '.', '.': '='}
def btoa(x: str) -> str: return base64.b64decode(x)
def atob(x: str) -> str: return base64.b64encode(bytes(x, 'utf-8')).decode('utf-8')


def genb64U(x: str) -> str:
    lt = list(atob(x))
    tro = []
    for el in lt:
        em = b64u_lookup.get(el, el)
        tro.append(em)
    return "".join(tro)


def recb64U(x: str) -> str:
    lt = list(x)
    tro = []
    for el in lt:
        em = b64u_lookup.get(el, el)
        tro.append(em)
    er = "".join(tro)
    return btoa(er)


def encodeTransE(to: str, amount: float, token: str, memo: str) -> str:
    transfer_op = ["transfer", {
        'to': to,
        'amount': f"{amount:.3f} {token.upper()}",
        'memo': memo
    }]
    jst = json.dumps(transfer_op)
    return genb64U(jst)

def encodeTransX(tx) -> str:
    jst = json.dumps(tx)
    return genb64U(jst)


def encodeTrans(receptorx: str, amount: float, token: str, memo: str) -> str:
    return encodeTransE(receptorx, amount, token, memo)

def clearmem():
    gc.collect()

#MDB