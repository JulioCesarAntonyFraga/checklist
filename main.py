import os
import re
from datetime import date
from functools import partial

from kivy.clock import Clock
import pymongo
from bson import ObjectId
from dotenv import load_dotenv
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.config import Config
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import (
    MDList,
    StringProperty,
    ThreeLineIconListItem,
    TwoLineAvatarIconListItem,
)
from kivymd.uix.picker import MDDatePicker
from kivymd.utils import asynckivy
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

import decorators



load_dotenv()

Config.set("input", "mouse", "mouse,disable_multitouch")


def sync_request(query, headers = None, **kwargs):
    transport = AIOHTTPTransport(url=os.getenv("BACKEND_ENDPOINT"), headers=headers)

    client = Client(transport=transport, fetch_schema_from_transport=True)

    result = client.execute(query, variable_values=kwargs)

    return result


async def async_request(query, headers = None, **kwargs):
    transport = AIOHTTPTransport(url=os.getenv("BACKEND_ENDPOINT"), headers=headers)

    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        result = await session.execute(query, variable_values=kwargs)

        return result


class Content(BoxLayout):
    pass


class CustomItem(TwoLineAvatarIconListItem):
    icon = StringProperty("")


class LoginScreen(Screen):
    def on_enter(self):
        self.storage = JsonStore("storage.json")

        if self.storage.exists("user"):
            user = self.storage.get("user")

            if user["remember"]:
                query = gql("""
                    mutation VerifyToken($token: String!) {
                        verifyToken(input: {
                                token: $token
                            }) {
                            payload
                        }
                    }
                """)

                result = sync_request(query, token=user["authToken"])

                if result["verifyToken"]["payload"] is not None:
                    Clock.schedule_once(self.to_screen1)

    def validate_inputs(self):
        valid_inputs = True

        email = self.ids.email_input.text
        password = self.ids.password_input.text

        email_regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

        if not email:
            self.ids.email_input.focus = True
            self.ids.email_input.helper_text = "Este campo é obrigatório"
            self.ids.email_input.error = True
            self.ids.email_input.focus = False

            valid_inputs = False

        elif not re.search(email_regex, email):
            self.ids.email_input.focus = True
            self.ids.email_input.helper_text = "Email inválido"
            self.ids.email_input.error = True
            self.ids.email_input.focus = False

            valid_inputs = False

        else:
            self.ids.email_input.focus = True
            self.ids.email_input.error = False
            self.ids.email_input.focus = False

        if not password:
            self.ids.password_input.focus = True
            self.ids.password_input.helper_text = "Este campo é obrigatório"
            self.ids.password_input.error = True
            self.ids.password_input.focus = False

            valid_inputs = False

        else:
            self.ids.password_input.focus = True
            self.ids.password_input.error = False
            self.ids.password_input.focus = False

        return valid_inputs

    def login(self):
        if self.validate_inputs():
            query = gql("""
                mutation Login($email: String!, $password: String!) {
                    tokenAuth(
                        input: {
                            email: $email,
                            password: $password
                        }
                    ) {
                        success,
                        errors,
                        token,
                        user {
                            id,
                            firstName,
                            lastName
                        }
                    }
                }
            """)

            email = self.ids.email_input.text

            result = sync_request(
                query, 
                email=email, 
                password=self.ids.password_input.text
            )

            user = result["tokenAuth"]["user"]
            user_name = f"{user['firstName']} {user['lastName']}"

            self.storage.put(
                "user", 
                id=user["id"], 
                name=user_name,
                email=email, 
                authToken=result["tokenAuth"]["token"],
                remember=self.ids.remember_input.active
            )

            self.manager.current = "screen1"

    def to_screen1(self, event):
        self.manager.current = "screen1"


class RegisterScreen(Screen):
    pass

class Screen1(Screen):
    @decorators.asynckivy_start
    async def load_checklists(self):
        query = gql("""
            query {
                allVerificationLists(completed: false) {
                    id,
                    name,
                    conclusionPercentage
                }
            }
        """)

        result = await async_request(query, {"Authentication": f"JWT {self.auth_token}"})

        for question in result["allVerificationLists"]:
            print(question)

        myclient = pymongo.MongoClient(
            "mongodb+srv://julio:senha@cluster0.pn3vb.mongodb.net/kivyapp?retryWrites=true&w=majority"
        )
        db = myclient["kivyapp"]
        col_lv = db["lvs"]

        for item in col_lv.find():

            checklist_table = ThreeLineIconListItem(
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

            self.manager.get_screen("screen1").ids.checklist.add_widget(checklist_table)

class Screen3(Screen):
    def remove_checklist(self, id):
        try:
            myclient = pymongo.MongoClient(
                "mongodb+srv://julio:senha@cluster0.pn3vb.mongodb.net/kivyapp?retryWrites=true&w=majority"
            )
            db = myclient["kivyapp"]
            col_lv = db["lvs"]

            col_lv = col_lv.delete_one({"_id": ObjectId("id do bagulho")})
        except Exception as erro:
            print(erro)

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

        self.manager.current = "screen3"
        self.manager.get_screen("screen3").ids.screen3_toolbar.title = nome_lv

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

            self.manager.get_screen("screen3").ids.box.add_widget(self.list_item)

        for i in range(1,10):
            self.list_item = MDExpansionPanel(
            content = Content(),
            on_open=self.panel_open,
            on_close=self.panel_close,
            icon=f"kivymd.png",
            panel_cls=MDExpansionPanelThreeLine(
                text=items[f'item{i}_nome'],
                secondary_text=items[f'item{i}_resultado'],
                tertiary_text=items[f'item{i}_prazo']
                )
            )

            self.manager.get_screen('screen3').ids.my_checklist.add_widget(self.list_item)

            if items[f'item{i}_resultado'] == 'Não conforme':
                self.list_item.content.ids.list.add_widget(MDTextField(text=items[f'item{i}_acao'],
                    size_hint= (0.98,0.1),
                    hint_text = 'Ação para uma não conformidade!',
                    icon_right= 'inbox',
                    ))
                self.list_item.content.ids.list.add_widget(MDTextField(text=items[f'item{i}_prazo'],
                    size_hint= (0.98,0.1),
                    hint_text = 'Prazo para uma não conformidade!',
                    icon_right= 'inbox',
                    ))
                self.list_item.content.ids.list.add_widget(MDTextField(text=items[f'item{i}_responsavel'],
                    size_hint= (0.98,0.1),
                    hint_text = 'Responsável para uma não conformidade!',
                    icon_right= 'inbox',
                    ))

    ###################BLOQUEIO DOS BOTAO PARA EDITAR CHCKLIST#########################
    def enable_checklist_inputs(self):
        if self.strng.get_screen("screen3").ids.profile_name_input.disabled == True:

            self.strng.get_screen("screen3").ids.profile_name_input.disabled = False

            self.strng.get_screen("screen3").ids.profile_data_input.disabled = False

            self.strng.get_screen(
                "screen3"
            ).ids.profile_responsavel_input.disabled = False

            self.strng.get_screen("screen3").ids.profile_acao_input.disabled = False

            self.strng.get_screen(
                "screen3"
            ).ids.profile_responsavel_realizar_input.disabled = False

            self.strng.get_screen("screen3").ids.profile_prazo_input.disabled = False

            self.strng.get_screen("screen3").ids.profile_status_input.disabled = False

            self.strng.get_screen("screen3").ids.save_checklist_button.disabled = False

            self.strng.get_screen(
                "screen3"
            ).ids.delete_checklist_button.disabled = False

        else:
            self.strng.get_screen("screen3").ids.profile_name_input.disabled = True

            self.strng.get_screen("screen3").ids.profile_data_input.disabled = True

            self.strng.get_screen(
                "screen3"
            ).ids.profile_responsavel_input.disabled = True

            self.strng.get_screen("screen3").ids.profile_acao_input.disabled = True

            self.strng.get_screen(
                "screen3"
            ).ids.profile_responsavel_realizar_input.disabled = True

            self.strng.get_screen("screen3").ids.profile_prazo_input.disabled = True

            self.strng.get_screen("screen3").ids.profile_status_input.disabled = True

            self.strng.get_screen("screen3").ids.save_checklist_button.disabled = True

            self.strng.get_screen("screen3").ids.delete_checklist_button.disabled = True

class Profile(Screen):
    def enable_profile_inputs(self):

        if self.manager.get_screen("profile").ids.profile_email_input.disabled == True:

            self.manager.get_screen("profile").ids.profile_email_input.disabled = False

            self.manager.get_screen("profile").ids.profile_name_input.disabled = False

            self.manager.get_screen("profile").ids.save_profile_button.disabled = False
        else:
            self.manager.get_screen("profile").ids.profile_email_input.disabled = True

            self.manager.get_screen("profile").ids.profile_name_input.disabled = True

            self.manager.get_screen("profile").ids.save_profile_button.disabled = True

    def update_profile(self):
        name = self.manager.get_screen("profile").ids.profile_name_input.text
        email = self.manager.get_screen("profile").ids.profile_email_input.text
        self.store.put("UserInfo", name=name, email=email)
        self.set_refresh()
        self.manager.get_screen('profile').ids.save_profile_button.disabled = True

class ChecklistName(Screen):
    def check_lv_name_and_description(self):
        print(self.manager.get_screen("checklistName").ids.name_text_field_lv.text)
        print(self.manager.get_screen("checklistName").ids.descricao_text_field_lv.text)
        if (
            self.manager.get_screen("checklistName").ids.name_text_field_lv.text != ""
            and self.manager.get_screen("checklistName").ids.descricao_text_field_lv.text
            != ""
        ):
            self.manager.get_screen("checklistName").ids.lv_name_button.disabled = False

        else:
            self.manager.get_screen("checklistName").ids.lv_name_button.disabled = True

############MAQUINARIO APP########################
class ChecklistApp(MDApp):
    panel_is_open = False

    try:
        name_perfil_toolbar = "Desconhecido"
        email_perfil_toolbar = "Desconhecido"
    except:
        pass

    teste = "teste"

    def build(self):
        self.strng = Builder.load_file("checklist.kv")
        return self.strng

    def panel_open(self, *args):
        self.panel_is_open = True

    def panel_close(self, *args):
        self.panel_is_open = False

    def delete_item(self, item):
        self.panel.content.remove_widget(item)
        self.panel.height -= item.height
        for index, val in enumerate(self.panel.content.children[::-1]):
            val.secondary_text = str(index + 1)

    @decorators.asynckivy_start
    async def update(self):
        await asynckivy.sleep(1)

        try:
            self.store = JsonStore("userProfile.json")
            nome = self.store.get("UserInfo")["name"]
            email = self.store.get("UserInfo")["email"]

            self.strng.get_screen("profile").ids.profile_name_input.text = nome
            self.strng.get_screen("profile").ids.profile_email_input.text = email

        except Exception:
            pass

    @decorators.asynckivy_start
    async def set_refresh(self):
        await asynckivy.sleep(1)

        try:
            self.store = JsonStore("userProfile.json")
            nome = self.store.get("UserInfo")["name"]
            email = self.store.get("UserInfo")["email"]

            await asynckivy.sleep(1)
            self.strng.get_screen("profile").ids.name_perfil_toolbar.text = nome
            self.strng.get_screen("profile").ids.email_perfil_toolbar.text = email

            self.strng.get_screen("screen1").ids.name_perfil_toolbar.text = nome
            self.strng.get_screen("screen1").ids.email_perfil_toolbar.text = email

            self.strng.get_screen("screen2").ids.name_perfil_toolbar.text = nome
            self.strng.get_screen("screen2").ids.email_perfil_toolbar.text = email

            self.strng.get_screen("screen3").ids.name_perfil_toolbar.text = nome
            self.strng.get_screen("screen3").ids.email_perfil_toolbar.text = email

            self.strng.get_screen("screen5").ids.name_perfil_toolbar.text = nome
            self.strng.get_screen("screen5").ids.email_perfil_toolbar.text = email

            self.strng.get_screen(
                "checklistName"
            ).ids.name_perfil_toolbar.text = nome
            self.strng.get_screen(
                "checklistName"
            ).ids.email_perfil_toolbar.text = email

            self.strng.get_screen("profile").ids.profile_name_input.text = nome
            self.strng.get_screen("profile").ids.profile_email_input.text = email
            self.s

        except Exception:
            pass
    
    #################FAZ OS INPUTS FICAREM EM BRANCO QUANDO C OU NA É ESCOLHIDO#################
    def clear_items_inputs(self):
        for i in range(1, 9):

            if (
                self.strng.get_screen(f"checklistItem{i}").ids.radio_item_c.active
                or self.strng.get_screen(f"checklistItem{i}").ids.radio_item_na.active
            ):

                self.strng.get_screen(f"checklistItem{i}").ids.acao_item.text = ""
                self.strng.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text = ""
                self.strng.get_screen(f"checklistItem{i}").ids.prazo_item.text = ""

    class ContentNavigationDrawer(BoxLayout):  #######PERFIL########
        pass

    class DrawerList(ThemableBehavior, MDList):  ######lISTAS DE AÇÕES DO PERFIL######
        pass


    @decorators.asyncio_run
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

        for i in range(1, 10):
            if (
                self.strng.get_screen(f"checklistItem{i}").ids.radio_item_c.active
                == True
            ):
                results.append("Conforme")
                conformes += 1

            if (
                self.strng.get_screen(f"checklistItem{i}").ids.radio_item_nc.active
                == True
            ):
                results.append("Não conforme")
                nao_conformes += 1

            if (
                self.strng.get_screen(f"checklistItem{i}").ids.radio_item_na.active
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

        for i in range(1,10):

            
            
            lv = {
                "nome_lv": self.strng.get_screen(
                    "checklistName"
                ).ids.name_text_field_lv.text,
                "descricao_lv": self.strng.get_screen(
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
                "item1_resultado": results[0],
                "item1_acao": self.strng.get_screen(
                    f"checklistItem{1}"
                ).ids.acao_item.text,
                "item1_prazo": self.strng.get_screen(
                    f"checklistItem{1}"
                ).ids.prazo_item.text,
                "item1_responsavel": self.strng.get_screen(
                    f"checklistItem{1}"
                ).ids.responsavel_item.text,
                "item2_nome": "As caixas estão com acúmulo excessivo de gordura?",
                "item2_resultado": results[1],
                "item2_acao": self.strng.get_screen(
                    f"checklistItem{2}"
                ).ids.acao_item.text,
                "item2_prazo": self.strng.get_screen(
                    f"checklistItem{2}"
                ).ids.prazo_item.text,
                "item2_responsavel": self.strng.get_screen(
                    f"checklistItem{2}"
                ).ids.responsavel_item.text,
                "item3_nome": "As caixas de gordura estão obstruídas?",
                "item3_resultado": results[2],
                "item3_acao": self.strng.get_screen(
                    f"checklistItem{3}"
                ).ids.acao_item.text,
                "item3_prazo": self.strng.get_screen(
                    f"checklistItem{3}"
                ).ids.prazo_item.text,
                "item3_responsavel": self.strng.get_screen(
                    f"checklistItem{3}"
                ).ids.responsavel_item.text,
                "item4_nome": "Há evidências de transbordo?",
                "item4_resultado": results[3],
                "item4_acao": self.strng.get_screen(
                    f"checklistItem{4}"
                ).ids.acao_item.text,
                "item4_prazo": self.strng.get_screen(
                    f"checklistItem{4}"
                ).ids.prazo_item.text,
                "item4_responsavel": self.strng.get_screen(
                    f"checklistItem{4}"
                ).ids.responsavel_item.text,
                "item5_nome": "Há evidência de odores?",
                "item5_resultado": results[4],
                "item5_acao": self.strng.get_screen(
                    f"checklistItem{5}"
                ).ids.acao_item.text,
                "item5_prazo": self.strng.get_screen(
                    f"checklistItem{5}"
                ).ids.prazo_item.text,
                "item5_responsavel": self.strng.get_screen(
                    f"checklistItem{5}"
                ).ids.responsavel_item.text,
                "item6_nome": "Há detritos de alimentos, sobras de embalagens, entre outros?",
                "item6_resultado": results[5],
                "item6_acao": self.strng.get_screen(
                    f"checklistItem{6}"
                ).ids.acao_item.text,
                "item6_prazo": self.strng.get_screen(
                    f"checklistItem{6}"
                ).ids.prazo_item.text,
                "item6_responsavel": self.strng.get_screen(
                    f"checklistItem{6}"
                ).ids.responsavel_item.text,
                "item7_nome": "Há telas (grade) de retenção nas áreas internas do refeitório cin objetivo de reter sobras de alimentos?",
                "item7_resultado": results[6],
                "item7_acao": self.strng.get_screen(
                    f"checklistItem{7}"
                ).ids.acao_item.text,
                "item7_prazo": self.strng.get_screen(
                    f"checklistItem{7}"
                ).ids.prazo_item.text,
                "item7_responsavel": self.strng.get_screen(
                    f"checklistItem{7}"
                ).ids.responsavel_item.text,
                "item8_nome": "As tampas das caixas estão encaixadas de acordo com a construção?",
                "item8_resultado": results[7],
                "item8_acao": self.strng.get_screen(
                    f"checklistItem{8}"
                ).ids.acao_item.text,
                "item8_prazo": self.strng.get_screen(
                    f"checklistItem{8}"
                ).ids.prazo_item.text,
                "item8_responsavel": self.strng.get_screen(
                    f"checklistItem{8}"
                ).ids.responsavel_item.text,
                "item9_nome": "O efluente está sendo direcionado para a Estação de tratamento de Efluente - ETE?",
                "item9_resultado": results[8],
                "item9_acao": self.strng.get_screen(
                    f"checklistItem{9}"
                ).ids.acao_item.text,
                "item9_prazo": self.strng.get_screen(
                    f"checklistItem{9}"
                ).ids.prazo_item.text,
                "item9_responsavel": self.strng.get_screen(
                    f"checklistItem{9}"
                ).ids.responsavel_item.text,
            }

        col_lv.insert_one(lv)
        self.load_checklist()
        self.strng.get_screen('screen1').manager.current = 'screen1'
        print(results)

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
        self.change_screen_to_checklists()

    ############MUDANDO A TELA PARA CHECKLIST INFORMAÇOES##########
    def change_screen(self, ThreeLineIconListItem):
        self.strng.current = "screen3"

    ###############MUDANDO A TELA PARA O MENU DAS CHECKLISTS###########
    def change_screen_to_checklists(self):
        self.strng.current = "screen1"

    def change_screen_to_checklistname(self):
        self.strng.current = "checklistName"

    ####################MUDANDO A TELA PARA A TELA INICIAR UM NOVA VERIFICAÇAO#############
    def start_checklist(self):
        self.strng.current = "checklistName"

    ####################FUNCAO DE BLOQUEI DOS BOTAO CASO NAO SEJA SELECIONADO AS OPCOES DA VERIFICAÇAO############
    def enable_items_inputs(self):

        for i in range(1, 10):

            if (
                self.strng.get_screen(f"checklistItem{i}").ids.radio_item_nc.active
                == True
            ):
                self.strng.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.disabled = False
                self.strng.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.disabled = False
                self.strng.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.disabled = False

            else:
                self.strng.get_screen(f"checklistItem{i}").ids.acao_item.disabled = True
                self.strng.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.disabled = True
                self.strng.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.disabled = True

    def disable_nextButton(self):
        for i in range(1, 10):
            self.strng.get_screen(f"checklistItem{i}").ids.next_button.disabled = True

    ####################FUNCAO PARA LIBERAR OS BOTÕES CASO SEJA SELECIONADO AS OPCOES DA VERIFICAÇAO############
    def check_lv_items(self):

        for i in range(1, 10):
            if (
                self.strng.get_screen(f"checklistItem{i}").ids.radio_item_nc.active
                == True
                and self.strng.get_screen(
                    f"checklistItem{i}"
                ).ids.acao_item.text.split()
                != []
                and self.strng.get_screen(
                    f"checklistItem{i}"
                ).ids.responsavel_item.text.split()
                != []
                and self.strng.get_screen(
                    f"checklistItem{i}"
                ).ids.prazo_item.text.split()
                != []
                or self.strng.get_screen(f"checklistItem{i}").ids.radio_item_c.active
                == True
                or self.strng.get_screen(f"checklistItem{i}").ids.radio_item_na.active
                == True
            ):

                self.strng.get_screen(
                    f"checklistItem{i}"
                ).ids.next_button.disabled = False



if __name__ == "__main__":
    ChecklistApp().run()
