# API Usage Examples

## curl

Create an identity:

```bash
curl -X POST "http://127.0.0.1:8000/identity" \
  -H "Content-Type: application/json" \
  -d '{"id":"user2","name":"Bob","email":"bob@example.com"}'
```

List identities:

```bash
curl http://127.0.0.1:8000/identities
```

Get dashboard summary:

```bash
curl http://127.0.0.1:8000/dashboard
```

## Python example

```python
import requests

base = 'http://127.0.0.1:8000'
resp = requests.post(f'{base}/identity', json={'id':'user2','name':'Bob','email':'bob@example.com'})
print(resp.json())
print(requests.get(f'{base}/dashboard').json())
```
