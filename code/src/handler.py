def add_one(x):
    return x + 1

def handler(event, context):
    print(add_one(1))
    return {"status": 200}