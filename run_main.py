from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import tkinter as tk
from tkinter import filedialog
from converter import CMP
from kivy.clock import Clock
import threading
from kivy.properties import StringProperty
import temp_data
##Window.maximize()


class ComparatorApp(App):
    fixed_log_info = ""
    log_info = StringProperty("info")
    path = ""
    texts = None
    
    def update_log_info(self,dt = None):
        self.Info.text = str(self.log_info)
        ##to do сделать блокировку кнопки пока не закончится работа потока

    def ch_ipath(self,instance):
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askdirectory()
        self.chosen_path.text = str(path)
        return path

    def do_compare(self,instance):
        def inline_foo(text,freez = False): 
            if freez:self.fixed_log_info += "+  " + text + "\n"
            self.log_info =  self.fixed_log_info  + "+  " + text + "\n"
        try:
            if self.chosen_path.text == "":
                raise Exception("Не выбрана папка с файлами")
            threading.Thread(target=CMP,args=(self.chosen_path.text,inline_foo)).start()
        except Exception as ex:
            self.log_info = f"Произошла ошибка:\n{str(ex)}"

        
    def render_compare(self,instance):
        try:
            self.texts = temp_data.texts
            if self.texts == None:raise Exception("Нет результатов сравнения,пожалуйста сначала запустите сравнение")
            self.texts_list = GridLayout()
            self.texts_list.cols = 5
            self.texts_list.size_hint=(1, None)
            self.texts_list.height = self.texts_list.minimum_height

            for items in self.texts:
                match items['coef']:
                    case _ if items['coef'] <= 10:r_color = "green"
                    case _ if items['coef'] <= 50:r_color = "yellow"
                    case _ if items['coef'] <= 99:r_color = "orange"
                    case _ if items['coef'] >= 99:r_color = "red"

                for item in items.values():
                    elem = TextInput(text = f"{item}")
                    elem.size_hint=(0.2, None)
                    elem.halign = "center"
                    elem.background_color = r_color
                    elem.font_size = 16
                    elem.padding_y = [elem.height / 2.0 - (elem.line_height / 2.0) * len(elem._lines), 0]
                    self.texts_list.height += elem.height/len(items.values())
                    self.texts_list.add_widget(elem)

            self.Result = ScrollView()
            self.Result.do_scroll_x = False
            self.Result.do_scroll_y = True

            self.Result.add_widget(self.texts_list)

            self.Explanation = Button(text = "Алгоритм показывает максимально похожий фаил для каждого файла.")
            self.Explanation.background_color = "white"
            self.Explanation.size_hint_y = .1

            self.column_def = GridLayout()
            self.column_def.cols = 5
            self.column_def.size_hint=(1, None)
            self.column_def.height = 30
            definitons = ["Дата создания","Дата изменения","Первый фаил","Второй фаил","Схожесть в %"]
            for _def in definitons:self.column_def.add_widget(TextInput(text = f"{_def}"))

            self.mB.remove_widget(self.ch_ipath_btn)
            self.mB.remove_widget(self.compare_btn)
            self.mB.remove_widget(self.render_compare_btn)

            self.mB.add_widget(self.Explanation)
            self.mB.add_widget(self.column_def)
            self.mB.add_widget(self.Result)
            Window.size = (800,800)
        except Exception as ex:
            self.log_info = f"Произошла ошибка:\n{str(ex)}" 
        

    def build(self):
        Window.size = (600,400)
        self.mB = GridLayout(cols = 1)
        self.ch_ipath_btn = Button(text = "Выбрать папку с файлами",on_press = self.ch_ipath)
        self.ch_ipath_btn.size_hint_y = .2

        self.chosen_path = Label(text = "",color = "yellow")
        self.chosen_path.size_hint_y = .2
        
        self.compare_btn = Button(text = "Начать сравнение",on_press = self.do_compare)
        self.compare_btn.size_hint_y = .2

        self.render_compare_btn = Button(text = "Показать сравнение",on_press = self.render_compare)
        self.render_compare_btn.size_hint_y = .2

        Clock.schedule_interval(self.update_log_info, 0.1)

        self.Info = TextInput(text = "info")
        self.Info.size_hint=(1, None)
        self.Info.background_color = "black"
        self.Info.foreground_color = [0,255,0,1]
        self.Info.halign = "center"
        
        self.mB.add_widget(self.ch_ipath_btn)
        self.mB.add_widget(self.chosen_path)
        self.mB.add_widget(self.compare_btn)
        self.mB.add_widget(self.render_compare_btn)
        self.mB.add_widget(self.Info)
        return self.mB
    

if __name__ == "__main__":
    ComparatorApp().run()