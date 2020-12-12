from datetime import date
from functools import partial

import pymongo
from bson import ObjectId
from kivy.lang import Builder
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import (
    MDList,
    StringProperty,
    ThreeLineIconListItem,
    TwoLineAvatarIconListItem,
)
from kivymd.uix.picker import MDDatePicker
from kivymd.utils import asynckivy


class Content(BoxLayout):
    pass


class CreateCheckList(ThreeLineIconListItem):
    pass


class CustomItem(TwoLineAvatarIconListItem):
    icon = StringProperty("")


class ExpansionpanelContent(BoxLayout):
    pass


interface = Builder.load_file("interface.kv")


############MAQUINARIO APP########################
class ChecklistApp(MDApp):
    panel_is_open = False

    try:
        name_perfil_toolbar = "Desconhecido"
        email_perfil_toolbar = "Desconhecido"
    except:
        pass

    teste = "teste"

    def panel_open(self, *args):
        self.panel_is_open = True

    def panel_close(self, *args):
        self.panel_is_open = False

    def delete_item(self, item):
        self.panel.content.remove_widget(item)
        self.panel.height -= item.height
        for index, val in enumerate(self.panel.content.children[::-1]):
            val.secondary_text = str(index + 1)

    def update(self):
        async def update():
            await asynckivy.sleep(1)
            try:
                self.store = JsonStore("userProfile.json")
                nome = self.store.get("UserInfo")["name"]
                email = self.store.get("UserInfo")["email"]

                interface.get_screen("profile").ids.profile_name_input.text = nome
                interface.get_screen("profile").ids.profile_email_input.text = email

            except Exception as erro:
                print(erro)

        asynckivy.start(update())

    def set_refresh(self):
        async def set_refresh():
            await asynckivy.sleep(1)
            try:
                self.store = JsonStore("userProfile.json")
                nome = self.store.get("UserInfo")["name"]
                email = self.store.get("UserInfo")["email"]

                await asynckivy.sleep(1)
                interface.get_screen("profile").ids.name_perfil_toolbar.text = nome
                interface.get_screen("profile").ids.email_perfil_toolbar.text = email

                interface.get_screen("screen1").ids.name_perfil_toolbar.text = nome
                interface.get_screen("screen1").ids.email_perfil_toolbar.text = email

                interface.get_screen("screen2").ids.name_perfil_toolbar.text = nome
                interface.get_screen("screen2").ids.email_perfil_toolbar.text = email

                interface.get_screen("screen3").ids.name_perfil_toolbar.text = nome
                interface.get_screen("screen3").ids.email_perfil_toolbar.text = email

                interface.get_screen("screen5").ids.name_perfil_toolbar.text = nome
                interface.get_screen("screen5").ids.email_perfil_toolbar.text = email

                interface.get_screen(
                    "checklistName"
                ).ids.name_perfil_toolbar.text = nome
                interface.get_screen(
                    "checklistName"
                ).ids.email_perfil_toolbar.text = email

                interface.get_screen("profile").ids.profile_name_input.text = nome
                interface.get_screen("profile").ids.profile_email_input.text = email

            except Exception as erro:
                print(erro)

        asynckivy.start(set_refresh())

    def update_profile(self):
        name = interface.get_screen("profile").ids.profile_name_input.text
        email = interface.get_screen("profile").ids.profile_email_input.text
        self.store.put("UserInfo", name=name, email=email)
        self.set_refresh()

    def build(self):
        """Carregamento e construção ao iniciar o app."""
        return interface

    def on_start(self):
        """Função ao iniciar o app ele vai carregar isso antes de mostrar tela."""
        self.load_checklist()
        self.set_refresh()
        self.update()
        self.store = JsonStore("userProfile.json")
        try:
            if self.store.get("UserInfo")["name"] != "":
                print(self.store.get("UserInfo")["name"])
                interface.get_screen("screen1").manager.current = "screen1"
            else:
                print(self.store.get("UserInfo")["name"])
                interface.get_screen("welcomescreen").manager.current = "welcomescreen"
        except:
            interface.get_screen("welcomescreen").manager.current = "welcomescreen"

    def clear_items_inputs(self):
        for i in range(1, 9):

            if (
                interface.get_screen(f"checklistItem{i}").ids.radio_item_c.active
                or interface.get_screen(f"checklistItem{i}").ids.radio_item_na.active
            ):

                interface.get_screen(f"checklistItem{i}").ids.acao_item.text = ""
                interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text = ""
                interface.get_screen(f"checklistItem{i}").ids.prazo_item.text = ""

    class ContentNavigationDrawer(BoxLayout):  #######PERFIL########
        pass

    class DrawerList(ThemableBehavior, MDList):  ######lISTAS DE AÇÕES DO PERFIL######
        pass

    def check_lv_name_and_description(self):
        print(interface.get_screen("checklistName").ids.name_text_field_lv.text)
        print(interface.get_screen("checklistName").ids.descricao_text_field_lv.text)
        if (
            interface.get_screen("checklistName").ids.name_text_field_lv.text != ""
            and interface.get_screen("checklistName").ids.descricao_text_field_lv.text
            != ""
        ):
            interface.get_screen("checklistName").ids.lv_name_button.disabled = False

        else:
            interface.get_screen("checklistName").ids.lv_name_button.disabled = True

    def add_new_lv(self):
        conformes = 0
        nao_conformes = 0
        nao_aplicaveis = 0
        myclient = pymongo.MongoClient(
            "mongodb+srv://julio:senha@cluster0.pn3vb.mongodb.net/kivyapp?retryWrites=true&w=majority"
        )
        db = myclient["kivyapp"]
        col_lv = db["lvs"]

        today = str(date.today())

        self.store = JsonStore("userProfile.json")
        nome = self.store.get("UserInfo")["name"]
        email = self.store.get("UserInfo")["email"]

        results = []

        for i in range(1, 9):
            if (
                interface.get_screen(f"checklistItem{i}").ids.radio_item_c.active
                == True
            ):
                results.append("Conforme")
                conformes += 1

            if (
                interface.get_screen(f"checklistItem{i}").ids.radio_item_nc.active
                == True
            ):
                results.append("Não conforme")
                nao_conformes += 1

            if (
                interface.get_screen(f"checklistItem{i}").ids.radio_item_na.active
                == True
            ):
                results.append("Não aplicável")
                nao_aplicaveis += 1

        porcentagem_conformes = conformes * 100 / 9

        status_lv = ""

        if porcentagem_conformes < 100:
            status_lv = "Pendente"

        else:
            status_lv = "Concluído"

        lv = {}

        for i in range(1, 9):

            lv = {
                "nome_lv": interface.get_screen(
                    "checklistName"
                ).ids.name_text_field_lv.text,
                "descricao_lv": interface.get_screen(
                    "checklistName"
                ).ids.descricao_text_field_lv.text,
                "nome_usuario": nome,
                "email_usuario": email,
                "Data_emissao": today.replace("-", "/"),
                "porcentagem_c": round(porcentagem_conformes, 2),
                "quantidade_nc": nao_conformes,
                "quantidade_na": nao_aplicaveis,
                "lv_status": status_lv,
                "item1_nome": "Os locais adjacentes das caixas estão limpos e organizados?",
                "item1_resultado": results[i - 1],
                "item1_acao": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text,
                "item1_prazo": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text,
                "item1_responsavel": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text,
                "item2_nome": "As caixas estão com acúmulo excessivo de gordura?",
                "item2_resultado": results[i - 1],
                "item2_acao": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text,
                "item2_prazo": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text,
                "item2_responsavel": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text,
                "item3_nome": "As caixas de gordura estão obstruídas?",
                "item3_resultado": results[i - 1],
                "item3_acao": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text,
                "item3_prazo": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text,
                "item3_responsavel": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text,
                "item4_nome": "Há evidências de transbordo?",
                "item4_resultado": results[i - 1],
                "item4_acao": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text,
                "item4_prazo": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text,
                "item4_responsavel": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text,
                "item5_nome": "Há evidência de odores?",
                "item5_resultado": results[i - 1],
                "item5_acao": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text,
                "item5_prazo": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text,
                "item5_responsavel": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text,
                "item6_nome": "Há detritos de alimentos, sobras de embalagens, entre outros?",
                "item6_resultado": results[i - 1],
                "item6_acao": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text,
                "item6_prazo": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text,
                "item6_responsavel": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text,
                "item7_nome": "Há telas (grade) de retenção nas áreas internas do refeitório cin objetivo de reter sobras de alimentos?",
                "item7_resultado": results[i - 1],
                "item7_acao": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text,
                "item7_prazo": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text,
                "item7_responsavel": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text,
                "item8_nome": "As tampas das caixas estão encaixadas de acordo com a construção?",
                "item8_resultado": results[i - 1],
                "item8_acao": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text,
                "item8_prazo": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text,
                "item8_responsavel": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text,
                "item9_nome": "O efluente está sendo direcionado para a Estação de tratamento de Efluente - ETE?",
                "item9_resultado": results[i - 1],
                "item9_acao": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text,
                "item9_prazo": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text,
                "item9_responsavel": interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text,
            }

        col_lv.insert_one(lv)

    ##################CONFIRMAÇAO DE SAIDA APP################
    dialog = None

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Você deseja mesmo sair ?",
                buttons=[
                    MDFlatButton(
                        text="Sim",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_username_dialogue,
                    ),
                    MDFlatButton(
                        text="Não",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_username_dialogue_app,
                    ),
                ],
            )
        self.dialog.open()

    def show_alert_checklist_exit_operation(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Você deseja mesmo cancelar a verificação ?",
                buttons=[
                    MDFlatButton(
                        text="Sim",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_username_dialogue1,
                    ),
                    MDFlatButton(
                        text="Não",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_username_dialogue,
                    ),
                ],
            )
        self.dialog.open()

        ####################TELE DE REALMENTE QUER CONFIRMAR EXCLUIR CHECKLIST######################

    def show_alert__delete_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Você deseja mesmo excluir ?",
                buttons=[
                    MDFlatButton(
                        text="Sim",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_username_dialogue_excluir,
                    ),
                    MDFlatButton(
                        text="Não",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_username_dialogue,
                    ),
                ],
            )
        self.dialog.open()
        #################BLOCO DE AVISO NOME INVALIDO FECHANDO##################

    def close_username_dialogue1(self, obj):
        self.change_screen_to_checklists()
        self.dialog.dismiss()

    def close_username_dialogue(self, obj):
        self.change_screen_to_checklistname()
        self.dialog.dismiss()

    #############FUNCAO PARA BLOCO DE AVISO PARA SAIR DO APP################
    def close_username_dialogue_app(self, obj):
        quit()

    #####################BLOCO DE AVISO ECLUIR CHECKLIST FECHANDO##############
    def close_username_dialogue_excluir(self, obj):
        self.dialog.dismiss()
        self.remove_checklist()
        self.change_screen_to_checklists()

    #################REMOVE WIDGET CHECKLIST##################
    def remove_checklist(self):
        try:
            myclient = pymongo.MongoClient(
                "mongodb+srv://julio:senha@cluster0.pn3vb.mongodb.net/kivyapp?retryWrites=true&w=majority"
            )
            db = myclient["kivyapp"]
            col_lv = db["lvs"]

            col_lv = col_lv.delete_one({"_id": ObjectId("id do bagulho")})
        except Exception as erro:
            print(erro)

    ############MUDANDO A TELA PARA CHECKLIST INFORMAÇOES##########
    def change_screen(self, ThreeLineIconListItem):
        interface.get_screen("screen3").manager.current = "screen3"

    ###############MUDANDO A TELA PARA O MENU DAS CHECKLISTS###########
    def change_screen_to_checklists(self):
        interface.get_screen("screen1").manager.current = "screen1"

    def change_screen_to_checklistname(self):
        interface.get_screen("checklistName").manager.current = "checklistName"

    ####################MUDANDO A TELA PARA A TELA INICIAR UM NOVA VERIFICAÇAO#############
    def start_checklist(self):
        interface.get_screen("checklistName").manager.current = "checklistName"

    ##################FUNCAO PARA JANELHINHA DE DATA#########################
    def get_date(self, date):
        """
        :type date: <class 'datetime.date'>
        """

    ##################FUNCAO PARA JANELHINHA DE DATA#########################
    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()

    #########FUNCAO RECARREGAR OS DELETALHES DO PEFIL APOS MUDANÇA##############

    #########PREENCHIMENTOD DO NOME NA TELA DE LOGIN OBRIGATORIO FUNCAO############
    def check_username(self):
        self.username_text = interface.get_screen(
            "usernamescreen"
        ).ids.username_text_fied.text
        username_check_false = True
        try:
            int(self.username_text)
        except:
            username_check_false = False
        if username_check_false or self.username_text.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(
                text="OK", on_release=self.close_username_dialogue
            )
            self.dialog = MDDialog(
                title="Nome inválido",
                text="Por favor preencha um nome válido",
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue],
            )
            self.dialog.open()
        else:
            interface.get_screen("usernamescreen").ids.disabled_button.disabled = False

    ####################PREENCHIMENTO DO EMAIL TELA DE LOGIN OBRIGATORIO###################
    def get_email(self):
        self.email_text = interface.get_screen("dob").ids.email_text_fied.text
        username_check_false = True
        try:
            int(self.username_text)
        except:
            username_check_false = False
        if username_check_false or self.email_text.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(
                text="OK", on_release=self.close_username_dialogue
            )
            self.dialog = MDDialog(
                title="Email inválido",
                text="Por favor preencha um email válido",
                size_hint=(0.7, 0.2),
                buttons=[cancel_btn_username_dialogue],
            )
            self.dialog.open()
        else:
            name = interface.get_screen("usernamescreen").ids.username_text_fied.text
            email = interface.get_screen("dob").ids.email_text_fied.text
            self.store.put("UserInfo", name=name, email=email)
            interface.get_screen("dob").ids.disabled_button2.disabled = False
            self.set_refresh()
            self.update()

    ####################FUNCAO DE BLOQUEI DOS BOTAO CASO NAO SEJA SELECIONADO AS OPCOES DA VERIFICAÇAO############
    def enable_items_inputs(self):

        for i in range(1, 9):

            ##Item 1
            if (
                interface.get_screen(f"checklistItem{i}").ids.radio_item_nc.active
                == True
            ):
                interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.disabled = False
                interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.disabled = False
                interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.disabled = False

            else:
                interface.get_screen(f"checklistItem{i}").ids.acao_item.disabled = True
                interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.disabled = True
                interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.disabled = True

    def disable_nextButton(self):
        for i in range(1, 9):
            interface.get_screen(f"checklistItem{i}").ids.next_button.disabled = True

    ####################FUNCAO PARA LIBERAR OS BOTAO CASO SEJA SELECIONADO AS OPCOES DA VERIFICAÇAO############

    def check_lv_items(self):

        for i in range(1, 9):
            if (
                interface.get_screen(f"checklistItem{i}").ids.radio_item_nc.active
                == True
                and interface.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text.split()
                != []
                and interface.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text.split()
                != []
                and interface.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text.split()
                != []
                or interface.get_screen(f"checklistItem{i}").ids.radio_item_c.active
                == True
                or interface.get_screen(f"checklistItem{i}").ids.radio_item_na.active
                == True
            ):

                interface.get_screen(
                    f"checklistItem{i}"
                ).ids.next_button.disabled = False

    ###################BLOQUEIO DOS BOTAO PARA EDITAR CHCKLIST#########################
    def enable_checklist_inputs(self):
        if interface.get_screen("screen3").ids.profile_name_input.disabled == True:

            interface.get_screen("screen3").ids.profile_name_input.disabled = False

            interface.get_screen("screen3").ids.profile_data_input.disabled = False

            interface.get_screen(
                "screen3"
            ).ids.profile_responsavel_input.disabled = False

            interface.get_screen("screen3").ids.profile_acao_input.disabled = False

            interface.get_screen(
                "screen3"
            ).ids.profile_responsavel_realizar_input.disabled = False

            interface.get_screen("screen3").ids.profile_prazo_input.disabled = False

            interface.get_screen("screen3").ids.profile_status_input.disabled = False

            interface.get_screen("screen3").ids.save_checklist_button.disabled = False

            interface.get_screen(
                "screen3"
            ).ids.delete_checklist_button.disabled = False

        else:
            interface.get_screen("screen3").ids.profile_name_input.disabled = True

            interface.get_screen("screen3").ids.profile_data_input.disabled = True

            interface.get_screen(
                "screen3"
            ).ids.profile_responsavel_input.disabled = True

            interface.get_screen("screen3").ids.profile_acao_input.disabled = True

            interface.get_screen(
                "screen3"
            ).ids.profile_responsavel_realizar_input.disabled = True

            interface.get_screen("screen3").ids.profile_prazo_input.disabled = True

            interface.get_screen("screen3").ids.profile_status_input.disabled = True

            interface.get_screen("screen3").ids.save_checklist_button.disabled = True

            interface.get_screen("screen3").ids.delete_checklist_button.disabled = True

    #######################BLOQUEIO DOS BOTAO PARA EDITAR PERFIL################
    def enable_profile_inputs(self):

        if interface.get_screen("profile").ids.profile_email_input.disabled == True:

            interface.get_screen("profile").ids.profile_email_input.disabled = False

            interface.get_screen("profile").ids.profile_name_input.disabled = False

            interface.get_screen("profile").ids.save_profile_button.disabled = False
        else:
            interface.get_screen("profile").ids.profile_email_input.disabled = True

            interface.get_screen("profile").ids.profile_name_input.disabled = True

            interface.get_screen("profile").ids.save_profile_button.disabled = True

    def load_checklist(self):
        myclient = pymongo.MongoClient(
            "mongodb+srv://julio:senha@cluster0.pn3vb.mongodb.net/kivyapp?retryWrites=true&w=majority"
        )
        db = myclient["kivyapp"]
        col_lv = db["lvs"]

        for item in col_lv.find():

            self.checklist_table = ThreeLineIconListItem(
                text=item["nome_lv"],
                secondary_text=item["descricao_lv"],
                tertiary_text=item["Data_emissao"],
                on_press=partial(
                    self.checklist_screen,
                    id=str(item["_id"]),
                    nome_lv=item["nome_lv"],
                    descricao_lv=item["descricao_lv"],
                    data_emissao=item["Data_emissao"],
                    porcentagem_c=item["porcentagem_c"],
                    quantidade_nc=item["quantidade_nc"],
                    quantidade_na=item["quantidade_na"],
                    lv_status=item["lv_status"],
                    item1_nome=item["item1_nome"],
                    item1_resultado=item["item1_resultado"],
                    item1_acao=item["item1_acao"],
                    item1_prazo=item["item1_prazo"],
                    item1_responsavel=item["item1_responsavel"],
                    item2_nome=item["item2_nome"],
                    item2_resultado=item["item2_resultado"],
                    item2_acao=item["item2_acao"],
                    item2_prazo=item["item2_prazo"],
                    item2_responsavel=item["item2_responsavel"],
                    item3_nome=item["item3_nome"],
                    item3_resultado=item["item4_resultado"],
                    item3_acao=item["item3_acao"],
                    item3_prazo=item["item3_prazo"],
                    item3_responsavel=item["item3_responsavel"],
                    item4_nome=item["item3_responsavel"],
                    item4_resultado=item["item4_resultado"],
                    item4_acao=item["item4_acao"],
                    item4_prazo=item["item4_prazo"],
                    item4_responsavel=item["item4_responsavel"],
                    item5_nome=item["item5_nome"],
                    item5_resultado=item["item5_resultado"],
                    item5_acao=item["item5_acao"],
                    item5_prazo=item["item5_prazo"],
                    item5_responsavel=item["item5_responsavel"],
                    item6_nome=item["item6_nome"],
                    item6_resultado=item["item6_resultado"],
                    item6_acao=item["item6_acao"],
                    item6_prazo=item["item6_prazo"],
                    item6_responsavel=item["item6_responsavel"],
                    item7_nome=item["item7_nome"],
                    item7_resultado=item["item7_resultado"],
                    item7_acao=item["item7_acao"],
                    item7_prazo=item["item7_prazo"],
                    item7_responsavel=item["item7_responsavel"],
                    item8_nome=item["item8_nome"],
                    item8_resultado=item["item8_resultado"],
                    item8_acao=item["item8_acao"],
                    item8_prazo=item["item8_prazo"],
                    item8_responsavel=item["item8_responsavel"],
                    item9_nome=item["item9_nome"],
                    item9_resultado=item["item9_resultado"],
                    item9_acao=item["item9_acao"],
                    item9_prazo=item["item9_prazo"],
                    item9_responsavel=item["item9_responsavel"],
                ),
            )

            interface.get_screen("screen1").ids.checklist.add_widget(
                self.checklist_table
            )

    def checklist_screen(
        self,
        event,
        id,
        nome_lv,
        descricao_lv,
        data_emissao,
        porcentagem_c,
        quantidade_nc,
        quantidade_na,
        lv_status,
        item1_nome,
        item1_resultado,
        item1_acao,
        item1_prazo,
        item1_responsavel,
        item2_nome,
        item2_resultado,
        item2_acao,
        item2_prazo,
        item2_responsavel,
        item3_nome,
        item3_resultado,
        item3_acao,
        item3_prazo,
        item3_responsavel,
        item4_nome,
        item4_resultado,
        item4_acao,
        item4_prazo,
        item4_responsavel,
        item5_nome,
        item5_resultado,
        item5_acao,
        item5_prazo,
        item5_responsavel,
        item6_nome,
        item6_resultado,
        item6_acao,
        item6_prazo,
        item6_responsavel,
        item7_nome,
        item7_resultado,
        item7_acao,
        item7_prazo,
        item7_responsavel,
        item8_nome,
        item8_resultado,
        item8_acao,
        item8_prazo,
        item8_responsavel,
        item9_nome,
        item9_resultado,
        item9_acao,
        item9_prazo,
        item9_responsavel,
    ):

        interface.get_screen("screen3").manager.current = "screen3"
        interface.get_screen("screen3").ids.screen3_toolbar.title = nome_lv

        items = {
            "item1_nome": item1_nome,
            "item1_resultado": item1_resultado,
            "item1_acao": item1_acao,
            "item1_prazo": item1_prazo,
            "item1_responsavel": item1_responsavel,
            "item2_nome": item2_nome,
            "item2_resultado": item2_resultado,
            "item2_acao": item2_acao,
            "item2_prazo": item2_prazo,
            "item2_responsavel": item2_responsavel,
            "item3_nome": item3_nome,
            "item3_resultado": item3_resultado,
            "item3_acao": item3_acao,
            "item3_prazo": item3_prazo,
            "item3_responsavel": item3_responsavel,
            "item4_nome": item4_nome,
            "item4_resultado": item4_resultado,
            "item4_acao": item4_acao,
            "item4_prazo": item4_prazo,
            "item4_responsavel": item4_responsavel,
            "item5_nome": item5_nome,
            "item5_resultado": item5_resultado,
            "item5_acao": item5_acao,
            "item5_prazo": item5_prazo,
            "item5_responsavel": item5_responsavel,
            "item6_nome": item6_nome,
            "item6_resultado": item6_resultado,
            "item6_acao": item6_acao,
            "item6_prazo": item6_prazo,
            "item6_responsavel": item6_responsavel,
            "item7_nome": item7_nome,
            "item7_resultado": item7_resultado,
            "item7_acao": item7_acao,
            "item7_prazo": item7_prazo,
            "item7_responsavel": item7_responsavel,
            "item8_nome": item8_nome,
            "item8_resultado": item8_resultado,
            "item8_acao": item8_acao,
            "item8_prazo": item8_prazo,
            "item8_responsavel": item8_responsavel,
            "item9_nome": item9_nome,
            "item9_resultado": item9_resultado,
            "item9_acao": item9_acao,
            "item9_prazo": item9_prazo,
            "item9_responsavel": item9_responsavel,
        }

        for i in range(1, 10):

            self.list_item = ThreeLineIconListItem(
                text=items[f"item{i}_nome"], secondary_text=items[f"item{i}_resultado"]
            )

            interface.get_screen("screen3").ids.box.add_widget(self.list_item)


if __name__ == "__main__":
    ChecklistApp().run()
