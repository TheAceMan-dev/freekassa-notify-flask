from flask import Flask, request, Response
import hashlib, os

app = Flask(__name__)

def md5(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()

# секrets берём из Replit Secrets (добавим после импорта)
SECRET2 = os.getenv("FREKASSA_SECRET2", "")
SHOP_ID = os.getenv("FREKASSA_SHOP_ID", "")
EXPECTED_AMOUNT = os.getenv("EXPECTED_AMOUNT")  # например "10.00"

@app.get("/")
def ok():
    return "OK: FreeKassa notify is up"

@app.post("/freekassa/notify")
def notify():
    f = request.form

    sign_expected = md5(f"{f.get('MERCHANT_ID','')}:{f.get('AMOUNT','')}:{SECRET2}:{f.get('MERCHANT_ORDER_ID','')}")
    if (f.get("SIGN","").lower() != sign_expected.lower()):
        return Response("bad sign", 400)

    if SHOP_ID and f.get("MERCHANT_ID") != str(SHOP_ID):
        return Response("wrong shop", 400)

    if EXPECTED_AMOUNT and f.get("AMOUNT") != str(EXPECTED_AMOUNT):
        return Response("wrong amount", 400)

    # TODO: тут отметь оплату в своей базе по MERCHANT_ORDER_ID/intid
    print("FK notify:", f.to_dict())  # будет видно в Console

    return Response("YES", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 3000)))
