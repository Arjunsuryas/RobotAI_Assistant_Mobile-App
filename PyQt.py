from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label


class MyTabs(TabbedPanel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.do_default_tab = False
        self.tab_pos = 'bottom_mid'

        # Chat tab
        chat_tab = TabbedPanelItem(text='Chat')
        chat_tab.add_widget(Label(text='Chat Screen'))
        self.add_widget(chat_tab)

        # History tab
        history_tab = TabbedPanelItem(text='History')
        history_tab.add_widget(Label(text='History Screen'))
        self.add_widget(history_tab)

        # Settings tab
        settings_tab = TabbedPanelItem(text='Settings')
        settings_tab.add_widget(Label(text='Settings Screen'))
        self.add_widget(settings_tab)


class TabApp(App):
    def build(self):
        return MyTabs()


if __name__ == '__main__':
    TabApp().run()
