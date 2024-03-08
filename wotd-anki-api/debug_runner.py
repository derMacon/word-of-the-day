import os

from src.logic.controller import Controller
from src.logic.persistence_manager import PersistenceManager

contr = Controller()
# contr.login(os.environ["EMAIL"], os.environ["PASSWORD"])

cookies = [{'domain': 'ankiweb.net', 'expiry': 1744495220, 'httpOnly': False, 'name': 'has_auth', 'path': '/', 'sameSite': 'Lax', 'secure': False, 'value': '1'}, {'domain': 'ankiweb.net', 'expiry': 1744495220, 'httpOnly': True, 'name': 'ankiweb', 'path': '/', 'sameSite': 'Lax', 'secure': True, 'value': 'eyJvcCI6ImNrIiwiaWF0IjoxNzA5OTM1MjIwLCJqdiI6MCwiayI6IkhgI1BmVEEmN2NqRHxXTlUiLCJjIjoxLCJ0IjoxNzA5OTM1MjIwfQ.qIc8nlNXkpk3JuywOBUi-Udzq45PaMDdsiiyC1ifzP0'}]
print("test print before: ", cookies)

pers = PersistenceManager()
# pers.insert_data('key1', cookies)
out = pers.read_data('key1')
print("after: ", out)

# # cookies = [{'has_auth': '1'}, {'ankiweb': 'eyJvcCI6ImNrIiwiaWF0IjoxNzA5OTM1MjIwLCJqdiI6MCwiayI6IkhgI1BmVEEmN2NqRHxXTlUiLCJjIjoxLCJ0IjoxNzA5OTM1MjIwfQ.qIc8nlNXkpk3JuywOBUi-Udzq45PaMDdsiiyC1ifzP0'}]
# out = contr.list_decks(cookies)
# print(out)