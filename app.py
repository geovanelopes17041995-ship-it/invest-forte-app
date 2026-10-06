import streamlit as st
import pandas as pd
import random
import mercadopago
import urllib.parse

# ---------------------------------------------------------
# CONFIGURAÇÃO DO MERCADO PAGO
# ---------------------------------------------------------
MERCADOPAGO_ACCESS_TOKEN = "APP_USR-4934588586838432-XXXXXXXX-241983636"
sdk = mercadopago.SDK(MERCADOPAGO_ACCESS_TOKEN)

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Invest Forte | Desde 1995",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# ESTILIZAÇÃO CSS (VISUAL EXTREMAMENTE CHAMATIVO & MODERNO)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 20% 20%, #1e1b4b 0%, #0f172a 40%, #020617 100%) !important;
        color: #FFFFFF;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .brand-logo {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }

    .brand-badge {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-left: 10px;
    }

    .card-branc-login {
        background: #FFFFFF;
        border-radius: 24px;
        padding: 35px;
        color: #0F172A;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 30px rgba(56, 189, 248, 0.2);
    }

    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 12px !important;
        padding: 12px 14px !important;
        font-weight: 500;
    }

    .stButton>button {
        width: 100%;
        border-radius: 14px;
        font-weight: 800;
        font-size: 1.05rem;
        background: linear-gradient(90deg, #2563eb 0%, #3b82f6 100%);
        color: #FFFFFF !important;
        border: none;
        padding: 14px 20px;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.5);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 25px -5px rgba(37, 99, 235, 0.7);
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%);
    }

    .card-dashboard {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }

    .card-item-invest {
        background: rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(10px);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 16px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        transition: all 0.3s ease;
    }

    .card-item-invest:hover {
        border-color: rgba(56, 189, 248, 0.5);
        background: rgba(255, 255, 255, 0.1);
    }

    .highlight-badge {
        background: linear-gradient(90deg, #10b981, #059669);
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 12px;
        text-transform: uppercase;
    }

    .highlight-vip {
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 12px;
        text-transform: uppercase;
    }

    .highlight-master {
        background: linear-gradient(90deg, #ec4899, #8b5cf6);
        color: white;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 12px;
        text-transform: uppercase;
    }

    /* Estilo dos Botões de Compartilhamento Social */
    .btn-share {
        display: inline-block;
        width: 100%;
        text-align: center;
        padding: 14px 20px;
        border-radius: 14px;
        font-weight: 700;
        color: #FFFFFF !important;
        text-decoration: none !important;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }
    .btn-whatsapp {
        background: #25D366;
        box-shadow: 0 8px 16px rgba(37, 211, 102, 0.3);
    }
    .btn-facebook {
        background: #1877F2;
        box-shadow: 0 8px 16px rgba(24, 119, 242, 0.3);
    }
    .btn-instagram {
        background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
        box-shadow: 0 8px 16px rgba(220, 39, 67, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# INICIALIZAÇÃO DE DADOS EM MEMÓRIA
# ---------------------------------------------------------
if "usuarios" not in st.session_state:
    st.session_state.usuarios = {
        "admin@investforte.com": {
            "nome": "Cliente Demonstracao",
            "senha": "123",
            "saldo": 12500.00,
            "extrato": [],
            "codigo_ref": "REF123",
            "indicado_por": None,
            "bono_recebido": False
        }
    }

if "usuario_logado" not in st.session_state:
    st.session_state.usuario_logado = None

if "saques_bloqueados_global" not in st.session_state:
    st.session_state.saques_bloqueados_global = False

query_params = st.query_params
eh_admin_master = query_params.get("admin") == "true"

# ---------------------------------------------------------
# FUNÇÃO PARA GERAR PIX NO MERCADO PAGO
# ---------------------------------------------------------
def gerar_pix_mercadopago(valor, email_cliente, nome_cliente):
    try:
        partes_nome = nome_cliente.split()
        primeiro_nome = partes_nome[0] if partes_nome else "Cliente"
        sobrenome = partes_nome[-1] if len(partes_nome) > 1 else "InvestForte"

        payment_data = {
            "transaction_amount": float(valor),
            "description": f"Deposito Invest Forte - {nome_cliente}",
            "payment_method_id": "pix",
            "payer": {
                "email": email_cliente,
                "first_name": primeiro_nome,
                "last_name": sobrenome,
            }
        }

        payment_response = sdk.payment().create(payment_data)
        payment = payment_response.get("response", {})

        if "point_of_interaction" in payment:
            qr_base64 = payment["point_of_interaction"]["transaction_data"]["qr_code_base64"]
            pix_copia_cola = payment["point_of_interaction"]["transaction_data"]["qr_code"]
            id_pagamento = payment["id"]
            return {"id": id_pagamento, "qr_base64": qr_base64, "copia_cola": pix_copia_cola}, None
        else:
            msg_erro = payment.get("message", "Erro ao comunicar com o Mercado Pago.")
            return None, msg_erro
    except Exception as e:
        return None, str(e)

# ---------------------------------------------------------
# TOPO / BARRA DE NAVEGAÇÃO
# ---------------------------------------------------------
col_nav1, col_nav2 = st.columns([2, 1])

with col_nav1:
    st.markdown("""
        <div>
            <span class="brand-logo">INVEST FORTE</span>
            <span class="brand-badge">Tradição desde 1995</span>
        </div>
    """, unsafe_allow_html=True)

with col_nav2:
    if st.session_state.usuario_logado:
        nome_usr = st.session_state.usuarios[st.session_state.usuario_logado]['nome']
        st.markdown(f"<div style='text-align: right; color: #FFFFFF; font-weight: 600; margin-bottom: 5px;'>Olá, <span style='color: #38bdf8;'>{nome_usr.split()[0]}</span></div>", unsafe_allow_html=True)
        if st.button("Sair da Conta", key="btn_logout"):
            st.session_state.usuario_logado = None
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# TELA DE ACESSO (DESLOGADO)
# ---------------------------------------------------------
if st.session_state.usuario_logado is None:
    col_texto, col_espaco, col_form = st.columns([1.2, 0.1, 1])

    with col_texto:
        st.markdown("""
        <div style="background: rgba(56, 189, 248, 0.1); border: 1px solid rgba(56, 189, 248, 0.3); display: inline-block; padding: 6px 16px; border-radius: 30px; margin-bottom: 15px;">
            <span style="color: #38bdf8; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.05em; text-transform: uppercase;">
                🛡 Solidez & Confiança • Desde 1995
            </span>
        </div>
        <h1 style="font-size: 3.2rem; font-weight: 800; line-height: 1.15; margin-bottom: 20px; background: linear-gradient(180deg, #FFFFFF 0%, #CBD5E1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Sua liberdade financeira começa com rentabilidade real.
        </h1>
        <p style="font-size: 1.25rem; color: #94A3B8; line-height: 1.6; margin-bottom: 30px;">
            Acesse as melhores oportunidades do mercado a partir de R$ 10,00 até R$ 50.000,00. Gerencie seu saldo com total segurança, receba depósitos via Pix instantâneo e faça resgates rápidos.
        </p>
        <div style="display: flex; gap: 20px; font-size: 0.95rem; color: #CBD5E1;">
            <div>⚡ <b>Pix Instantâneo</b></div>
            <div>🔒 <b>Segurança Máxima</b></div>
            <div>📈 <b>Cotas de R$ 10 a R$ 50.000</b></div>
        </div>
        """, unsafe_allow_html=True)

    with col_form:
        st.markdown('<div class="card-branc-login">', unsafe_allow_html=True)
        
        opcoes_menu = ["🔑 Entrar", "📝 Criar conta grátis"]
        if eh_admin_master:
            opcoes_menu.append("⚙ Master")

        aba_acesso = st.radio("", opcoes_menu, horizontal=True, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)

        if aba_acesso == "🔑 Entrar":
            st.markdown("<h3 style='color:#0F172A; margin-top:0; font-weight: 800;'>Aceder à sua conta</h3>", unsafe_allow_html=True)
            email = st.text_input("Seu e-mail:")
            senha = st.text_input("Sua senha:", type="password")
            
            if st.button("Aceder agora"):
                if email in st.session_state.usuarios and st.session_state.usuarios[email]["senha"] == senha:
                    st.session_state.usuario_logado = email
                    st.success("Autenticado com sucesso!")
                    st.rerun()
                else:
                    st.error("E-mail ou senha incorretos.")

        elif aba_acesso == "📝 Criar conta grátis":
            st.markdown("<h3 style='color:#0F172A; margin-top:0; font-weight: 800;'>Cadastre-se agora!</h3>", unsafe_allow_html=True)
            novo_nome = st.text_input("Nome Completo:")
            novo_email = st.text_input("Preencha seu e-mail:")
            nova_senha = st.text_input("Crie uma senha:", type="password")
            confirma_senha = st.text_input("Confirme a senha:", type="password")
            codigo_indicacao = st.text_input("Código de Indicação (Opcional):", placeholder="Ex: REF123")
            
            if st.button("Criar conta grátis"):
                if not novo_nome or not novo_email or not nova_senha:
                    st.error("Preencha todos os campos obrigatórios.")
                elif nova_senha != confirma_senha:
                    st.error("As senhas não coincidem.")
                elif novo_email in st.session_state.usuarios:
                    st.error("Este e-mail já está registado.")
                else:
                    quem_indicou = None
                    if codigo_indicacao.strip():
                        for u_email, u_dados in st.session_state.usuarios.items():
                            if u_dados.get("codigo_ref") == codigo_indicacao.strip():
                                quem_indicou = u_email
                                break

                    novo_ref = f"REF{random.randint(1000, 9999)}"
                    st.session_state.usuarios[novo_email] = {
                        "nome": novo_nome,
                        "senha": nova_senha,
                        "saldo": 0.00,
                        "extrato": [],
                        "codigo_ref": novo_ref,
                        "indicado_por": quem_indicou,
                        "bono_recebido": False
                    }
                    st.success("Conta criada! Alterne para a aba 'Entrar'.")

        elif aba_acesso == "⚙ Master":
            st.markdown("<h3 style='color:#0F172A; margin-top:0; font-weight: 800;'>Painel Master</h3>", unsafe_allow_html=True)
            senha_master = st.text_input("Senha Master:", type="password")
            if senha_master == "1234":
                st.success("Sessão de Admin ativa")
                bloqueio = st.toggle("Bloquear Saques Globalmente", value=st.session_state.saques_bloqueados_global)
                if bloqueio != st.session_state.saques_bloqueados_global:
                    st.session_state.saques_bloqueados_global = bloqueio
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TELA INTERNA (UTILIZADOR LOGADO)
# ---------------------------------------------------------
else:
    usr = st.session_state.usuarios[st.session_state.usuario_logado]

    aba_ativa = st.radio(
        "", 
        ["📊 Visão Geral", "📥 Depositar", "📤 Saque Pix", "🤝 Indicações & Redes", "📜 Extrato"], 
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if aba_ativa == "📊 Visão Geral":
        st.markdown(f"""
        <div class="card-dashboard">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="opacity: 0.8; font-size: 0.95rem; font-weight: 600;">Saldo Total Disponível</span>
                <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); padding: 4px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700;">
                    ● Status: {'🚫 Saques Suspensos' if st.session_state.saques_bloqueados_global else '✅ Sistema Operacional'}
                </span>
            </div>
            <h1 style="font-size: 3.5rem; margin: 10px 0px; font-weight: 800; color: #FFFFFF;">R$ {usr['saldo']:,.2f}</h1>
            <span style="font-size: 0.85rem; color: #94A3B8;">Invest Forte • Desde 1995 garantindo rentabilidade</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 💎 Oportunidades em Destaque")
        
        cotas = [
            {"nome": "Cota Micro Start", "minimo": 10.0, "retorno": "105% do CDI", "tag": "Iniciante", "css_tag": "highlight-badge"},
            {"nome": "Cota Renda Fixa Flex", "minimo": 50.0, "retorno": "115% do CDI", "tag": "Popular", "css_tag": "highlight-badge"},
            {"nome": "Cota FII Imobiliário Prime", "minimo": 100.0, "retorno": "0.9% a.m. dividendos", "tag": "Recomendado", "css_tag": "highlight-badge"},
            {"nome": "Cota Bronze Plus", "minimo": 200.0, "retorno": "120% do CDI", "tag": "Intermediário", "css_tag": "highlight-badge"},
            {"nome": "Cota Prata Executiva", "minimo": 300.0, "retorno": "125% do CDI", "tag": "Intermediário", "css_tag": "highlight-badge"},
            {"nome": "Cota Ouro Premium", "minimo": 500.0, "retorno": "1.2% a.m. + IPCA", "tag": "Destaque", "css_tag": "highlight-vip"},
            {"nome": "Cota Platina Pro", "minimo": 1000.0, "retorno": "140% do CDI", "tag": "VIP", "css_tag": "highlight-vip"},
            {"nome": "Cota Safira High Yield", "minimo": 3000.0, "retorno": "1.6% a.m. fixo", "tag": "VIP", "css_tag": "highlight-vip"},
            {"nome": "Cota Esmeralda Capital", "minimo": 5000.0, "retorno": "160% do CDI", "tag": "Elite", "css_tag": "highlight-vip"},
            {"nome": "Cota Diamante Private", "minimo": 10000.0, "retorno": "2.1% a.m. dividendos", "tag": "Private", "css_tag": "highlight-master"},
            {"nome": "Cota Institutional Master", "minimo": 50000.0, "retorno": "2.8% a.m. + Performance", "tag": "Master Black", "css_tag": "highlight-master"}
        ]

        for c in cotas:
            st.markdown(f"""
            <div class="card-item-invest">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <h4 style="margin: 0; font-size: 1.2rem; font-weight: 700; color: #FFFFFF;">{c['nome']}</h4>
                    <span class="{c['css_tag']}">{c['tag']}</span>
                </div>
                <p style="margin: 0; font-size: 1rem; color: #CBD5E1;">Aporte Mínimo: <b style="color: #38bdf8;">R$ {c['minimo']:,.2f}</b> | Projeção: <b style="color: #34d399;">{c['retorno']}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Investir R$ {c['minimo']:,.2f} em {c['nome']}", key=f"btn_{c['nome']}"):
                if st.session_state.saques_bloqueados_global:
                    st.error("Operações suspensas pelo sistema.")
                elif usr["saldo"] >= c["minimo"]:
                    usr["saldo"] -= c["minimo"]
                    usr["extrato"].append({"tipo": "Investimento", "valor": -c["minimo"], "status": "Aprovado", "descricao": c["nome"]})
                    st.success(f"Aporte de R$ {c['minimo']:,.2f} realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("Saldo insuficiente para realizar este aporte.")

    elif aba_ativa == "📥 Depositar":
        st.markdown("### 📥 Depositar via Mercado Pago (Pix Real)")
        valor_deposito = st.number_input("Valor do depósito (R$):", min_value=1.0, value=100.0, step=10.0)

        if st.button("Gerar PIX Real Mercado Pago"):
            with st.spinner("Gerando chave Pix no Mercado Pago..."):
                res_pix, erro = gerar_pix_mercadopago(
                    valor=valor_deposito,
                    email_cliente=st.session_state.usuario_logado,
                    nome_cliente=usr["nome"]
                )

            if erro:
                st.error(f"⚠ Erro Mercado Pago: {erro}")
            else:
                st.success(f"✅ QR Code Pix Gerado com Sucesso! (ID: {res_pix['id']})")
                
                st.image(f"data:image/jpeg;base64,{res_pix['qr_base64']}", width=250)
                
                st.markdown("**Pix Copia e Cola:**")
                st.code(res_pix["copia_cola"], language="text")
                st.info("Assim que realizar o pagamento no seu banco, o valor cairá diretamente na sua conta!")

                if st.button("Simular Confirmação de Saldo no App"):
                    usr["saldo"] += valor_deposito
                    usr["extrato"].append({"tipo": "Depósito Pix (Mercado Pago)", "valor": valor_deposito, "status": "Aprovado", "descricao": f"ID MP: {res_pix['id']}"})
                    st.success("Saldo creditado na plataforma!")
                    st.rerun()

    elif aba_ativa == "📤 Saque Pix":
        st.markdown("### 📤 Solicitar Resgate via Pix")
        st.write(f"Saldo disponível: **R$ {usr['saldo']:,.2f}**")

        if st.session_state.saques_bloqueados_global:
            st.error("🔒 Saques temporariamente suspensos.")
        else:
            chave_pix = st.text_input("Chave Pix:")
            valor_saque = st.number_input("Valor do saque (R$):", min_value=10.0, value=10.0, step=10.0)

            if st.button("Confirmar Saque"):
                if not chave_pix.strip():
                    st.error("Introduza uma chave Pix.")
                elif valor_saque > usr["saldo"]:
                    st.error("Saldo insuficiente.")
                else:
                    usr["saldo"] -= valor_saque
                    usr["extrato"].append({"tipo": "Saque Pix", "valor": -valor_saque, "status": "Processado", "descricao": f"Chave: {chave_pix}"})
                    st.success("Saque processado com sucesso!")
                    st.rerun()

    elif aba_ativa == "🤝 Indicações & Redes":
        st.markdown("### 🎁 Indique e Compartilhe")
        st.write("Partilhe o seu código de indicação ou a plataforma com amigos nas redes sociais.")
        
        cod_ref = usr.get("codigo_ref", "REF123")
        st.text_input("Seu código exclusivo:", value=cod_ref, disabled=True)

        st.markdown("<br><h4>📲 Compartilhar Plataforma</h4>", unsafe_allow_html=True)

        # Monta a mensagem de compartilhamento
        msg = f"Acesse a Invest Forte (Desde 1995)! Cadastre-se com meu código de indicação: {cod_ref}"
        msg_enc = urllib.parse.quote(msg)

        # Links das APIs oficiais das redes
        url_whatsapp = f"https://api.whatsapp.com/send?text={msg_enc}"
        url_facebook = f"https://www.facebook.com/sharer/sharer.php?quote={msg_enc}"

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f'<a href="{url_whatsapp}" target="_blank" class="btn-share btn-whatsapp">💬 WhatsApp</a>', unsafe_allow_html=True)
            
        with c2:
            st.markdown(f'<a href="{url_facebook}" target="_blank" class="btn-share btn-facebook">📘 Facebook</a>', unsafe_allow_html=True)
            
        with c3:
            st.markdown('<a href="https://www.instagram.com" target="_blank" class="btn-share btn-instagram">📸 Instagram</a>', unsafe_allow_html=True)

        st.caption("Nota para o Instagram: O Instagram não aceita compartilhamento direto de links externos. O seu texto de indicação com código foi preparado para colar na sua bio ou stories.")

    elif aba_ativa == "📜 Extrato":
        st.markdown("### 📜 Histórico de Movimentações")
        if not usr["extrato"]:
            st.info("Nenhuma movimentação registada.")
        else:
            for t in reversed(usr["extrato"]):
                sinal = "+" if t["valor"] > 0 else ""
                st.write(f"**{t['tipo']}**: {sinal}R$ {t['valor']:,.2f} | `{t['status']}` | _{t.get('descricao', '')}_")
                st.divider()