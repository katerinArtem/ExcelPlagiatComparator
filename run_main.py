from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import tkinter as tk
from tkinter import filedialog
from converter import Conv
from kivy.clock import Clock
import threading
##Window.maximize()


class ComparatorApp(App):
    val = ""
    texts = []
    def update(self,dt = None):
        self.Info.text = str(self.val)
        ##to do сделать блокировку кнопки пока не закончится работа потока

    def do_compare(self,path):
        def inline_foo(text):
            self.val = text
            Clock.schedule_once(self.update)
        conv = Conv()
        try:
            self.texts = conv.CMP(path,inline_foo)
            self.texts_list = GridLayout()
            self.texts_list.cols = 3
            self.texts_list.size_hint=(1, None)
            self.texts_list.height = self.texts_list.minimum_height

            for item in self.texts:
                
                if item['coef'] < 50 and item['coef'] > 10:r_color = "yellow"
                elif item['coef'] < 99 and item['coef'] > 50:r_color = "orange"
                elif item['coef'] > 99:r_color = "red"
                else:r_color = "green"

                self.var1 = TextInput(text = f"{item['name']}")
                self.var1.size_hint=(0.4, None)
                self.var1.halign = "center"
                self.var1.background_color = r_color
                self.var1.font_size = 25

                self.var2 = TextInput(text = f"{item['pair']}")
                self.var2.size_hint=(0.4, None)
                self.var2.halign = "center"
                self.var2.background_color = r_color
                self.var2.font_size = 25

                self.var3 = TextInput(text = f"{round(item['coef'],2)}%")
                self.var3.size_hint=(0.2, None)
                self.var3.halign = "center"
                self.var3.background_color = r_color
                self.var3.font_size = 25

                self.texts_list.height += self.var1.height
                self.texts_list.add_widget(self.var1)
                self.texts_list.add_widget(self.var2)
                self.texts_list.add_widget(self.var3)
                    
            
            self.Result = ScrollView()
            self.Result.do_scroll_x = False
            self.Result.do_scroll_y = True

            self.Result.add_widget(self.texts_list)

            self.Explanation = Button(text = "Алгоритм показывает максимально похожий фаил для каждого файла.")
            self.Explanation.background_color = "white"
            self.Explanation.size_hint_y = .1

            self.mB.add_widget(self.Explanation)
            self.mB.add_widget(self.Result)
            Window.size = (800,800)
        except Exception as ex:
            self.Info.text = f"Произошла ошибка:\n{str(ex)}" 
        
    def ch_ipath(self,instance):
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askdirectory()
        threading.Thread(target=self.do_compare,args=(path,)).start()

    def build(self):
        Window.size = (500,300)
        self.mB = GridLayout(cols = 1)
        self.ch_ipath_btn = Button(text = "Выбрать папку с файлами",on_press = self.ch_ipath)
        self.ch_ipath_btn.size_hint_y = .1
        self.Info = Label(text = "info",color = "yellow")
        self.Info.size_hint_y = .1
        
        self.mB.add_widget(self.ch_ipath_btn)
        self.mB.add_widget(self.Info)
        return self.mB
    
if __name__ == "__main__":
    ComparatorApp().run()