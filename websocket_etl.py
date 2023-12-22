import websocket
import json
import pandas as pd
import pyodbc
import time
import random

def db_connect():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=database-hackathon.cfn2vvgqdwd8.ap-southeast-2.rds.amazonaws.com,1433;'
        'DATABASE=Hackathon;'
        'UID=admin;'
        'PWD=Hackathon2023db;'
        'TrustServerCertificate=yes'  # Added this line
    )

def write_to_db(new_data):
    conn = db_connect()
    cursor = conn.cursor()
    
    # Construct the SQL INSERT query
    query = """
    INSERT INTO dbo.Fact_test1 (type, symbol, price, volume, timestamp) 
    VALUES (?, ?, ?, ?, ?)
    """
    cursor.execute(query, (new_data['type'], new_data['symbol'], new_data['price'], new_data['volume'], new_data['timestamp']))
    
    conn.commit()
    cursor.close()
    conn.close()

def modify_data(data, prefix_number):
    # Modify data with a given prefix number
    modified_data = data.copy()
    modified_data['type'] = 'mock' + str(prefix_number) + '_' + data['type']
    modified_data['symbol'] = 'mock' + str(prefix_number) + '_' + data['symbol']

    # Apply a random multiplier to price and volume
    modified_data['price'] *= random.uniform(0.9, 1.1)
    modified_data['volume'] *= random.uniform(0.9, 1.1)

    return modified_data

def on_message(ws, message):
    msg = json.loads(message)

    if msg['type'] == 'trade':
        for data in msg['data']:
            original_data = {
                'type': msg['type'],
                'symbol': data['s'],
                'price': data['p'],
                'volume': data['v'],
                'timestamp': data['t']
            }
            write_to_db(original_data)

            # Create and write 10 modified data entries
            for i in range(1, 11):
                modified_data = modify_data(original_data, i)
                write_to_db(modified_data)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    # Subscribing to several stock symbols
    ws.send('{"type":"subscribe","symbol":"AAPL"}')
    ws.send('{"type":"subscribe","symbol":"AMZN"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')
    ws.send('{"type":"subscribe","symbol":"IC MARKETS:1"}')
    ws.send('{"type":"subscribe","symbol":"BINANCE:BSWUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:BALUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:POLYUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:DREPUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:LTCDOWNUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:PLAUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:BETHUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:SXPUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:ANYUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:LENDUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:BETAUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:VGXUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:SCUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:EOSDOWNUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:ZILUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:LINKUPUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:TCTUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:KLAYUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:HCUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:LAZIOUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:SLPUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:ADAUPUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCSTUSDT"}');
    ws.send('{"type":"subscribe","symbol":"BINANCE:DOTUSDT"}');


if __name__ == "__main__":
    # Enabling WebSocket trace
    websocket.enableTrace(True)

    # Creating the WebSocketApp
    ws = websocket.WebSocketApp("wss://ws.finnhub.io?token=clpluqhr01qr1q7f03h0clpluqhr01qr1q7f03hg",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    # Running the WebSocketApp
    ws.run_forever()

