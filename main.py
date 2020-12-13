import pymongo
from kivymd.uix.snackbar import Snackbar
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDFloatingActionButton, MDRectangleFlatIconButton, MDFloatingActionButton
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.picker import MDDatePicker
from datetime import date
from kivymd.utils import asynckivy
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import IRightBodyTouch
from kivymd.uix.list import StringProperty, TwoLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine, MDExpansionPanelOneLine
from kivymd import images_path
from kivy.uix.widget import Widget
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem, ThreeLineListItem, ThreeLineIconListItem, MDIconButton, ImageLeftWidget
from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from bson import ObjectId
from datetime import date
from kivy.animation import Animation
from functools import partial



class Content(BoxLayout):
    pass


##################TELAS APP####################
class WelcomeScreen(Screen):
    pass


class UsernameScreen(Screen):
    pass


class DOB(Screen):
    pass


class Profile(Screen):  #####PERFIL#####
    pass


class Screen1(Screen):  #####CHECKLISTS######
    pass


class Screen2(Screen):  #####MINHAS CHECKLISTS#####
    pass


class Screen3(Screen):  #####CHECKLIST SELECIONADA#####
    pass


class Screen5(Screen):
    pass


class CreateCheckList(ThreeLineIconListItem):
    pass


class ChecklistName(Screen):  #####NOME CHECKLIST#####
    pass


class ChecklistItem1(Screen):  #####ITEM 1 NOVA LV#####
    pass


class ChecklistItem2(Screen):  #####ITEM 1 NOVA LV#####
    pass


class ChecklistItem3(Screen):  #####ITEM 1 NOVA LV#####
    pass


class ChecklistItem4(Screen):  #####ITEM 1 NOVA LV#####
    pass


class ChecklistItem5(Screen):  #####ITEM 1 NOVA LV#####
    pass


class ChecklistItem6(Screen):  #####ITEM 1 NOVA LV#####
    pass


class ChecklistItem7(Screen):  #####ITEM 1 NOVA LV#####
    pass


class ChecklistItem8(Screen):  #####ITEM 1 NOVA LV#####
    pass


class ChecklistItem9(Screen):  #####ITEM 1 NOVA LV#####
    pass


class CustomItem(TwoLineAvatarIconListItem):
    icon = StringProperty('')


class ExpansionpanelContent(BoxLayout):
    pass

#######INTEGRANDO TELAS NO GERENCIADOR DE SCREEN########
sm = ScreenManager()
sm.add_widget(WelcomeScreen(name='welcomescreen'))
sm.add_widget(UsernameScreen(name='usernamescreen'))
sm.add_widget(DOB(name='dob'))
sm.add_widget(Profile(name='profile'))
sm.add_widget(Screen1(name='screen1'))
sm.add_widget(Screen2(name='screen2'))
sm.add_widget(Screen3(name='screen3'))
sm.add_widget(Screen5(name='screen5'))
sm.add_widget(ChecklistName(name='checklistName'))
sm.add_widget(ChecklistItem1(name='checklistItem1'))
sm.add_widget(ChecklistItem2(name='checklistItem2'))
sm.add_widget(ChecklistItem3(name='checklistItem3'))
sm.add_widget(ChecklistItem4(name='checklistItem4'))
sm.add_widget(ChecklistItem5(name='checklistItem5'))
sm.add_widget(ChecklistItem6(name='checklistItem6'))
sm.add_widget(ChecklistItem7(name='checklistItem7'))
sm.add_widget(ChecklistItem8(name='checklistItem8'))
sm.add_widget(ChecklistItem9(name='checklistItem9'))



############MAQUINARIO APP########################
class PawareApp(MDApp):
    panel_is_open = False

    try:
        name_perfil_toolbar = "Desconhecido"
        email_perfil_toolbar = "Desconhecido"
    except:
        pass

    
    teste = 'teste'

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
                nome = self.store.get('UserInfo')['name']
                email = self.store.get('UserInfo')['email']

                self.strng.get_screen('profile').ids.profile_name_input.text = nome
                self.strng.get_screen('profile').ids.profile_email_input.text = email

            except Exception as erro:
                print(erro)

        asynckivy.start(update())

    def set_refresh(self):
        async def set_refresh():
            await asynckivy.sleep(1)
            try:
                self.store = JsonStore("userProfile.json")
                nome = self.store.get('UserInfo')['name']
                email = self.store.get('UserInfo')['email']

                await asynckivy.sleep(1)
                self.strng.get_screen('profile').ids.name_perfil_toolbar.text = nome
                self.strng.get_screen('profile').ids.email_perfil_toolbar.text = email

                self.strng.get_screen('screen1').ids.name_perfil_toolbar.text = nome
                self.strng.get_screen('screen1').ids.email_perfil_toolbar.text = email

                self.strng.get_screen('screen2').ids.name_perfil_toolbar.text = nome
                self.strng.get_screen('screen2').ids.email_perfil_toolbar.text = email

                self.strng.get_screen('screen3').ids.name_perfil_toolbar.text = nome
                self.strng.get_screen('screen3').ids.email_perfil_toolbar.text = email

                self.strng.get_screen('screen5').ids.name_perfil_toolbar.text = nome
                self.strng.get_screen('screen5').ids.email_perfil_toolbar.text = email

                self.strng.get_screen('profile').ids.profile_name_input.text = nome
                self.strng.get_screen('profile').ids.profile_email_input.text = email

                self.load_checklist()

            except Exception as erro:
                print(erro)

        asynckivy.start(set_refresh())

    def update_profile(self):
        name = self.strng.get_screen('profile').ids.profile_name_input.text
        email = self.strng.get_screen('profile').ids.profile_email_input.text
        self.store.put('UserInfo', name=name, email=email)
        self.set_refresh()
        self.strng.get_screen('profile').ids.save_profile_button.disabled = True

    #######################CARREGAMENTO E CONTRUCAO AO INICIAR O APP##############

    def build(self):
        self.strng = Builder.load_file('conteudos.kv')
        return self.strng
        
    def chek_profile_inputs(self):
        name = self.strng.get_screen('profile').ids.profile_name_input.text
        email = self.strng.get_screen('profile').ids.profile_email_input.text

        if name != '' and email != '':
            self.strng.get_screen('profile').ids.save_profile_button.disabled = False

        else:
            self.strng.get_screen('profile').ids.save_profile_button.disabled = True

    #############FUNCAO AO INICIAR O APP ELE VAI CARREGAR ISSO ANTES DE MOSTRAR TELA#################
    def on_start(self):

        self.load_checklist()
        self.set_refresh()
        self.update()      
        self.store = JsonStore("userProfile.json")
        try:
            if self.store.get('UserInfo')['name'] != "":
                self.strng.get_screen('screen1').manager.current = 'screen1'
            else:
                self.strng.get_screen('welcomescreen').manager.current = 'welcomescreen'
        except:
            self.strng.get_screen('welcomescreen').manager.current = 'welcomescreen'

    def clear_items_inputs(self):

        for i in range(1,9):

            if self.strng.get_screen(f'checklistItem{i}').ids.radio_item_c.active or self.strng.get_screen(
                f'checklistItem{i}').ids.radio_item_na.active:

                self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text = ''
                self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text = ''
                self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text = ''

    class ContentNavigationDrawer(BoxLayout):  #######PERFIL########
        pass

    class DrawerList(ThemableBehavior, MDList):  ######lISTAS DE AÇÕES DO PERFIL######
        pass

    def check_lv_name_and_description(self):
        if self.strng.get_screen('checklistName').ids.name_text_field_lv.text != '' and self.strng.get_screen(
                'checklistName').ids.descricao_text_field_lv.text != '':
            self.strng.get_screen('checklistName').ids.lv_name_button.disabled = False

        else:
            self.strng.get_screen('checklistName').ids.lv_name_button.disabled = True

    def add_new_lv(self):
        conformes = 0
        nao_conformes = 0
        nao_aplicaveis = 0
        myclient = pymongo.MongoClient(
            "mongodb+srv://julio:senha@cluster0.pn3vb.mongodb.net/kivyapp?retryWrites=true&w=majority")
        db = myclient["kivyapp"]
        col_lv = db["lvs"]

        today = str(date.today())

        self.store = JsonStore("userProfile.json")
        nome = self.store.get('UserInfo')['name']
        email = self.store.get('UserInfo')['email']

        results = []

        for i in range(1,10):
            if self.strng.get_screen(f'checklistItem{i}').ids.radio_item_c.active == True:
                results.append('Conforme')
                conformes += 1



            if self.strng.get_screen(f'checklistItem{i}').ids.radio_item_nc.active == True:
                results.append('Não conforme')
                nao_conformes += 1


            if self.strng.get_screen(f'checklistItem{i}').ids.radio_item_na.active == True:
                results.append('Não aplicável')
                nao_aplicaveis += 1

        porcentagem_conformes = conformes * 100 / 9

        status_lv = ''

        if porcentagem_conformes < 100:
            status_lv = 'Pendente'

        else:
            status_lv = 'Concluído'

        lv={}

        for i in range(1,10):

            print(self.strng.get_screen(f'checklistItem{i}').ids.acao_item.text, self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.text, self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.text)
            
            lv = {
                "nome_lv": self.strng.get_screen('checklistName').ids.name_text_field_lv.text,
                "descricao_lv": self.strng.get_screen('checklistName').ids.descricao_text_field_lv.text,
                "nome_usuario": nome,
                "email_usuario": email,
                "Data_emissao": today.replace('-', '/'),
                "porcentagem_c": round(porcentagem_conformes, 2),
                "quantidade_nc": nao_conformes,
                "quantidade_na": nao_aplicaveis,
                "lv_status": status_lv,

                "item1_nome": "Os locais adjacentes das caixas estão limpos e organizados?",
                "item1_resultado": results[0],
                "item1_acao": str(self.strng.get_screen(f'checklistItem{1}').ids.acao_item.text),
                "item1_prazo": str(self.strng.get_screen(f'checklistItem{1}').ids.prazo_item.text),
                "item1_responsavel": str(self.strng.get_screen(f'checklistItem{1}').ids.responsavel_item.text),

                "item2_nome": "As caixas estão com acúmulo excessivo de gordura?",
                "item2_resultado": results[1],
                "item2_acao": str(self.strng.get_screen(f'checklistItem{2}').ids.acao_item.text),
                "item2_prazo": str(self.strng.get_screen(f'checklistItem{2}').ids.prazo_item.text),
                "item2_responsavel": str(self.strng.get_screen(f'checklistItem{2}').ids.responsavel_item.text),

                "item3_nome": "As caixas de gordura estão obstruídas?",
                "item3_resultado": results[2],
                "item3_acao": str(self.strng.get_screen(f'checklistItem{3}').ids.acao_item.text),
                "item3_prazo": str(self.strng.get_screen(f'checklistItem{3}').ids.prazo_item.text),
                "item3_responsavel": str(self.strng.get_screen(f'checklistItem{3}').ids.responsavel_item.text),

                "item4_nome": "Há evidências de transbordo?",
                "item4_resultado": results[3],
                "item4_acao": str(self.strng.get_screen(f'checklistItem{4}').ids.acao_item.text),
                "item4_prazo": str(self.strng.get_screen(f'checklistItem{4}').ids.prazo_item.text),
                "item4_responsavel": str(self.strng.get_screen(f'checklistItem{4}').ids.responsavel_item.text),

                "item5_nome": "Há evidência de odores?",
                "item5_resultado": results[4],
                "item5_acao": str(self.strng.get_screen(f'checklistItem{5}').ids.acao_item.text),
                "item5_prazo": str(self.strng.get_screen(f'checklistItem{5}').ids.prazo_item.text),
                "item5_responsavel": str(self.strng.get_screen(f'checklistItem{5}').ids.responsavel_item.text),

                "item6_nome": "Há detritos de alimentos, sobras de embalagens, entre outros?",
                "item6_resultado": results[5],
                "item6_acao": str(self.strng.get_screen(f'checklistItem{6}').ids.acao_item.text),
                "item6_prazo": str(self.strng.get_screen(f'checklistItem{6}').ids.prazo_item.text),
                "item6_responsavel": str(self.strng.get_screen(f'checklistItem{6}').ids.responsavel_item.text),

                "item7_nome": "Há telas (grade) de retenção nas áreas internas do refeitório cin objetivo de reter sobras de alimentos?",
                "item7_resultado": results[6],
                "item7_acao": str(self.strng.get_screen(f'checklistItem{7}').ids.acao_item.text),
                "item7_prazo": str(self.strng.get_screen(f'checklistItem{7}').ids.prazo_item.text),
                "item7_responsavel": str(self.strng.get_screen(f'checklistItem{7}').ids.responsavel_item.text),

                "item8_nome": "As tampas das caixas estão encaixadas de acordo com a construção?",
                "item8_resultado": results[7],
                "item8_acao": str(self.strng.get_screen(f'checklistItem{8}').ids.acao_item.text),
                "item8_prazo": str(self.strng.get_screen(f'checklistItem{8}').ids.prazo_item.text),
                "item8_responsavel": str(self.strng.get_screen(f'checklistItem{9}').ids.responsavel_item.text),

                "item9_nome": "O efluente está sendo direcionado para a Estação de tratamento de Efluente - ETE?",
                "item9_resultado": results[8],
                "item9_acao": str(self.strng.get_screen(f'checklistItem{9}').ids.acao_item.text),
                "item9_prazo": str(self.strng.get_screen(f'checklistItem{9}').ids.prazo_item.text),
                "item9_responsavel": str(self.strng.get_screen(f'checklistItem{9}').ids.responsavel_item.text),

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
                        text="Sim", text_color=self.theme_cls.primary_color, on_release=self.close_username_dialogue
                    ),
                    MDFlatButton(
                        text="Não", text_color=self.theme_cls.primary_color, on_release=self.close_username_dialogue_app
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
                        text="Sim", text_color=self.theme_cls.primary_color, on_release=self.close_username_dialogue1
                    ),
                    MDFlatButton(
                        text="Não", text_color=self.theme_cls.primary_color, on_release=self.close_username_dialogue
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
                        text="Sim", text_color=self.theme_cls.primary_color,
                        on_release=self.close_username_dialogue_excluir
                    ),
                    MDFlatButton(
                        text="Não", text_color=self.theme_cls.primary_color, on_release=self.close_username_dialogue
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

    #################REMOVE WIDGET CHECKLIST##################
    def remove_checklist(self, id):
        try:
            myclient = pymongo.MongoClient(
                "mongodb+srv://julio:senha@cluster0.pn3vb.mongodb.net/kivyapp?retryWrites=true&w=majority")
            db = myclient["kivyapp"]
            col_lv = db["lvs"]

            col_lv = col_lv.delete_one(
                {
                    "_id": ObjectId(id)
                }
            )

            self.load_checklist()
            self.strng.get_screen('screen1').manager.current = 'screen1'

        except Exception as erro:
            print(erro)

    ############MUDANDO A TELA PARA CHECKLIST INFORMAÇOES##########
    def change_screen(self, ThreeLineIconListItem):
        self.strng.get_screen('screen3').manager.current = 'screen3'

    ###############MUDANDO A TELA PARA O MENU DAS CHECKLISTS###########
    def change_screen_to_checklists(self):
        self.strng.get_screen('screen1').manager.current = 'screen1'

    def change_screen_to_checklistname(self):
        self.strng.get_screen('checklistName').manager.current = 'checklistName'

    ####################MUDANDO A TELA PARA A TELA INICIAR UM NOVA VERIFICAÇAO#############
    def start_checklist(self):
        self.strng.get_screen('checklistName').manager.current = 'checklistName'

    ##################FUNCAO PARA JANELHINHA DE DATA#########################
    def get_date(self, date):
        '''
        :type date: <class 'datetime.date'>
        '''

    ##################FUNCAO PARA JANELHINHA DE DATA#########################
    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()

    #########FUNCAO RECARREGAR OS DELETALHES DO PEFIL APOS MUDANÇA##############

    #########PREENCHIMENTOD DO NOME NA TELA DE LOGIN OBRIGATORIO FUNCAO############
    def check_username(self):
        self.username_text = self.strng.get_screen('usernamescreen').ids.username_text_fied.text
        username_check_false = True
        try:
            int(self.username_text)
        except:
            username_check_false = False
        if username_check_false or self.username_text.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='OK', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(title='Nome inválido', text="Por favor preencha um nome válido",
                                   size_hint=(0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            self.strng.get_screen('usernamescreen').ids.disabled_button.disabled = False

    ####################PREENCHIMENTO DO EMAIL TELA DE LOGIN OBRIGATORIO###################
    def get_email(self):
        self.email_text = self.strng.get_screen('dob').ids.email_text_fied.text
        username_check_false = True
        try:
            int(self.username_text)
        except:
            username_check_false = False
        if username_check_false or self.email_text.split() == []:
            cancel_btn_username_dialogue = MDFlatButton(text='OK', on_release=self.close_username_dialogue)
            self.dialog = MDDialog(title='Email inválido', text="Por favor preencha um email válido",
                                   size_hint=(0.7, 0.2), buttons=[cancel_btn_username_dialogue])
            self.dialog.open()
        else:
            name = self.strng.get_screen('usernamescreen').ids.username_text_fied.text
            email = self.strng.get_screen('dob').ids.email_text_fied.text
            self.store.put('UserInfo', name=name, email=email)
            self.strng.get_screen('dob').ids.disabled_button2.disabled = False
            self.set_refresh()
            self.update()

    ####################FUNCAO DE BLOQUEI DOS BOTAO CASO NAO SEJA SELECIONADO AS OPCOES DA VERIFICAÇAO############
    def enable_items_inputs(self):
        
        for i in range(1,10):

            ##Item 1
            if self.strng.get_screen(f'checklistItem{i}').ids.radio_item_nc.active == True:
                self.strng.get_screen(f'checklistItem{i}').ids.acao_item.disabled = False
                self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.disabled = False
                self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.disabled = False

            else:
                self.strng.get_screen(f'checklistItem{i}').ids.acao_item.disabled = True
                self.strng.get_screen(f'checklistItem{i}').ids.responsavel_item.disabled = True
                self.strng.get_screen(f'checklistItem{i}').ids.prazo_item.disabled = True


    def disable_nextButton(self):
        for i in range(1,10):
            self.strng.get_screen(f'checklistItem{i}').ids.next_button.disabled = True


    ####################FUNCAO PARA LIBERAR OS BOTAO CASO SEJA SELECIONADO AS OPCOES DA VERIFICAÇAO############

    def check_lv_items(self):

        for i in range(1,10):
            if self.strng.get_screen(f'checklistItem{i}').ids.radio_item_nc.active == True and self.strng.get_screen(
                    f'checklistItem{i}').ids.acao_item.text.split() != [] and self.strng.get_screen(
                f'checklistItem{i}').ids.responsavel_item.text.split() != [] and self.strng.get_screen(
                f'checklistItem{i}').ids.prazo_item.text.split() != [] or self.strng.get_screen(
                f'checklistItem{i}').ids.radio_item_c.active == True or self.strng.get_screen(
                f'checklistItem{i}').ids.radio_item_na.active == True:

                self.strng.get_screen(f'checklistItem{i}').ids.next_button.disabled = False


    ###################BLOQUEIO DOS BOTAO PARA EDITAR CHCKLIST#########################
    def enable_checklist_inputs(self):
        if self.strng.get_screen('screen3').ids.profile_name_input.disabled == True:

            self.strng.get_screen('screen3').ids.profile_name_input.disabled = False

            self.strng.get_screen('screen3').ids.profile_data_input.disabled = False

            self.strng.get_screen('screen3').ids.profile_responsavel_input.disabled = False

            self.strng.get_screen('screen3').ids.profile_acao_input.disabled = False

            self.strng.get_screen('screen3').ids.profile_responsavel_realizar_input.disabled = False

            self.strng.get_screen('screen3').ids.profile_prazo_input.disabled = False

            self.strng.get_screen('screen3').ids.profile_status_input.disabled = False

            self.strng.get_screen('screen3').ids.save_checklist_button.disabled = False

            self.strng.get_screen('screen3').ids.delete_checklist_button.disabled = False

        else:
            self.strng.get_screen('screen3').ids.profile_name_input.disabled = True

            self.strng.get_screen('screen3').ids.profile_data_input.disabled = True

            self.strng.get_screen('screen3').ids.profile_responsavel_input.disabled = True

            self.strng.get_screen('screen3').ids.profile_acao_input.disabled = True

            self.strng.get_screen('screen3').ids.profile_responsavel_realizar_input.disabled = True

            self.strng.get_screen('screen3').ids.profile_prazo_input.disabled = True

            self.strng.get_screen('screen3').ids.profile_status_input.disabled = True

            self.strng.get_screen('screen3').ids.save_checklist_button.disabled = True

            self.strng.get_screen('screen3').ids.delete_checklist_button.disabled = True

    #######################BLOQUEIO DOS BOTAO PARA EDITAR PERFIL################
    def enable_profile_inputs(self):

        if self.strng.get_screen('profile').ids.profile_email_input.disabled == True:

            self.strng.get_screen('profile').ids.profile_email_input.disabled = False

            self.strng.get_screen('profile').ids.profile_name_input.disabled = False

        else:
            self.strng.get_screen('profile').ids.profile_email_input.disabled = True

            self.strng.get_screen('profile').ids.profile_name_input.disabled = True


    def load_checklist(self):
        self.strng.get_screen('screen1').ids.checklist.clear_widgets()
        myclient = pymongo.MongoClient("mongodb+srv://julio:senha@cluster0.pn3vb.mongodb.net/kivyapp?retryWrites=true&w=majority")
        db = myclient["kivyapp"]
        col_lv = db["lvs"]

        for item in col_lv.find():

            self.checklist_table = ThreeLineIconListItem(
                          text=item['nome_lv'],
                          secondary_text=item['descricao_lv'],
                          tertiary_text=item['Data_emissao'],
                          on_press=partial(self.checklist_screen, id = str(item['_id']), nome_lv = item['nome_lv'], descricao_lv = item['descricao_lv'], data_emissao = item['Data_emissao'], porcentagem_c = item['porcentagem_c'], quantidade_nc = item['quantidade_nc'], quantidade_na = item['quantidade_na'], lv_status = item['lv_status'], item1_nome = item['item1_nome'], item1_resultado = item['item1_resultado'], item1_acao = item['item1_acao'], item1_prazo = item['item1_prazo'], item1_responsavel = item['item1_responsavel'], item2_nome = item['item2_nome'], item2_resultado = item['item2_resultado'], item2_acao = item['item2_acao'], item2_prazo = item['item2_prazo'], item2_responsavel = item['item2_responsavel'], item3_nome = item['item3_nome'], item3_resultado = item['item4_resultado'], item3_acao = item['item3_acao'], item3_prazo = item['item3_prazo'], item3_responsavel = item['item3_responsavel'], item4_nome = item['item3_nome'], item4_resultado = item['item4_resultado'], item4_acao = item['item4_acao'], item4_prazo = item['item4_prazo'], item4_responsavel = item['item4_responsavel'], item5_nome = item['item5_nome'], item5_resultado = item['item5_resultado'], item5_acao = item['item5_acao'], item5_prazo = item['item5_prazo'], item5_responsavel = item['item5_responsavel'], item6_nome = item['item6_nome'], item6_resultado = item['item6_resultado'], item6_acao = item['item6_acao'], item6_prazo = item['item6_prazo'], item6_responsavel = item['item6_responsavel'], item7_nome = item['item7_nome'], item7_resultado = item['item7_resultado'], item7_acao = item['item7_acao'], item7_prazo = item['item7_prazo'], item7_responsavel = item['item7_responsavel'], item8_nome = item['item8_nome'], item8_resultado = item['item8_resultado'], item8_acao = item['item8_acao'], item8_prazo = item['item8_prazo'], item8_responsavel = item['item8_responsavel'], item9_nome = item['item9_nome'], item9_resultado = item['item9_resultado'], item9_acao = item['item9_acao'], item9_prazo = item['item9_prazo'], item9_responsavel = item['item9_responsavel'])
            )

            self.checklist_table

            self.strng.get_screen('screen1').ids.checklist.add_widget(self.checklist_table)

    def checklist_screen(self, event, id, nome_lv, descricao_lv, data_emissao, porcentagem_c, quantidade_nc, quantidade_na, lv_status, item1_nome, item1_resultado, item1_acao, item1_prazo, item1_responsavel, item2_nome, item2_resultado, item2_acao, item2_prazo, item2_responsavel, item3_nome, item3_resultado, item3_acao, item3_prazo, item3_responsavel, item4_nome, item4_resultado, item4_acao, item4_prazo, item4_responsavel, item5_nome, item5_resultado, item5_acao, item5_prazo, item5_responsavel, item6_nome, item6_resultado, item6_acao, item6_prazo, item6_responsavel, item7_nome, item7_resultado, item7_acao, item7_prazo, item7_responsavel, item8_nome, item8_resultado, item8_acao, item8_prazo, item8_responsavel, item9_nome, item9_resultado, item9_acao, item9_prazo, item9_responsavel):

        self.strng.get_screen('screen3').manager.current = 'screen3'
        self.strng.get_screen('screen3').ids.screen3_toolbar.title = nome_lv

        self.strng.get_screen('screen3').ids.my_checklist.clear_widgets()
        
        self.btn = MDFloatingActionButton(icon='trash-can-outline', pos_hint={"center_x": .9, "center_y": 0.1}, on_press=lambda x: self.remove_checklist(id))
        self.strng.get_screen('screen3').add_widget(self.btn)


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

        self.edit_lv = MDTextField(text=str(porcentagem_c),
            size_hint= (0.98,0.1),
            hint_text = 'Ação para uma não conformidade!',
            icon_right= 'inbox',
            helper_text= 'Ação para uma não conformidade!',
            helper_text_mode= 'on_error'
            
            )

        self.status_lv =MDTextField(text=lv_status,
            size_hint= (0.98,0.1),
            hint_text = 'Status da LV',
            icon_right= 'inbox',
            helper_text= 'Status da LV',
            helper_text_mode= 'on_error'
            )
        self.data_lv =MDTextField(text=data_emissao,
            size_hint= (0.98,0.1),
            hint_text = 'Ação para uma não conformidade!',
            icon_right= 'inbox',
            helper_text= 'Ação para uma não conformidade!',
            helper_text_mode= 'on_error'
            )

        self.strng.get_screen('screen3').ids.my_checklist.add_widget(self.edit_lv)
        self.strng.get_screen('screen3').ids.my_checklist.add_widget(self.status_lv)
        self.strng.get_screen('screen3').ids.my_checklist.add_widget(self.data_lv)

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

            self.strng.get_screen('screen3').ids.my_checklist.add_widget(self.list_item)

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
  
        
        
PawareApp().run()