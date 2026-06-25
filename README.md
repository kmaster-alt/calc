
# Calculator HTTP Server

## Description

A simple Python HTTP server that performs basic arithmetic operations and returns results in JSON format.

## Requirements

* Python 3

## Run

```bash
python a.py
```

Server runs at:

```text
http://localhost:5000
```

## Endpoints

* `/add?a=10&b=5`
* `/sub?a=10&b=5`
* `/multiply?a=10&b=5`
* `/divide?a=10&b=5`

## Example Response

```json
{
  "a": 10,
  "b": 5,
  "operation": "addition",
  "result": 15
}
```



Kenneth Master

