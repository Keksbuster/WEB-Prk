#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       datastore.py
#       
#       Copyright 2010 Christian Vervoorts <christian@eeepc>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

# ----------------------------------------------------------
class Lagerbereich:
# ----------------------------------------------------------
    def __init__(self, name):
        self.name = name
        self.artikle_list = []
    
    def __str__(self):
        return self.name

# ----------------------------------------------------------
class Artikle:
# ----------------------------------------------------------
    def __init__(self, name, lagerort, mindest_menge, max_menge, aktuelle_menge):
        self.name = name
        self.lagerort = lagerort
        self.mindest_menge = mindest_menge
        self.max_menge = max_menge
        self.aktuelle_menge = aktuelle_menge
    
    def __str__(self):
        return "%s, %s" % (self.name, self.lagerort)

# ----------------------------------------------------------
class Warehouse:
# ----------------------------------------------------------
    def __init__(self):
        self.lagerbereich = {}
        self.produkte = {}

    def newProduct(self, name, lagerort, mindest_menge, max_menge, aktuelle_menge):
        pass

    def newLagerort(self, name):
        pass
    
    def editProduct(self, name, lagerort, mindest_menge, max_menge, aktuelle_menge):
        pass

    def editLagerort(self, name):
        pass

    def deleteProduct(self, name):
        pass
    
    def deleteLagerort(self, name):
        pass

    def getProducts(self):
        pass
    
    def getProduct(self, name):
        pass
    
    def getLagerorte(self):
        pass
    
    def getLagerort(self, name):
        pass   
         
         
def main():
    test = Lagerbereich("lager B")
    artikle = Artikle("Artikle 1", "lager B", 5, 20, 10)
    
    print artikle
    print test
    
    return 0

if __name__ == '__main__':
    main()
