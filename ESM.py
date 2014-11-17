from __future__ import print_function
import kivy
kivy.require('1.5.1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from run_trial import main


class Flex(FloatLayout):
    pass


# Window for status of model calculation
class OutputProgress(FloatLayout):
    pass


# Window for visual output
class VisualOutput(FloatLayout):
    model_variables = (['a','b','c'])
    
    def __init__(self, a, b, c, **kwargs):
        super(VisualOutput, self).__init__(**kwargs)
        model_values = ([a,b,c])
        self.add_widget(Label(text='Model sent variables: ' + str(self.model_variables) + ', with values: ' + str(model_values),size_hint=(0.3, 0.3),pos_hint={'center_x': 0.5, 'y': 0.8}))
        print(model_values)

# Window with backround info on modeling etc.
class BackgroundInfo(FloatLayout):
    pass


# Window with info for chosen scenario
class ScenarioInfo(FloatLayout):
    current_scenario = StringProperty('Rainfall in Raleigh')
    def __init__(self, **kwargs):
        super(ScenarioInfo, self).__init__(**kwargs)
        #self.add_widget(Label(text='Current Scenario:\n' + self.current_scenario,size_hint=(1,0.20),pos_hint={'center_x': 0.50, 'y': 0.6},font_size=str(self.height*20) + 'sp', markup=True))
        
    def on_current_scenario(self, value, instance):
        pass


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

    def btn_action(self):
        scn_sel =  ScenarioSelectorPopup()
        scn_sel.attach_to = self
        scn_sel.open()
        print(self,self.parent)


# Popup window that contains information on a particular variable
class VariablePopups(ModalView):
    current_value = StringProperty(None)

    def __init__(self, **kwargs):
        super(VariablePopups, self).__init__(**kwargs)
        popup_layout = GridLayout(cols=1, rows=3, size_hint=(0.9, 0.9),pos_hint={'center_x': 0.5,'center_y': 0.5})
        popup_layout.add_widget(Label(text=self.current_value, bold=True, font_size=28, size_hint_y=0.2))
        popup_layout.add_widget(Label(text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.', text_size=(1920*0.2, None), font_size=str(self.height*0.2) + 'sp', color=(0,0,0,0), halign='justify', markup=True))
        popup_button = Button(text='Press to close.', size_hint_y=0.25, pos_hint={'center_x': 0.5}, bold=True, font_size=24)
        popup_layout.add_widget(popup_button)
        popup_button.bind(on_press=self.dismiss)
        self.add_widget(popup_layout)
        print(self.current_value) #REMOVE LATER


# Window for variable manipulation (see .kv file)
# WINDOW TITLE: Conduct a Model Trial
class VariableWidget(FloatLayout):
    # THESE WILL EVENTUALLY BE REFERENCED FROM A DATABASE?
    v1 = NumericProperty(0)
    v2 = NumericProperty(0)
    v3 = NumericProperty(200)
    val = StringProperty(None)
    current_scenario = StringProperty('Rainfall in Raleigh')
    var_name1 = ['Precipitation', 'meters/year']
    var_name2 = ['Dam Height', 'meters']
    var_name3 = ['Time', 'years']

    def on_current_scenario(self, instance, value): #REMOVE LATER
        print("the instance is:" + " " + str(instance)) #REMOVE LATER

    def btn_action(self, btn):
        self.val = btn.text[0:-2]
        VariablePopups.current_value = self.val
        VariablePopups().open()
        print(self.v1, self.val, self.current_scenario) #REMOVE LATER

    def sldr_action(self, btn, sldr):
        if btn.pos_hint['y'] == 310.0/460.0:
            btn.text = str(self.var_name1[0]) + ':\n' + str(int(sldr.value)) +  ' ' + str(self.var_name1[1])
            self.v1 = int(sldr.value)
            return self.v1
        elif btn.pos_hint['y'] == 210.0/460.0:
            btn.text = str(self.var_name2[0]) + ':\n' + str(int(sldr.value)) +  ' ' + str(self.var_name2[1])
            self.v2 = int(sldr.value)
            return self.v2
        elif btn.pos_hint['y'] == 110.0/460.0:
            btn.text = str(self.var_name3[0]) + ':\n' + str(int(sldr.value)) +  ' ' + str(self.var_name3[1])
            self.v3 = int(sldr.value)
            return self.v3

    def run_graphic(self, btn):
        btn.text = 'Running...'

    def start_run(self, btn):
        btn.text = 'Press To Run Trial'
        main.run_ESM_trial(main(self.current_scenario, self.v1, self.v2, self.v3))
        print(self.parent.children)
        print(self.parent)


# Main window widget
# WINDOW TITLE: Earth Surface Modeler
class LayoutGUI(FloatLayout):

    def __init__(self, **kwargs):
        super(LayoutGUI, self).__init__(**kwargs)
        #self.add_widget(VariableWidget()) #moved to ChildModelGUIApp class
        #self.add_widget(ScenerioSelector()) #moved to ChildModelGUIApp class
        self.add_widget(BackgroundInfo())
        self.add_widget(VisualOutput(VariableWidget().v1,VariableWidget().v2,VariableWidget().v3))
        self.add_widget(OutputProgress())
        self.add_widget(Flex())


# Main app class
class ChildModelGUIApp(App):

    def on_change(self,instance):
        self.content.clear_widgets()
        self.content.add_widget(ScenarioInfo())
        self.content.add_widget(VariableWidget())
        print(self.lay.children)

    def build(self):
        select_button = Button(text='Press to Select Scenario',background_normal='Images\ScenarioSelect.png',background_down='Images\ScenarioSelectDown.png',size_hint=(0.75, 0.4),pos_hint={'center_x': 0.5,'center_y': 0.25},font_size='20sp',markup=True)
        select_scn = ScenerioSelector()
        select_scn.add_widget(select_button)
        select_popup = ScenarioSelectorPopup()
        select_button.bind(on_press=select_popup.open)
        select_button.bind(on_release=lambda select_button: print(select_popup)) #Required for select_popup to work after window resize (extremely annoying)
        select_popup.bind(on_dismiss=self.on_change)
        root = FloatLayout()
        self.content = content = FloatLayout()
        root.add_widget(content)
        self.lay = lay = LayoutGUI()
        lay.add_widget(root)

        self.content.add_widget(ScenarioInfo())
        self.content.add_widget(VariableWidget())
        lay.add_widget(select_scn)
        return lay

if __name__ == '__main__':
    ChildModelGUIApp().run()