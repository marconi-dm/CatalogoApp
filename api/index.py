import os

import psycopg
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string

load_dotenv()

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
SITE_URL = os.getenv(
    "SITE_URL",
    "https://esco-products.vercel.app"
)

@app.route("/")
def home():
    return "CatalogoApp API funcionando!"


# =========================================================
# LISTAR TODOS OS PRODUTOS
# =========================================================

@app.route("/api/products")
def get_products():
    if not DATABASE_URL:
        return jsonify({"error": "DATABASE_URL não configurada"}), 500

    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:

                cursor.execute("""
                    SELECT
                        id,
                        title,
                        item_description,
                        unit_weight,
                        base_code,
                        machine,
                        item_category,
                        specifications,
                        pmid,
                        media,
                        system_type
                    FROM products
                    WHERE active = TRUE
                    ORDER BY title;
                """)

                rows = cursor.fetchall()

                products = []

                for row in rows:
                    products.append({
                        "id": row[0],
                        "title": row[1],
                        "item_description": row[2],
                        "unit_weight": float(row[3]) if row[3] is not None else None,
                        "base_code": row[4],
                        "machine": row[5],
                        "item_category": row[6],
                        "specifications": row[7],
                        "pmid": row[8],
                        "media": row[9],
                        "system_type": row[10],
                    })

                return jsonify(products)

    except Exception as error:
        print(f"Erro ao acessar o banco: {error}")

        return jsonify({
            "error": "Erro ao acessar o banco de dados"
        }), 500


# =========================================================
# BUSCAR PRODUTO INDIVIDUAL + COMPATIBILIDADE
# =========================================================

@app.route("/api/products/<int:product_id>")
def get_product(product_id):
    if not DATABASE_URL:
        return jsonify({"error": "DATABASE_URL não configurada"}), 500

    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:

                # -------------------------------------------------
                # PRODUTO PRINCIPAL
                # -------------------------------------------------

                cursor.execute("""
                    SELECT
                        id,
                        title,
                        item_description,
                        unit_weight,
                        base_code,
                        machine,
                        item_category,
                        specifications,
                        pmid,
                        media,
                        system_type
                    FROM products
                    WHERE id = %s
                      AND active = TRUE;
                """, (product_id,))

                row = cursor.fetchone()

                if not row:
                    return jsonify({
                        "error": "Produto não encontrado"
                    }), 404

                product = {
                    "id": row[0],
                    "title": row[1],
                    "item_description": row[2],
                    "unit_weight": float(row[3]) if row[3] is not None else None,
                    "base_code": row[4],
                    "machine": row[5],
                    "item_category": row[6],
                    "specifications": row[7],
                    "pmid": row[8],
                    "media": row[9],
                    "system_type": row[10],
                }

                base_code = product["base_code"]
                machine = product["machine"]
                category = product["item_category"]


                # -------------------------------------------------
                # CONVERTE RESULTADO SQL EM JSON
                # -------------------------------------------------

                def rows_to_products(rows):
                    return [
                        {
                            "id": item[0],
                            "title": item[1],
                            "item_description": item[2],
                            "unit_weight": float(item[3])
                            if item[3] is not None
                            else None,
                            "base_code": item[4],
                            "machine": item[5],
                            "item_category": item[6],
                            "specifications": item[7],
                            "pmid": item[8],
                            "media": item[9],
                            "system_type": item[10],
                        }
                        for item in rows
                    ]


                # -------------------------------------------------
                # LISTAS DE COMPATIBILIDADE
                # -------------------------------------------------

                compatible_adapters = []
                compatible_points = []
                compatible_locks = []
                compatible_pin_collar = []


                # -------------------------------------------------
                # COMPATIBILIDADE
                # -------------------------------------------------

                if base_code:

                    # =================================================
                    # POINT / MAXDRP POINT
                    # =================================================

                    if category in ("POINT", "MAXDRP POINT"):

                        # ADAPTER
                        # Mesmo BaseCode + mesma Machine

                        cursor.execute("""
                            SELECT
                                id,
                                title,
                                item_description,
                                unit_weight,
                                base_code,
                                machine,
                                item_category,
                                specifications,
                                pmid,
                                media,
                                system_type
                            FROM products
                            WHERE active = TRUE
                              AND base_code = %s
                              AND machine = %s
                              AND item_category = 'ADAPTER'
                            ORDER BY pmid;
                        """, (base_code, machine))

                        compatible_adapters = rows_to_products(
                            cursor.fetchall()
                        )


                        # LOCK
                        # Mesmo BaseCode

                        cursor.execute("""
                            SELECT
                                id,
                                title,
                                item_description,
                                unit_weight,
                                base_code,
                                machine,
                                item_category,
                                specifications,
                                pmid,
                                media,
                                system_type
                            FROM products
                            WHERE active = TRUE
                              AND base_code = %s
                              AND item_category = 'LOCK'
                            ORDER BY pmid;
                        """, (base_code,))

                        compatible_locks = rows_to_products(
                            cursor.fetchall()
                        )


                        # PIN / COLLAR
                        # Mesmo BaseCode

                        cursor.execute("""
                            SELECT
                                id,
                                title,
                                item_description,
                                unit_weight,
                                base_code,
                                machine,
                                item_category,
                                specifications,
                                pmid,
                                media,
                                system_type
                            FROM products
                            WHERE active = TRUE
                              AND base_code = %s
                              AND item_category = 'PIN/COLLAR'
                            ORDER BY pmid;
                        """, (base_code,))

                        compatible_pin_collar = rows_to_products(
                            cursor.fetchall()
                        )


                    # =================================================
                    # ADAPTER
                    # =================================================

                    elif category == "ADAPTER":

                        # POINT / MAXDRP POINT
                        # Mesmo BaseCode + mesma Machine

                        cursor.execute("""
                            SELECT
                                id,
                                title,
                                item_description,
                                unit_weight,
                                base_code,
                                machine,
                                item_category,
                                specifications,
                                pmid,
                                media,
                                system_type
                            FROM products
                            WHERE active = TRUE
                              AND base_code = %s
                              AND machine = %s
                              AND item_category IN (
                                  'POINT',
                                  'MAXDRP POINT'
                              )
                            ORDER BY pmid;
                        """, (base_code, machine))

                        compatible_points = rows_to_products(
                            cursor.fetchall()
                        )


                    # =================================================
                    # LOCK / PIN-COLLAR
                    # =================================================

                    elif category in ("LOCK", "PIN/COLLAR"):

                        # POINT / MAXDRP POINT
                        # Mesmo BaseCode

                        cursor.execute("""
                            SELECT
                                id,
                                title,
                                item_description,
                                unit_weight,
                                base_code,
                                machine,
                                item_category,
                                specifications,
                                pmid,
                                media,
                                system_type
                            FROM products
                            WHERE active = TRUE
                              AND base_code = %s
                              AND item_category IN (
                                  'POINT',
                                  'MAXDRP POINT'
                              )
                            ORDER BY pmid;
                        """, (base_code,))

                        compatible_points = rows_to_products(
                            cursor.fetchall()
                        )


                # -------------------------------------------------
                # RESPOSTA FINAL
                # -------------------------------------------------

                product["compatible"] = {
                    "adapters": compatible_adapters,
                    "points": compatible_points,
                    "locks": compatible_locks,
                    "pin_collar": compatible_pin_collar,
                }

                return jsonify(product)

    except Exception as error:
        print(f"Erro ao acessar produto: {error}")

        return jsonify({
            "error": "Erro ao acessar o banco de dados"
        }), 500

# =========================================================
# COMPARTILHAMENTO / OPEN GRAPH
# =========================================================

@app.route("/share/produto/<int:product_id>")
def share_product(product_id):
    if not DATABASE_URL:
        return "DATABASE_URL não configurada", 500

    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        pmid,
                        item_description,
                        specifications,
                        media
                    FROM products
                    WHERE id = %s
                      AND active = TRUE;
                    """,
                    (product_id,)
                )

                row = cursor.fetchone()

                if not row:
                    return "Produto não encontrado", 404

                pmid = row[0]
                item_description = row[1]
                specifications = row[2]
                media = row[3]

                title = (
                    f"ESCO® GET — PMID {pmid}"
                    if pmid
                    else "ESCO® GET"
                )

                raw_description = (
                    item_description
                    or specifications
                    or "Conheça este produto ESCO® GET."
                )

                description = " ".join(
                    raw_description.split()
                )

                if len(description) > 180:
                    description = (
                        description[:177].rstrip()
                        + "..."
                    )

                if media:
                    media_name = (
                        media
                        .strip()
                        .replace(" ", "_")
                    )

                    image_url = (
                        "https://res.cloudinary.com/"
                        "gjkugh3z/image/upload/"
                        "w_1200,h_630,c_pad,b_white,"
                        "f_jpg,q_auto/"
                        f"{media_name}.jpg"
                    )

                else:
                    image_url = (
                        "https://res.cloudinary.com/"
                        "gjkugh3z/image/upload/"
                        "w_1200,h_630,c_pad,b_white,"
                        "f_jpg,q_auto/"
                        "v1789928458/Weir_Group.jpg"
                    )

                product_url = (
                    f"{SITE_URL}/produto/{product_id}"
                )

                share_url = (
                    f"{SITE_URL}/share/produto/{product_id}"
                )

                html = """
                <!DOCTYPE html>

                <html lang="pt-BR">

                <head>

                    <meta charset="UTF-8">

                    <meta
                        name="viewport"
                        content="width=device-width, initial-scale=1.0"
                    >

                    <title>{{ title }}</title>

                    <meta
                        property="og:title"
                        content="{{ title }}"
                    >

                    <meta
                        property="og:description"
                        content="{{ description }}"
                    >

                    <meta
                        property="og:image"
                        content="{{ image_url }}"
                    >

                    <meta
                        property="og:image:secure_url"
                        content="{{ image_url }}"
                    >

                    <meta
                        property="og:image:type"
                        content="image/jpeg"
                    >

                    <meta
                        property="og:image:width"
                        content="1200"
                    >

                    <meta
                        property="og:image:height"
                        content="630"
                    >

                    <meta
                        property="og:url"
                        content="{{ share_url }}"
                    >

                    <meta
                        property="og:type"
                        content="product"
                    >

                    <meta
                        property="og:site_name"
                        content="ESCO® GET"
                    >

                    <meta
                        name="twitter:card"
                        content="summary_large_image"
                    >

                    <meta
                        name="twitter:title"
                        content="{{ title }}"
                    >

                    <meta
                        name="twitter:description"
                        content="{{ description }}"
                    >

                    <meta
                        name="twitter:image"
                        content="{{ image_url }}"
                    >

                    <link
                        rel="canonical"
                        href="{{ product_url }}"
                    >

                </head>

                <body>

                    <p>
                        Abrindo produto ESCO® GET...
                    </p>

                    <p>
                        <a href="{{ product_url }}">
                            Ver produto
                        </a>
                    </p>

                    <script>
                        window.location.replace(
                            {{ product_url | tojson }}
                        );
                    </script>

                </body>

                </html>
                """

                return render_template_string(
                    html,
                    title=title,
                    description=description,
                    image_url=image_url,
                    product_url=product_url,
                    share_url=share_url,
                )

    except Exception as error:
        print(
            f"Erro ao gerar compartilhamento: {error}"
        )

        return "Erro ao carregar produto", 500