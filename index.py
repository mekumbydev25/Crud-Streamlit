# IMPORTAÇÕES
import streamlit as st
import pandas as pd
import sqlite3
import time
from CRUDINTERFACE.src.crudinterface.db import tabela
from CRUDINTERFACE.src.crudinterface.db import funcoes

# UI Streamlit

def UI():
    tabela.Tabela()
    #configuração do layout da página
    st.set_page_config(page_title="CRUD", layout="centered")
    
    # ========= SideBar ========= #
    with st.sidebar:
        st.title("Limpeza no Banco")
        limpeza = st.button(label="Limpar os campos vazios banco.", width="stretch")
        if limpeza:
            try:
                dados_removidos = funcoes.Clean_Data()
                if dados_removidos > 0:
                    st.toast(f"Limpeza concluída: {dados_removidos} registros inválidos removidos",icon="✅")
                else:
                    st.info("Nenhum registro vazio foi encontrado")
            except Exception as e:
                st.error(f"Erro ao Limpar os registros vazios do banco: {e}")
        st.divider()
        
        st.subheader("ZONA DE PERIGO")
        confirmar = st.checkbox(label="Tem certeza que pretende apagar Tudo")
        if st.button("Zerar banco de dados", disabled=not confirmar):
            try:
                funcoes.Reset_Table()
                st.toast("Banco Zerado! o proximo registro terá o ID 1", icon="✅")
                
            except Exception as e:
                st.error(f"Erro ao Zerar o banco: {e}")
                
    # ========== Container Principal =========== #
    with st.container(border=True):
            st.markdown("<h2 style='text-align:center; margin-bottom:20px;'>Seja Bem-vindo ao CRUD</h2>", unsafe_allow_html=True)
            #st.markdown("<p style='text-align:start; color:gray; font-size:25px; margin-bottom:5px;'>Menu de navegação</p>", unsafe_allow_html=True)
            st.divider()
                        
            abas = st.tabs(["Cadastrar usuários","Listar Dados", "Procurar Dados", "Deletar Dados", "Atualizar Dados"])
                    
            # ============== CADASTRAR USUÁRIOS =============== # 
            with abas[0]:
                with st.form(key="Form_CadastrarUsuario", border=True, clear_on_submit=True):
                    st.markdown("<h2 style='text-align:center; margin-bottom:20px;'>Cadastro de clientes</h2>", unsafe_allow_html=True)
                    nome = st.text_input(label="Informe o seu nome: ", placeholder="o seu nome").strip()
                    telefone = st.text_input(label="Informe o seu nº de telefone: ", placeholder="9xxxxxxxx", max_chars=9).strip()
                    endereco = st.text_input(label="Informe o seu endereço: ", placeholder="o seu endereço").strip()
                    btn_cadastrar = st.form_submit_button("Cadastrar", width=200)
                    
                if btn_cadastrar:
                    if not nome or not telefone or not endereco:
                        st.error("Preencha todos os campos")
                    elif not telefone.isdigit() or len(telefone) != 9 or not telefone.startswith("9"):
                        st.error("O telefone deve conter apenas números válidos com 9 dígitos")
                    else:
                        try:
                            funcoes.insert_Data(nome, telefone, endereco)
                            st.toast("Usuário cadastrado com sucesso",icon="✅")
                            
                        except sqlite3.IntegrityError:
                            st.error("Já existe um usuário com este telefone.")
                            
                        except Exception as e:
                            st.error(f"Erro ao cadastrar: {e}")
                            
            # ===============   LISTAR USUÁRIOS ================ #             
            with abas[1]:
                with st.form(key="Form_ListarUsuarios", border=True):
                    st.markdown("<h2 style='text-align:center; margin-bottom:20px;'>Listagem de Usuários</h2>", unsafe_allow_html=True)
                    btn_listar = st.form_submit_button(label="Listar usuários", width=200)
                if btn_listar:
                    try: 
                        data = funcoes.List_Data()
                        if not data:
                            st.info("Ainda não existe nenhum usuário cadastrado")
                        else:
                            with st.spinner("A Listar...", show_time=True):
                                time.sleep(4)
                                st.dataframe(pd.DataFrame(data, columns=["Id", "Nome", "Telefone", "Endereço"]), hide_index=True)
                    except Exception as e:
                        st.error(f"Erro ao listar usuários: {e}")
                    
            # ===============   PROCURAR USUÁRIOS ================ #  
            with abas[2]:
                with st.form(key="Form_ProcurarUsuarios", border=True, clear_on_submit=True):
                    st.markdown("<h2 style='text-align:center; margin-bottom:20px;'>Procurar Usuários</h2>", unsafe_allow_html=True)
                    id_procurar = st.text_input(label="Informe o id do usuário:", placeholder="o id do usuário", key="id_procurar").strip()
                    btn_procurar = st.form_submit_button(label="Procurar usuários", width=200)
                    
                if btn_procurar:
                    if not id_procurar.isdigit():
                        st.error("Informe um id válido (apenas números).")
                    else:
                        try:
                            user = funcoes.Find_Data(int(id_procurar))
                            if user is None:
                                st.warning("Não existe nenhum usuário com este id.")
                            else:
                                with st.spinner("A procurar...", show_time=True):
                                    time.sleep(4)
                                    st.toast("Usuário encontrado com sucesso",icon="✅")
                                    st.dataframe(pd.DataFrame([user], columns=["Id", "Nome", "Telefone", "Endereço"]), hide_index=True)
                                    
                                    
                        except Exception as e:
                            st.error(f"Erro ao procurar usuário {e}")
                            
                            
            # ===============   DELETAR USUÁRIOS ================ #            
            with abas[3]:
                with st.form(key="Form_DeletarUsuarios", border=True, clear_on_submit=True):
                    st.markdown("<h2 style='text-align:center; margin-bottom:20px;'>Deletar Usuários</h2>", unsafe_allow_html=True)
                    id_deletar = st.text_input(label="Informe o id:", placeholder="o id que vai deletar", key="id_deletar").strip()
                    btn_deletar = st.form_submit_button(label="Deletar usuário", width=200)
                    
                if btn_deletar:
                    if not id_deletar.isdigit():
                        st.error("Informe um id válido (apenas números).")
                    else:
                        try:
                            user_deletar = funcoes.Find_Data(int(id_deletar))
                            if user_deletar is None:
                                st.error("Não existe usuário com este id.")
                            else:
                                funcoes.Delete_Data(int(id_deletar))
                                st.toast(f"Usuário de id {id_deletar} foi deletado com sucesso",icon="✅")
                        except Exception as e:
                            st.error(f"Erro ao deletar usuário. {e}")
                        
                        
            # ===============   ATUALIZAR USUÁRIOS ================ #            
            with abas[4]:
                with st.form(key="Form_AtualizarUsuarios", border=True, clear_on_submit=True):
                    st.markdown("<h2 style='text-align:center; margin-bottom:20px;'>Atualizar Usuários</h2>", unsafe_allow_html=True)
                    id_atualizar = st.text_input(label="Informe o id:", placeholder="o id do usuário", key="id_atualizar").strip()
                    novo_endereco = st.text_input(label="Informe o novo endereço: ", placeholder="o seu endereço atual", key="novo_endereco").strip()
                    btn_atualizar = st.form_submit_button(label="Atualizar dados", width=200)
                    
                if btn_atualizar:
                    if not id_atualizar.isdigit():
                        st.error("Informe um id válido (apenas números).")
                    elif not novo_endereco:
                        st.error("O endereço não pode estar vazio")
                    else:
                        try:
                            if funcoes.Find_Data(int(id_atualizar)) is None:
                                st.error("Não existe usuário com este id.")
                            else:
                                funcoes.Update_Data(novo_endereco, int(id_atualizar))
                                user_atualizado = funcoes.Find_Data(int(id_atualizar))
                                st.toast("Os dados do usuário foram atualizados",icon="✅")
                                st.dataframe(pd.DataFrame([user_atualizado], columns=["Id", "Nome", "Telefone", "Endereço"]), hide_index=True)
                        except Exception as e:
                            st.error(f"Erro ao atualizar os dados. {e}")

UI()
#================================#
#==Developmment by: MekumbyDev ==#
#================================#