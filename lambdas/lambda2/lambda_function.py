import json
import urllib.request

def lambda_handler(event, context):
    url = "https://open.er-api.com/v6/latest/USD"

    try:
        with urllib.request.urlopen(url) as response:
            body = response.read()
            data = json.loads(body.decode())

            # Extract exchange rate to EUR (or fallback to Not found)
            eur_rate = data.get("rates", {}).get("EUR", "Not found")

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "base": "USD",
                    "target": "EUR",
                    "rate": eur_rate
                })
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }