import json
import hashlib
import asyncio
import aiohttp

MAINNET = 'https://voynich-mainnet.azurewebsites.net/api/traversal'

REQUIRED = [
    'derivative', 'action', 'face', 'maturity', 
    'collateral', 'interest', 'fixed',
    'late', 'fee', 'due', 'cap', 'asset', 'uid', 'hash'
]

NUMERICS = [
    'face', 'maturity', 'interest', 
    'late', 'fee', 'cap'
]

TRANSACTT = ['mint', 'settle']

async def enlighten(pkg):
    rtrn = {'status': False, 'log': 'Failed to communicate with voynich mainnet'}
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(MAINNET, json=pkg['body'], headers={
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip, deflate"
            }) as response:
                rtrn = await response.json()
    except Exception as error:
        print("Voynich Main Network Communication Error:", error)
    return rtrn

def signature(value, salt, iterations=1000, key_length=64, algo='sha512'):
    return hashlib.pbkdf2_hmac(algo, value.encode('utf-8'), salt.encode('utf-8'), iterations, dklen=key_length).hex()

def formatted(transaction):
    proc = all(key in transaction and transaction[key] not in [None, ''] for key in REQUIRED)
    numrl = all(isinstance(transaction[key], (int, float)) and transaction[key] >= 0 for key in NUMERICS)
    truthy = isinstance(transaction.get('fixed', None), bool)
    isoey = isinstance(transaction.get('due', None), str) and transaction['due'].replace('-', '').isdigit()
    proper = transaction.get('action') in TRANSACTT
    exc = proc and numrl and truthy and isoey
    return proper and exc

async def adopt(address, enigma, email):
    action = 'adopt'
    adoption = await enlighten({'body': {'action': action, 'address': address, 'enigma': enigma, 'email': email}})
    return adoption

async def validate(address):
    action = 'validate'
    taken = await enlighten({'body': {'address': address, 'action': action}})
    return taken

async def holdings(address):
    action = 'holdings'
    wallet = await enlighten({'body': {'address': address, 'action': action}})
    return wallet

async def supported():
    action = 'supported'
    latest = await enlighten({'body': {'action': action}})
    return latest

async def power(asset, address=None, hash=None):
    action = 'power'
    payload = {'action': action, 'asset': asset}
    if address and hash:
        payload.update({'address': address, 'hash': hash})
    result = await enlighten({'body': payload})
    return result

async def transaction_hash(hash):
    action = 'hash'
    details = await enlighten({'body': {'action': action, 'hash': hash}})
    return details

def consensus(contract, wallet):
    sigil = signature(wallet['key'], wallet['pen'])
    consent = signature(contract, sigil)
    address = wallet['address']
    return {'address': address, 'consent': consent}

def sign(contract, wallet, sibyl):
    member_consensus = consensus(contract, wallet)
    broker_consensus = consensus(contract, sibyl)
    return {
        'memberAddress': member_consensus['address'],
        'memberConsent': member_consensus['consent'],
        'brokerAddress': broker_consensus['address'],
        'brokerConsent': broker_consensus['consent']
    }

async def transact(transaction, wallet, sibyl):
    rtrn = {'status': False, 'log': 'Invalid Transaction'}
    if formatted(transaction):
        contract = json.dumps(transaction)
        consent = sign(contract, wallet, sibyl)
        rtrn = await enlighten({'body': {'transaction': transaction, 'consent': consent}})
    return rtrn

async def report(wallet, month, year, sibyl):
    rtrn = {'status': False, 'log': 'Invalid Request'}
    if isinstance(year, int) and 1000 <= year <= 9999 and isinstance(month, int) and 1 <= month <= 12:
        period = {'month': month, 'year': year}
        contract = json.dumps(period)
        consent = sign(contract, wallet, sibyl)
        action = 'close'
        rtrn = await enlighten({'body': {'action': action, 'period': period, 'consent': consent}})
    return rtrn

async def liability(address, month, year, sibyl):
    rtrn = {'status': False, 'log': 'Invalid Request'}
    if isinstance(year, int) and 1000 <= year <= 9999 and isinstance(month, int) and 1 <= month <= 12:
        period = {'month': month, 'year': year}
        contract = json.dumps(period)
        broker_consensus = consensus(contract, sibyl)
        consent = {'brokerAddress': broker_consensus['address'], 'brokerConsent': broker_consensus['consent']}
        action = 'close'
        rtrn = await enlighten({'body': {'action': action, 'address': address, 'period': period, 'consent': consent}})
    return rtrn

async def compliant(wallet, sibyl):
    rtrn = {'status': False, 'log': 'Invalid Request'}
    contract = f"{wallet['address']}{sibyl['address']}"
    consent = sign(contract, wallet, sibyl)
    action = 'kyc'
    rtrn = await enlighten({'body': {'action': action, 'consent': consent}})
    return rtrn


__all__ = [
    'adopt', 'validate', 'holdings', 'supported', 'power', 
    'transaction_hash', 'transact', 'report', 'liability', 'compliant'
]
