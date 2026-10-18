from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import Product, SessionLocal

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Home page

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={}
    )


# View products

@app.get("/products", response_class=HTMLResponse)
def view_products(request: Request):
    with SessionLocal() as db:
        products = db.query(Product).all()

        return templates.TemplateResponse(
            request=request,
            name="products.html",
            context={"products": products}
        )


# Add product page

@app.get("/add-products", response_class=HTMLResponse)
def add_product_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="add_products.html",
        context={"error": ""}
    )


# Add product

@app.post("/add-product")
def add_product(
    request: Request,
    name: str = Form(...),
    price: float = Form(...),
    description: str = Form(""),
    link: str = Form(...)
):
    if "amazon.in" in link or "amazon.com" in link:
        with SessionLocal() as db:
            product = Product(
                name=name,
                price=price,
                description=description,
                link=link
            )

            db.add(product)
            db.commit()

        return templates.TemplateResponse(
    request=request,
    name="added.html",
    context={}
)
    else:
        return templates.TemplateResponse(
            request=request,
            name="add_products.html",
            context={"error": "Please enter an Amazon product link."}
        )


# Delete product

@app.post("/delete-product/{product_id}")
def delete_product(request:Request, product_id: int):
    with SessionLocal() as db:
        product = db.query(Product).filter(
            Product.id == product_id
        ).first()

        if product:
            db.delete(product)
            db.commit()

    return templates.TemplateResponse(
        request=request,
        name="deleted.html",
        context={}
    )