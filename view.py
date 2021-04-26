"""Fisierul contine clasa corespunzatoare viewport-ul aplicatiei"""

from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene)
from PyQt5.QtCore import (QBasicTimer, QRectF)
from PyQt5.QtGui import QPainter

from engine import GraphEngine


class GraphicsView(QGraphicsView):
    """Viewport-ul aplicatiei

    Aceasta clasa este responsabila pentru vizualizarea
    nodurilor, muchiilor, respectiv si a animatiilor
    acestora.

    Atribute
    --------
    frame_graph : QFrame
        este parintele viewport-ului
    engine : GraphEngine
        engin-ul grafului
    frameRateTimer : QBasicTimer
        timer-ul pentru a urmarii frame rate-ul
    scene : QGraphicsScene
        scene-ul unde se vor afisa nodurile si muchiile

    Metode
    ------
    resizeEvent(event)
        redimensionarea viewport-ului
    timerEvent(timerEvent)
        urmareste frame rate-ul
    """

    def __init__(self, parent):
        super(GraphicsView, self).__init__(parent=parent)
        self.setRenderHint(QPainter.HighQualityAntialiasing)

        self.frame_graph = parent
        self.engine = GraphEngine(self)

        # Setarea la 60 de frame-uri (refresh o data la 17 milisec)
        self.frameRateTimer = QBasicTimer()
        self.frameRateTimer.start(17, self)

        # Setarea scene-ului
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.show()

    def resizeEvent(self, event):
        """Redimensionarea viewport-ului

        La fiecare redimensionare a viewport-ului trebuie redimensionat
        si scene-ul pntru a asigura redarea corecta a elementelor grafului
        """

        self.scene.setSceneRect(QRectF(0, 0, self.width(), self.height()))

    def timerEvent(self, timerEvent):
        """Urmareste frame rate-ul aplicatiei

        La fiecare 17 milisecunde se va aplea aceasta funtie, se vor
        face modificarile corespunzatoare (actualizarea pozitilor nodurilor
        si a randarea muchiilor) apoi se va apela funtia update() pentru a
        anunta viewport-ul ca s-au facut modificari
        """

        if self.engine.force_mode:
            self.engine.update_nodes()
            self.engine.update_connections()
        self.engine.draw_edges()
        self.update()
