
from PySide2.QtCore import*
from PySide2.QtGui import*
from PySide2.QtWidgets import*
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from PySide2.QtGui import QPixmap
import codecs
import os

CUR_DIR = os.path.dirname(__file__)
ICON_DIR = f'{CUR_DIR}/icons'.replace('\\', '/')



class MyLightTool(QDialog):
    def __init__(self, parent):
        super(MyLightTool, self).__init__(parent)

        self.setWindowTitle('My Light Tool')
        self.resize(400, 300)
        self.setStyleSheet(
            '''
                
                background-color: #6A6464;
                color: #e9e6eb;
                font-size: 15px;
                font-family: Comic Sans MS 
                

            '''

        )

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.key_light_name = None
        self.fill_light_name = None
        self.rim_light_name = None
        
        self.key_light_color = (1.0, 1.0, 1.0)  
        self.fill_light_color = (1.0, 1.0, 1.0) 
        self.rim_light_color = (1.0, 1.0, 1.0) 


        #////INIT BOX PRESET WIDGET///

        self.inputWidget= QWidget()
        self.inputLayout = QGridLayout()
        self.inputWidget.setLayout(self.inputLayout)

     
        
       
        icon_pixmap = QPixmap(os.path.join(ICON_DIR, "Time.png"))
        icon_pixmap = QPixmap(os.path.join(ICON_DIR, "Time.png")).scaled(30, 30)
        
        self.iconLabel = QLabel()
        self.iconLabel.setPixmap(icon_pixmap)
        self.iconLabel.setFixedWidth(30)
        
        self.nameLabel = QLabel('Presets:')
        self.nameLabel.setFixedWidth(70)
        
        #///////////////////////////////////COMBO BOXXX////////////////////////////
        
        self.lightComboBox = QComboBox()
        
        icon_morning = QIcon(os.path.join(ICON_DIR, "Morning.png"))
        icon_noon = QIcon(os.path.join(ICON_DIR, "Noon.png"))
        icon_evening = QIcon(os.path.join(ICON_DIR, "Evening.png"))
        icon_night = QIcon(os.path.join(ICON_DIR, "Night.png"))
        
        self.lightComboBox.addItem('None')
        self.lightComboBox.addItem(icon_morning, 'Morning')
        self.lightComboBox.addItem(icon_noon, 'Noon')
        self.lightComboBox.addItem(icon_evening, 'Evening')
        self.lightComboBox.addItem(icon_night, 'Night')
        self.lightComboBox.setStyleSheet(
            '''
                
                background-color: #96969b;
                color:#3C3D37;

            '''
        )
        
        

        self.inputLayout.addWidget(self.iconLabel,0, 0 )
        self.inputLayout.addWidget(self.nameLabel, 0, 1)
        self.inputLayout.addWidget(self.lightComboBox,0 ,2)

        #/// input preset button widget///
        self.buttonWidget = QWidget()
        self.buttonLayout = QHBoxLayout()
        self.buttonWidget.setLayout(self.buttonLayout)
        
        self.presetButton = QPushButton('Create 3 Points Light')
        self.presetButton.setToolTip('*Preset Lights are not editable.')

        self.presetButton.setMinimumHeight(30)
        
        okicon_path = os.path.join(ICON_DIR, "Ok.png")
        okicon = QIcon(okicon_path)
        
        self.presetButton.setIcon(okicon)
        self.presetButton.setIconSize(QSize(34, 34))
      
        self.presetButton.setStyleSheet(
            '''
                QPushButton {
                    border-width: 2px;
                    border-style: outset;
                    border-radius: 5px;
                    border-color:#241e23;
                    background-color:#241e23;
                }

                QPushButton:hover {
                    background-color:#F1E5D1;
                    color: black;
                }

                QPushButton:pressed {
                    background-color:#C39898;
                }
            '''
        )

       
        self.presetButton.clicked.connect(self.createScene)
      
        self.buttonLayout.addWidget(self.presetButton)

        #/////input settingLIght \\\\\\\\\\\\\\\\\\\
        self.settingWidget= QWidget()
        self.settingLayout = QGridLayout()
        self.settingWidget.setLayout(self.settingLayout)
        
        self.lightsettingWidget = QWidget()
        self.lightsettingLayout = QGridLayout()
        self.lightsettingWidget.setLayout(self.lightsettingLayout)
        
        seticon_pixmap = QPixmap(os.path.join(ICON_DIR, "Setting.png"))
        seticon_pixmap = QPixmap(os.path.join(ICON_DIR, "Setting.png")).scaled(30, 30)
        
        self.seticonLabel = QLabel()
        self.seticonLabel.setPixmap(seticon_pixmap)
        self.seticonLabel.setFixedWidth(30)
        
        exicon_pixmap = QPixmap(os.path.join(ICON_DIR, "Exposure.png"))
        exicon_pixmap = QPixmap(os.path.join(ICON_DIR, "Exposure.png")).scaled(30, 30)
        
        self.exiconLabel = QLabel()
        self.exiconLabel.setPixmap(exicon_pixmap)
        self.exiconLabel.setFixedWidth(30)
        
        coloricon_pixmap = QPixmap(os.path.join(ICON_DIR, "Color.png"))
        coloricon_pixmap = QPixmap(os.path.join(ICON_DIR, "Color.png")).scaled(30, 30)
        
        self.coloriconLabel = QLabel()
        self.coloriconLabel.setPixmap(coloricon_pixmap)
        self.coloriconLabel.setFixedWidth(30)
        
        
        self.settingLabel = QLabel('Setting')
        self.settingLabel.setFixedWidth(55)
        self.expoLabel = QLabel('Exposure')
        self.expoLabel.setFixedWidth(100)
        self.colLabel = QLabel('Color')
        self.colLabel.setFixedWidth(50)

        self.keyLabel = QLabel('Key Light')
        self.fillLabel = QLabel('Fill Light')
        self.rimLabel = QLabel('Rim Light')

        self.keySlide = QSlider(Qt.Horizontal)

        self.keySlide.setMinimum(0)
        self.keySlide.setMaximum(5)

        self.keySlide.setSingleStep(3)

        self.keySlide.valueChanged.connect(self.value_changed)

        self.keySlide.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 2px;
                margin: 0px;
                background-color: #F1E5D1;
                border: 1px solid #D6D6D6;
            }
            QSlider::handle:horizontal {
                height: 0px;
                width: 0px;
                margin: -10px 0px -10px 0px;
                border-top: 6px solid ;
                border-left: 3px solid ;
                border-right: 3px solid ;
            }
  
        """)
        
        
        self.fillSlide = QSlider(Qt.Horizontal)

        self.fillSlide.setMinimum(0)
        self.fillSlide.setMaximum(5)

        self.fillSlide.setSingleStep(3)

        self.fillSlide.valueChanged.connect(self.value_changed)

        self.fillSlide.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 2px;
                margin: 0px;
                background-color: #F1E5D1;
                border: 1px solid #D6D6D6;
            }
            QSlider::handle:horizontal {
                height: 0px;
                width: 0px;
                margin: -10px 0px -10px 0px;
                border-top: 6px solid ;
                border-left: 3px solid ;
                border-right: 3px solid ;
            }
  
        """)
        
        self.rimSlide = QSlider(Qt.Horizontal)

        self.rimSlide.setMinimum(0)
        self.rimSlide.setMaximum(5)

        self.rimSlide.setSingleStep(3)

        self.rimSlide.valueChanged.connect(self.value_changed)
        
        self.rimSlide.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 2px;
                margin: 0px;
                background-color: #F1E5D1;
                border: 1px solid #D6D6D6;
            }
            QSlider::handle:horizontal {
                height: 0px;
                width: 0px;
                margin: -10px 0px -10px 0px;
                border-top: 6px solid ;
                border-left: 3px solid ;
                border-right: 3px solid ;
            }
  
        """)
    
     #///////////////color////////////
        
        self.colorPicker = QColorDialog()
        self.colorButton = QPushButton(' ')
        self.colorButton.setStyleSheet(
        '''
        QPushButton {
            background-color: #96969b;
            color: #3C3D37;
            height: 3px;
        }
        QPushButton:hover {
            background-color: #F1E5D1;
        }
        '''
        )
       
        self.colorButton.clicked.connect(self.openColorDialog)
        self.colorButton.setToolTip('Choose the color for the Key Light.')
        
         #####FILL
        self.fillcolorPicker = QColorDialog()
        self.fillcolorButton = QPushButton(' ')
        self.fillcolorButton.setStyleSheet (
        '''
        QPushButton {
            background-color: #96969b;
            color: #3C3D37;
            height: 3px;
            }
        QPushButton:hover {
            background-color: #F1E5D1;
            }
        '''
        )
        self.fillcolorButton.clicked.connect(self.openFillColorDialog)
        self.fillcolorButton.setToolTip('Choose the color for the Fill Light.')

        #####RIM
        
        self.rimcolorPicker = QColorDialog()
        self.rimcolorButton = QPushButton(' ')
        self.rimcolorButton.setStyleSheet(
        '''
        QPushButton {
            background-color: #96969b;
            color: #3C3D37;
            height: 3px;
        }
        QPushButton:hover {
            background-color: #F1E5D1;
        }
        '''
        )
        self.rimcolorButton.clicked.connect(self.openRimColorDialog)
        self.rimcolorButton.setToolTip('Choose the color for the Rim Light.')
        
            
        #LAYOUT

        self.settingLayout.addWidget(self.seticonLabel, 0, 0)
        self.settingLayout.addWidget(self.settingLabel, 0, 1)
        self.settingLayout.addWidget(self.exiconLabel, 0, 2)
        self.settingLayout.addWidget(self.expoLabel,0 ,3)
        self.settingLayout.addWidget(self.coloriconLabel, 0, 4)
        self.settingLayout.addWidget(self.colLabel,0 ,5)
        
        self.lightsettingLayout.addWidget(self.keyLabel,1 ,0)
        self.lightsettingLayout.addWidget(self.fillLabel,2 ,0)
        self.lightsettingLayout.addWidget(self.rimLabel,3 ,0)
        self.lightsettingLayout.addWidget(self.keySlide,1 ,1)
        self.lightsettingLayout.addWidget(self.fillSlide,2 ,1)
        self.lightsettingLayout.addWidget(self.rimSlide,3 ,1)
        self.lightsettingLayout.addWidget(self.colorButton, 1, 2) 
        self.lightsettingLayout.addWidget(self.fillcolorButton, 2, 2) 
        self.lightsettingLayout.addWidget(self.rimcolorButton, 3, 2) 
        
   

        #/// input Light Type Box widget///
        
        self.typeinputWidget= QWidget()
        self.typeinputLayout = QGridLayout()
        self.typeinputWidget.setLayout(self.typeinputLayout)

        
        self.typeboxLabel = QLabel('Maya Light Create')
        self.typeboxLabel.setFixedWidth(130)
        
        self.typeComboBox = QComboBox()
        
        icon_Spotlight = QIcon(os.path.join(ICON_DIR, "Spotlight.png"))
        icon_Area = QIcon(os.path.join(ICON_DIR, "Area.png"))
        icon_Direct = QIcon(os.path.join(ICON_DIR, "Direct.png"))
        icon_Point = QIcon(os.path.join(ICON_DIR, "Point.png"))
        
        self.typeComboBox.addItem(icon_Spotlight,'Spot Light')
        self.typeComboBox.addItem(icon_Area, 'Area Light')
        self.typeComboBox.addItem(icon_Direct, 'Directional')
        self.typeComboBox.addItem(icon_Point, 'Point Light')
        
        self.typeComboBox.setStyleSheet(
            '''
                
                background-color: #96969b;
                color:#3C3D37;

            '''
        )

        self.typeinputLayout.addWidget(self.typeboxLabel, 0, 0)
        self.typeinputLayout.addWidget(self.typeComboBox,0 ,1)

      #/// input Light Type BUTTON widget///
        self.typebuttonWidget = QWidget()
        self.typebuttonLayout = QVBoxLayout()
        self.typebuttonWidget.setLayout(self.typebuttonLayout)

        self.typeButton = QPushButton('Create Light')

        self.typeButton.setMinimumHeight(30)
        self.typeButton.setStyleSheet(
            '''
                QPushButton {
                    border-width: 2px;
                    border-style: outset;
                    border-radius: 5px;
                    border-color:#241e23;
                    background-color:#241e23;
                
                }

                QPushButton:hover {
                    background-color:#F1E5D1;
                    color: black;
                }

                QPushButton:pressed {
                    background-color:#C39898;
                }
            '''
        )
        self.typeButton.clicked.connect(self.createLight)
        self.typeButton.setToolTip('Create new light of the selected type.')

        self.closeButton = QPushButton('Close')
        self.closeButton.setToolTip('Close the light tool.')
        self.closeButton.setMinimumHeight(30)
        self.closeButton.setStyleSheet(
            '''
                QPushButton {
                    border-width: 2px;
                    border-style: outset;
                    border-color:#423c3c;
                    border-radius: 5px;
                    background-color:#423c3c;
                }

                QPushButton:hover {
                    background-color:#F1E5D1;
                    color: black;
                }

                QPushButton:pressed {
                    background-color:#C39898;
                }


            '''
        )

        self.byeMovie = QMovie((os.path.join(ICON_DIR, "Bye.gif")))
        self.byeMovie.frameChanged.connect(self.updateIcon)
        self.byeMovie.start()
        
        self.closeButton.setIconSize(QSize(34, 34))
        self.closeButton.setIcon(QIcon(self.byeMovie.currentPixmap()))
        
        self.typeButton.setIcon(okicon)
        self.typeButton.setIconSize(QSize(34, 34))

        self.typebuttonLayout.addWidget(self.typeButton)
        self.typebuttonLayout.addWidget(self.closeButton)

        # /// main LAYOUT //////
        self.mainLayout.addWidget(self.inputWidget)
        self.mainLayout.addWidget(self.buttonWidget)

        self.mainLayout.addWidget(self.settingWidget)
        self.mainLayout.addWidget(self.lightsettingWidget)

        self.mainLayout.addWidget(self.typeinputWidget)
        self.mainLayout.addWidget(self.typebuttonWidget)
  

        self.setWindowIcon(QIcon(os.path.join(ICON_DIR, "WindowTitle.png")))

    
 
    def updateIcon(self):
        self.closeButton.setIcon(QIcon(self.byeMovie.currentPixmap()))

    def closeSlot(self):
        self.close()
        
    #///////////////// COLOR //////////////////////////
        
    def updateColorButton(self, button, color):
        button.setStyleSheet(f'''
            QPushButton {{
                background-color: {color.name()};
                color: #3C3D37;
            }}
            QPushButton:hover {{
                background-color: #F1E5D1;
            }}
        ''')

    def openColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.key_light_color = (color.redF(), color.greenF(), color.blueF())  
            self.updateColorButton(self.colorButton, color)
            self.updateLightColors()
            
    def openFillColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.fill_light_color = (color.redF(), color.greenF(), color.blueF())  
            self.updateColorButton(self.fillcolorButton, color)
            self.updateLightColors()

    def openRimColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.rim_light_color = (color.redF(), color.greenF(), color.blueF()) 
            self.updateColorButton(self.rimcolorButton, color)
            self.updateLightColors()
            
    def updateLightColors(self):
        if self.key_light_name:
            cmds.setAttr(f'{self.key_light_name}.color', *self.key_light_color, type='double3')
        
        if self.fill_light_name:
            cmds.setAttr(f'{self.fill_light_name}.color', *self.fill_light_color, type='double3')
        
        if self.rim_light_name:
            cmds.setAttr(f'{self.rim_light_name}.color', *self.rim_light_color, type='double3')
       
     #/////////////////SLIDER///////////  
           
    def value_changed(self, value):
        
        slider = self.sender()
        
        if slider == self.keySlide:
            light = 'keyLight'
        elif slider == self.fillSlide:
            light = 'fillLight'
        elif slider == self.rimSlide:
            light = 'rimLight'
        else:
            return 

        cmds.setAttr(f'{light}.aiExposure', value)
          
    def createLight(self):
        light_type = self.typeComboBox.currentText()

        if light_type == "Spot Light":
            cmds.spotLight()
        elif light_type == "Area Light":
            cmds.shadingNode('aiAreaLight', asLight=True)
        elif light_type == "Directional":
            cmds.directionalLight()
        elif light_type == "Point Light":
            cmds.pointLight()
        else:
            print("No valid light type selected.")
            
        self.updateLightExposures()
        
    def updateLightExposures(self):
        if self.key_light_name:
            cmds.setAttr(f'{self.key_light_name}.aiExposure', self.keySlide.value())
        if self.fill_light_name:
            cmds.setAttr(f'{self.fill_light_name}.aiExposure', self.fillSlide.value())
        if self.rim_light_name:
            cmds.setAttr(f'{self.rim_light_name}.aiExposure', self.rimSlide.value())


    ######################### PRESETS ########################################
    def createScene(self):
  
        preset = self.lightComboBox.currentText()  
        lights = self.create_3pt_lighting(preset)

        camera = self.create_camera()
        controller = self.create_controller()
        plane = self.create_plane()
        
        self.parent_controller(controller, camera, lights, plane)  


    def create_3pt_lighting(self, preset):
        """Creates a 3-point lighting setup based on the selected preset."""
        
        light_group = cmds.group(em=True, name= self.lightComboBox.currentText())
        self.key_light_name = self.create_key_light()
        self.rim_light_name = self.create_rim_light()
        self.fill_light_name = self.create_fill_light()
        

        preset_exposures = {
            "Morning": (4, 2, 1),
            "Noon": (6, 3, 2),
            "Evening": (3, 1.5, 2),
            "Night": (1, 0.5, 0.5),
            "None": (5, 2.5, 3),
        }
        
        preset_colors = {
            "Morning": (1, 0.8, 0.6),  
            "Noon": (1, 1, 1),        
            "Evening": (1, 0.5, 0.5),  
            "Night": (0.2, 0.2, 0.5),   
            "None": (1, 1, 1),          
        }
        
        exposures = preset_exposures.get(preset, (1, 1, 1))
        
        if preset == "None":
            key_color = self.key_light_color if hasattr(self, 'key_light_color') else (1, 1, 1)
            fill_color = self.fill_light_color if hasattr(self, 'fill_light_color') else (1, 1, 1)
            rim_color = self.rim_light_color if hasattr(self, 'rim_light_color') else (1, 1, 1)
            
            self.apply_light_settings(self.key_light_name, exposures[0], key_color)
            self.apply_light_settings(self.rim_light_name, exposures[1], rim_color)
            self.apply_light_settings(self.fill_light_name, exposures[2], fill_color)
        else:
            colors = preset_colors.get(preset, (1, 1, 1))
            self.apply_light_settings(self.key_light_name, exposures[0], colors)
            self.apply_light_settings(self.rim_light_name, exposures[1], colors)
            self.apply_light_settings(self.fill_light_name, exposures[2], colors)
            

        cmds.parent(self.key_light_name, self.rim_light_name, self.fill_light_name, light_group)
        cmds.setAttr(f'{self.key_light_name}.visibility', 1)
        cmds.setAttr(f'{self.rim_light_name}.visibility', 1)
        cmds.setAttr(f'{self.fill_light_name}.visibility', 1)
        
        return light_group

    def apply_light_settings(self, light, exposure, color):
        cmds.setAttr(f'{light}.aiExposure', exposure)
        cmds.setAttr(f'{light}.color', color[0], color[1], color[2], type='double3')

    def create_key_light(self):
        """Creates the key light and sets attributes."""
        area_light = cmds.shadingNode('aiAreaLight', asLight=True)
        area_light = cmds.rename(area_light, 'keyLight')
        cmds.setAttr(f'{area_light}.translate', -2.5, 2.5, 2.5)
        cmds.setAttr(f'{area_light}.rotate', -15, -45, 0)
        return area_light

    def create_rim_light(self):
        """Creates the rim light and sets attributes."""
        area_light = cmds.shadingNode('aiAreaLight', asLight=True)
        area_light = cmds.rename(area_light, 'rimLight')
        cmds.setAttr(f'{area_light}.translate', 2.5, 2.5, -2.5)
        cmds.setAttr(f'{area_light}.rotate', -15, 135, 0)
        return area_light

    def create_fill_light(self):
        """Creates the fill light and sets attributes."""
        area_light = cmds.shadingNode('aiAreaLight', asLight=True)
        area_light = cmds.rename(area_light, 'fillLight')
        cmds.setAttr(f'{area_light}.translate', 2.5, 2.5, 2.5)
        cmds.setAttr(f'{area_light}.rotate', -15, 45, 0)
        return area_light
    
    def create_camera(self):
        camera = cmds.camera(name='potraitCamera')[0]

        cmds.setAttr(f'{camera}.translate', 0,2,4)
        cmds.setAttr(f'{camera}.rotate', -10, 0, 0)
        return camera
    
    def create_controller(self):
        controller = cmds.circle(name='setup_controller')[0]
        cmds.scale(2, 2, 2, controller)
        cmds.move(0, 5, 0, controller)
        cmds.rotate(-90, 0, 0, controller)
        return controller
    

    def plane_curve(self, plane):
        edge = f'{plane}.e[3]'
        extrude = cmds.polyExtrudeEdge(edge)[0]
        cmds.setAttr(extrude + '.localTranslateZ', 5)

        bevel = cmds.polyBevel3(edge)[0]
        cmds.setAttr(bevel + '.segments', 20)
        cmds.setAttr(bevel + '.offset', 0.15)
    
    def create_plane(self):
       
        plane = cmds.polyPlane(sx=1, sy=1, name='backdrop')[0]
        cmds.scale(20,20,10, plane)
        
        self.apply_arnold_shader(plane, 'planeShader')
        self.plane_curve(plane)
        
        return plane

    def apply_arnold_shader(self,object, name=str):
        arnold_shader = cmds.shadingNode('aiStandardSurface', asShader=True, name=name)
        cmds.select(object)
        cmds.hyperShade(assign=arnold_shader)

    def parent_controller(self, controller, camera,plane, lights):
        # Group the camera and lights
        group = cmds.group(camera,plane,lights, name='Cam_Lights_BG')
        cmds.parentConstraint(controller, group, maintainOffset=True)
        cmds.parent(group, controller)


def myrun():
    mayaMainWindow = omui.MQtUtil.mainWindow()
    ptr = wrapInstance(int(mayaMainWindow), QWidget)

    global ui
    try:
        ui.close()
    except:
        pass

    ui = MyLightTool(parent=ptr)
    ui.show()


