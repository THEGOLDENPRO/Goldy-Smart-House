import goldy_smart_house

def log(client:goldy_smart_house.client.Client, text:str):
    if client.enable_logs:
        if not client.method == None:
            print(f"[{client.method.name}] " + text)

        else:
            print(text)