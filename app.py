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

