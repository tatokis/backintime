# Translated and extended from the TreeSortFilter C++ Class of the following
#
#/****************************************************************************
#**
#** Copyright (C) 2009 Nokia Corporation and/or its subsidiary(-ies).
#** Contact: Nokia Corporation (qt-info@nokia.com)
#**
#** This file is part of the test suite of the Qt Toolkit.
#**
#** $QT_BEGIN_LICENSE:LGPL$
#** Commercial Usage
#** Licensees holding valid Qt Commercial licenses may use this file in
#** accordance with the Qt Commercial License Agreement provided with the
#** Software or, alternatively, in accordance with the terms contained in
#** a written agreement between you and Nokia.
#**
#** GNU Lesser General Public License Usage
#** Alternatively, this file may be used under the terms of the GNU Lesser
#** General Public License version 2.1 as published by the Free Software
#** Foundation and appearing in the file LICENSE.LGPL included in the
#** packaging of this file.  Please review the following information to
#** ensure the GNU Lesser General Public License version 2.1 requirements
#** will be met: http://www.gnu.org/licenses/old-licenses/lgpl-2.1.html.
#**
#** In addition, as a special exception, Nokia gives you certain
#** additional rights. These rights are described in the Nokia Qt LGPL
#** Exception version 1.0, included in the file LGPL_EXCEPTION.txt in this
#** package.
#**
#** GNU General Public License Usage
#** Alternatively, this file may be used under the terms of the GNU
#** General Public License version 3.0 as published by the Free Software
#** Foundation and appearing in the file LICENSE.GPL included in the
#** packaging of this file.  Please review the following information to
#** ensure the GNU General Public License version 3.0 requirements will be
#** met: http://www.gnu.org/copyleft/gpl.html.
#**
#** If you are unsure which license is appropriate for your use, please
#** contact the sales department at http://www.qtsoftware.com/contact.
#** $QT_END_LICENSE$
#**
#****************************************************************************/

from PyQt4 import QtCore, QtGui

class TreeSortFilter(QtGui.QSortFilterProxyModel):
	def __init__(self, parent = None): 
		QtGui.QSortFilterProxyModel.__init__(self)
	
	def filterAcceptsRow(self, sourceRow, sourceParent):
		
		if self.filterRegExp().isEmpty():
			return True
		
		current = QtCore.QModelIndex(self.sourceModel().index(sourceRow, self.filterKeyColumn(), sourceParent))
		
		if self.sourceModel().hasChildren(current):
			atLeastOneValidChild = False
			i = 0
			while not atLeastOneValidChild:
				child = QtCore.QModelIndex(current.child(i, current.column()))
				
				if not child.isValid(): # No Valid Child
					break
				
				atLeastOneValidChild = self.filterAcceptsRow(i, current)
				i = i+1
			
			currentItemAccepted  = ( self.filterRegExp().indexIn(self.sourceModel().data(current)) != -1 )
			return atLeastOneValidChild or currentItemAccepted
		
		currentItemAccepted  = ( self.filterRegExp().indexIn(self.sourceModel().data(current)) != -1 )
		return bool(currentItemAccepted)

	def invalidateFilter(self):
		QtGui.QSortFilterProxyModel.invalidateFilter( self )
		return
