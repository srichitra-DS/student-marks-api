import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

with open("students.json") as f:
    student_data = json.load(f)

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.end_headers()

    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path != "/api":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        query = parse_qs(parsed_url.query)
        names = query.get("name", [])

        marks = []
        for name in names:
            mark = next((student["marks"] for student in student_data if student["name"] == name), None)
            marks.append(mark)

        response = json.dumps({ "marks": marks }).encode()

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")  # 🔥 This enables CORS
        self.end_headers()
        self.wfile.write(response)