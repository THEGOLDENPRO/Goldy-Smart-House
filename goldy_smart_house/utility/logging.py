import goldy_smart_house

def log(client:goldy_smart_house.client.Client, text:str):
    if client.enable_logs:
        print(text)