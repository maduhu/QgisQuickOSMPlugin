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
from QuickOSM.ProcessingQuickOSM import *

from QuickOSM.CoreQuickOSM.FileQuery import FileQuery
from os.path import isfile,join,basename,dirname,abspath

class ReadIniFilePathGeoAlgorithm(GeoAlgorithm):
    '''
    Read an INI file 
    '''
    
    def __init__(self):
        self.INI_FILEPATH = 'QUERY_FILE'
        self.LAYERS = ['multipolygons', 'multilinestrings', 'lines', 'points']
        self.WHITE_LIST = {}
        for layer in self.LAYERS:
            self.WHITE_LIST[layer] = 'WHITE_LIST_'+layer
        GeoAlgorithm.__init__(self)

    def defineCharacteristics(self):
        self.name = "Read an ini file from string"
        self.group = "Tools"
        
        self.addParameter(ParameterString(self.INI_FILEPATH, 'Filepath (ini)', '', False))
        
        for layer in self.LAYERS:
            self.addOutput(OutputString(self.WHITE_LIST[layer],'White list '+ layer +' layer'))
        
        self.addOutput(OutputString('QUERY_STRING',"Query string"))

    def help(self):
        locale = QSettings().value("locale/userLocale")[0:2]
        locale = "." + locale

        currentFile = __file__
        if currentFile.endswith('pyc'):
            currentFile = currentFile[:-1]
        currentFile = basename(currentFile)
        
        helps = [currentFile + locale +".html", currentFile + ".html"]
        
        docPath = join(dirname(dirname(dirname(abspath(__file__)))),'doc')
        for helpFileName in helps :
            fileHelpPath = join(docPath,helpFileName)
            if isfile(fileHelpPath):
                return False, fileHelpPath
        
        return False, None
    
    def getIcon(self):
        return QIcon(dirname(__file__) + '/../../icon.png')

    def processAlgorithm(self, progress):
        self.progress = progress
        self.progress.setInfo("Reading the ini file")
                
        filePath = self.getParameterValue(self.INI_FILEPATH)
        iniFile = FileQuery(filePath)
        iniDict = None
        if iniFile.isValid():
            iniDict = iniFile.getContent()
        
        self.setOutputValue('QUERY_STRING',iniDict['metadata']['query'])
        
        for layer in self.LAYERS:
            csv = iniDict['layers'][layer]['columns']
            self.setOutputValue(self.WHITE_LIST[layer],csv)