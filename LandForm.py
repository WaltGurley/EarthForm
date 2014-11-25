from __future__ import print_function
import kivy
kivy.require('1.5.1')


# from kivy.config import Config
# Config.set('graphics','resizable',0)
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
from kivy.uix.image import Image
from run_trial import main
from kivy.clock import Clock
from threading import Thread


class Flex(FloatLayout):
    pass


# Window for status of model calculation
class OutputProgress(FloatLayout):
    val = NumericProperty(0)

    def increment_value(self, frac):
        self.val = frac

# Window for visual output
class VisualOutput(FloatLayout):
    rain_image = Image(source='Images\ESMgraphic.zip',pos_hint={'center_x': 0.50,'center_y': 0.50},anim_delay=0.05)
    def __init__(self, val1='', val2='', val3='', var1='', var2='', var3='', **kwargs):
        super(VisualOutput, self).__init__(**kwargs)
        self.model_values = ([val1, val2, val3])
        self.model_variables = ([var1, var2, var3])
        if val1 != '':
            self.add_widget(Label(text='Model sent variables: ' + str(self.model_variables) + '\nwith values: ' + str(self.model_values),size_hint=(0.3, 0.3),pos_hint={'center_x': 0.5, 'y': 0.8}))
            self.add_widget(self.rain_image)


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
                self.progress_update = OutputProgress()
                self.parent.add_widget(self.progress_update)
                break
        else:
            self.progress_update = OutputProgress()
            self.parent.add_widget(self.progress_update)

    def start_run(self, btn):
        current_run_vis_out = VisualOutput(self.v1, self.v2, self.v3, self.var_name1[0], self.var_name2[0], self.var_name3[0])
        for i in range(len(self.parent.children)):
            if 'VisualOutput' in str(self.parent.children[i]):
                self.parent.remove_widget(self.parent.children[i])
                self.parent.add_widget(current_run_vis_out)
                break
        else:
            self.parent.add_widget(current_run_vis_out)

        trial_inputs = main(self.current_scenario, self.v1, self.v2, self.v3)
        res = main.run_ESM_trial(trial_inputs)
        for i in res:
            self.progress = int(i)*100/self.v3
            self.progress_update.increment_value(self.progress)
            
        current_run_vis_out.remove_widget(current_run_vis_out.rain_image)
        btn.text = 'Press To Run Trial'

    # KIVY FILE IS POINTING TO THIS def WHEN RUN BUTTON IS CLICKED
    def start_start_run_thread(self, btn):
        self.child_thread = Thread(target=self.start_run, args=(btn,))
        self.child_thread.daemon = True
        self.child_thread.start()


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
        select_scn = ScenerioSelector()
        select_button = Button(text='Press to Select Scenario',background_normal='Images\ScenarioSelect.png',background_down='Images\ScenarioSelectDown.png',size_hint=(0.75, 0.4),pos_hint={'center_x': 0.5,'center_y': 0.25},font_size='20sp',markup=True)
        select_scn.add_widget(select_button)
        select_popup = ScenarioSelectorPopup()
        select_button.bind(on_press=lambda select_button: select_popup.open()) # Required for select_popup to work after window resize (extremely annoying)
        select_popup.bind(on_dismiss=self.on_change)
        self.content = FloatLayout()
        self.lay = lay = LayoutGUI()
        lay.add_widget(self.content)

        self.content.add_widget(ScenarioInfo())
        self.content.add_widget(VariableWidget())
        self.content.add_widget(VisualOutput())
        lay.add_widget(select_scn)
        return lay


if __name__ == '__main__':
    ChildModelGUIApp().run()