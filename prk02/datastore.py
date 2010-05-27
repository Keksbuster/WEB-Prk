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
    """ Die Klasse Lagerbereich
        
        Diese Klasse enthält einen Lagerbereich und eine Liste mit allen Artikle die zu diesem Lagerbereich gehören
        """ 
    def __init__(self, name):
        self.name = name
        self.artikle_list = []
    
    def AddProduct(self, name):
        if(name in self.artikle_list):
            raise "Key exist"
        else:
            self.artikle_list.append(name)
    
    def __str__(self):
        string = self.name + ";"
        for (nr, elm) in enumerate(self.artikle_list):
            if(nr == 0):
                string += elm
            else:
                string += ";" + elm
        return string

# ----------------------------------------------------------
class Artikle:
    """ Die Artikle-Klasse
        
        Die Artikle Klasse enthält einen Artikle und verwaltet die Informationen und den Lagerbestand dieses Artikles.
        """
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
    
    def decrement(self):
        if(self.aktuelle_menge -1 < self.mindest_menge):
            return 1
        else:
            self.aktuelle_menge -= 1
            return 0
            
    def __str__(self):
        return "%s;%s;%d;%d;%d" % (self.name, self.lagerort, self.mindest_menge, self.max_menge, self.aktuelle_menge)
    

# ----------------------------------------------------------
class Warehouse:
    """ Die Warehouse-Klasse
    
        Die Warehouse-Klasse beinhaltet ein oder mehrere Lagerbereiche und Artikle und verwaltet und organisiert das zusammenspiel zwischen diese Klassen.
        Eigentliche Schnittstelle zum Nutzer
        """
    def __init__(self):
        self.lagerbereich = {}
        self.produkte = {}

    def newProduct(self, name, lagerort, mindest_menge, max_menge, aktuelle_menge):
        try:
            self.lagerbereich[lagerort].AddProduct(name)
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
        #FIXME Brauchen wir die Methode eigentlich?
        pass

    def deleteProduct(self, name):
        lager = self.produkte[name].lagerort
        self.lagerbereich[lager].artikle_list.remove(name)
        del self.produkte[name]
    
    def deleteLagerort(self, name):
        if(len(self.lagerbereich[name].artikle_liste) > 0):
            return 1
        else:
            del self.lagerbereich[name]
            return 0

    def getProducts(self):
        return self.produkte
    
    def getProduct(self, name):
        return self.produkte[name]
    
    def getLagerorte(self):
        return self.lagerbereich
    
    def getLagerort(self, name):
        return self.lagerbereich[name]   
         
         
def main():
    """ main Funktion
        
        Testet nur ein paar Funktionen mehr nicht
        """
    database = Warehouse()
    database.newLagerort("lager B")
    database.newProduct("Artikle 1", "lager B", 5, 20, 10)
    database.newProduct("Artikle 2", "lager B", 8, 12, 9)
    
    print database.getProduct("Artikle 1")
    print database.getProduct("Artikle 2")
    print database.getLagerort("lager B")
    
    database.newProduct("Artikle 1", "lager C", 5, 20, 10)

    database.getProduct("Artikle 1").increment()
    database.getProduct("Artikle 2").decrement()
    
    print
    print database.getProduct("Artikle 1")
    print database.getProduct("Artikle 2")
    print database.getLagerort("lager B")
    print
    print database.getProducts()
    
    return 0

if __name__ == '__main__':
    main()
