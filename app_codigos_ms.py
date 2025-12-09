import streamlit as st
import pandas as pd
import numpy as np
import os
import difflib
import uuid
from datetime import datetime
import base64

def set_fondo_login():
    with open("login_fondo.jpg", "rb") as img_file:
        img_bytes = img_file.read()
    img_base64 = base64.b64encode(img_bytes).decode()

    st.markdown(
        f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{img_base64}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="IA de Códigos - Multisuministros CR",
    layout="wide",
    page_icon="🤖"
)

# =========================
# ESTILOS PERSONALIZADOS
# =========================
CUSTOM_CSS = """
<style>
/* Fondo general */
.stApp {
    background: radial-gradient(circle at top, #e3f2fd 0, #f8f9ff 35%, #eef2ff 100%);
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Encabezado principal */
.ms-header {
    background: linear-gradient(90deg, #003c8f, #1976d2, #e30613);
    padding: 18px 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 1.2rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.20);
    display: flex;
    align-items: center;
    gap: 16px;
}

.ms-header-icon {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    background: radial-gradient(circle at 30% 30%, #ff80ab, #c51162);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    box-shadow: 0 0 18px rgba(255, 128, 171, 0.9);
}

.ms-header-title {
    font-size: 1.9rem;
    font-weight: 750;
    letter-spacing: 0.04em;
}

.ms-header-subtitle {
    font-size: 0.95rem;
    opacity: 0.9;
}

/* Tarjetas */
.ms-card {
    background-color: white;
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.12);
    margin-bottom: 1.2rem;
}

/* Badges */
.ms-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 600;
}

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

/* Login */
.login-bg {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
}

.login-card {
    background: rgba(255,255,255,0.96);
    padding: 32px 30px 26px 30px;
    border-radius: 24px;
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.35);
    max-width: 420px;
    width: 100%;
    text-align: center;
}

.login-robot {
    width: 80px;
    height: 80px;
    border-radius: 26px;
    background: radial-gradient(circle at 30% 20%, #ff80ab, #7e57c2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 3rem;
    margin: 0 auto 14px auto;
    box-shadow: 0 0 28px rgba(126, 87, 194, 0.8);
}

.login-title {
    font-size: 1.35rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
}

.login-subtitle {
    font-size: 0.9rem;
    color: #4b5563;
    margin-bottom: 1.4rem;
}

.login-footer {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-top: 0.75rem;
}

/* Sidebar user info */
.sidebar-user-box {
    padding: 10px 12px;
    border-radius: 14px;
    background: rgba(255,255,255,0.9);
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.10);
    font-size: 0.85rem;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 999px;
    padding-top: 4px;
    padding-bottom: 4px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# =========================
# USUARIOS Y ROLES
# =========================
USERS = {
    # === ADMINISTRADORES ===
    "Aherrera": {
        "password": "Aherrera2025!",
        "role": "admin",
        "nombre": "Alison Herrera"
    },
    "Jcorrales": {
        "password": "Jcorrales2025!",
        "role": "admin",
        "nombre": "Jcorrales"
    },
    "Acamacho": {
        "password": "Acamacho2025!",
        "role": "admin",
        "nombre": "Acamacho"
    },

    # === VENDEDORES ===
    "Lsibaja": {
        "password": "Lsibaja2025!",
        "role": "vendedor",
        "nombre": "Lsibaja"
    },
    "Bmadrigal": {
        "password": "Bmadrigal2025!",
        "role": "vendedor",
        "nombre": "Bmadrigal"
    },
    "Jorozco": {
        "password": "Jorozco2025!",
        "role": "vendedor",
        "nombre": "Jorozco"
    },
    "Ypadilla": {
        "password": "Ypadilla2025!",
        "role": "vendedor",
        "nombre": "Ypadilla"
    },
    "Odiaz": {
        "password": "Odiaz2025!",
        "role": "vendedor",
        "nombre": "Odiaz"
    },
    "Acampos": {
        "password": "Acampos2025!",
        "role": "vendedor",
        "nombre": "Acampos"
    },
    "Evargas": {
        "password": "Evargas2025!",
        "role": "vendedor",
        "nombre": "Evargas"
    },
    "Egonzales": {
        "password": "Egonzales2025!",
        "role": "vendedor",
        "nombre": "Egonzales"
    },
    "Gmarin": {
        "password": "Gmarin2025!",
        "role": "vendedor",
        "nombre": "Gmarin"
    },
    "Dhidalgo": {
        "password": "Dhidalgo2025!",
        "role": "vendedor",
        "nombre": "Dhidalgo"
    },
    "Hgonzales": {
        "password": "Hgonzales2025!",
        "role": "vendedor",
        "nombre": "Hgonzales"
    },
    "Pprado": {
        "password": "Pprado2025!",
        "role": "vendedor",
        "nombre": "Pprado"
    },
    "Efernandez": {
        "password": "Efernandez2025!",
        "role": "vendedor",
        "nombre": "Efernandez"
    },
    "Ajimenez": {
        "password": "Ajimenez2025!",
        "role": "vendedor",
        "nombre": "Ajimenez"
    },
}

# =========================
# CONSTANTES
# =========================
RUTA_CSV = "productos_codigos.csv"
RUTA_SOLICITUDES = "solicitudes_codigos.csv"

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

COLUMNAS_SOLICITUDES = [
    "id",
    "fecha",
    "usuario",
    "nombre_vendedor",
    "tipo_solicitud",
    "descripcion_solicitada",
    "proveedor",
    "cabys_solicitado",
    "precio_solicitado",
    "codigo_relacionado",
    "estado",            # Pendiente / Completada / Rechazada
    "comentario_admin",
    "codigo_final",
    "descripcion_final"
]

# =========================
# FUNCIONES DE DATOS - PRODUCTOS
# =========================
def normalizar_df_productos(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()

    # Asegurar columnas
    for col in COLUMNAS_BASE:
        if col not in df.columns:
            df[col] = np.nan

    # Tipos numéricos
    for col in ["precio_costo", "margen_objetivo", "precio_sugerido", "precio_venta_actual"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Activo
    if "activo" in df.columns:
        df["activo"] = df["activo"].fillna("Sí")
    else:
        df["activo"] = "Sí"

    return df[COLUMNAS_BASE]


def cargar_datos():
    if os.path.exists(RUTA_CSV):
        df_raw = pd.read_csv(RUTA_CSV, dtype=str)
        return normalizar_df_productos(df_raw)
    else:
        return normalizar_df_productos(pd.DataFrame())


def guardar_datos(df):
    df.to_csv(RUTA_CSV, index=False)


def calcular_precio_sugerido(precio_costo, margen_objetivo):
    try:
        if precio_costo is None:
            return None
        costo = float(precio_costo)
        margen = float(margen_objetivo) / 100.0
        return round(costo * (1 + margen), 2)
    except Exception:
        return None


def clasificar_estado_precio(precio_sugerido, precio_venta):
    try:
        if pd.isna(precio_venta) or precio_venta == 0:
            return "Sin dato"
        if pd.isna(precio_sugerido) or precio_sugerido == 0:
            return "Sin dato"
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
# FUNCIONES DE DATOS - SOLICITUDES
# =========================
def crear_df_solicitudes_vacio():
    return pd.DataFrame(columns=COLUMNAS_SOLICITUDES)


def cargar_solicitudes():
    if os.path.exists(RUTA_SOLICITUDES):
        df = pd.read_csv(RUTA_SOLICITUDES, dtype=str)
        for col in COLUMNAS_SOLICITUDES:
            if col not in df.columns:
                df[col] = ""
        return df[COLUMNAS_SOLICITUDES]
    else:
        return crear_df_solicitudes_vacio()


def guardar_solicitudes(df_solicitudes):
    df_solicitudes.to_csv(RUTA_SOLICITUDES, index=False)


# =========================
# LOGIN
# =========================
def mostrar_login():
    # Fondo futurista con la imagen
     set_fondo_login()
    
    st.markdown(
        """
        <style>
            .stApp {
                background-image: url("login_fondo.jpg");
                background-size: 140%;
                background-position: top center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    
    st.markdown(
        """
        <style>
            .login-wrapper {
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .login-card {
                background: rgba(0, 0, 0, 0.60);
                border-radius: 20px;
                padding: 35px 30px;
                max-width: 420px;
                width: 100%;
                box-shadow: 0 10px 28px rgba(0,0,0,0.7);
                color: #ffffff;
                text-align: center;
                backdrop-filter: blur(8px);
                font-family: "Segoe UI", sans-serif;
            }

            .login-title {
                font-size: 30px;
                font-weight: 700;
                margin-bottom: 8px;
                color: #6bb6ff;
                text-shadow: 0 0 10px rgba(107,182,255,0.9);
            }

            .login-subtitle {
                font-size: 15px;
                opacity: 0.85;
                margin-bottom: 25px;
            }

            .stTextInput > div > div > input {
                background: rgba(255,255,255,0.9);
                border-radius: 10px;
                height: 45px;
                font-size: 16px;
            }

            .stButton>button {
                background: #00d4ff;
                color: #000000;
                font-weight: 700;
                border-radius: 10px;
                padding: 10px 0;
                width: 100%;
                border: none;
                font-size: 18px;
                box-shadow: 0 0 18px rgba(0,212,255,0.8);
            }

            .stButton>button:hover {
                background: #00a8cc;
                box-shadow: 0 0 25px rgba(0,212,255,1);
            }
        </style>
        <div class="login-wrapper">
            <div class="login-card">
                <div class="login-title">IA de Códigos - Multisuministros</div>
                <div class="login-subtitle">
                    Iniciá sesión para gestionar códigos, CABYS y solicitudes.
                </div>
        """,
        unsafe_allow_html=True
    )

    # -------- FORMULARIO REAL STREAMLIT ----------
    usuario = st.text_input("Usuario", key="login_usuario")
    password = st.text_input("Contraseña", type="password", key="login_password")

    col_b1, col_b2 = st.columns([1, 1.2])
    with col_b1:
        recordarme = st.checkbox("Recordarme", value=False)
    with col_b2:
        ingresar = st.button("Ingresar 🚀", use_container_width=True)

    if ingresar:
        if usuario in USERS and USERS[usuario]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.usuario = usuario
            st.session_state.rol = USERS[usuario]["role"]
            st.session_state.nombre_mostrar = USERS[usuario]["nombre"]

            if not recordarme:
                # Sesión solo mientras la pestaña esté abierta
                pass

            st.success("Inicio de sesión exitoso. Cargando panel...")
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos.")

    st.markdown("</div></div>", unsafe_allow_html=True)



# =========================
# INICIALIZAR SESIÓN
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "df_productos" not in st.session_state:
    st.session_state.df_productos = cargar_datos()

if "df_solicitudes" not in st.session_state:
    st.session_state.df_solicitudes = cargar_solicitudes()

# ====== SI NO ESTÁ LOGUEADO, SOLO MUESTRO LOGIN Y TERMINO ======
if not st.session_state.logged_in:
    mostrar_login()
    st.stop()

# Ya logueado
df = st.session_state.df_productos
df_solicitudes = st.session_state.df_solicitudes
rol_actual = st.session_state.rol
nombre_usuario = st.session_state.nombre_mostrar
usuario_login = st.session_state.usuario

# =========================
# ENCABEZADO
# =========================
st.markdown(
    """
    <div class="ms-header">
        <div class="ms-header-icon">🤖</div>
        <div>
            <div class="ms-header-title">IA de Códigos - Multisuministros de Costa Rica</div>
            <div class="ms-header-subtitle">
                Búsqueda inteligente de productos, CABYS, control de precios y flujo de solicitudes entre vendedores y administración.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Configuración")

st.sidebar.markdown(
    f"""
    <div class="sidebar-user-box">
    <b>Sesión activa</b><br>
    {nombre_usuario}<br>
    <span style="font-size:0.8rem; color:#6b7280;">Rol: {rol_actual.capitalize()}</span>
    </div>
    """,
    unsafe_allow_html=True
)

if st.sidebar.button("Cerrar sesión", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.usuario = None
    st.session_state.rol = None
    st.session_state.nombre_mostrar = None
    st.rerun()()

margen_global = st.sidebar.number_input(
    "Margen objetivo por defecto (%)",
    min_value=0.0,
    max_value=200.0,
    value=65.0,
    step=0.5
)

st.sidebar.info(
    "💡 Consejo: podés ir agregando o cargando productos desde archivos CSV.\n"
    "La app guarda todo en `productos_codigos.csv` y `solicitudes_codigos.csv`."
)

# =========================
# TABS PRINCIPALES
# =========================
tab_busqueda, tab_admin, tab_alertas, tab_solicitudes = st.tabs(
    [
        "🔍 Buscador inteligente",
        "📦 Administrar productos",
        "🚨 Alertas inteligentes",
        "📨 Solicitudes vendedores"
    ]
)

# =========================
# TAB 1: BUSCADOR INTELIGENTE
# =========================
with tab_busqueda:
    st.markdown('<div class="ms-card">', unsafe_allow_html=True)
    st.subheader("🔍 Buscador IA de códigos y productos")

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
            mask = df["descripcion"].astype(str).str.contains(consulta_lower, case=False, na=False)
            resultados_directos = df[mask]
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

            if resultados.empty:
                descripciones = df["descripcion"].astype(str).tolist()
                similares = difflib.get_close_matches(consulta, descripciones, n=20, cutoff=0.3)
                resultados = df[df["descripcion"].isin(similares)]

        st.markdown("#### Resultados encontrados")

        if resultados.empty:
            st.warning("No se encontraron productos con esa búsqueda.")
        else:
            vista = resultados.copy()
            cols_vista = [
                "codigo_interno", "descripcion", "cabys", "proveedor",
                "precio_costo", "margen_objetivo", "precio_sugerido",
                "precio_venta_actual", "estado_precio"
            ]
            cols_vista = [c for c in cols_vista if c in vista.columns]
            vista = vista[cols_vista]
            st.dataframe(vista, use_container_width=True, hide_index=True)

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
        st.info("Escribí algo en la barra de búsqueda para empezar a usar la IA de códigos. 🧠")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB 2: ADMINISTRAR PRODUCTOS
# =========================
with tab_admin:
    st.markdown('<div class="ms-card">', unsafe_allow_html=True)
    st.subheader("📦 Administración de productos")

    if rol_actual != "admin":
        st.warning("Solo el personal de administración puede gestionar productos.")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        submodo = st.radio(
            "¿Qué querés hacer?",
            ["Agregar / editar productos manualmente", "Cargar productos desde archivo CSV"],
            horizontal=True
        )

        # ---------- MODO MANUAL ----------
        if submodo == "Agregar / editar productos manualmente":
            modo = st.radio(
                "Acción",
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

                    enviado = st.form_submit_button("💾 Guardar producto")

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
                            st.success("✅ Producto agregado correctamente.")

            else:  # Editar producto
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

                        enviado = st.form_submit_button("💾 Guardar cambios")

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
                                st.success("✅ Cambios guardados correctamente.")

        # ---------- CARGA DESDE CSV ----------
        else:
            st.markdown("### 📥 Cargar todos los códigos existentes")

            st.markdown(
                "- El archivo debe ser **CSV**.\n"
                "- Como mínimo debe tener las columnas: `codigo_interno` y `descripcion`.\n"
                "- Opcionalmente puede incluir: `categoria, proveedor, cabys, unidad, precio_costo, margen_objetivo, precio_venta_actual, notas, activo`."
            )

            modo_carga = st.selectbox(
                "¿Cómo querés cargar los datos?",
                [
                    "Reemplazar TODOS los productos por el archivo subido",
                    "Agregar / actualizar productos (según código interno)"
                ]
            )

            archivo = st.file_uploader("Subí el archivo CSV", type="csv")

            if archivo is not None:
                try:
                    df_nuevo_raw = pd.read_csv(archivo, dtype=str)
                    if "codigo_interno" not in df_nuevo_raw.columns or "descripcion" not in df_nuevo_raw.columns:
                        st.error("El archivo debe contener al menos las columnas 'codigo_interno' y 'descripcion'.")
                    else:
                        df_nuevo = normalizar_df_productos(df_nuevo_raw)

                        if st.button("Aplicar carga de productos"):
                            if "Reemplazar" in modo_carga:
                                st.session_state.df_productos = df_nuevo
                            else:
                                combinado = pd.concat(
                                    [st.session_state.df_productos, df_nuevo],
                                    ignore_index=True
                                )
                                combinado = combinado.drop_duplicates(subset=["codigo_interno"], keep="last")
                                st.session_state.df_productos = combinado

                            guardar_datos(st.session_state.df_productos)
                            st.success("✅ Carga de productos realizada correctamente.")
                except Exception as e:
                    st.error(f"Ocurrió un error al leer el archivo: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TAB 3: ALERTAS INTELIGENTES
# =========================
with tab_alertas:
    st.markdown('<div class="ms-card">', unsafe_allow_html=True)
    st.subheader("🚨 Alertas inteligentes de productos")

    if df.empty:
        st.info("Todavía no hay productos registrados para analizar.")
    else:
        sin_cabys = df[(df["cabys"].isna()) | (df["cabys"].astype(str).str.strip() == "")]
        por_debajo = df[df["estado_precio"] == "Por debajo"]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Productos sin CABYS")
            if sin_cabys.empty:
                st.success("✅ Todos los productos registrados tienen CABYS.")
            else:
                st.dataframe(
                    sin_cabys[["codigo_interno", "descripcion", "proveedor", "precio_costo"]],
                    use_container_width=True,
                    hide_index=True
                )

        with col2:
            st.markdown("#### Precios por debajo del sugerido")
            if por_debajo.empty:
                st.success("✅ No hay productos con precio por debajo del sugerido.")
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

# =========================
# TAB 4: SOLICITUDES DE VENDEDORES
# =========================
with tab_solicitudes:
    st.markdown('<div class="ms-card">', unsafe_allow_html=True)
    st.subheader("📨 Solicitudes de creación / cambio de código")

    # ----- MODO VENDEDOR -----
    if rol_actual == "vendedor":
        st.markdown("### 🧑‍💼 Módulo para vendedores")

        nombre_vendedor = nombre_usuario  # viene del login

        tipo_solicitud = st.selectbox(
            "Tipo de solicitud",
            ["Nuevo producto", "Cambio de precio", "Agregar / cambiar CABYS", "Otro"]
        )

        descripcion_solicitada = st.text_area(
            "Descripción del producto que querés crear o modificar *",
            placeholder="Escribí la descripción lo más completa posible..."
        )

        col_ven1, col_ven2, col_ven3 = st.columns(3)
        with col_ven1:
            proveedor_sol = st.text_input("Proveedor (opcional)")
        with col_ven2:
            cabys_sol = st.text_input("CABYS que querés agregar (opcional)")
        with col_ven3:
            precio_sol = st.text_input("Precio sugerido (opcional)")

        codigo_relacionado = st.text_input(
            "Código interno relacionado (si ya existe alguno parecido, opcional)"
        )

        if descripcion_solicitada.strip():
            st.markdown("#### 🔎 Productos similares a tu descripción")
            des_lower = descripcion_solicitada.strip()
            descripciones = df["descripcion"].astype(str).tolist()
            similares = difflib.get_close_matches(des_lower, descripciones, n=20, cutoff=0.3)
            similares_df = df[df["descripcion"].isin(similares)]

            if similares_df.empty:
                st.info("No se encontraron productos similares en la base actual.")
            else:
                st.dataframe(
                    similares_df[
                        ["codigo_interno", "descripcion", "proveedor", "precio_venta_actual"]
                    ],
                    use_container_width=True,
                    hide_index=True
                )

        enviado_vend = st.button("📨 Enviar solicitud al administrador")

        if enviado_vend:
            if not descripcion_solicitada.strip():
                st.error("La descripción es obligatoria.")
            else:
                nuevo_id = str(uuid.uuid4())[:8]
                fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")

                nueva_solicitud = {
                    "id": nuevo_id,
                    "fecha": fecha_hoy,
                    "usuario": usuario_login,
                    "nombre_vendedor": nombre_vendedor,
                    "tipo_solicitud": tipo_solicitud,
                    "descripcion_solicitada": descripcion_solicitada.strip(),
                    "proveedor": proveedor_sol.strip(),
                    "cabys_solicitado": cabys_sol.strip(),
                    "precio_solicitado": precio_sol.strip(),
                    "codigo_relacionado": codigo_relacionado.strip(),
                    "estado": "Pendiente",
                    "comentario_admin": "",
                    "codigo_final": "",
                    "descripcion_final": ""
                }

                st.session_state.df_solicitudes = pd.concat(
                    [st.session_state.df_solicitudes, pd.DataFrame([nueva_solicitud])],
                    ignore_index=True
                )
                guardar_solicitudes(st.session_state.df_solicitudes)

                st.success("✅ Solicitud enviada correctamente. El administrador la revisará.")

        # Mostrar solicitudes del vendedor
        st.markdown("---")
        st.markdown("### 🧾 Tus solicitudes")

        mis_sol = st.session_state.df_solicitudes[
            st.session_state.df_solicitudes["usuario"] == usuario_login
        ]

        if mis_sol.empty:
            st.info("Todavía no tenés solicitudes registradas.")
        else:
            vista_sol = mis_sol[
                [
                    "fecha", "tipo_solicitud", "descripcion_solicitada",
                    "estado", "codigo_final", "descripcion_final", "comentario_admin"
                ]
            ].sort_values("fecha", ascending=False)
            st.dataframe(vista_sol, use_container_width=True, hide_index=True)

    # ----- MODO ADMIN -----
    else:
        st.markdown("### 🧑‍💻 Módulo de administración")

        pendientes = st.session_state.df_solicitudes[
            st.session_state.df_solicitudes["estado"] == "Pendiente"
        ]

        st.markdown("#### 📌 Solicitudes pendientes")

        if pendientes.empty:
            st.info("No hay solicitudes pendientes por el momento.")
        else:
            opciones_ids = [
                f"{row['id']} - {row['nombre_vendedor']} - {row['tipo_solicitud']}"
                for _, row in pendientes.iterrows()
            ]
            opcion_sel = st.selectbox(
                "Seleccioná una solicitud para revisarla",
                options=opciones_ids
            )

            sel_id = opcion_sel.split(" - ")[0]
            sol = pendientes[pendientes["id"] == sel_id].iloc[0]
            idx_global = st.session_state.df_solicitudes[
                st.session_state.df_solicitudes["id"] == sel_id
            ].index[0]

            st.markdown("##### Detalle de la solicitud")
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.write("**ID:**", sol["id"])
                st.write("**Fecha:**", sol["fecha"])
                st.write("**Usuario vendedor:**", sol["usuario"])
                st.write("**Nombre vendedor:**", sol["nombre_vendedor"])
                st.write("**Tipo solicitud:**", sol["tipo_solicitud"])
            with col_s2:
                st.write("**Descripción solicitada:**", sol["descripcion_solicitada"])
                st.write("**Proveedor:**", sol["proveedor"])
                st.write("**CABYS solicitado:**", sol["cabys_solicitado"])
                st.write("**Precio sugerido:**", sol["precio_solicitado"])
                st.write("**Código relacionado:**", sol["codigo_relacionado"])

            if sol["descripcion_solicitada"].strip():
                st.markdown("#### 🔎 Productos similares en la base actual")
                des_lower = sol["descripcion_solicitada"].strip()
                descripciones = df["descripcion"].astype(str).tolist()
                similares = difflib.get_close_matches(des_lower, descripciones, n=20, cutoff=0.3)
                similares_df = df[df["descripcion"].isin(similares)]

                if similares_df.empty:
                    st.info("No se encontraron productos similares en la base actual.")
                else:
                    st.dataframe(
                        similares_df[
                            ["codigo_interno", "descripcion", "proveedor", "precio_venta_actual"]
                        ],
                        use_container_width=True,
                        hide_index=True
                    )

            st.markdown("---")
            st.markdown("#### 🛠 Actualizar estado de la solicitud")

            with st.form("form_admin_sol"):
                estado_nuevo = st.selectbox(
                    "Estado",
                    ["Pendiente", "Completada", "Rechazada"],
                    index=1
                )
                codigo_final = st.text_input(
                    "Código final (el que quedó en el sistema)",
                    value=sol["codigo_final"]
                )
                descripcion_final = st.text_input(
                    "Descripción final",
                    value=sol["descripcion_final"]
                )
                comentario_admin = st.text_area(
                    "Comentario para el vendedor",
                    value=sol["comentario_admin"],
                    height=80
                )

                guardar_cambios = st.form_submit_button("💾 Guardar cambios")

                if guardar_cambios:
                    st.session_state.df_solicitudes.at[idx_global, "estado"] = estado_nuevo
                    st.session_state.df_solicitudes.at[idx_global, "codigo_final"] = codigo_final.strip()
                    st.session_state.df_solicitudes.at[idx_global, "descripcion_final"] = descripcion_final.strip()
                    st.session_state.df_solicitudes.at[idx_global, "comentario_admin"] = comentario_admin.strip()

                    guardar_solicitudes(st.session_state.df_solicitudes)
                    st.success("✅ Solicitud actualizada correctamente.")

        st.markdown("---")
        st.markdown("#### 🧾 Historial de solicitudes")
        if st.session_state.df_solicitudes.empty:
            st.info("Todavía no hay solicitudes registradas.")
        else:
            vista_hist = st.session_state.df_solicitudes[
                ["fecha", "usuario", "nombre_vendedor", "tipo_solicitud", "estado", "codigo_final", "descripcion_final"]
            ].sort_values("fecha", ascending=False)
            st.dataframe(vista_hist, use_container_width=True, hide_index=True)

    st.markdown('</div>', unsafe_allow_html=True)
