import asyncio
from huqt_oracle_client import client, AdvancedTrader

class MyTrader(AdvancedTrader):
    def __init__(self, account, api_key, url, secure = True):
        super().__init__(account, api_key, url, secure)

    def handle_md_update(self, data):
        print(data)
    
    def handle_open_orders_update(self, data):
        print(data)
    
    def handle_positions_update(self, data):
        print(data)
    
    def handle_fill_update(self, data):
        print(data)
    
    def handle_recent_fills(self, data):
        print(data)
    
    def handle_exchange_status_update(self, data):
        print(data)
    
    
async def main():
    account = "admin"
    t = MyTrader(account, "admin_api_key", 'huqt-oracle-rust.fly.dev:443', secure=True)
    await t.listen()
    # response = admin.set_position(account, "BMM", 10)
    # print(response)
    # response = admin.settle_partition(partition, settle_prices= {'BMM': 10})
    # print(response)
    # response = admin.
if __name__ == '__main__':
    asyncio.run(main())
    # main()