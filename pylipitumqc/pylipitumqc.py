import os
import sys
import numpy as np
import pandas as pd
import glob
import initExample
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pkg_resources



stream1 =pkg_resources.resource_stream(__name__, 'data/profile_pc.txt')
stream2  = pkg_resources.resource_stream(__name__, 'data/pcpositive_targetlistms1_results_alex123_ms1.tab')
stream3 = pkg_resources.resource_stream(__name__, 'data/pctargettargetlist_results_alex123_ms2.tab')
results = pd.read_csv(stream2, sep="\t")
results = results[results['Is apex'] == 'YES']
results = results[results['Intensity'] >= 50]
results = results[results['Adduct'] == '+H+' ]
results =  results[results['Lipid species'] == 'PC 36:2' ]  
rt = results['RetentionTime'].values.tolist() 
masses = results['Measured m/z'].values.tolist()
intensities = results['Intensity'].values.tolist()
theomasses = results['Target m/z'].values.tolist()
ccs_results = pd.read_csv(stream3, sep="\t")
ccs_values = ccs_results[ccs_results['Adduct'] == '+H+' ]
ccs_values =  ccs_results[ccs_results['Lipid species'] == 'PC 36:2' ] 
css_values = ccs_values['CCs'].values.tolist() 
ccs_mass = ccs_values['Measured m/z'].values.tolist()




app = QtGui.QApplication([])
view = pg.GraphicsView()
l = pg.GraphicsLayout(border=(100,100,100))
view.setCentralItem(l)
view.show()
view.setWindowTitle('pyLipiTUMqc')
view.resize(1200,100)
pg.setConfigOptions(antialias=True)

text = """Pauling Group Computational Lipidomics TUM"""
l.addLabel(text, col=1, colspan=4)
l.nextRow()

## Put vertical label on left side
l.addLabel('LC- MS QC', angle=-90, rowspan=3)


p1 = l.addPlot(title="RT Dist")
y,x = np.histogram(rt, bins=20)
p1.plot(x,y, stepMode = True, fillLevel = 0, fillOutline = True, brush = (0,0,255,150))
p1.setLabel('left', "Frequency")
p1.setLabel('bottom', "Time")



p2 = l.addPlot(title = "Ion Mobility")
p2.plot(ccs_mass, css_values, pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
p2.setLabel('left', "CCS")
p2.setLabel('bottom', "m/z")
#p2.setLogMode(x=True, y=False)


p3 = l.addPlot(title = "Mass Spectra")
p3.plot(masses,intensities, pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
p3.setLabel('left', "Intensity")
p3.setLabel('bottom', "m/z")
p3.setLogMode(x=False, y=True)

l.nextRow()
p4 = l.addPlot(title = "LC-MS Profile",row=2, col=1, colspan=2)
p4.setLabel('left', "Intensity")
p4.setLabel('bottom', "m/z")
p4.setLogMode(x=False, y=True)
spectra = pd.read_csv(stream1, sep="\t")
offset = 0.007
lowerxlim = 786.600732 - (offset)
upperxlim = 786.600732 + (offset)
mzs = spectra['m/z'].values.tolist()
y2 = spectra['intensity'].values.tolist()    
p4.plot(mzs, y2, pen=(255,255,255,200))
lr = pg.LinearRegionItem([lowerxlim, upperxlim])
lr.setZValue(-0.007)
p4.addItem(lr)

p5 = l.addPlot(title = 'Tolerance Region',row=2, col=3)
p5.plot(mzs,y2)
p5.setLabel('left', "Intensity")
p5.setLabel('bottom', "m/z")
p5.setLogMode(x=False, y=True)
def updatePlot():
    p5.setXRange(*lr.getRegion(), padding=0)
def updateRegion():
    lr.setRegion(p5.getViewBox().viewRange()[0])
lr.sigRegionChanged.connect(updatePlot)
p5.sigXRangeChanged.connect(updateRegion)
updatePlot()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()

