import asyncio
import websockets
import json
import requests

countnr = 0

api_url = 'https://api.solanagateway.com/api/v1/pumpfun/price?mint=CONTRACT/MINT-ADDRESS'
webhook_url = 'YOUR WEBHOOK URL'
avatar_url = 'AVATAR URL'
payload2 = {
    'content': 'Started Scanning',
    'username': 'Coin Tracker',
    'avatar_url': avatar_url
}

response_start = requests.post(webhook_url, json=payload2)

async def subscribe():
    uri = "wss://pumpportal.fun/api/data"
    async with websockets.connect(uri) as websocket:
        try:
            # Subscribing to trades on tokens
            payload = {
                "method": "subscribeTokenTrade",
                "keys": ["CONTRACT/MINT-ADDRESS"]  # array of token CAs to watch
            }
            await websocket.send(json.dumps(payload))

            # Listening for messages
            async for message in websocket:

                global countnr

                response_price = requests.get(api_url)
                data3 = response_price.json()
                usdprice = data3.get('priceInUSD')

                data = json.loads(message)
                tx_type = data.get('txType')
                token_amount = data.get('tokenAmount')
                signature = data.get('signature')

                message_content = f"Token update:\nAction: {tx_type}\nAmount: {token_amount}\nToken Price: {usdprice}"
                payload = {
                    'content': message_content,
                    'username': 'Coin Tracker',
                    'avatar_url': avatar_url 
                }

                response_price = requests.get(api_url)

                response = requests.post(webhook_url, json=payload)

                countnr = countnr + 1

                if response.status_code == 204:
                    print('Message sent successfully.')
                    print(countnr)
                else:
                    print(f'Failed to send message. Status code: {response.status_code}')
                    print('Response:', response.text)



        except Exception as e:
            print(f"An error occurred: {e}")

# Run the subscribe function
if __name__ == "__main__":
    asyncio.run(subscribe())
