#!/usr/bin/python3
# main.py
# @author Dan Woolsey
#
# Basic UI for testing purposes with debugging info and touchscreen buttons
# to switch microstepping values and control movement

from kivy.app import App

from kivy.core.window import Window

from kivy.properties import ObjectProperty

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

def forwards(instance):
    print("will send output to bottom box")

def backwards(instance):
    print("will send output to bottom box")

def release(instance):
    print("button was released")

class PumpTestApp(App):

    size_input = ObjectProperty()
    time_input = ObjectProperty()
    ms_button = ObjectProperty()

    # this will start an instance of Pumpy
    # and begin a progress bar along the bottom
    def infuse(self, instance):
        print("starting infusion")
        size = self.size_input.text;
        time = self.time_input.text;
        ms = self.spinner.text;
        print("syringe size = " + size)
        print("infusion time = " + time)
        print("microsteps = " + ms)

    def show_spinner_value(self, spinner, text):
        return text;

    def build(self):
        #Window.clearcolor=(1,1,1,1)

        main_layout = GridLayout(rows=7, row_force_default=True, row_default_height=70)

        title = Label(text="Pumpy")

        #middle_layout = GridLayout(cols=2)

        #middle_left_layout = GridLayout(rows=2)

        size_label = Label(text="Syringe Size:")
        self.size_input = TextInput(text="", multiline=False)
        #size_input.bind(on_text_validate=on_enter)

        size_layout = GridLayout(cols=2)
        size_layout.add_widget(size_label)
        size_layout.add_widget(self.size_input)

        time_label = Label(text="Infusion Time:")
        self.time_input = TextInput(text="", multiline=False)

        time_layout = GridLayout(cols=2)
        time_layout.add_widget(time_label)
        time_layout.add_widget(self.time_input)

        ms_label = Label(text="MICROSTEPPING")
        self.ms_button = Button(text="Select value")

        self.spinner = Spinner(
            text = "Select MS Value",
            values = ("1", "1/2", "1/4", "1/8", "1/16"),
            size_hint=(None, None),
            size=(150, 50)
        )

        self.spinner.bind(text=self.show_spinner_value)

        ms_layout = GridLayout(cols=2)
        ms_layout.add_widget(ms_label)
        ms_layout.add_widget(self.spinner)

        go_button = Button(text="INFUSE")
        go_button.bind(on_press=self.infuse)

        b1 = Button(text="CONTINUED INFUSION")
        b1.bind(on_press=forwards)
        b1.bind(on_release=release)

        b2 = Button(text="CONTINUED WITHDRAWAL")
        b2.bind(on_press=backwards)
        b2.bind(on_release=release)

        #middle_layout.add_widget(middle_left_layout)
        #middle_layout.add_widget(middle_right)

        main_layout.add_widget(title)
        main_layout.add_widget(size_layout)
        main_layout.add_widget(time_layout)
        main_layout.add_widget(ms_layout)
        main_layout.add_widget(go_button)
        main_layout.add_widget(b1)
        main_layout.add_widget(b2)

        return main_layout

if __name__ == "__main__":
    PumpTestApp().run()


#
"""
self.ms_dropdown = DropDown()
for option in MS_VALUES:
    option_button = Button(text="%s" % option, size_hint_y=None, height=44)
    option_button.bind(on_press=lambda btn: self.ms_dropdown.select(option_button.text))
    option_button.bind(on_release=lambda btn: setattr(self.ms_button, 'text', option_button.text))
    self.ms_dropdown.add_widget(option_button)

self.ms_button.bind(on_release=self.ms_dropdown.open)
self.ms_dropdown.bind(on_select=lambda instance, x: setattr(self.ms_button, 'text', x))
"""
