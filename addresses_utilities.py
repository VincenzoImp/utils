import re

def bitcoin(address):
    def taproot(address):
        schema = '^((bc)(0([ac-hj-np-z02-9]{39}|[ac-hj-np-z02-9]{59})|1[ac-hj-np-z02-9]{8,89}))$'
        if re.match(schema, address) is None:
            return False
        return True
    def segwit(address):
        schema = '^((bc)(0([ac-hj-np-z02-9]{39}|[ac-hj-np-z02-9]{59})|1[ac-hj-np-z02-9]{8,87}))$'
        if re.match(schema, address) is None:
            return False
        return True
    def script(address):
        schema = '^[3][a-km-zA-HJ-NP-Z1-9]{25,34}$'
        if re.match(schema, address) is None:
            return False
        return True
    def legacy(address):
        schema = '^[1][a-km-zA-HJ-NP-Z1-9]{25,34}$'
        if re.match(schema, address) is None:
            return False
        return True
    if taproot(address):
        return True
    if segwit(address):
        return True
    if script(address):
        return True
    if legacy(address):
        return True
    return False

def ethereum(address):
    schema = '^((0x)([0-9a-fA-F]{40}))$'
    if re.match(schema, address) is None:
        return False
    return True

def litecoin(address):
    schema = '^([LM3]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}||ltc1[a-z0-9]{39,59})$'
    if re.match(schema, address) is None:
        return False
    return True

def dogecoin(address):
    schema = '^D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}'
    schema2 = 'D[a-zA-Z0-9_.-]{33}'
    if re.match(schema, address) is None and re.match(schema2, address) is None:
        return False
    return True

def monero(address):
    schema = '[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}'
    if re.match(schema, address) is None:
        return False
    return True

def dash(address):
    schema = 'X[1-9A-HJ-NP-Za-km-z]{33}'
    if re.match(schema, address) is None:
        return False
    return True  

def cardano(address):
    schema = 'addr1[a-z0-9]+'
    if re.match(schema, address) is None:
        return False
    return True

def cosmos(address):
    schema = 'cosmos[a-zA-Z0-9_.-]{10,}'
    if re.match(schema, address) is None:
        return False
    return True

def iota(address):
    schema = 'iota[a-z0-9]{10,}'
    if re.match(schema, address) is None:
        return False
    return True

def lisk(address):
    schema = '[0-9]{19}L'
    if re.match(schema, address) is None:
        return False
    return True

def nem(address):
    schema = '[N][A-Za-z0-9-]{37,52}'
    if re.match(schema, address) is None:
        return False
    return True

def neo(address):
    schema = 'A[0-9a-zA-Z]{33}'
    if re.match(schema, address) is None:
        return False
    return True

def polkadot(address):
    schema = '1[0-9a-zA-Z]{47}'
    if re.match(schema, address) is None:
        return False
    return True

def ripple(address):
    schema = '^([r])([1-9A-HJ-NP-Za-km-z]{24,34})$'
    if re.match(schema, address) is None:
        return False
    return True

def stellar(address):
    schema = 'G[0-9A-Z]{40,60}'
    if re.match(schema, address) is None:
        return False
    return True

def ethereum_classic(address):
    return ethereum(address)

def binance_smart_chain(address):
    return ethereum(address)

def binance_beacon_chain(address):
    schema = '^((bnb1)[0-9a-z]{38})$'
    if re.match(schema, address) is None:
        return False
    return True

def bitcoin_cash(address):
    legacy = '[13][a-km-zA-HJ-NP-Z1-9]{33}'
    cashaddr = '((bitcoincash):)?(q|p)[a-z0-9]{41}'
    if re.match(legacy, address) is None and re.match(cashaddr, address) is None:
        return False
    return True

def solana(address):
    schema = '^[1-9A-HJ-NP-Za-km-z]{32,44}$'
    if re.match(schema, address) is None:
        return False
    return True

def tron(address):
    schema = '^((T)[a-zA-Z0-9]{33})$'
    if re.match(schema, address) is None:
        return False
    return True

def algorand(address):
    schema = '^[A-Z2-7]{58}$'
    if re.match(schema, address) is None:
        return False
    return True

def vechain(address):
    return ethereum(address)

def email(address):
    if address.count('@') == 1 and address.count('.') >= 1:
        address = address.replace('@', '').replace('.', '')
        return re.match(r"^[a-zA-Z0-9~!$%^&*_=+}{'?-]+$", address) is not None
    return False

def get_addresses(string):
    foo = {
        'bitcoin': bitcoin,
        'ethereum': ethereum,
        'litecoin': litecoin,
        'dogecoin': dogecoin,
        'monero': monero,
        'dash': dash,
        'cardano': cardano,
        'cosmos': cosmos,
        'iota': iota,
        'lisk': lisk,
        'polkadot': polkadot,
        'ripple': ripple,
        'stellar': stellar,
        'neo': neo,
        'bitcoin-cash': bitcoin_cash,
        'ethereum-classic': ethereum_classic,
        'binance-smart-chain': binance_smart_chain,
        'binance-beacon-chain': binance_beacon_chain,
        'solana': solana,
        'tron': tron,
        'algorand': algorand,
        'vechain': vechain,
    }
    crypto = {key : [] for key in foo.keys()}
    for address in string.split():
        for key in foo.keys():
            if foo[key](address):
                crypto[key].append(address)
    for key in crypto.keys():
        crypto[key] = list(set(crypto[key]))
    return crypto

def get_crypto():
    return list(get_addresses('').keys())