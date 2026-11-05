import streamlit as st
import unicodedata
from html import escape

st.set_page_config(page_title="mise. — cozinhe com o que tem", page_icon="🥬", layout="wide")

# ---------- Visual identity ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #F7F6F1; color: #26352D; }
.block-container { max-width: 1050px; padding-top: 2.2rem; padding-bottom: 4rem; }
.brand { font-family: 'Playfair Display', serif; font-size: 2.25rem; letter-spacing: -1.5px; color: #26352D; font-weight: 600; }
.kicker { color: #758276; font-size: .72rem; letter-spacing: 2.3px; font-weight: 700; }
.hero { background: #E9EDE5; border-radius: 22px; padding: 2.2rem 2.4rem; margin: 1.1rem 0 1.6rem; }
.hero h1 { font-family: 'Playfair Display', serif; font-size: clamp(2rem, 4vw, 3.2rem); line-height: 1.1; color: #26352D; margin: .3rem 0 .7rem; }
.hero p { color: #657368; font-size: 1.02rem; max-width: 560px; }
.section-title { font-family: 'Playfair Display', serif; font-size: 1.55rem; color: #26352D; margin: .6rem 0 .2rem; }
.hint { color: #778278; font-size: .88rem; }
div[data-testid="stTextInput"] input { border-radius: 12px; background: #fff; border-color: #DCE1D8; }
div[data-testid="stButton"] button { border-radius: 12px; border: 1px solid #D6DDD2; min-height: 2.6rem; }
div[data-testid="stButton"] button[kind="primary"] { background: #344B3C; border-color: #344B3C; color: white; }
.recipe-card { background: #fff; border: 1px solid #E6E8E1; border-radius: 18px; padding: 1.15rem 1.25rem; min-height: 190px; }
.recipe-name { font-family: 'Playfair Display', serif; font-size: 1.35rem; color: #26352D; }
.recipe-meta { color: #7C877C; font-size: .8rem; margin: .35rem 0 .8rem; }
.pill { display: inline-block; background: #EDF1E9; color: #53664F; padding: .28rem .65rem; border-radius: 99px; font-size: .76rem; margin: .12rem .18rem .12rem 0; }
hr { border-color: #E3E6DE; }
.stAlert { border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

RECIPES = [
    {
        "name": "Omelete de tomate e queijo", "time": 12, "category": "Rápida",
        "ingredients": ["ovo", "tomate", "queijo", "azeite"],
        "optional": ["cebola", "orégano", "pimenta"],
        "description": "Leve, prática e ótima para aproveitar ingredientes frescos.",
        "steps": [
            "Quebre os ovos em uma tigela, tempere com sal e pimenta e bata com um garfo.",
            "Pique o tomate e o queijo em pedaços pequenos.",
            "Aqueça um fio de azeite em uma frigideira antiaderente e refogue o tomate por 1 minuto.",
            "Despeje os ovos. Quando começarem a firmar, espalhe o queijo por cima.",
            "Dobre a omelete ao meio e cozinhe até chegar ao ponto desejado. Sirva em seguida."
        ]
    },
    {
        "name": "Arroz de frigideira com legumes", "time": 20, "category": "Aproveitamento",
        "ingredients": ["arroz", "cenoura", "ovo", "cebola"],
        "optional": ["ervilha", "milho", "shoyu", "cebolinha"],
        "description": "Uma refeição completa para transformar arroz já cozido.",
        "steps": [
            "Se ainda não estiver cozido, prepare o arroz normalmente antes de começar.",
            "Rale a cenoura e pique a cebola.",
            "Aqueça um fio de óleo ou azeite e refogue a cebola e a cenoura por 3 a 4 minutos.",
            "Abra um espaço na frigideira, coloque o ovo e mexa até cozinhar.",
            "Junte o arroz cozido e misture bem. Se tiver, finalize com shoyu ou cebolinha.",
            "Aqueça por mais 2 minutos e ajuste o tempero."
        ]
    },
    {
        "name": "Macarrão cremoso de uma panela", "time": 25, "category": "Conforto",
        "ingredients": ["macarrão", "leite", "queijo", "alho"],
        "optional": ["tomate", "creme de leite", "espinafre", "orégano"],
        "description": "Cremoso e simples, com pouca louça para lavar.",
        "steps": [
            "Pique ou amasse o alho e rale o queijo.",
            "Coloque o macarrão em uma panela e cubra com água e um pouco de leite.",
            "Cozinhe em fogo médio, mexendo frequentemente e adicionando líquido se necessário.",
            "Quando a massa estiver quase al dente, acrescente o alho e o queijo.",
            "Mexa até o queijo derreter e o molho ficar cremoso. Ajuste sal e pimenta.",
            "Desligue o fogo e deixe descansar por 1 minuto antes de servir."
        ]
    },
    {
        "name": "Panqueca simples", "time": 25, "category": "Clássico",
        "ingredients": ["ovo", "leite", "farinha"],
        "optional": ["queijo", "tomate", "banana", "canela"],
        "description": "Uma massa versátil que aceita recheios doces ou salgados.",
        "steps": [
            "Misture o ovo, o leite e a farinha até obter uma massa lisa.",
            "Aqueça uma frigideira antiaderente levemente untada.",
            "Despeje uma pequena porção de massa e gire a frigideira para espalhar.",
            "Quando as bordas soltarem, vire e doure o outro lado.",
            "Repita com o restante da massa e sirva com o recheio que tiver disponível."
        ]
    },
    {
        "name": "Salada morna de grão-de-bico", "time": 15, "category": "Leve",
        "ingredients": ["grão-de-bico", "tomate", "cebola", "azeite"],
        "optional": ["limão", "pepino", "salsinha", "queijo"],
        "description": "Uma opção leve, saborosa e rica em fibras.",
        "steps": [
            "Escorra e enxágue o grão-de-bico cozido ou em conserva.",
            "Pique o tomate e a cebola em cubinhos.",
            "Aqueça o grão-de-bico em uma frigideira com um fio de azeite por 3 minutos.",
            "Misture com o tomate e a cebola.",
            "Tempere com sal, pimenta, azeite e limão, se tiver. Finalize com ervas."
        ]
    },
    {
        "name": "Legumes salteados com ovo", "time": 18, "category": "Rápida",
        "ingredients": ["cenoura", "ovo", "cebola", "azeite"],
        "optional": ["abobrinha", "brócolis", "pimentão", "shoyu"],
        "description": "Use os legumes disponíveis e finalize com ovo para uma refeição prática.",
        "steps": [
            "Corte os legumes em tiras ou cubos pequenos para cozinharem por igual.",
            "Aqueça azeite em uma frigideira e refogue a cebola.",
            "Adicione os legumes mais firmes primeiro e salteie por 5 a 7 minutos.",
            "Abra um espaço no centro, acrescente o ovo e mexa até cozinhar.",
            "Misture tudo, tempere e sirva. Se tiver, finalize com shoyu."
        ]
    },
]

# Variações comuns e sinônimos são convertidos para um nome padrão.
ALIASES = {
    "ovos": "ovo", "ovo caipira": "ovo", "ovos caipiras": "ovo",
    "tomates": "tomate", "tomate italiano": "tomate", "tomate cereja": "tomate",
    "queijos": "queijo", "mussarela": "queijo", "muçarela": "queijo", " queijo prato": "queijo",
    "cenouras": "cenoura", "cebolas": "cebola", "cebola roxa": "cebola",
    "dente de alho": "alho", "dentes de alho": "alho", "alho picado": "alho",
    "massa": "macarrão", "espaguete": "macarrão", "penne": "macarrão", "talharim": "macarrão",
    "arroz cozido": "arroz", "arroz pronto": "arroz",
    "grao de bico": "grão-de-bico", "grao-de-bico": "grão-de-bico",
    "farinha de trigo": "farinha", "leite integral": "leite", "leite desnatado": "leite",
    "abobrinhas": "abobrinha", "brocolis": "brócolis", "ervilhas": "ervilha",
    "milhos": "milho", "pimentões": "pimentão", "pimentoes": "pimentão",
    "azeite de oliva": "azeite", "óleo": "azeite", "oleo": "azeite",
}

def _fold(value):
    """Remove acentos e padroniza espaços para comparar variações."""
    value = unicodedata.normalize("NFKD", value.strip().lower())
    return "".join(ch for ch in value if not unicodedata.combining(ch))

# Chaves de alias também são comparadas sem acentos.
ALIASES_FOLDED = {_fold(k): v for k, v in ALIASES.items()}

def normalize(value):
    value = re.sub(r"\s+", " ", value.strip().lower())
    folded = _fold(value)
    if folded in ALIASES_FOLDED:
        return ALIASES_FOLDED[folded]
    # Singularização simples para plurais frequentes em português.
    if folded.endswith("s") and len(folded) > 3:
        singular = folded[:-1]
        if singular in ALIASES_FOLDED:
            return ALIASES_FOLDED[singular]
    return value

def add_ingredients(raw_value):
    # Aceita também listas separadas por vírgula ou ponto e vírgula.
    items = [normalize(part) for part in re.split(r"[,;]", raw_value) if part.strip()]
    for item in items:
        if item and item not in st.session_state.ingredients:
            st.session_state.ingredients.append(item)

if "ingredients" not in st.session_state:
    st.session_state.ingredients = []
if "selected_recipe" not in st.session_state:
    st.session_state.selected_recipe = None

# Header
left, right = st.columns([3, 1])
with left:
    st.markdown('<div class="brand">mise.</div><div class="kicker">COZINHE COM O QUE VOCÊ JÁ TEM</div>', unsafe_allow_html=True)
with right:
    st.markdown("<div style='text-align:right;color:#879184;padding-top:15px;font-size:.85rem'>menos desperdício<br>mais possibilidades</div>", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="kicker">SUA COZINHA, NOVAS IDEIAS</div>
  <h1>O que vamos cozinhar hoje?</h1>
  <p>Conte o que tem na geladeira, escolha quanto tempo você tem e descubra uma boa ideia para a próxima refeição.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-title">1. O que você tem em casa?</div>', unsafe_allow_html=True)
st.markdown('<div class="hint">Adicione os ingredientes um por vez. Você também pode experimentar os exemplos abaixo.</div>', unsafe_allow_html=True)

with st.form("ingredient_form", clear_on_submit=True):
    a, b = st.columns([4, 1])
    with a:
        new_ingredient = st.text_input("Ingrediente", placeholder="Ex.: ovos, tomate, arroz...", label_visibility="collapsed")
    with b:
        add = st.form_submit_button("＋ Adicionar", use_container_width=True)
    if add and new_ingredient.strip():
        add_ingredients(new_ingredient)
        st.rerun()

if st.session_state.ingredients:
    chips = st.columns([5, 1])
    with chips[0]:
        st.markdown("".join([f'<span class="pill">{x}</span>' for x in st.session_state.ingredients]), unsafe_allow_html=True)
    with chips[1]:
        if st.button("Limpar tudo", use_container_width=True):
            st.session_state.ingredients = []
            st.session_state.selected_recipe = None
            st.rerun()
else:
    st.caption("Sua lista ainda está vazia.")

with st.expander("＋ Experimente com alguns ingredientes"):
    examples = ["ovo", "tomate", "queijo", "arroz", "cenoura", "macarrão", "leite", "cebola", "alho"]
    cols = st.columns(3)
    for i, item in enumerate(examples):
        with cols[i % 3]:
            if st.button(item.capitalize(), key=f"ex_{item}", use_container_width=True):
                if item not in st.session_state.ingredients:
                    st.session_state.ingredients.append(item)
                st.rerun()

st.markdown("---")
st.markdown('<div class="section-title">2. Quanto tempo você tem?</div>', unsafe_allow_html=True)
time_choice = st.radio("Tempo disponível", ["Até 15 min", "Até 30 min", "Até 45 min", "Sem pressa"], horizontal=True, label_visibility="collapsed")
time_limit = {"Até 15 min": 15, "Até 30 min": 30, "Até 45 min": 45, "Sem pressa": 999}[time_choice]

st.markdown("")
find = st.button("Encontrar receitas para mim  →", type="primary", use_container_width=True)

if find:
    if not st.session_state.ingredients:
        st.warning("Adicione pelo menos um ingrediente para encontrar receitas.")
    else:
        st.session_state.selected_recipe = None
        st.session_state.show_results = True

if st.session_state.get("show_results", False):
    user_items = set(st.session_state.ingredients)
    matches = []
    for recipe in RECIPES:
        if recipe["time"] <= time_limit:
            required = set(recipe["ingredients"])
            optional = set(recipe.get("optional", []))
            hits = required & user_items
            optional_hits = optional & user_items
            missing = required - user_items
            # Uma correspondência já pode gerar uma ideia; receitas mais próximas
            # do que a pessoa tem aparecem primeiro. Ingredientes opcionais dão bônus.
            if hits:
                coverage = len(hits) / len(required)
                score = coverage + (0.08 * len(optional_hits))
                matches.append((score, len(hits), len(optional_hits), recipe))
    matches.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)

    st.markdown("---")
    st.markdown('<div class="section-title">Ideias para a sua cozinha</div>', unsafe_allow_html=True)
    if not matches:
        st.info("Ainda não encontramos uma combinação com esses ingredientes e esse tempo. Tente adicionar mais um ou dois itens — ou escolha um tempo maior.")
    else:
        st.markdown(f'<div class="hint">Encontramos {len(matches)} ideia(s) a partir do que você tem. As primeiras opções são as que aproveitam melhor seus ingredientes.</div>', unsafe_allow_html=True)
        for idx, (score, hits, optional_hits, recipe) in enumerate(matches[:5]):
            missing = [x for x in recipe["ingredients"] if x not in user_items]
            if not missing:
                match_label = "Você tem todos os ingredientes principais"
            elif len(missing) == 1:
                match_label = "Falta só 1 ingrediente principal"
            else:
                match_label = f"Faltam {len(missing)} ingredientes principais"
            with st.container(border=True):
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.markdown(f'<div class="recipe-name">{recipe["name"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="recipe-meta">◷ {recipe["time"]} min &nbsp; · &nbsp; {recipe["category"]} &nbsp; · &nbsp; {hits}/{len(recipe["ingredients"])} ingredientes principais disponíveis</div>', unsafe_allow_html=True)
                    st.write(recipe["description"])
                    st.caption(match_label)
                    if missing:
                        st.caption("Para a versão completa, pode faltar: " + ", ".join(missing))
                    if optional_hits:
                        st.caption("Também aproveita: " + ", ".join(sorted(optional_hits)))
                with c2:
                    st.write("")
                    if st.button("Ver receita", key=f"recipe_{idx}", type="primary", use_container_width=True):
                        st.session_state.selected_recipe = recipe["name"]
                        st.rerun()

if st.session_state.selected_recipe:
    recipe = next(r for r in RECIPES if r["name"] == st.session_state.selected_recipe)
    st.markdown("---")
    st.markdown(f'<div class="kicker">MODO DE PREPARO · {recipe["time"]} MIN</div><div class="section-title">{recipe["name"]}</div>', unsafe_allow_html=True)
    st.write(recipe["description"])
    st.markdown("**Ingredientes principais**")
    st.write(", ".join(recipe["ingredients"]))
    if recipe.get("optional"):
        st.markdown("**Extras opcionais**")
        st.write(", ".join(recipe["optional"]))
    st.caption("Confira o que você tem e adapte temperos e quantidades ao seu gosto.")
    st.markdown("**Modo de preparo**")
    for n, step in enumerate(recipe["steps"], 1):
        st.markdown(f"**{n}.** {step}")
    if st.button("← Voltar às sugestões"):
        st.session_state.selected_recipe = None
        st.rerun()

st.markdown("---")
st.markdown("<div style='text-align:center;color:#929B90;font-size:.78rem'>mise. · uma boa ideia começa com o que você já tem.</div>", unsafe_allow_html=True)
