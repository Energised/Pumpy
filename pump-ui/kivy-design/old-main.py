#!/usr/bin/python3
# main.py
# @author Dan Woolsey
#
# Basic UI for testing purposes with debugging info and touchscreen buttons
# to switch microstepping values and control movement

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

def forwards(instance):
    print("will send output to bottom box")

def backwards(instance):
    print("will send output to bottom box")

def release(instance):
    print("button was released")

class PumpTestApp(App):
    def build(self):
        main_layout = GridLayout(rows=3)

        title = Label(text="PumpTest")

        middle_layout = GridLayout(cols=2)

        middle_left_layout = GridLayout(rows=2)

        b1 = Button(text="MOVE FORWARDS")
        b1.bind(on_press=forwards)
        b1.bind(on_release=release)

        b2 = Button(text="MOVE BACKWARDS")
        b2.bind(on_press=backwards)
        b2.bind(on_release=release)

        middle_left_layout.add_widget(b1)
        middle_left_layout.add_widget(b2)

        middle_right = Label(text="MICROSTEPPING")

        middle_layout.add_widget(middle_left_layout)
        middle_layout.add_widget(middle_right)

        main_layout.add_widget(title)
        main_layout.add_widget(middle_layout)
        main_layout.add_widget(Label(text="debug box here"))

        return main_layout

if __name__ == "__main__":
    PumpTestApp().run()
