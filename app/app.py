from flask import Flask, render_template, redirect, url_for, session
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key = "clave_secreta_123"


# ==========================================================
# LISTA DE PRODUCTOS
# Para agregar un producto nuevo, copia uno de estos bloques
# y cambia id, nombre, precio, descripcion e imagen.
# La imagen debe estar en: static/sources/
# ==========================================================
productos = [
    {
        "id": 1,
        "nombre": "9 AM Dive",
        "precio": 150000,
        "descripcion": "Fragancia fresca y acuática ideal para uso diario.",
        "imagen": "sources/9 am dive (1).png"
    },
    {
        "id": 2,
        "nombre": "Eros Flame",
        "precio": 220000,
        "descripcion": "Perfume intenso con notas cítricas y especiadas.",
        "imagen": "sources/EROS FLAME.png"
    },
    {
        "id": 3,
        "nombre": "Her Confession",
        "precio": 180000,
        "descripcion": "Aroma femenino elegante y sofisticado.",
        "imagen": "sources/Her Confession.png"
    },
    {
        "id": 4,
        "nombre": "Khamrah Qahwa",
        "precio": 200000,
        "descripcion": "Fragancia dulce con notas de café y vainilla.",
        "imagen": "sources/Khamrah Qahwa.png"
    },{
        "id": 5,
        "nombre": "Club de nuit sillage",
        "precio": 130000,
        "descripcion": "Club de Nuit Sillage de Armaf es una cautivadora fragancia masculina que pertenece a la familia olfativa Almizcle Floral Amaderado. Este perfume, lanzado en 2020, ofrece una combinación intrigante de notas que crean una experiencia olfativa única y atractiva.",
        "imagen": "sources/club de nuit.png"
    }
]


# ==========================================================
# FUNCIONES AUXILIARES
# ==========================================================
def obtener_producto(id):
    return next((p for p in productos if p["id"] == id), None)


def obtener_carrito():
    return session.get("carrito", [])


# ==========================================================
# RUTAS PRINCIPALES
# ==========================================================
@app.route("/")
def inicio():
    return render_template("index.html", productos=productos)


@app.route("/producto/<int:id>")
def detalle_producto(id):
    producto = obtener_producto(id)

    if producto:
        return render_template("detalle.html", producto=producto)

    return render_template("404.html"), 404


# ==========================================================
# CARRITO
# ==========================================================
@app.route("/agregar-carrito/<int:id>")
def agregar_carrito(id):
    producto = obtener_producto(id)

    if not producto:
        return render_template("404.html"), 404

    carrito = obtener_carrito()

    # Si el producto ya existe en el carrito, aumenta cantidad
    for item in carrito:
        if item["id"] == id:
            item["cantidad"] += 1
            break
    else:
        # Si no existe, lo agrega
        carrito.append({
            "id": producto["id"],
            "nombre": producto["nombre"],
            "precio": producto["precio"],
            "imagen": producto["imagen"],
            "cantidad": 1
        })

    session["carrito"] = carrito

    return redirect(url_for("ver_carrito"))


@app.route("/carrito")
def ver_carrito():
    carrito = obtener_carrito()
    total = sum(item["precio"] * item["cantidad"] for item in carrito)

    return render_template(
        "carrito.html",
        carrito=carrito,
        total=total
    )


@app.route("/eliminar-del-carrito/<int:id>")
def eliminar_del_carrito(id):
    carrito = [
        item for item in obtener_carrito()
        if item["id"] != id
    ]

    session["carrito"] = carrito
    return redirect(url_for("ver_carrito"))


@app.route("/vaciar-carrito")
def vaciar_carrito():
    session["carrito"] = []
    return redirect(url_for("ver_carrito"))


# ==========================================================
# COMPRA Y COMPROBANTE
# ==========================================================
@app.route("/comprar")
def comprar():
    carrito = obtener_carrito()

    if not carrito:
        return redirect(url_for("inicio"))

    total = sum(
        item["precio"] * item["cantidad"]
        for item in carrito
    )

    comprobante = {
        "numero": random.randint(100000, 999999),
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "items": carrito,
        "total": total
    }

    # Vaciar carrito después de comprar
    session["carrito"] = []

    return render_template(
        "comprobante.html",
        comprobante=comprobante
    )


# ==========================================================
# ERROR 404
# ==========================================================
@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================
if __name__ == "__main__":
    app.run(debug=True)