# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
                                 A QGIS plugin
 OSM's Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from QuickOSM import *
from QuickOSMWidget import *
from osm_file import Ui_ui_osm_file
from os.path import dirname,abspath,join,isfile
from QuickOSM.CoreQuickOSM.Parser.OsmParser import *
from qgis.utils import iface

class OsmFileWidget(QuickOSMWidget, Ui_ui_osm_file):
    def __init__(self, parent=None):
        '''
        OsmFileWidget constructor
        '''
        QuickOSMWidget.__init__(self)
        self.setupUi(self)
        
        #Set default osmconf
        self.defaultOsmConf = join(dirname(dirname(abspath(__file__))),"osmconf.ini")
        if not isfile(self.defaultOsmConf):
            self.defaultOsmConf = ''
        self.lineEdit_osmConf.setText(self.defaultOsmConf)
        self.pushButton_openOsmFile.setEnabled(False)
        
        #Connect
        self.pushButton_browseOsmFile.clicked.connect(self.setOsmFilePath)
        self.pushButton_browseOsmConf.clicked.connect(self.setOsmConfPath)
        self.lineEdit_osmConf.textEdited.connect(self.disableRunButton)
        self.lineEdit_osmFile.textEdited.connect(self.disableRunButton)
        self.pushButton_openOsmFile.clicked.connect(self.openFile)
        self.pushButton_resetIni.clicked.connect(self.resetIni)
        
    def setOsmFilePath(self):
        '''
        Fill the osm file
        '''
        osmFile = QFileDialog.getOpenFileName(parent=None, caption=QApplication.translate("QuickOSM", 'Select *.osm or *.pbf'),filter="OSM file (*.osm *.pbf)")
        self.lineEdit_osmFile.setText(osmFile)
        self.disableRunButton()
            
    def setOsmConfPath(self):
        '''
        Fill the osmConf file
        '''
        osmConf = QFileDialog.getOpenFileName(parent=None, caption=QApplication.translate("QuickOSM", 'Select osm conf'), filter="OsmConf file (*.ini)")
        if osmConf:
            self.lineEdit_osmConf.setText(osmConf)
        self.disableRunButton()
        
    def resetIni(self):
        '''
        Reset the default osmConf file
        '''
        self.lineEdit_osmConf.setText(self.defaultOsmConf)
            
    def disableRunButton(self):
        '''
        If the two fields are empty
        '''
        if self.lineEdit_osmConf.text() and self.lineEdit_osmFile.text():
            self.pushButton_openOsmFile.setEnabled(True)
        else:
            self.pushButton_openOsmFile.setEnabled(False)
        
    def openFile(self):
        '''
        Open the osm file with the osmconf
        '''
        #Get fields
        osmFile = self.lineEdit_osmFile.text()
        osmConf = self.lineEdit_osmConf.text()
        
        #Which geometry at the end ?
        outputGeomTypes = self.getOutputGeomTypes()
        
        try:
            if not outputGeomTypes:
                raise OutPutGeomTypesException
            
            if not isfile(osmFile):
                raise FileDoesntExistException(suffix="*.osm or *.pbf")
            
            if not isfile(osmConf):
                raise FileDoesntExistException(suffix="*.ini")
            
            osmParser = OsmParser(osmFile, loadOnly=True, osmConf=osmConf, layers = outputGeomTypes)
            layers = osmParser.parse()
            for layer,item in layers.iteritems():
                QgsMapLayerRegistry.instance().addMapLayer(item)
            
        except GeoAlgorithmExecutionException,e:
            self.displayGeoAlgorithmException(e)
        except Exception,e:
            self.displayException(e)

class OsmFileDockWidget(QDockWidget):
    def __init__(self, parent=None):
        QDockWidget.__init__(self)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.setWidget(OsmFileWidget())
        self.setWindowTitle(QApplication.translate("ui_osm_file", "QuickOSM - OSM File"))