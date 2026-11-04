"""
trigonometria - site feito só com Python (Streamlit)
Rodar:  streamlit run app.py
"""
import math
import streamlit as st

st.set_page_config(page_title="trigonometria", page_icon="📐")

# ============================================================
# PARTE 1 - LÓGICA (funções de cálculo, sem nada de interface)
# ============================================================

NOTAVEIS = {
    0:  ("0", "1", "0"),
    30: ("1/2", "√3/2", "√3/3"),
    45: ("√2/2", "√2/2", "1"),
    60: ("√3/2", "1/2", "√3"),
    90: ("1", "0", "não existe"),
}


def quadrante(graus):
    a = graus % 360
    if a % 90 == 0:
        return "sobre um eixo"
    return f"{int(a // 90) + 1}º quadrante"


def angulo_de_referencia(graus):
    a = graus % 360
    if a <= 90:
        return a
    if a <= 180:
        return 180 - a
    if a <= 270:
        return a - 180
    return 360 - a


def razoes(graus):
    r = math.radians(graus)
    tan = None if abs(math.cos(r)) < 1e-12 else math.tan(r)
    return math.sin(r), math.cos(r), tan


def triangulo(dados, v1, v2=None):
    """Devolve (hipotenusa, oposto, adjacente, angulo_em_graus)."""
    if dados == "Hipotenusa e ângulo":
        h, t = v1, v2
        return h, h * math.sin(math.radians(t)), h * math.cos(math.radians(t)), t
    if dados == "Cateto oposto e ângulo":
        o, t = v1, v2
        return o / math.sin(math.radians(t)), o, o / math.tan(math.radians(t)), t
    if dados == "Cateto adjacente e ângulo":
        a, t = v1, v2
        return a / math.cos(math.radians(t)), a * math.tan(math.radians(t)), a, t
    if dados == "Hipotenusa e cateto oposto":
        h, o = v1, v2
        return h, o, math.sqrt(h**2 - o**2), math.degrees(math.asin(o / h))
    if dados == "Hipotenusa e cateto adjacente":
        h, a = v1, v2
        return h, math.sqrt(h**2 - a**2), a, math.degrees(math.acos(a / h))
    o, a = v1, v2  # os dois catetos
    return math.hypot(o, a), o, a, math.degrees(math.atan(o / a))


def lei_dos_senos(a, A, B):
    b = a * math.sin(math.radians(B)) / math.sin(math.radians(A))
    R = a / (2 * math.sin(math.radians(A)))
    return b, R


def lado_por_cossenos(b, c, A):
    return math.sqrt(b**2 + c**2 - 2 * b * c * math.cos(math.radians(A)))


def angulo_por_cossenos(a, b, c):
    cos_a = (b**2 + c**2 - a**2) / (2 * b * c)
    if not -1 <= cos_a <= 1:
        return None
    return math.degrees(math.acos(cos_a))


def equacao(funcao, k):
    """Soluções de f(x) = k em [0, 360)."""
    if funcao in ("sen", "cos") and abs(k) > 1:
        return []
    if funcao == "sen":
        x = math.degrees(math.asin(k))
        sols = [x, 180 - x]
    elif funcao == "cos":
        x = math.degrees(math.acos(k))
        sols = [x, 360 - x]
    else:
        x = math.degrees(math.atan(k))
        sols = [x, x + 180]
    return sorted({round(s % 360, 6) for s in sols})


# ============================================================
# PARTE 2 - INTERFACE (o que aparece na página)
# ============================================================

st.title("📐 trigonometria")
st.caption("Resolvedor de questões de trigonometria feito em Python.")

abas = st.tabs([
    "Ângulo", "Triângulo retângulo", "Lei dos senos",
    "Lei dos cossenos", "Equações", "Conversão",
])

# ---------- Aba 1: razões de um ângulo ----------
with abas[0]:
    graus = st.number_input("Ângulo (graus)", value=30.0, key="ang")
    if st.button("Calcular", key="b1"):
        s, c, t = razoes(graus)
        st.write(f"**{graus}°** está no **{quadrante(graus)}**")
        col1, col2, col3 = st.columns(3)
        col1.metric("sen", f"{s:.4f}")
        col2.metric("cos", f"{c:.4f}")
        col3.metric("tg", "não existe" if t is None else f"{t:.4f}")
        ref = angulo_de_referencia(graus)
        if round(ref) in NOTAVEIS and abs(ref - round(ref)) < 1e-9:
            es, ec, et = NOTAVEIS[round(ref)]
            st.info(
                f"Ângulo de referência: {round(ref)}°. Valores exatos (em módulo): "
                f"sen = {es}, cos = {ec}, tg = {et}. Atenção ao sinal do quadrante."
            )

# ---------- Aba 2: triângulo retângulo ----------
with abas[1]:
    opcoes = [
        "Hipotenusa e ângulo", "Cateto oposto e ângulo", "Cateto adjacente e ângulo",
        "Hipotenusa e cateto oposto", "Hipotenusa e cateto adjacente", "Os dois catetos",
    ]
    dados = st.selectbox("O que você sabe?", opcoes)
    nomes = {
        "Hipotenusa e ângulo": ("Hipotenusa", "Ângulo θ (graus)"),
        "Cateto oposto e ângulo": ("Cateto oposto", "Ângulo θ (graus)"),
        "Cateto adjacente e ângulo": ("Cateto adjacente", "Ângulo θ (graus)"),
        "Hipotenusa e cateto oposto": ("Hipotenusa", "Cateto oposto"),
        "Hipotenusa e cateto adjacente": ("Hipotenusa", "Cateto adjacente"),
        "Os dois catetos": ("Cateto oposto", "Cateto adjacente"),
    }[dados]
    v1 = st.number_input(nomes[0], min_value=0.01, value=10.0, key="t1")
    v2 = st.number_input(nomes[1], min_value=0.01, value=30.0, key="t2")
    if st.button("Resolver", key="b2"):
        try:
            h, o, a, t = triangulo(dados, v1, v2)
            st.success(
                f"Hipotenusa = {h:.4f} | Oposto = {o:.4f} | "
                f"Adjacente = {a:.4f} | θ = {t:.4f}° | outro ângulo = {90 - t:.4f}°"
            )
        except (ValueError, ZeroDivisionError):
            st.error("Esses valores não formam um triângulo retângulo.")

# ---------- Aba 3: lei dos senos ----------
with abas[2]:
    st.latex(r"\frac{a}{\sin A} = \frac{b}{\sin B} = 2R")
    a = st.number_input("Lado a", min_value=0.01, value=10.0, key="s1")
    A = st.number_input("Ângulo A (oposto a a)", min_value=0.1, max_value=179.9, value=30.0, key="s2")
    B = st.number_input("Ângulo B", min_value=0.1, max_value=179.9, value=45.0, key="s3")
    if st.button("Calcular", key="b3"):
        b, R = lei_dos_senos(a, A, B)
        st.success(f"b = {b:.4f}  |  raio da circunferência circunscrita R = {R:.4f}")

# ---------- Aba 4: lei dos cossenos ----------
with abas[3]:
    st.latex(r"a^2 = b^2 + c^2 - 2bc\cos A")
    modo = st.radio("Quero achar", ["O lado a", "O ângulo A"], horizontal=True)
    if modo == "O lado a":
        b = st.number_input("Lado b", min_value=0.01, value=7.0, key="c1")
        c = st.number_input("Lado c", min_value=0.01, value=5.0, key="c2")
        A = st.number_input("Ângulo A (graus)", min_value=0.1, max_value=179.9, value=60.0, key="c3")
        if st.button("Calcular", key="b4"):
            st.success(f"a = {lado_por_cossenos(b, c, A):.4f}")
    else:
        a = st.number_input("Lado a", min_value=0.01, value=7.0, key="c4")
        b = st.number_input("Lado b", min_value=0.01, value=5.0, key="c5")
        c = st.number_input("Lado c", min_value=0.01, value=8.0, key="c6")
        if st.button("Calcular", key="b5"):
            res = angulo_por_cossenos(a, b, c)
            if res is None:
                st.error("Esses lados não formam um triângulo.")
            else:
                st.success(f"A = {res:.4f}°")

# ---------- Aba 5: equações ----------
with abas[4]:
    f = st.selectbox("Função", ["sen", "cos", "tg"])
    k = st.number_input("Valor de k (f(x) = k)", value=0.5, key="e1")
    if st.button("Resolver", key="b6"):
        sols = equacao(f, k)
        if not sols:
            st.error("Sem solução: seno e cosseno só assumem valores entre −1 e 1.")
        else:
            st.success("Soluções em [0°, 360°): " + "  e  ".join(f"{s:g}°" for s in sols))
            st.caption("Some 360°·n (ou 180°·n para a tangente) para a solução geral.")

# ---------- Aba 6: conversão ----------
with abas[5]:
    sentido = st.radio("Converter", ["Graus → radianos", "Radianos → graus"], horizontal=True)
    valor = st.number_input("Valor", value=180.0, key="v1")
    if st.button("Converter", key="b7"):
        if sentido == "Graus → radianos":
            st.success(f"{valor}° = {math.radians(valor):.6f} rad = {valor / 180:.4f}π rad")
        else:
            st.success(f"{valor} rad = {math.degrees(valor):.4f}°")
