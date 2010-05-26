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
    
    def edit(self, name, lagerort, mindest_menge, max_menge, aktuelle_menge):
        self.name = name
        self.lagerort = lagerort
        self.mindest_menge = mindest_menge
        self.max_menge = max_menge
        self.aktuelle_menge = aktuelle_menge
    
    def increment(self):
        if(self.aktuelle_menge +1 > self.max_menge):
            return 1
        else:
            self.aktuelle_menge += 1
            return 0
            
    def __str__(self):
        return "%s, %s" % (self.name, self.lagerort)
    

# ----------------------------------------------------------
class Warehouse:
# ----------------------------------------------------------
    def __init__(self):
        self.lagerbereich = {}
        self.produkte = {}

    def newProduct(self, name, lagerort, mindest_menge, max_menge, aktuelle_menge):
        try:
            self.produkte[name] = Artikle(name, lagerort, mindest_menge, max_menge, aktuelle_menge)
            return 0
        except:
            return 1

    def newLagerort(self, name):
        try:
            self.lagerbereich[name] = Lagerbereich(name)
            return 0
        except:
            return 1
    
    def editProduct(self, name, lagerort, mindest_menge, max_menge, aktuelle_menge):
        self.produkte[name].edit(name, lagerort, mindest_menge, max_menge, aktuelle_menge)

    def editLagerort(self, name):
        pass

    def deleteProduct(self, name):
        del self.produkte[name]
    
    def deleteLagerort(self, name):
        del self.lagerbereich[name]

    def getProducts(self):
        return self.produkte
    
    def getProduct(self, name):
        return self.produkte[name]
    
    def getLagerorte(self):
        return self.lagerbereich
    
    def getLagerort(self, name):
        return self.lagerbereich[name]   
         
         
def main():
    database = Warehouse()
    database.newLagerort("lager B")
    database.newProduct("Artikle 1", "lager B", 5, 20, 10)
    
    print database.getProduct("Artikle 1")
    print database.getLagerort("lager B")
    
    return 0

if __name__ == '__main__':
    main()
