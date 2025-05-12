import json
import urllib.request

def lambda_handler(event, context):
    params = event.get("queryStringParameters", {}) or {}
    base = params.get("base", "USD")
    target = params.get("target", "EUR")

    url = f"https://open.er-api.com/v6/latest/{base}"

    try:
        with urllib.request.urlopen(url) as response:
            body = response.read()
            data = json.loads(body.decode())

            rate = data.get("rates", {}).get(target, "Not found")

            return {
                "statusCode": 200,
                "body": json.dumps({
                    "base": base,
                    "target": target,
                    "rate": rate
                })
            }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
