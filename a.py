import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def parse_number(value):
    number = float(value)
    return int(number) if number.is_integer() else number


def format_result(value):
    return int(value) if isinstance(value, float) and value.is_integer() else value


OPERATIONS = {
    "/add": ("addition", add),
    "/sub": ("subtraction", sub),
    "/multiply": ("multiplication", multiply),
    "/divide": ("division", divide),
}


class CalculatorHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path not in OPERATIONS:
            self._send_json({"error": "Not found"}, 404)
            return

        params = parse_qs(urlparse(self.path).query)
        a = parse_number(params.get("a", ["0"])[0])
        b = parse_number(params.get("b", ["0"])[0])
        operation_name, operation = OPERATIONS[path]

        try:
            result = format_result(operation(a, b))
            self._send_json({
                "a": a,
                "b": b,
                "operation": operation_name,
                "result": result,
            })
        except ValueError as error:
            self._send_json({"error": str(error)}, 400)

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class ReuseHTTPServer(HTTPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    port = 5000
    try:
        server = ReuseHTTPServer(("localhost", port), CalculatorHandler)
    except OSError:
        print(f"Port {port} is already in use.")
        print("Stop the other server with: pkill -f \"python3 app.py\"")
        print("Or disable AirPlay Receiver in System Settings → General → AirDrop & Handoff")
        raise SystemExit(1)

    print(f"Running on http://localhost:{port}")
    server.serve_forever()
