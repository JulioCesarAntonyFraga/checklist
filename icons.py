from kivy.lang import Builder
from kivymd.app import MDApp


class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        return Builder.load_string(
            '''
BoxLayout:
    orientation:'vertical'
    MDToolbar:
        title: 'Bottom navigation'
        md_bg_color: .2, .2, .2, 1
        specific_text_color: 1, 1, 1, 1
    MDBottomNavigation:
        panel_color: .2, .2, .2, 1
        MDBottomNavigationItem:
            name: 'screen 1'
            text: 'Python'
            icon: 'language-python'
            MDLabel:
                text: 'Python'
                halign: 'center'
        MDBottomNavigationItem:
            name: 'screen 2'
            text: 'C++'
            icon: 'language-cpp'
            MDLabel:
                text: 'I programming of C++'
                halign: 'center'
        MDBottomNavigationItem:
            name: 'screen 3'
            text: 'JS'
            icon: 'language-javascript'
            MDLabel:
                text: 'JS'
                halign: 'center'
'''
        )


Test().run()
=======
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineIconListItem

Builder.load_string(
    '''
#:import images_path kivymd.images_path
<CustomOneLineIconListItem>:
    IconLeftWidget:
        icon: root.icon
<PreviousMDIcons>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(20)
        MDBoxLayout:
            adaptive_height: True
            MDIconButton:
                icon: 'magnify'
            MDTextField:
                id: search_field
                hint_text: 'Search icon'
                on_text: root.set_list_md_icons(self.text, True)
        RecycleView:
            id: rv
            key_viewclass: 'viewclass'
            key_size: 'height'
            RecycleBoxLayout:
                padding: dp(10)
                default_size: None, dp(48)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
'''
)


class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()


class PreviousMDIcons(Screen):

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        def add_icon_item(name_icon):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": name_icon,
                    "text": name_icon,
                    "callback": lambda x: x,
                }
            )

        self.ids.rv.data = []
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)

class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = PreviousMDIcons()

    def build(self):
        return self.screen

    def on_start(self):
        self.screen.set_list_md_icons()


MainApp().run()