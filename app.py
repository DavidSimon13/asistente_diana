
import streamlit as st
from datetime import datetime

APP_NAME = "Asistente Diana"

TERADATA = {
    "ip": "150.100.43.100",
    "instancia": "KLARMXPU/KLARMXPV",
    "profile": "PLAOMXP_LUSER",
    "role": "RLARMXP_ENDUSR_MI05779"
}

VPN_GUIDE_LINK = "https://docs.google.com/presentation/d/1gOInm65Oesu6MtUaAefto_uc2FJsB4H8GF6vZxt_xi4/edit?slide=id.g3356b0b5634_127_70#slide=id.g3356b0b5634_127_70"

CITRIX_PHONE = "55 5522 61190"

VPN_SUPPORT = {
    "correo": "vpn.soporte.mx@bbva.com",
    "telefono": "55 5226 1190",
    "conmutador": "55 5621 3434 ext. 61190 opción 1"
}

MODULES = {
    "teradata": {
        "name": "Alta Usuario Teradata",
        "keywords": ["teradata", "alta usuario", "role", "vobo", "reasignacion", "reasignación"],
        "steps": [
            "Validar que exista una licencia para reasignación.",
            "Confirmar Vo.Bo. del usuario que cede la licencia.",
            "Confirmar Vo.Bo. del N4 del usuario receptor.",
            "Generar correo Vo.Bo.",
            "Crear role / solicitud correspondiente.",
            "Levantar alta en Helix.",
            "Agregar comentario del jefe.",
            "Validar acceso por Citrix."
        ],
        "validations": [
            "No hay altas nuevas por adelgazamiento de plataforma.",
            "La licencia se obtiene por reasignación.",
            "Se requiere Vo.Bo. del usuario que cede y del N4.",
            f"Profile estándar: {TERADATA['profile']}.",
            f"Role estándar: {TERADATA['role']}."
        ]
    },
    "citrix": {
        "name": "Citrix / Bloqueo de usuario",
        "keywords": ["citrix", "bloqueo", "usuario bloqueado", "no puedo entrar"],
        "steps": [
            "Identificar si el bloqueo es de usuario o de Citrix.",
            f"Reportar al número: {CITRIX_PHONE}.",
            "Esperar indicaciones del soporte.",
            "Volver a validar acceso."
        ],
        "validations": [
            "Este número aplica solo para Citrix o bloqueo de usuario.",
            "No usar este flujo para errores VPN."
        ]
    },
    "vpn": {
        "name": "VPN / Acceso remoto",
        "keywords": ["vpn", "certificate", "certificado", "cisco", "enrolamiento"],
        "steps": [
            "Si ya cuentas con permiso VPN y aparece error, cierra VPN y reinicia el equipo.",
            "Abre Cisco nuevamente e intenta iniciar sesión.",
            "Si el error continúa, contacta soporte VPN.",
            "Si no cuentas con permiso VPN, levanta Jira con la guía oficial.",
            "Diana debe acompañarte paso a paso con el manual."
        ],
        "validations": [
            "VPN no se mezcla con Citrix.",
            "Para error VPN usar soporte VPN.",
            "Para alta nueva usar el manual y levantar Jira."
        ]
    },
    "iam": {
        "name": "IAM Plataformas",
        "keywords": ["iam", "plantilla", "clonar", "unix", "linux", "windows", "apx", "base de datos", "criptografia", "criptografía"],
        "steps": [
            "Ubicar la plantilla correcta.",
            "No editar la plantilla original.",
            "Clonar la plantilla.",
            "Borrar texto hasta 'Plantilla' en el resumen.",
            "Editar descripción con los datos solicitados.",
            "Adjuntar evidencias o Vo.Bo. si aplica.",
            "Dar seguimiento en comentarios."
        ],
        "validations": [
            "Si el servicio no aparece en catálogo, no lo gestiona IAM Plataformas.",
            "No editar plantilla original.",
            "Siempre clonar."
        ]
    },
    "formato_roles": {
        "name": "Formato Privilegios a Roles",
        "keywords": ["formato", "dml", "privilegios", "roles", "asignar privilegios"],
        "steps": [
            "Seleccionar manejador: DB2 / Oracle / Teradata / Sybase / Informix / SQL.",
            "En Solicitante, colocar la M del usuario.",
            "En Rol, colocar el role y la M.",
            "En datos de usuario M o XM, colocar equipo, usuario de red y correo.",
            "Validar que no queden espacios obligatorios en blanco."
        ],
        "validations": [
            "Usuario debe tener formato M o XM.",
            "Rol debe incluir la M del usuario.",
            "Correo debe ser corporativo.",
            "No dejar campos obligatorios vacíos."
        ]
    },
    "impedimentos": {
        "name": "Dependencias / Impedimentos",
        "keywords": ["impedimento", "dependencia", "bloqueo", "blocked", "no puedo avanzar"],
        "steps": [
            "Clasificar si es dependencia o impedimento.",
            "Crear impedimento si existe bloqueo real.",
            "Definir problem solvers.",
            "Agregar etiqueta correcta.",
            "Dar seguimiento.",
            "Escalar si aplica.",
            "Cerrar como RESOLVED o DISCARDED."
        ],
        "validations": [
            "Riesgos o warnings no son impedimentos.",
            "Solicitudes dentro del SLA no son impedimentos."
        ]
    },
    "analysis": {
        "name": "Analysis 2.0 / Decision Framework",
        "keywords": ["analysis", "análisis", "decision framework", "riesgos it", "enterprise"],
        "steps": [
            "Crear Enterprise.",
            "Crear tarea de análisis.",
            "Completar Riesgos IT.",
            "Completar Decision Framework.",
            "Llenar documento de análisis.",
            "Cambiar estado a Analysis To Do.",
            "Agregar comentario requerido."
        ],
        "validations": [
            "Riesgos IT es obligatorio antes del Decision Framework.",
            "Analysis To Do formaliza la iniciativa."
        ]
    }
}

def detect_module(text: str):
    text = text.lower()
    best = None
    best_score = 0
    for key, module in MODULES.items():
        score = 0
        for kw in module["keywords"]:
            if kw.lower() in text:
                score += 3
            for token in text.split():
                if token and token in kw.lower():
                    score += 1
        if score > best_score:
            best_score = score
            best = key
    return best

def correo_vobo():
    return f"""Hola [NOMBRE DEL JEFE] buen día, espero que se encuentren muy bien.

El motivo de este correo es solicitar tu amable Vo.Bo. para levantar las solicitudes de creación de rol en JIRA y posteriormente el alta de usuario en Helix.

Estos movimientos son por reasignación:
[Usuario a quien se hará la reasignación]

Saludos.

---

NOTA: Envíale este mensaje al usuario para que nos ayude con el Vo.Bo.

Te comparto el siguiente mensaje para que se lo envíes a tu jefe directo y pueda otorgar el Vo.Bo. correspondiente para tu alta de Teradata:

“Yo como jefe del usuario XXXXX otorgo el Vo.Bo. para alta del usuario MX indicando los siguientes datos:
-ID
-Nombre
-Puesto
-Área
-IP
-Instancia
-Profile a asignar
-Role”

Yo te proporciono los siguientes datos:
-IP: {TERADATA['ip']}
-Instancia: {TERADATA['instancia']}
-Profile a asignar: {TERADATA['profile']}
-Role: {TERADATA['role']}
"""

def comentario_helix():
    return f"""Yo como jefe del usuario XXXXX otorgo el Vo.Bo. para alta del usuario MX indicando los siguientes datos:

-ID:
-Nombre:
-Puesto:
-Área:
-IP: {TERADATA['ip']}
-Instancia: {TERADATA['instancia']}
-Profile a asignar: {TERADATA['profile']}
-Role: {TERADATA['role']}
"""

def formato_roles():
    return """BASE DE DATOS / MANEJADOR:
TERADATA

SOLICITANTE:
Usuario: M123456
Rol: RLARMXP_ENDUSR_M123456

DATOS SOLO PARA USUARIO M O XM:
Nombre del equipo: Data Engineering
Usuario de red: M123456
Mail: usuario@bbva.com
"""

def respuesta(text):
    key = detect_module(text)
    lower = text.lower()

    if "correo" in lower and "vobo" in lower:
        return "Generador: Correo Vo.Bo. Teradata", correo_vobo()
    if "comentario" in lower and "helix" in lower:
        return "Generador: Comentario Helix", comentario_helix()
    if "formato" in lower and ("dml" in lower or "privilegio" in lower or "role" in lower):
        return "Generador: Formato de privilegios", formato_roles()

    if not key:
        return "No detecté un módulo específico", "Puedo ayudarte con Teradata, Citrix, VPN, IAM, Jira/Helix, impedimentos, Analysis 2.0 y formato de privilegios."

    mod = MODULES[key]
    output = []

    if key == "teradata":
        output.append("⚠️ En Teradata ya no hay altas nuevas por adelgazamiento de la plataforma. La licencia se obtiene por reasignación con Vo.Bo. del usuario que cede y del N4 del usuario receptor.")

    if key == "citrix":
        output.append(f"📞 Para Citrix o bloqueo de usuario, reporta al número: {CITRIX_PHONE}")

    if key == "vpn":
        output.append("🔐 Si ya tenías permiso VPN y aparece error, primero sigue la guía de la imagen: cerrar VPN, reiniciar equipo y abrir Cisco nuevamente.")
        output.append(f"📧 Soporte VPN: {VPN_SUPPORT['correo']}")
        output.append(f"☎️ Teléfono: {VPN_SUPPORT['telefono']}")
        output.append(f"☎️ Conmutador: {VPN_SUPPORT['conmutador']}")
        output.append("🏢 Si no se soluciona: Parque BBVA piso 8 / Torre BBVA piso 14.")
        output.append(f"📘 Guía alta VPN: {VPN_GUIDE_LINK}")

    output.append("### Paso a paso")
    output += [f"{i}. {step}" for i, step in enumerate(mod["steps"], 1)]

    output.append("### Validaciones")
    output += [f"- {v}" for v in mod["validations"]]

    return mod["name"], "\n".join(output)

st.set_page_config(page_title="Asistente Diana Demo", layout="wide", page_icon="🤖")

st.markdown("""
<style>
.stApp {background: linear-gradient(135deg,#061428,#001f3f,#020812); color: white;}
section[data-testid="stSidebar"] {background: #061428;}
h1, h2, h3 {color: #ffffff;}
.card {background: rgba(9,35,67,.82); border: 1px solid #1a78c2; border-radius: 18px; padding: 18px; box-shadow: 0 0 18px rgba(0,160,255,.18);}
.big {font-size: 44px; font-weight: 800;}
.blue {color: #2bb8ff;}
.small {color:#c8d8e8;}
button[kind="primary"] {background:#0072ce;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🤖 Asistente Diana")
    st.caption("Copiloto de procesos BBVA")
    st.markdown("---")
    st.markdown("### ⚙️ Configuración")
    theme = st.selectbox("Tema", ["Clásico BBVA", "Oscuro profesional", "Turquesa fresco", "Púrpura creativo"])
    detail = st.toggle("Respuestas detalladas", True)
    images = st.toggle("Mostrar modo guía visual", True)
    st.markdown("---")
    st.markdown("### Módulos")
    for module in MODULES.values():
        st.write("• " + module["name"])

col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="big">¡Hola! 👋 Soy <span class="blue">Diana</span></div>', unsafe_allow_html=True)
    st.write("Tu asistente inteligente de BBVA para procesos internos, guías, formatos y soporte.")
    st.markdown('<div class="card">Estoy aquí para ayudarte con procesos, dudas y cualquier consulta que necesites.<br><b>¿En qué puedo ayudarte hoy?</b></div>', unsafe_allow_html=True)

    query = st.text_input("Escribe tu pregunta", placeholder="Ejemplo: Necesito dar de alta un usuario en Teradata")

    quick = st.columns(4)
    examples = [
        "Necesito dar de alta un usuario en Teradata",
        "Hazme el correo VoBo",
        "Tengo error VPN",
        "Necesito formato DML"
    ]
    for i, ex in enumerate(examples):
        if quick[i].button(ex):
            query = ex

    if query:
        title, body = respuesta(query)
        st.markdown(f"## {title}")
        st.markdown(f'<div class="card">{body}</div>', unsafe_allow_html=True)
        if images:
            if "vpn" in query.lower():
                st.info("Modo guía visual: aquí Diana mostraría la imagen del error VPN y señalaría los pasos.")
            else:
                st.info("Modo guía visual: Diana mostraría capturas del manual con señalaciones específicas.")
        if st.button("Da click si deseas que te guíe", type="primary"):
            st.success("Modo guía activado. Diana te acompañará paso a paso con validaciones antes de avanzar.")

with col2:
    st.markdown("### Demo en acción")
    st.markdown("""
<div class="card">
<b>Tú:</b> Necesito dar de alta un usuario en Teradata<br><br>
<b>Diana:</b> Claro, te guío paso a paso. Primero recuerda que no hay altas nuevas; la licencia se obtiene por reasignación con Vo.Bo. del usuario que cede y del N4.
<br><br>
✅ Validar licencia<br>
✅ Solicitar Vo.Bo.<br>
✅ Crear role<br>
✅ Registrar en Helix<br>
✅ Validar acceso
</div>
""", unsafe_allow_html=True)

    st.markdown("### Generadores rápidos")
    if st.button("📧 Correo Vo.Bo."):
        st.code(correo_vobo())
    if st.button("💬 Comentario Helix"):
        st.code(comentario_helix())
    if st.button("📄 Formato DML"):
        st.code(formato_roles())

st.markdown("---")
st.caption("Asistente Diana · Demo MVP · Conocimiento interno + externo · Guía paso a paso · Generadores · Soporte visual")
