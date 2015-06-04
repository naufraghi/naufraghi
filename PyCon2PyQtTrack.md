# PyQt Track per il PyCon2 #

Tempi: 1h di contenuti + 30m di tempo per gli interventi

# Introduzione #

Il tutorial copre la realizzazione di due semplici applicazioni Qt, una ToDo list e un Gui per giocare a Sudoku.
L'intento è di presentare alcune delle caratteristiche vincenti del framework Qt, in particolare:
  * Signal e Slot
  * QWidget
  * QSettings
  * Designer
  * QStyleSheet
  * QPainter
  * Webkit

# Organizzazione #

  * Presentazione features di Qt, esempi scelti dal QtDemo
    * Grafica
    * Stampa
    * i18n

  * Creazione di una semplice applicazione
    * Todo manager, con topic, priorità e scadenza
    * GUI facile senza Designer
    * QSettings
    * QStyleSheet
    * Signals e Slots

  * Potenzialità del Designer e del QPainter
    * Gioco Sudoku
    * Stampa Sudoku

  * Uso di webkit
  * Impacchettamento con PyInstaller sviluppati per la presentazione.

# Idee forse da integrare #

Gotcha sul funzionamento di super() su classi PyQt: http://docs.huihoo.com/pyqt/pyqt4.html#super-and-pyqt-classes