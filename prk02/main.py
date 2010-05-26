#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       main.py
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

from datastore import Warehouse
from cPickle import dump, load, dumps, loads
import wsgiserver
import cgi
import os.path
import os

# ----------------------------------------------------------
def Message_p(start_response, Status_spl, Message_spl):
# ----------------------------------------------------------
    response_headers = [('Content-type','text/plain')]
    start_response(Status_spl, response_headers)
    return [Message_spl]

# ----------------------------------------------------------
def ServeFile_p(start_response, Path_spl):
# ----------------------------------------------------------
   # hier nur Auswertung von Textdateien, XHTML-Dateien und CSS-Dateien
    try:
        File_o = file(Path_spl, "r")
        Content_s = File_o.read()
        File_o.close()
      
        response_headers = [('Content-type','text/plain')]
        (root, ext) = os.path.splitext(Path_spl)
        if ext == ".css":
            response_headers = [('Content-type','text/css')]
        elif ext == ".html":
            response_headers = [('Content-type','text/html')]

        start_response("200 OK", response_headers)
        return [Content_s]
    except:
        return Message_p(start_response, "404 Not found", "Datei " + Path_spl + " nicht vorhanden")

# ----------------------------------------------------------
def Static_p(environ, start_response):
# ----------------------------------------------------------
    Path_s = environ["PATH_INFO"]
    (head, tail) = os.path.split(Path_s)
    if tail == "":
        return Message_p(start_response, '404 Not found', 'Static : unbekannte Ressource' + Path_s + '\n')
    else:
        return ServeFile_p(start_response, "static/" + tail)

# ----------------------------------------------------------
def Home_p(environ, start_response): 
# ----------------------------------------------------------
    Path_s = environ["PATH_INFO"]
    if Path_s == "/":
        # keine weiteren Angaben im Ressource-Pfad
        # Startseite anzeigen
        return Message_p(start_response, '200 OK' , os.environ["DATAFILE"])
    else:
        return Message_p(start_response, '404 Not found', 'Home : unbekannte Anforderung' + Path_s + '\n')
      

def main():
    # ----------------------------------------------------------
    # das DispatchInfo-Objekt erhaelt ein Dictionary mit Zuordnungen von Pfaden und Verarbeitungsfunktionen
    # bei Anfragen wird versucht, die laengste Uebereinstimmung im Pfad zu finden
    # gelingt dies, wird der restliche Bestandteile des Ressource-Pfads im Environment unter PATH_INFO abgelegt
    #
    # Beispiele:
    # /                   -> Prozedur Home_p
    # /unbekannt          -> Prozedur Home_p
    # /newsletter         -> Prozedur Newsletter_p
    # /newsletter/css     -> Prozedur Newsletter_p
    # /newsletter/js      -> Prozedur Newsletter_p
    # /newsletter/js/lib  -> Prozedur Newsletter_p
    # /newsletter/js/app  -> Prozedur Newsletter_p
    # /static             -> Prozedur Static_p
    
    try:
        inp = open('data.dat', 'rb')
        datastore = load(inp)
        inp.close()
    except:
        print "New File!"
        datastore = Warehouse()
    
    os.environ['DATAFILE'] = dumps(datastore)
    DispatchInfo = wsgiserver.WSGIPathInfoDispatcher({'/': Home_p, '/static':Static_p})
   
    # Server lauscht auf Port 8080, IP ist localhost
    server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8080), DispatchInfo, timeout=100)
   
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
        out = open('data.dat', 'wb')
        dump(datastore, out)
        out.close()
   
# ----------------------------------------------------------
# ----------------------------------------------------------
    return 0

if __name__ == '__main__':
    main()
