import json
from pathlib import Path
from django.http import Http404,JsonResponse,HttpResponse
from django.shortcuts import render
from django.urls import path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "dev-data" / "data.json"


#Load Json data from file
def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

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

def overview_view(request):
    data = load_data()
    template_overview = (BASE_DIR / "templates" / "template-overview.html").read_text(encoding="utf-8")
    template_card = (BASE_DIR / "templates" / "template-card.html").read_text(encoding="utf-8")
    cards_html = "".join([replace_template(template_card,product) for product in data])
    template_overview_with_cards = template_overview.replace("{%PRODUCT_CARDS%}", cards_html)
    
    return HttpResponse(template_overview_with_cards, content_type="text/html")

def product_view(request):
    query_params = request.GET
    product_id = int(query_params.get("id", 0))
    print("Product ID:", product_id)  # Debugging statement
    data = load_data()
    product = data[product_id]
    template_product = (BASE_DIR / "templates" / "template-product.html").read_text(encoding="utf-8")
    output = replace_template(template_product, product)
    return HttpResponse(output, content_type="text/html")

def api_view(request):
    data = load_data()
    return JsonResponse(data, safe=False)

def page_not_found_view(request, unmatched_path):
    page_not_found = "<h1>Page not found</h1>"
    return HttpResponse(page_not_found, content_type="text/html", status=404)



urlpatterns = [
    path('', overview_view, name='overview'),
    path('overview/', overview_view, name='overview'),
    path('product', product_view, name='product'),
    path('api/', api_view, name='api'),
    path('<path:unmatched_path>', page_not_found_view, name='page_not_found'),
]