from http.server import BaseHTTPRequestHandler, HTTPServer
import uuid
import json
import fakedb

class WebRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self) -> None:

        if self.path == '/':
            self.send_response(200)
            # self.send_header("Content-Type", "text/html")
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(self.get_users().encode("utf-8"))

    def do_POST(self) -> None:
        
        if self.path == '/user':

            content_length = int(self.headers.get("Content-Length", 0))

            new_user: str = self.rfile.read(content_length).decode("utf-8")

            self.add_user(new_user)

            self.send_response(201)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(new_user.encode("utf-8"))

    def get_users(self) -> str:
        
        my_users: list[dict[str, int | str]] = []
        for user in fakedb.users:
            result = {key: user.get(key, "-") for key in user.keys() if key != "id"}
            my_users.append(result)
         
        return json.dumps(my_users)

    def add_user(self, user: str) -> str:

        new_user: dict[str, str |int] = json.loads(user)
        new_user["id"] = str(uuid.uuid4())
        fakedb.users.append(new_user)
        return json.dumps(fakedb.users)

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    print("Listening http://localhost:8000")
    server.serve_forever()