from beem import Hive
from beembase import operations
from beembase.operations import Escrow_transfer
from beem.transactionbuilder import TransactionBuilder
from tools.tools import getFutureT, getIdfromHash, encodeTransX
import qrcode


nodes = [
    "https://api.hive.blog",
    "https://api.openhive.network",
    "https://hiveapi.actifit.io",
    "https://hive-api.dlux.io",
    "https://api.syncad.com"
]

hive = Hive(nodes)


def escrow_transfer(payer: str,
                    receiver: str,
                    agent: str,
                    amount: float,
                    token: str,
                    fee: float) -> dict:
    """
    Inicia un contrato escrow enviando fondos a la cuenta de escrow.

    :param payer: nombre de la cuenta que paga (requiere Active key)
    :param receiver: cuenta que recibirá los fondos tras la aprobación
    :param agent: cuenta del árbitro que liberará fondos en disputa
    :param escrow_id: identificador numérico único para el contrato
    :param amount: cantidad de tokens a bloquear
    :param token: símbolo de la moneda (“HIVE” o “HBD”)
    :param fee: comisión que cobra el agente
    :param ratification_deadline: fecha límite para aprobaciones (ISO 8601)
    :param escrow_expiration: fecha de expiración del escrow (ISO 8601)
    :return: respuesta de la transacción
    """
    if token.upper() not in ["HBD", "HIVE"]:
        raise Exception("Error en token")

    hbd_amount = "0.000 HBD"
    hive_amount = "0.000 HIVE"

    if token.upper() == 'HBD':
        hbd_amount = f"{amount:.3f} HBD"
    else:
        hive_amount = f"{amount:.3f} HIVE"

    fee = f"{0:.3f} {token.upper()}"

    deadline = getFutureT(24)
    expiration = getFutureT(36)

    textM = f"""
    {payer}
    {receiver}
    {agent}
    {hive_amount}
    {hbd_amount}
    {fee}
    {deadline}
    {expiration}    
    """
    escrow_id = int(getIdfromHash(textM))

    data = operations.Escrow_transfer(**{
        'from': payer,
        'to': receiver,
        'agent': agent,
        'escrow_id': escrow_id,
        'hbd_amount': hbd_amount,
        'hive_amount': hive_amount,
        'fee': fee,
        'ratification_deadline': deadline,
        'escrow_expiration': expiration
    })
    
    return data.json()

sender='manuphotos'
receiver='ertytuxs'
agent='tuxtify'
amount=0.001
token='HBD'
fee=0

tj=TransactionBuilder(blockchain_instance=hive)
tj.appendOps(Escrow_transfer(**escrow_transfer(sender,receiver,agent,amount,token,fee)))
print(tj.json().get('operations')[0])
fdata=tj.json().get('operations')[0]
odata=encodeTransX(fdata)
sig = f"hive://sign/op/{odata}?s={sender}"
img = qrcode.make(sig)
img.save(f"QR_{tj.json().get('operations')[0][1].get('escrow_id','0')}.png")
print(sig)
