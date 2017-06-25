from doco.client import Client
c = Client(apikey='7430687741504d4c477771664a505a5a4a5749526e6a79526c734656346d51787a436c4d6469454e437231')
user = { 'nickname': 'ふー', 'nickname_y': 'フー'}
res = c.send(utt='好き', apiname='Dialogue', **user)
print(res)
print(res['utt'])
