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
Wir haben versucht das Entwurfsmuster Observer Pattern anzuwenden. Dabei ist unser Observer quasi die Spielinstanz, welche auf entsprechende Eingaben der Spieler reagiert und über das Spielbrett Information an alle weiteren teilnehmenden Spielern weitergibt.
 

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
Sie können das Projekt mit Docker starten. Die Befehle dafür sind in der README.md beschrieben.

Während der Entwicklung haben wir das Projekt über Python (python3 app.py) gestartet, im /database/db_manager.py muss man dafür allerdings eine Zeile (Zeile 11) wie im Kommentar beschrieben anpassen und die nötigen Pythonmodule (requirements.txt) installiert haben.


## Dokumentation (Entwicklersicht)

Grundlegend haben wir 4 größere Komponenten:

### 1. Datenbank mit sqllite3
Wir haben dabei eine DB_Manager Klasse in python geschrieben mit der wir die Datenbank (kundendatenbank.sql) zur Laufzeit bearbeiten und entsprechende Information gezielt auslesen können.

### 2. Backend
Wir verwenden verschiedene Klassen zur Abstraktion der Blokus Objekte.
Dazu zählen:

1. Blöcke 
2. Spieler (Player)
3. Spielbrett (Board)
4. Spiel (Game/AI-Game)
5. AI-Spieler (AIPlayer)

Die Blöcke und das Spielbrett sind dabei intern als mehrdimensionale Arrays dargestellt. Die Blöcke können beispielsweise ihren internen Zustand (Attribut block_matrix) über die Rotationsfunktion und Reflectfunktion ändern. Jeder Spieler beginnt dann mit einem Dictionary mit den 21 verschiedenen Blockinstanzen

Eine zentrale Funktion des Spielbretts ist die is_move_valid bzw. is_first_move_valid die bestimmt ob ein Zug auf dem aktullen Stand des Spielfelds gültig ist

Der AI-Spieler basiert auf folgenden Funktionalitäten.
1. Er speichert seiner vorhandenen "Corners" (potenzielle Einfügestellen)
2. Er probiert auf einen kopierten Demoboard (welches den aktuellen Stand des Boards darstellt) verschiedene Züge aus und bewertet diese abhängig von den neue generierten "Corners".
3. Ziel des AI-Spielers ist es möglichst mittig zu spielen und möglichst viele neue "Corners" zu erzeugen.
4. Dabei kann es theoretisch gegen Ende des Spiels passieren das der AI-Spieler eine Einfügemöglichkeit übersieht (begrenzte Schleifedurchläufe bei der Evaluierung der Züge) und so frühzeitig aufgibt.
5. Die Stärke des AI-Spielers kann mit einer entsprechenden Anzahl an Schleifendurchläufen (AIPlayer.py Zeile 431 und 449 -> Verhältnis der beiden Schleifendurchläufe zueinander möglichst beibehalten) angepasst werden (je mehr Durchläufe desto bessere Züge).


### 3. Server und Sockets
Wir nutzen Flask als Webserver und SocketIO für die Socket Events.

Wir haben dabei verschiedene Routen für Authentifizierungsfunktionalitäten (auth.py -> Login, SignUp, Reset_PW etc.) die Lobby/Spielfunktionalitäten (lobby.py -> start_game, join_lobby, socketevents) und generelle Routen (main.py -> home, profile).

Bei unserem Aufbau gab es vor allem Probleme mit der Gruppierung von Users in Lobbys, dies sollte normalerweise über das SocketIO Modul von Python abgedeckt werden, konnten wird allerdings bei uns nicht umsetzen. Deshalb werden die Lobbyinformation aktuell in die Datenbank gespeichert und für die beiden Lobbys gibt es unterschiedliche Socket Events.

Hier könnte die Lobbystruktur weiterentwicklet werden sodass die Lobbyzuteilung in der Session wirklich umgesetzt wird und nicht über die Datenbank läuft.

### 4. Frontend
Für das Frontend verwendeten wir Javascript, HTML und CSS


(Was müssen externe Entwickler über die Struktur des Projektes wissen? Welche Erweiterungsmöglichkeiten gibt es? Welches sind die wichtigsten Klassen/Module?)


## Fazit
Das Projekt hat spaß gemacht und besonders spannend war die Implementierung der KI, die sehr Interessant und Lehrreich war. Im Verlauf der Entwicklung konnten wir alle unsere Programmierfähigkeiten erweitern und neues Wissen erlangen. Wir stießen allerdings auf Herausforderungen, insbesondere im Bereich des Frontends und bei der Implementierung der Sockets - ein Gebiet, das für uns alle im Team neu war. Aufgrund der zeitlichen Beschränkungen und der parallelen Arbeit an anderen Projekten dieses Semesters konnten wir uns nicht vollständig darauf konzentrieren.

Für zukünftige Projekte planen wir, tägliche Meetings einzuführen, da wir festgestellt haben, dass regelmäßige Abstimmungen sehr hilfreich und aufschlussreich sind. Dies hängt jedoch stark von der Kompatibilität mit dem Semesterplan ab, denn im aktuellen Zeitrahmen war dies nicht umsetzbar.

Außerdem möchten wir beim nächsten Mal unsere Webanwendung nicht lokal hosten, sondern einen externen Hosting-Dienst nutzen.

Zusammengefasst hat das Projekt, trotz der knappen Zeit, unsere Kompetenzen als Softwareentwickler gestärkt und uns wertvolle Einblicke in einem Softwareporjekt gebracht (Beginn des Projekts bis Abschluss des Projekts alle Phasen miterlebt).





