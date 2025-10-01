import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ========================
# CONFIGURAÇÃO DA PÁGINA
# ========================
st.set_page_config(page_title="CRTN BELÉM", layout="centered")

# ========================
# ESTILO VISUAL PRETO E DOURADO COMPLETO
# ========================
st.markdown("""
<style>
/* Fundo da página inteiro */
body, .block-container {
    background-color: #000000 !important;
    color: #d4af37 !important;
}

/* Cabeçalhos */
h1, h2, h3, h4 {
    color: #d4af37 !important;
    text-shadow: 1px 1px 2px #333333;
}

/* Texto normal */
p, span, label, div, td, th {
    color: #d4af37 !important;
}

/* Botões gerais */
div.stButton > button {
    background-color: #d4af37 !important;  /* fundo dourado */
    color: #000000 !important;            /* letras pretas */
    font-weight: bold !important;         /* negrito */
    font-size: 18px !important;           /* maior para destacar */
    height: 45px !important;
    width: 250px !important;
    border-radius: 12px !important;
    border: 2px solid #d4af37 !important;
    transition: background 0.3s;
    margin: 8px 0;
}
div.stButton > button:hover {
    background-color: #f0c75e !important; /* dourado mais claro ao passar o mouse */
    color: #000000 !important;
}

/* Cards de informações */
.card {
    background-color: #1a1a1a;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 10px;
    box-shadow: 3px 3px 10px rgba(255, 215, 0, 0.2);
    color: #d4af37 !important;
}

/* Inputs e selects */
input, select, textarea {
    border-radius: 10px;
    padding: 5px;
    background-color: #333333;
    color: #d4af37 !important;
    border: 1px solid #d4af37;
}

/* Placeholder dos inputs */
::placeholder {
    color: #d4af37 !important;
}
</style>
""", unsafe_allow_html=True)

# ========================
# ADMINISTRADORES (professores)
# ========================
administradores = {
    "Professor Hercules Pereira": "Pedro123*",
    "Professor Fernando Quirino Bernardo": "Carol123*"
}

# ========================
# BANCO DE DADOS
# ========================
if "alunos" not in st.session_state:
    st.session_state.alunos = pd.DataFrame([
        {"Nome": "João Silva", "Faixa": "Azul", "Graus": 2, "Presenças": 10, "Faltas": 2},
        {"Nome": "Maria Souza", "Faixa": "Roxa", "Graus": 1, "Presenças": 8, "Faltas": 4},
        {"Nome": "Carlos Lima", "Faixa": "Branca", "Graus": 3, "Presenças": 12, "Faltas": 0},
        {"Nome": "Lucas Infantil", "Faixa": "Cinza/Laranja", "Graus": 1, "Presenças": 5, "Faltas": 1},
    ])

if "historico" not in st.session_state:
    st.session_state.historico = pd.DataFrame(columns=["Aluno", "Tipo", "Data"])

# ========================
# SESSÃO
# ========================
if "logado" not in st.session_state:
    st.session_state.logado = False
    st.session_state.usuario = ""
if "aluno_logado" not in st.session_state:
    st.session_state.aluno_logado = None

# ========================
# FUNÇÃO DE FAIXA VISUAL COM BARRAS
# ========================
def faixa_visual(faixa, graus):
    cor = {
        "Branca": "white",
        "Cinza": "lightgrey",
        "Cinza/Laranja": "orange",
        "Cinza/Amarela": "yellow",
        "Laranja": "orange",
        "Amarela": "yellow",
        "Verde": "green",
        "Azul": "blue",
        "Roxa": "purple",
        "Marrom": "brown",
        "Preta": "black"
    }.get(faixa, "grey")
    cor_texto = "black" if cor in ["white", "yellow", "lightgrey"] else "white"
    barras = ""
    for i in range(4):
        if i < graus:
            barras += f"<div style='display:inline-block; width:20px; height:10px; margin:1px; background:{cor_texto}; border-radius:3px;'></div>"
        else:
            barras += f"<div style='display:inline-block; width:20px; height:10px; margin:1px; background:lightgrey; border-radius:3px;'></div>"
    return f"<div style='background:{cor}; color:{cor_texto}; padding:10px; border-radius:10px; text-align:center; font-weight:bold;'>{faixa}<br>{barras}</div>"

# ========================
# CABEÇALHO
# ========================
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image(os.path.join(os.getcwd(), "logo_crtn2.jpeg"), width=100)
    except:
        st.markdown("<h2 style='color:#d4af37;'>CRTN</h2>", unsafe_allow_html=True)
with col2:
    st.markdown("""
        <div style='padding:15px; background:#000000; color:#d4af37; font-size:26px; font-weight:bold; 
                    border-radius:10px; text-align:center; box-shadow:3px 3px 10px rgba(255, 215, 0, 0.2);'>
            CRTN BELÉM - SISTEMA DE PRESENÇA
        </div>
    """, unsafe_allow_html=True)
st.write("")

# ========================
# PERFIL DE ACESSO
# ========================
perfil = st.sidebar.radio("Quem está acessando?", ["Aluno", "Professor"])

# ========================
# FUNÇÃO REGISTRAR HISTÓRICO
# ========================
def registrar_historico(aluno, tipo):
    hoje = datetime.now().strftime("%d/%m/%Y")
    st.session_state.historico = pd.concat([
        st.session_state.historico,
        pd.DataFrame([{"Aluno": aluno, "Tipo": tipo, "Data": hoje}])
    ], ignore_index=True)

# ========================
# LOGIN PROFESSOR
# ========================
if perfil == "Professor":
    if not st.session_state.logado:
        st.subheader("🔐 Login do Professor")
        usuario = st.text_input("Usuário (nome completo)")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if usuario in administradores and administradores[usuario] == senha:
                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.success(f"Bem-vindo {usuario}!")
            else:
                st.error("Usuário ou senha incorretos.")
        st.stop()

# ========================
# LOGIN / CADASTRO ALUNO
# ========================
if perfil == "Aluno":
    st.subheader("🎓 Acesso do Aluno")

    if st.session_state.aluno_logado is None:
        acao_aluno = st.radio("Você já está cadastrado?", ["Sim, quero logar", "Não, quero me cadastrar"])
        
        if acao_aluno == "Sim, quero logar":
            aluno_nome = st.selectbox("Selecione seu nome:", st.session_state.alunos["Nome"], key="login_aluno")
            if st.button("Entrar"):
                st.session_state.aluno_logado = aluno_nome
        
        else:  # Cadastro
            st.markdown("📝 **Cadastro de Aluno**")
            nome = st.text_input("Nome completo", key="cadastro_nome")
            faixa = st.selectbox("Faixa atual", [
                "Branca", "Cinza", "Cinza/Laranja", "Cinza/Amarela",
                "Laranja", "Amarela", "Verde", "Azul", "Roxa", "Marrom", "Preta"
            ], key="cadastro_faixa")
            grau = st.slider("Grau da faixa", 0, 4, 0, key="cadastro_grau")
            if st.button("Cadastrar"):
                if nome.strip() == "":
                    st.error("Digite um nome válido.")
                else:
                    st.session_state.alunos = pd.concat([
                        st.session_state.alunos,
                        pd.DataFrame([{
                            "Nome": nome,
                            "Faixa": faixa,
                            "Graus": grau,
                            "Presenças": 0,
                            "Faltas": 0
                        }])
                    ], ignore_index=True)
                    st.session_state.aluno_logado = nome

# ========================
# ALUNO LOGADO
# ========================
if perfil == "Aluno" and st.session_state.aluno_logado:
    aluno = st.session_state.aluno_logado
    st.subheader(f"📌 Marcar Presença - {aluno}")

    if st.button("Marcar presença"):
        idx = st.session_state.alunos[st.session_state.alunos["Nome"] == aluno].index[0]
        st.session_state.alunos.loc[idx, "Presenças"] += 1
        registrar_historico(aluno, "Presença")
        st.success(f"Presença registrada para {aluno}!")

    st.subheader("📊 Meu histórico")
    dados = st.session_state.alunos[st.session_state.alunos["Nome"] == aluno].iloc[0]
    presencas = dados["Presenças"]
    faltas = dados["Faltas"]
    total = presencas + faltas
    pct = round(presencas / total * 100, 1) if total > 0 else 0

    st.markdown(f"""
    <div class="card">
    - <b>Faixa:</b> {dados["Faixa"]}<br>
    - <b>Graus:</b> {dados["Graus"]}<br>
    - <b>Presenças:</b> {presencas}<br>
    - <b>Faltas:</b> {faltas}<br>
    - <b>Aproveitamento:</b> {pct}%
    </div>
    """, unsafe_allow_html=True)
    st.markdown(faixa_visual(dados["Faixa"], dados["Graus"]), unsafe_allow_html=True)

# ========================
# PAINEL PROFESSOR LOGADO
# ========================
if perfil == "Professor" and st.session_state.logado:
    st.subheader(f"🛡️ Painel do Professor - {st.session_state.usuario}")

    # --------- MARCAR PRESENÇA / FALTA MÚLTIPLOS ALUNOS ---------
    st.markdown("### 🟢 Registrar Presença/Falta")
    alunos_selecionados = st.multiselect(
        "Selecione os alunos para presença/falta:", 
        st.session_state.alunos["Nome"], key="multiselect_presenca"
    )
    acao_presenca = st.radio("O que deseja registrar?", ["Presença", "Falta"], key="radio_presenca")
    if st.button("Registrar Presença/Falta para Selecionados"):
        if alunos_selecionados:
            for aluno in alunos_selecionados:
                idx = st.session_state.alunos[st.session_state.alunos["Nome"] == aluno].index[0]
                if acao_presenca == "Presença":
                    st.session_state.alunos.loc[idx, "Presenças"] += 1
                    registrar_historico(aluno, "Presença")
                else:
                    st.session_state.alunos.loc[idx, "Faltas"] += 1
                    registrar_historico(aluno, "Falta")
            st.success(f"{acao_presenca}(s) registrado(s) para: {', '.join(alunos_selecionados)}")
        else:
            st.warning("Selecione pelo menos um aluno.")

    # --------- ALTERAR GRADUAÇÃO / GRAU MÚLTIPLOS ALUNOS ---------
    st.markdown("### 🎖 Alterar Graduação/Grau para Múltiplos Alunos")
    alunos_alterar = st.multiselect(
        "Selecione os alunos para alterar graduação:", 
        st.session_state.alunos["Nome"], key="multiselect_grau"
    )
    nova_faixa = st.selectbox("Nova faixa:", [
        "Branca", "Cinza", "Cinza/Laranja", "Cinza/Amarela",
        "Laranja", "Amarela", "Verde", "Azul", "Roxa", "Marrom", "Preta"
    ], key="select_faixa")
    novo_grau = st.slider("Novo grau:", 0, 4, 0, key="slider_grau")
    if st.button("Atualizar Graduação de Todos Selecionados"):
        if alunos_alterar:
            for aluno in alunos_alterar:
                idx = st.session_state.alunos[st.session_state.alunos["Nome"] == aluno].index[0]
                st.session_state.alunos.loc[idx, "Faixa"] = nova_faixa
                st.session_state.alunos.loc[idx, "Graus"] = novo_grau
            st.success(f"Graduação atualizada para {', '.join(alunos_alterar)}: {nova_faixa} com {novo_grau} grau(s)")
        else:
            st.warning("Selecione pelo menos um aluno para atualizar.")

    # --------- EXCLUIR ALUNOS (MÚLTIPLOS) ---------
    with st.expander("❌ Excluir Alunos da Base", expanded=False):
        alunos_excluir = st.multiselect(
            "Selecione os alunos que deseja excluir:", 
            st.session_state.alunos["Nome"], key="multiselect_excluir"
        )
        if st.button("Excluir Alunos Selecionados"):
            if alunos_excluir:
                for aluno in alunos_excluir:
                    st.session_state.alunos = st.session_state.alunos[st.session_state.alunos["Nome"] != aluno].reset_index(drop=True)
                    st.session_state.historico = st.session_state.historico[st.session_state.historico["Aluno"] != aluno].reset_index(drop=True)
                st.success(f"Alunos excluídos com sucesso: {', '.join(alunos_excluir)}")
            else:
                st.warning("Selecione pelo menos um aluno para excluir.")

    # --------- HISTÓRICO COMPLETO POR ALUNO ---------
    st.markdown("### 📅 Histórico Completo de um Aluno")
    aluno_historico = st.selectbox("Selecione o aluno para ver histórico:", st.session_state.alunos["Nome"], key="select_historico")
    historico_aluno = st.session_state.historico[st.session_state.historico["Aluno"] == aluno_historico]
    if not historico_aluno.empty:
        st.dataframe(historico_aluno[["Data", "Tipo"]].sort_values(by="Data", ascending=False))
    else:
        st.info("Nenhuma presença ou falta registrada ainda.")
