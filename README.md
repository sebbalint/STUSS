# STUSS
Code database for the STUSS-Gondel solution

Die gitignore ist erstmal für python-Code generiert.

https://education.lego.com/en-us/product-resources/mindstorms-ev3/teacher-resources/python-for-ev3

https://pybricks.com/ev3-micropython/startrun.html

## Änderungen zur Struktur
- Die Gondel ist jetzt eine Klasse, dass die Threads die Attribute dieser besser übergeben bekommen können.
- Man muss in jeder Funktion die Tasten neuzuweisen, das geht mit den EventHandler-Funktionen.
- Alles in eine Klasse zu machen find ich tatsächlich irgendwie angenehmer, weil man sich dann auch nicht alles überall importieren muss.
    - also alle anderen Dateien außer der main.py sind nicht mehr nötig eig. und sind nurnoch da für Codeschnipsel.

## Anwendungssachen, die grad so implementiert sind vorerst
- backspace-Taste am EV3 ist immer als Notstopptaste verwendet/reserviert
- im free_transit sind die Richtungen die Richtungen und die Mitteltaste ist zurück zum Menü
    - kann man später so machen, dass der doppelt gedrückt werden muss um das ausversehen Drücken zu entschärfen

## Orientierungsprojekte
- https://github.com/ev3dev/ev3dev-lang-python-demo/blob/stretch/robots/misc/console_menu.py
- https://github.com/ev3dev/ev3dev-lang-python-demo/blob/stretch/robots/GRIPP3R/GRIPP3R.py
- https://github.com/ev3dev/ev3dev-lang-python-demo/blob/stretch/robots/EXPLOR3R/auto-drive.py
- https://github.com/ev3dev/ev3dev-lang-python-demo/blob/stretch/robots/EXPLOR3R/remote-control.py

## Ideen
- 2 Modi:
    - Automatisches hin und herfahren gestartet durch Knopfdruck
    - genaue Fernsteuerung mit Pfeiltasten

- Menü zur Auswahl
- Not-Stop Knopf

## Multithreading Basics
Für den Not-Stop Knopf brauchen wir Multithreading hier ist eine einfache Erklärung:
https://sites.google.com/site/ev3devpython/learn_ev3_python/threads