from __future__ import print_function
import kivy
kivy.require('1.5.1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.progressbar import ProgressBar
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from run_trial import main
from kivy.clock import Clock
import threading


class Flex(FloatLayout):
    pass


# Window for status of model calculation
class OutputProgress(FloatLayout):
    val = NumericProperty(10)

    def increment_value(self, dt):
        print(dt)
        self.val += 10

# Window for visual output
class VisualOutput(FloatLayout):

    def __init__(self, val1='', val2='', val3='', var1='', var2='', var3='', **kwargs):
        super(VisualOutput, self).__init__(**kwargs)
        model_values = ([val1, val2, val3])
        model_variables = ([var1, var2, var3])
        if val1 != '':
            self.add_widget(Label(text='Model sent variables: ' + str(model_variables) + '\nwith values: ' + str(model_values),size_hint=(0.3, 0.3),pos_hint={'center_x': 0.5, 'y': 0.8}))

# Window with backround info on modeling etc.
class BackgroundInfo(FloatLayout):
    pass


# Window with info for chosen scenario
class ScenarioInfo(FloatLayout):
    current_scenario = StringProperty('Rainfall in Raleigh')
    def __init__(self, **kwargs):
        super(ScenarioInfo, self).__init__(**kwargs)


# Popup window for selecting Scenario
class ScenarioSelectorPopup(ModalView):
    
    def change_scenario(self, name):
        VariableWidget.current_scenario = name
        if name == 'Rainfall in Raleigh' or name == None:
            VariableWidget.var_name1 = ['Precipitation', 'meters/year']
            VariableWidget.var_name2 = ['Dam Height', 'meters']
            VariableWidget.var_name3 = ['Time', 'years']
            ScenarioInfo.current_scenario = 'Rainfall in Raleigh'
        elif name == 'Uplift in the Appalachians':
            VariableWidget.var_name1 = ['S2_Var1', 'units']
            VariableWidget.var_name2 = ['S2_Var2', 'units']
            VariableWidget.var_name3 = ['S2_Var3', 'units']
            ScenarioInfo.current_scenario = 'Uplift in the Appalachians'
        elif name == 'Sawing the Beartooth Mtns':
            VariableWidget.var_name1 = ['S3_Var1', 'units']
            VariableWidget.var_name2 = ['S3_Var2', 'units']
            VariableWidget.var_name3 = ['S3_Var3', 'units']
            ScenarioInfo.current_scenario = 'Sawing the Beartooth Mtns'
        self.dismiss()


# Window for selecting Earth surface scenario
# WINDOW TITLE: Select the Earth surface scenario you wish to investigate
class ScenerioSelector(FloatLayout):
    pass
    #def btn_action(self):
    #    scn_sel =  ScenarioSelectorPopup()
    #    scn_sel.attach_to = self
    #    scn_sel.open()
    #    print(self,self.parent)


# Popup window that contains information on a particular variable
class VariablePopup(ModalView):
    current_value = StringProperty(None)

    def dismiss_button(self):
        print(self.size)
        self.dismiss()


# Window for variable manipulation (see .kv file)
# WINDOW TITLE: Conduct a Model Trial
class VariableWidget(FloatLayout):
    v1 = NumericProperty(0)
    v2 = NumericProperty(0)
    v3 = NumericProperty(200)
    val = StringProperty(None)
    progress = NumericProperty(0)
    current_scenario = StringProperty('Rainfall in Raleigh')
    var_name1 = ['Precipitation', 'meters/year']
    var_name2 = ['Dam Height', 'meters']
    var_name3 = ['Time', 'years']

    def btn_action(self, btn):
        self.val = btn.text
        VariablePopup.current_value = self.val
        VariablePopup().open()

    def sldr_action(self, btn, sldr):
        if btn.pos_hint['y'] == 310.0/460.0:
            btn.text = str(self.var_name1[0]) + ':\n' + str(int(sldr.value)) +  ' ' + str(self.var_name1[1])
            self.v1 = int(sldr.value)
        elif btn.pos_hint['y'] == 210.0/460.0:
            btn.text = str(self.var_name2[0]) + ':\n' + str(int(sldr.value)) +  ' ' + str(self.var_name2[1])
            self.v2 = int(sldr.value)
        elif btn.pos_hint['y'] == 110.0/460.0:
            btn.text = str(self.var_name3[0]) + ':\n' + str(int(sldr.value)) +  ' ' + str(self.var_name3[1])
            self.v3 = int(sldr.value)

    def run_graphic(self, btn):
        btn.text = 'Running...'

        for i in range(len(self.parent.children)):
            if 'OutputProgress' in str(self.parent.children[i]):
                self.parent.remove_widget(self.parent.children[i])
                self.output = (OutputProgress())
                self.parent.add_widget(self.output)
                break
        else:
            self.output = (OutputProgress())
            self.parent.add_widget(self.output)
        Clock.schedule_interval(self.output.increment_value,0.5)

    def start_run(self, btn):
        btn.text = 'Press To Run Trial'
        trial_inputs = main(self.current_scenario, self.v1, self.v2, self.v3)
        res = main.run_ESM_trial(trial_inputs)
        for i in res:
            self.progress = int(i)*100/self.v3
            self.v1 = self.progress
            print('Percent complete:', self.progress)

        for i in range(len(self.parent.children)):
            if 'VisualOutput' in str(self.parent.children[i]):
                self.parent.remove_widget(self.parent.children[i])
                self.parent.add_widget(VisualOutput(self.v1, self.v2, self.v3, self.var_name1[0], self.var_name2[0], self.var_name3[0]))
                break
        else:
            self.parent.add_widget(VisualOutput(self.v1, self.v2, self.v3, self.var_name1[0], self.var_name2[0], self.var_name3[0]))

# Main window widget
# WINDOW TITLE: Earth Surface Modeler
class LayoutGUI(FloatLayout):

    def __init__(self, **kwargs):
        super(LayoutGUI, self).__init__(**kwargs)
        #self.add_widget(VariableWidget()) #moved to ChildModelGUIApp class
        #self.add_widget(ScenerioSelector()) #moved to ChildModelGUIApp class
        self.add_widget(BackgroundInfo())
        #self.add_widget(VisualOutput(VariableWidget().v1,VariableWidget().v2,VariableWidget().v3, VariableWidget().var_name1[0], VariableWidget().var_name2[0], VariableWidget().var_name3[0]))
        #self.add_widget(OutputProgress())
        self.add_widget(Flex())


# Main app class
class ChildModelGUIApp(App):

    def on_change(self,instance):
        self.content.clear_widgets()
        self.content.add_widget(ScenarioInfo())
        self.content.add_widget(VariableWidget())
        self.content.add_widget(VisualOutput())

    def build(self):
        select_button = Button(text='Press to Select Scenario',background_normal='Images\ScenarioSelect.png',background_down='Images\ScenarioSelectDown.png',size_hint=(0.75, 0.4),pos_hint={'center_x': 0.5,'center_y': 0.25},font_size='20sp',markup=True)
        select_scn = ScenerioSelector()
        select_scn.add_widget(select_button)
        select_popup = ScenarioSelectorPopup()
        select_button.bind(on_press=select_popup.open)
        #select_button.bind(on_press=lambda select_button: print(select_popup)) #Required for select_popup to work after window resize (extremely annoying)
        select_popup.bind(on_dismiss=self.on_change)
        root = FloatLayout()
        self.content = content = FloatLayout()
        root.add_widget(content)
        self.lay = lay = LayoutGUI()
        lay.add_widget(root)
        print(self.lay, lay)

        self.content.add_widget(ScenarioInfo())
        self.content.add_widget(VariableWidget())
        self.content.add_widget(VisualOutput())
        lay.add_widget(select_scn)
        return lay


if __name__ == '__main__':
    ChildModelGUIApp().run()