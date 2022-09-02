import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import colorgram
from PyQt5 import uic
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import os
from PyQt5 import QtGui

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
form_class, QtBaseClass = uic.loadUiType(BASE_DIR + r'\rgb.ui')

class WindowClass(QDialog, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)
        self.graph_verticalLayout.addWidget(self.canvas)

        self.pushButton_open.clicked.connect(self.loadImageFromFile)     

    def loadImageFromFile(self) :
        fname = QFileDialog.getOpenFileName(self, 'Open file','./')

        # 이미지 선택 취소일 때
        if fname[0]=='':
            return -1

        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load(fname[0])
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(600)
        self.lbl_picture.setPixmap(self.qPixmapFileVar)
        self.filename.setText(fname[0])
        self.rgb_text.clear()

        image_file = fname[0]
        main_color_num = 256
        colors = colorgram.extract(image_file, main_color_num)
        
        values=[]
        rgb=[]
        # 텍스트
        for color in colors:
            append_text = "{}, {}%".format(str([color.rgb[0], color.rgb[1], color.rgb[2]]), str(round(color.proportion*100,2)))
            self.rgb_text.append(append_text)
            values.append(color.proportion)
            rgb.append([color.rgb[0], color.rgb[1], color.rgb[2]])
        
        # 그래프
        ax = self.fig.add_subplot(111)
        x = np.arange(1,len(values)+1)
        color_list =[]

        for i in range(len(values)):
            color_list.append((rgb[i][0]/255, rgb[i][1]/255, rgb[i][2]/255))

        ax.bar(x, values, color=color_list)
        ax.set_xticks(x)
        
        self.canvas.draw()

        self.fig.clear(True)

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_() 