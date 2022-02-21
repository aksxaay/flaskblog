bruhs = [
  {
    "symbol": "AAPL",
    "name": "Apple Inc",
    "currency": "USD",
    "exchange": "NASDAQ",
    "country": "United States",
    "type": "Common Stock"
  },
  
  {
    "symbol": "AAT",
    "name": "American Assets Trust Inc",
    "currency": "USD",
    "exchange": "NYSE",
    "country": "United States",
    "type": "Real Estate Investment Trust (REIT)"
  }
  
]

print(type(bruhs))


for bruh in bruhs:
    print(bruh['symbol'])