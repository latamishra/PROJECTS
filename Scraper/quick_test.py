import requests
import json

# Test iPhone in US
print('Testing iPhone in US...')
response = requests.post('http://localhost:8000/compare', 
                        json={'country': 'US', 'query': 'iPhone 16 Pro, 128GB'}, 
                        timeout=120)
print(f'Status: {response.status_code}')
result = response.json()
print(f'Found {len(result.get("offers", []))} offers')
print(f'Note: {result.get("note", "No note")}')
if result.get('offers'):
    for i, offer in enumerate(result['offers'][:3]):
        print(f'  {i+1}. {offer["productName"][:50]}... - {offer["price"]} {offer["currency"]} ({offer["source"]})')

# Test bananas in US
print('\n' + '='*50)
print('Testing bananas in US...')
response = requests.post('http://localhost:8000/compare', 
                        json={'country': 'US', 'query': 'bananas'}, 
                        timeout=120)
print(f'Status: {response.status_code}')
result = response.json()
print(f'Found {len(result.get("offers", []))} offers')
print(f'Note: {result.get("note", "No note")}')
if result.get('offers'):
    for i, offer in enumerate(result['offers'][:3]):
        print(f'  {i+1}. {offer["productName"][:50]}... - {offer["price"]} {offer["currency"]} ({offer["source"]})')

# Test organic bananas in US
print('\n' + '='*50)
print('Testing organic bananas in US...')
response = requests.post('http://localhost:8000/compare', 
                        json={'country': 'US', 'query': 'organic bananas'}, 
                        timeout=120)
print(f'Status: {response.status_code}')
result = response.json()
print(f'Found {len(result.get("offers", []))} offers')
print(f'Note: {result.get("note", "No note")}')
if result.get('offers'):
    for i, offer in enumerate(result['offers'][:3]):
        print(f'  {i+1}. {offer["productName"][:50]}... - {offer["price"]} {offer["currency"]} ({offer["source"]})')
else:
    print('No offers found')
