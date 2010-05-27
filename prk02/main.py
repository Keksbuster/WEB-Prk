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

class WebServer:
    # ----------------------------------------------------------
    def __init__(self):
    # ----------------------------------------------------------
        pass
    
    def new(self):
        self.datastore = Warehouse()
    
    def load(self, file):
        inp = open(file, 'rb')
        self.datastore = load(inp)
        inp.close()
    
    def save(self, file):
        out = open(file, 'wb')
        dump(self.datastore, out)
        out.close()
    
    # ----------------------------------------------------------
    def Message_p(self, start_response, Status_spl, Message_spl):
    # ----------------------------------------------------------
        response_headers = [('Content-type','text/plain')]
        start_response(Status_spl, response_headers)
        return [Message_spl]
    
    # ----------------------------------------------------------
    def ServeFile_p(self, start_response, Path_spl):
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
            return self.Message_p(start_response, "404 Not found", "Datei " + Path_spl + " nicht vorhanden")
    
    # ----------------------------------------------------------
    def Static_p(self, environ, start_response):
    # ----------------------------------------------------------
        Path_s = environ["PATH_INFO"]
        (head, tail) = os.path.split(Path_s)
        if tail == "":
            return self.Message_p(start_response, '404 Not found', 'Static : unbekannte Ressource' + Path_s + '\n')
        else:
            return self.ServeFile_p(start_response, "static/" + tail)
    
    def Test_p(self, environ, start_response):
        status = '200 OK'
        response_headers = [('Content-type','text/html')]
        Parameter_o = {}
        if "REQUEST_METHOD" in environ:
            Method_s = environ["REQUEST_METHOD"]
        if Method_s == "GET":
            Parameter_o = cgi.parse_qs(environ["QUERY_STRING"])
            # weiter verarbeiten ...
        elif Method_s == "POST":
            Input_o = environ["wsgi.input"]
            len_i = int(environ["CONTENT_LENGTH"])
            Content_s = Input_o.read(len_i)
            Parameter_o = cgi.parse_qs(Content_s)
            print str(Parameter_o)
            # weiter verarbeiten ...
        return self.Message_p(start_response, '200 OK', 'Eingabe war : ' + str(Parameter_o) + '\n')
    # ----------------------------------------------------------
    def Home_p(self, environ, start_response): 
    # ----------------------------------------------------------
        Path_s = environ["PATH_INFO"]
        if Path_s == "/":
            # keine weiteren Angaben im Ressource-Pfad
            # Startseite anzeigen
            return self.Message_p(start_response, '200 OK' , dumps(self.datastore))
        else:
            return self.Message_p(start_response, '404 Not found', 'Home : unbekannte Anforderung' + Path_s + '\n')
      

def main():
    # ----------------------------------------------------------
    # das DispatchInfo-Objekt erhaelt ein Dictionary mit Zuordnungen von Pfaden und Verarbeitungsfunktionen
    # bei Anfragen wird  versucht, die laengste Uebereinstimmung im Pfad zu finden
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
    
    webserver = WebServer()
    try:
        webserver.load('data.dat')
    except:
        print "New File!"
        webserver.new()
    
    DispatchInfo = wsgiserver.WSGIPathInfoDispatcher({'/': webserver.Home_p, '/static':webserver.Static_p, '/test': webserver.Test_p})
   
    # Server lauscht auf Port 8080, IP ist localhost
    server = wsgiserver.CherryPyWSGIServer(('0.0.0.0', 8080), DispatchInfo, timeout=100)
   
    try:
        print "Server auf http://localhost:8080 gestartet..."
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print "\nServer gestoppt...\t",
        webserver.save('data.dat')
        print "Daten gesichert!"
   
# ----------------------------------------------------------
# ----------------------------------------------------------
    return 0

if __name__ == '__main__':
    main()
