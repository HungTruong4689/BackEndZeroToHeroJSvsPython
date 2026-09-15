# import time


# #PRINT A FILE
# with open("./txt/input.txt", "r",encoding='utf-8') as f:
#     text_in =f.read()

# print(text_in)
# text_out = "This is what we know about the avocado: \n" + text_in + "\nCreated on " + time.ctime() + "\n\n"

# #WRITE A FILE
# with open("./txt/output.txt", "w",encoding='utf-8') as f:
#     f.write(text_out)

# print("File written!")
import http.server
import json
import socketserver
from pathlib import Path
import socketserver
from urllib.parse import urlparse, parse_qs

BASE_DIR = Path(__file__).resolve().parent

def replace_template(template,product):
    output = template
    output  = output.replace("{%PRODUCT_NAME%}", str(product.get("productName","")))
    output = output.replace("{%PRODUCT_EMOJI%}", str(product.get("image","")))
    output  = output.replace("{%PRODUCT_PRICE%}", str(product.get("price","")))
    output = output.replace("{%PRODUCT_ORIGIN%}", str(product.get("from","")))
    output = output.replace("{%PRODUCT_NUTRIENTS%}", str(product.get("nutrients","")))
    output = output.replace("{%PRODUCT_QUANTITY%}", str(product.get("quantity","")))
    output  = output.replace("{%PRODUCT_DESCRIPTION%}", str(product.get("description","")))
    output = output.replace("{%PRODUCT_ID%}", str(product.get("id","")))
    if not product.get("organic",False):
        output = output.replace("{%NOT_ORGANIC%}", "not-organic")
    return output

temp_overview = (BASE_DIR / "templates" / "template-overview.html").read_text(encoding="utf-8")
temp_card = (BASE_DIR / "templates" / "template-card.html").read_text(encoding="utf-8")
temp_product = (BASE_DIR / "templates" / "template-product.html").read_text(encoding="utf-8")
data = json.loads((BASE_DIR / "dev-data" / "data.json").read_text(encoding="utf-8"))

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        pathname = parsed_url.path
        if pathname == "/" or pathname == "/overview":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            #print("check data from json file: ", data)
            cards_html = "".join([replace_template(temp_card, product) for product in data])
            temp_overview_with_cards = temp_overview.replace("{%PRODUCT_CARDS%}", cards_html)
            self.wfile.write(temp_overview_with_cards.encode("utf-8"))
        elif pathname == "/product":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            query_params = parse_qs(parsed_url.query)
            product_id = int(query_params.get("id", [0])[0])
            product = data[product_id]
            output = replace_template(temp_product, product)
            self.wfile.write(output.encode("utf-8"))
        elif pathname == "/api":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        else:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Page not found</h1>")

HOST = "127.0.0.1"
PORT = 9000

if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer((HOST, PORT), CustomHTTPRequestHandler) as httpd:
        url = f"http://{HOST}:{PORT}"
        clickable_url = f"\033]8;;{url}\033\\\033[34m{url}\033[0m\033]8;;\033\\"
        print(f"Listening for requests on port {PORT}... Click here to open: {clickable_url}")
        httpd.serve_forever()