# Projektdokumentation (Gruppe)

**Gruppenmitglieder:** Leon Ams, Sercan Berkpinar, Levin Bolbas, Lukas Buser
**Source Code Repo URL:** https://github.com/Levoo777/AdvancedSoftwareEngineering

## Requirements
Die Requirements wurden mithife von Github Issues erfasst. (https://github.com/Levoo777/AdvancedSoftwareEngineering/issues)

## Vorgehen
Am anfang des Semester gabe es wöchentliche Termine, welche aufgrund des steigendem Pensums des Semester in größere Zeitabstände gegen Ende des Semester abgehalten wurden.
Die Aufgaben wurden anhand der im vorhinein bekannten Wissensstand verteilt. Die Task wurden in den Besprechungstermine festgelegt und auch reviewt.
Im Projekt bestand der Haupteil der Entwicklung in Pair Programming.

## Rollen
Leon Ams -> Entwickler
Sercan Berkpinar -> Product Owner, Entwickler
Levin Bolbas -> Entwickler
Lukas Buser -> Scrum Master, Entwickler

Die Rollen wurden wie am Anfang festgelegt beibehalten.

## Architektur (siehe Tasks in Vorlesung)
Das Architekturdesign für das Blokus Webgame ist strukturiert und modular aufgebaut, was folgende Schichten umfasst:

- Web Interface: Die oberste Ebene, die als Benutzerschnittstelle dient, ermöglicht Spielern die Interaktion mit dem Spiel über ihren Browser.
- Authentication: Diese Sicherheitsschicht verwaltet die Authentifizierung von Nutzern, gewährleistet den autorisierten Zugang und schützt vor unbefugter Nutzung.
- Frontend Code (Visualization of Blokus): Verantwortlich für die Darstellung des Spiels, einschließlich der Spieloberfläche und visuellen Elemente. Diese Schicht nutzt Flask Socket.io zur Handhabung der Echtzeit-Webkommunikation.
- Flask Socket.io: Eine dedizierte Middleware-Schicht, die die Echtzeit-Websocket-Kommunikation zwischen dem Frontend und dem Server ermöglicht, was für Features wie den Gamechat und die Synchronisation des Spielfelds essentiell ist.
- Python Flask: Die Kern-Webanwendungsschicht, die die Serverlogik und Anfragenverarbeitung übernimmt. Sie verbindet die Frontend-Aktionen mit den Backend-Prozessen.
- Backend Code (Logic of Blokus): Hier befindet sich die Geschäftslogik des Spiels, die zentrale Spielmechaniken, Regeln und Entscheidungsprozesse steuert.
- Database: Die unterste Schicht, die für die Speicherung aller persistenten Daten zuständig ist, wie Benutzerprofile, Spielstände und historische Daten.

Anschließend haben wir ein Use Case Diagramm erstellt und daraus resultierend ein Klassendiagramm erstellt.

Die drei erstellten Diagramme sind hier zu finden: https://github.com/Levoo777/AdvancedSoftwareEngineering/tree/main/dokumentation

## Design (siehe Tasks in Vorlesung)
Wir haben das Entwurfsmuster Observer Pattern angewendet.
 

## Qualitätssicherung
(Welche Art von Tests haben wir implementiert (Beispiele)? Welche Abdeckung wurde erreicht (Nachweis)?)
Wir haben Unittests geschrieben mithilfe des Moduls Unittest von Python. Hiebei wurde ein eigener Custom Test Runner geschrieben welcher über die standard Funktionaität von dem Unittest Modul hinaus geht, um eine übersichtlichere Ausgabe zu erhalten.

Getestet wurden die Funktionen:
- Überprüfen ob ein Zug valide ist
- Überprüfen ob die Spieler Blöcke korrekt sind

Da diese die Grundbausteine von Blokus sind wurden diese immer wieder Ausgeführt um zu testen das nach neuen implementierungen noch alles stimmt.

## Reuse
Flask -> Flask ist ein leichtgewichtiges Web-Framework für Python
Flask_Socketio -> Flask_SocketIO ermöglicht Echtzeitkommunikation zwischen dem Webserver und dem Client über WebSockets
Flask_Login -> Flask_Login stellt Benutzerauthentifizierungs-Funktionalitäten bereit 
SQLlite3 -> SQLite3 ist eine leichtgewichtige, dateibasierte Datenbank, die einfache Datenpersistenz ermöglicht, ohne die Notwendigkeit eines separaten Datenbank-Servers.

## Continuous Integration
Zu Beginn wurde Frontend und Backend seperat entwickelt. Sobald das AI Game fertig implementiert wurde im Backend, begann die erste Integration mit dem Frontend. Hierbei wurde Pair Programming angewendet, von jeweils einem aus dem Frontend und einem aus dem Backend. Diese haben miteinander die integration durchgeführt. 
Nachfolgend wurde jede weitere implementierung aus dem Backend, direkt mit dem Frontend integriert um zu validieren, dass die Funktion auf der Weboberfläsche wie gewünscht agiert.

## Dokumentation (Benutzersicht)
(Wie wird die Software gebaut/gestartet?)


## Dokumentation (Entwicklersicht)
(Was müssen externe Entwickler über die Struktur des Projektes wissen? Welche Erweiterungsmöglichkeiten gibt es? Welches sind die wichtigsten Klassen/Module?)


## Fazit
Das Projekt hat spaß gemacht und besonders spannend war die Implementierung der KI, die sehr Interessant und Lehrreich war. Im Verlauf der Entwicklung konnten wir alle unsere Programmierfähigkeiten erweitern und neues Wissen erlangen. Wir stießen allerdings auf Herausforderungen, insbesondere im Bereich des Frontends und bei der Implementierung der Sockets - ein Gebiet, das für uns alle im Team neu war. Aufgrund der zeitlichen Beschränkungen und der parallelen Arbeit an anderen Projekten dieses Semesters konnten wir uns nicht vollständig darauf konzentrieren.

Für zukünftige Projekte planen wir, tägliche Meetings einzuführen, da wir festgestellt haben, dass regelmäßige Abstimmungen sehr hilfreich und aufschlussreich sind. Dies hängt jedoch stark von der Kompatibilität mit dem Semesterplan ab, denn im aktuellen Zeitrahmen war dies nicht umsetzbar.

Außerdem möchten wir beim nächsten Mal unsere Webanwendung nicht lokal hosten, sondern einen externen Hosting-Dienst nutzen.

Zusammengefasst hat das Projekt, trotz der knappen Zeit, unsere Kompetenzen als Softwareentwickler gestärkt und uns wertvolle Einblicke in einem Softwareporjekt gebracht (Beginn des Projekts bis Abschluss des Projekts alle Phasen miterlebt).





