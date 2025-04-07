# What is Crypticorn?

Crypticorn is at the forefront of cutting-edge artificial intelligence cryptocurrency trading.
Crypticorn offers AI-based solutions for both active and passive investors, including:
 - Prediction Dashboard with trading terminal,
 - AI Agents with different strategies,
 - DEX AI Signals for newly launched tokens,
 - DEX AI Bots

Use this API Client to contribute to the so-called Hive AI, a community driven AI Meta Model for predicting the
cryptocurrency market.

## Usage

Within an asynchronous context the session is closed automatically.
```python
async with ApiClient(base_url="http://localhost", jwt=jwt) as client:
        # json response
        response = await client.pay.products.get_products_without_preload_content()
        print(await response.json())
        # serialized response with pydantic models
        response = await client.pay.products.get_products()
        print(response)
        # json response with http info
        response = await client.pay.products.get_products_with_http_info()
        print(response)
```

Without the context you need to close the session manually.
```python
client = ApiClient(base_url="http://localhost", jwt=jwt)
response = asyncio.run(client.hive.models.get_all_models())
asyncio.run(client.close())
```