import streamlit as st
import pandas as pd
import numpy as np
import os
import difflib

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="IA de Códigos - Multisuministros CR",
    layout="wide",
    page_icon=""
)

# =========================
# ESTILOS PERSONALIZADOS
# =========================
CUSTOM_CSS = """
<style>
/* Fondo general */
.stApp {
    background-color: #f5f7fb;
}

/* Encabezado principal */
.ms-header {
    background: linear-gradient(90deg, #004b9b, #e30613);
    padding: 18px 30px;
    border-radius: 12px;
    color: white;
    margin-bottom: 1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.18);
}

/* Título */
.ms-header-title {
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 0.03em;
}

/* Subtítulo */
.ms-header-subtitle {
    font-size: 0.95rem;
    opacity: 0.9;
}

/* Tarjetas */
.ms-card {
    background-color: white;
    border-radius: 12px;
    padding: 16px 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    margin-bottom: 1rem;
}

/* Etiquetas pequeñas */
.ms-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
}

/* Estados de precio */
.badge-ok {
    background-color: #e0f7e9;
    color: #1b7947;
}
.badge-bajo {
    background-color: #ffebee;
    color: #c62828;
}
.badge-alto {
    background-color: #fff8e1;
    color: #f9a825;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =========================
# CONSTANTES
# =========================
RUTA_CSV = "productos_codigos.csv"
COLUMNAS_BASE = [
    "codigo_interno",
    "descripcion",
    "categoria",
    "proveedor",
    "cabys",
    "unidad",
    "precio_costo",
    "margen_objetivo",
    "precio_sugerido",
    "precio_venta_actual",
    "estado_precio",
    "notas",
    "activo"
]


# =========================
# FUNCIONES DE DATOS
# =========================
def crear_df_vacio():
    df = pd.DataFrame(columns=COLUMNAS_BASE)
    return df


def cargar_datos():
    if os.path.exists(RUTA_CSV):
        df = pd.read_csv(RUTA_CSV, dtype=str)
        # Convertir numéricos
        for col in ["precio_costo", "margen_objetivo", "precio_sugerido", "precio_venta_actual"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        if "activo" in df.columns:
            df["activo"] = df["activo"].fillna("Sí")
        else:
            df["activo"] = "Sí"
        # Asegurar todas las columnas
        for col in COLUMNAS_BASE:
            if col not in df.columns:
                if col == "activo":
                    df[col] = "Sí"
                else:
                    df[col] = np.nan
        return df[COLUMNAS_BASE]
    else:
        return crear_df_vacio()


def guardar_datos(df):
    df.to_csv(RUTA_CSV, index=False)


def calcular_precio_sugerido(precio_costo, margen_objetivo):
    """
    margen_objetivo viene como porcentaje (ej: 65 -> 65%)
    """
    try:
        if precio_costo is None:
            return None
        costo = float(precio_costo)
        margen = float(margen_objetivo) / 100.0
        return round(costo * (1 + margen), 2)
    except Exception:
        return None


def clasificar_estado_precio(precio_sugerido, precio_venta):
    """
    Devuelve: "OK", "Por debajo", "Por encima" o "Sin dato".
    """
    try:
        if pd.isna(precio_venta) or precio_venta == 0:
            return "Sin dato"
        if pd.isna(precio_sugerido) or precio_sugerido == 0:
            return "Sin dato"
        # Tolerancia del 5 %
        limite_inferior = precio_sugerido * 0.95
        limite_superior = precio_sugerido * 1.05
        if limite_inferior <= precio_venta <= limite_superior:
            return "OK"
        elif precio_venta < limite_inferior:
            return "Por debajo"
        else:
            return "Por encima"
    except Exception:
        return "Sin dato"


def badge_estado_html(estado):
    if estado == "OK":
        return '<span class="ms-badge badge-ok">Precio OK</span>'
    elif estado == "Por debajo":
        return '<span class="ms-badge badge-bajo">Por debajo del sugerido</span>'
    elif estado == "Por encima":
        return '<span class="ms-badge badge-alto">Por encima del sugerido</span>'
    else:
        return '<span class="ms-badge">Sin dato</span>'


# =========================
# INICIALIZAR SESIÓN
# =========================
if "df_productos" not in st.session_state:
    st.session_state.df_productos = cargar_datos()


# =========================
# ENCABEZADO
# =========================
st.markdown(
    """
    <div class="ms-header">
        <div class="ms-header-title">🧠 IA de Códigos - Multisuministros de Costa Rica</div>
        <div class="ms-header-subtitle">
            Búsqueda inteligente de productos, CABYS y control de precios con margen automático.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title(" Configuración")

margen_global = st.sidebar.number_input(
    "Margen objetivo por defecto (%)",
    min_value=0.0,
    max_value=200.0,
    value=65.0,
    step=0.5
)

st.sidebar.info(
    " Consejo: podés ir agregando productos poco a poco. "
    "La app guarda todo en el archivo `productos_codigos.csv`."
)

# =========================
# TABS PRINCIPALES
# =========================
tab_busqueda, tab_admin, tab_alertas = st.tabs(
    [" Buscador inteligente", " Administrar productos", " Alertas inteligentes"]
)

df = st.session_state.df_productos

# =========================
# TAB 1: BUSCADOR INTELIGENTE
# =========================
with tab_busqueda:
    st.markdown('<div class="ms-card">', unsafe_allow_html=True)
    st.subheader(" Buscador IA de códigos y productos")

    col_q1, col_q2 = st.columns([3, 1])

    with col_q1:
        consulta = st.text_input(
            "Escribí código, CABYS, descripción o proveedor",
            placeholder="Ej: servilleta, 413172, papel higiénico, FACELA..."
        )

    with col_q2:
        tipo_busqueda = st.selectbox(
            "Tipo de búsqueda",
            ["Automática", "Código interno", "CABYS", "Descripción", "Proveedor"]
        )

    if consulta.strip():
        consulta_lower = consulta.strip().lower()

        if tipo_busqueda == "Código interno":
            mask = df["codigo_interno"].astype(str).str.contains(consulta_lower, case=False, na=False)
            resultados = df[mask]

        elif tipo_busqueda == "CABYS":
            mask = df["cabys"].astype(str).str.contains(consulta_lower, case=False, na=False)
            resultados = df[mask]

        elif tipo_busqueda == "Proveedor":
            mask = df["proveedor"].astype(str).str.contains(consulta_lower, case=False, na=False)
            resultados = df[mask]

        elif tipo_busqueda == "Descripción":
            # Búsqueda directa + similar
            mask = df["descripcion"].astype(str).str.contains(consulta_lower, case=False, na=False)
            resultados_directos = df[mask]

            # Inteligente por similitud
            descripciones = df["descripcion"].astype(str).tolist()
            similares = difflib.get_close_matches(consulta, descripciones, n=20, cutoff=0.3)
            resultados_similares = df[df["descripcion"].isin(similares)]

            resultados = pd.concat([resultados_directos, resultados_similares]).drop_duplicates()

        else:  # Automática
            mask_codigo = df["codigo_interno"].astype(str).str.contains(consulta_lower, case=False, na=False)
            mask_cabys = df["cabys"].astype(str).str.contains(consulta_lower, case=False, na=False)
            mask_desc = df["descripcion"].astype(str).str.contains(consulta_lower, case=False, na=False)
            mask_prov = df["proveedor"].astype(str).str.contains(consulta_lower, case=False, na=False)

            resultados = df[mask_codigo | mask_cabys | mask_desc | mask_prov]

            # Si no encuentra nada, probamos similitud por descripción
            if resultados.empty:
                descripciones = df["descripcion"].astype(str).tolist()
                similares = difflib.get_close_matches(consulta, descripciones, n=20, cutoff=0.3)
                resultados = df[df["descripcion"].isin(similares)]

        st.markdown("#### Resultados encontrados")

        if resultados.empty:
            st.warning("No se encontraron productos con esa búsqueda.")
        else:
            # Mostrar una vista amigable
            vista = resultados.copy()
            # Ordenar columnas para la vista del buscador
            cols_vista = [
                "codigo_interno", "descripcion", "cabys", "proveedor",
                "precio_costo", "margen_objetivo", "precio_sugerido",
                "precio_venta_actual", "estado_precio"
            ]
            cols_vista = [c for c in cols_vista if c in vista.columns]
            vista = vista[cols_vista]
            st.dataframe(vista, use_container_width=True, hide_index=True)

            # Detalle de un producto específico
            cods_disp = vista["codigo_interno"].dropna().unique().tolist()
            if cods_disp:
                st.markdown("---")
                cod_seleccionado = st.selectbox(
                    "Ver detalle de un producto específico (por código interno)",
                    options=["(Ninguno)"] + cods_disp
                )
                if cod_seleccionado != "(Ninguno)":
                    prod = resultados[resultados["codigo_interno"] == cod_seleccionado].iloc[0]
                    st.markdown("##### Detalle del producto")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**Código interno:**", prod["codigo_interno"])
                        st.write("**Descripción:**", prod["descripcion"])
                        st.write("**Proveedor:**", prod["proveedor"])
                        st.write("**Categoría:**", prod["categoria"])
                        st.write("**Unidad:**", prod["unidad"])
                    with col_b:
                        st.write("**CABYS:**", prod["cabys"])
                        st.write("**Precio costo:**", prod["precio_costo"])
                        st.write("**Margen objetivo (%):**", prod["margen_objetivo"])
                        st.write("**Precio sugerido:**", prod["precio_sugerido"])
                        st.write("**Precio venta actual:**", prod["precio_venta_actual"])
                        st.markdown(
                            badge_estado_html(prod.get("estado_precio", "Sin dato")),
                            unsafe_allow_html=True
                        )
                        st.write("**Notas:**", prod.get("notas", ""))

    else:
        st.info("Escribí algo en la barra de búsqueda para empezar a usar la IA de códigos. ")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB 2: ADMINISTRAR PRODUCTOS
# =========================
with tab_admin:
    st.markdown('<div class="ms-card">', unsafe_allow_html=True)
    st.subheader(" Agregar / editar productos")

    modo = st.radio(
        "¿Qué querés hacer?",
        ["Agregar nuevo producto", "Editar producto existente"],
        horizontal=True
    )

    if modo == "Agregar nuevo producto":
        with st.form("form_nuevo_producto"):
            col1, col2 = st.columns(2)

            with col1:
                codigo_interno = st.text_input("Código interno *")
                descripcion = st.text_input("Descripción *")
                categoria = st.text_input("Categoría")
                proveedor = st.text_input("Proveedor")
                unidad = st.text_input("Unidad (ej. unidad, caja, pqt)", value="unidad")

            with col2:
                cabys = st.text_input("Código CABYS")
                precio_costo = st.number_input("Precio costo", min_value=0.0, value=0.0, step=1.0)
                margen_obj = st.number_input(
                    "Margen objetivo (%)",
                    min_value=0.0, max_value=200.0,
                    value=float(margen_global),
                    step=0.5
                )
                precio_venta_actual = st.number_input(
                    "Precio venta actual",
                    min_value=0.0,
                    value=0.0,
                    step=1.0
                )
                notas = st.text_area("Notas", height=80)

            activo = st.checkbox("Producto activo", value=True)

            enviado = st.form_submit_button(" Guardar producto")

            if enviado:
                if not codigo_interno or not descripcion:
                    st.error("Los campos con * son obligatorios (código interno y descripción).")
                else:
                    precio_sug = calcular_precio_sugerido(precio_costo, margen_obj)
                    estado_precio = clasificar_estado_precio(precio_sug, precio_venta_actual)

                    nuevo = {
                        "codigo_interno": codigo_interno.strip(),
                        "descripcion": descripcion.strip(),
                        "categoria": categoria.strip(),
                        "proveedor": proveedor.strip(),
                        "cabys": cabys.strip(),
                        "unidad": unidad.strip(),
                        "precio_costo": precio_costo,
                        "margen_objetivo": margen_obj,
                        "precio_sugerido": precio_sug,
                        "precio_venta_actual": precio_venta_actual if precio_venta_actual > 0 else np.nan,
                        "estado_precio": estado_precio,
                        "notas": notas.strip(),
                        "activo": "Sí" if activo else "No"
                    }

                    st.session_state.df_productos = pd.concat(
                        [st.session_state.df_productos, pd.DataFrame([nuevo])],
                        ignore_index=True
                    )
                    guardar_datos(st.session_state.df_productos)
                    st.success(" Producto agregado correctamente.")

    else:  # Editar producto existente
        if df.empty:
            st.warning("No hay productos registrados todavía. Primero agregá alguno.")
        else:
            opciones = (df["codigo_interno"].astype(str) + " - " +
                        df["descripcion"].astype(str)).tolist()
            opcion_sel = st.selectbox(
                "Seleccioná el producto a editar",
                options=opciones
            )

            idx = opciones.index(opcion_sel)
            producto_sel = df.iloc[idx]

            with st.form("form_editar_producto"):
                col1, col2 = st.columns(2)

                with col1:
                    codigo_interno = st.text_input(
                        "Código interno *",
                        value=str(producto_sel["codigo_interno"])
                    )
                    descripcion = st.text_input(
                        "Descripción *",
                        value=str(producto_sel["descripcion"])
                    )
                    categoria = st.text_input(
                        "Categoría",
                        value=str(producto_sel["categoria"])
                    )
                    proveedor = st.text_input(
                        "Proveedor",
                        value=str(producto_sel["proveedor"])
                    )
                    unidad = st.text_input(
                        "Unidad",
                        value=str(producto_sel["unidad"])
                    )

                with col2:
                    cabys = st.text_input(
                        "Código CABYS",
                        value=str(producto_sel["cabys"])
                    )
                    precio_costo = st.number_input(
                        "Precio costo",
                        min_value=0.0,
                        value=float(producto_sel["precio_costo"])
                        if not pd.isna(producto_sel["precio_costo"]) else 0.0,
                        step=1.0
                    )
                    margen_obj = st.number_input(
                        "Margen objetivo (%)",
                        min_value=0.0, max_value=200.0,
                        value=float(producto_sel["margen_objetivo"])
                        if not pd.isna(producto_sel["margen_objetivo"]) else float(margen_global),
                        step=0.5
                    )
                    precio_venta_actual = st.number_input(
                        "Precio venta actual",
                        min_value=0.0,
                        value=float(producto_sel["precio_venta_actual"])
                        if not pd.isna(producto_sel["precio_venta_actual"]) else 0.0,
                        step=1.0
                    )
                    notas = st.text_area(
                        "Notas",
                        value=str(producto_sel["notas"])
                        if not pd.isna(producto_sel["notas"]) else "",
                        height=80
                    )

                activo = st.checkbox(
                    "Producto activo",
                    value=(str(producto_sel["activo"]) == "Sí")
                )

                enviado = st.form_submit_button(" Guardar cambios")

                if enviado:
                    if not codigo_interno or not descripcion:
                        st.error("Los campos con * son obligatorios (código interno y descripción).")
                    else:
                        precio_sug = calcular_precio_sugerido(precio_costo, margen_obj)
                        estado_precio = clasificar_estado_precio(precio_sug, precio_venta_actual)

                        st.session_state.df_productos.at[idx, "codigo_interno"] = codigo_interno.strip()
                        st.session_state.df_productos.at[idx, "descripcion"] = descripcion.strip()
                        st.session_state.df_productos.at[idx, "categoria"] = categoria.strip()
                        st.session_state.df_productos.at[idx, "proveedor"] = proveedor.strip()
                        st.session_state.df_productos.at[idx, "cabys"] = cabys.strip()
                        st.session_state.df_productos.at[idx, "unidad"] = unidad.strip()
                        st.session_state.df_productos.at[idx, "precio_costo"] = precio_costo
                        st.session_state.df_productos.at[idx, "margen_objetivo"] = margen_obj
                        st.session_state.df_productos.at[idx, "precio_sugerido"] = precio_sug
                        st.session_state.df_productos.at[idx, "precio_venta_actual"] = (
                            precio_venta_actual if precio_venta_actual > 0 else np.nan
                        )
                        st.session_state.df_productos.at[idx, "estado_precio"] = estado_precio
                        st.session_state.df_productos.at[idx, "notas"] = notas.strip()
                        st.session_state.df_productos.at[idx, "activo"] = "Sí" if activo else "No"

                        guardar_datos(st.session_state.df_productos)
                        st.success(" Cambios guardados correctamente.")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB 3: ALERTAS INTELIGENTES
# =========================
with tab_alertas:
    st.markdown('<div class="ms-card">', unsafe_allow_html=True)
    st.subheader(" Alertas inteligentes de productos")

    if df.empty:
        st.info("Todavía no hay productos registrados para analizar.")
    else:
        # Productos sin CABYS
        sin_cabys = df[(df["cabys"].isna()) | (df["cabys"].astype(str).str.strip() == "")]
        # Productos con precio venta por debajo del sugerido
        por_debajo = df[df["estado_precio"] == "Por debajo"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Productos sin CABYS")
            if sin_cabys.empty:
                st.success(" Todos los productos registrados tienen CABYS.")
            else:
                st.dataframe(
                    sin_cabys[["codigo_interno", "descripcion", "proveedor", "precio_costo"]],
                    use_container_width=True,
                    hide_index=True
                )

        with col2:
            st.markdown("#### Precios por debajo del sugerido")
            if por_debajo.empty:
                st.success(" No hay productos con precio por debajo del sugerido.")
            else:
                st.dataframe(
                    por_debajo[
                        ["codigo_interno", "descripcion", "precio_costo",
                         "margen_objetivo", "precio_sugerido", "precio_venta_actual"]
                    ],
                    use_container_width=True,
                    hide_index=True
                )

        st.markdown("---")
        st.caption(
            "Estas alertas se actualizan automáticamente según los datos que registrés "
            "en la pestaña de administración."
        )

    st.markdown('</div>', unsafe_allow_html=True)
