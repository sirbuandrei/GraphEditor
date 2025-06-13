"""Fisierul contine clasele corespunzatoare elemenetelor grafice

Sunt 4 tipuri de elemente grafice : noduri, muchii, textul unui nod
si conexiunile dintre noduri.
"""

from PyQt5.QtWidgets import (QGraphicsItem, QWidget, QGraphicsSimpleTextItem, QGraphicsPathItem)
from PyQt5.QtCore import (QRectF, Qt, QPointF, QLineF)
from PyQt5.QtGui import (QPen, QColor, QFont, QPainterPath, QBrush, QPolygonF, QFontMetrics)

import random
import math
import numpy as np

# Fontul textului folosit
TEXT_FONT = QFont('Segoe UI Semibold', 11)


class Node(QGraphicsItem):
    """Nodurile grafului

    Nodurile grafului sunt elemente grafice in forma
    de cerc cu un text, textul reprezentand valoarea
    nodului

    Atribute
    --------
    engine : GraphicsEngine
        engin-ul aplicatiei
    radius : int
        raza nodului
    text : NodeText
        textul nodului
    connectedTo : list
        nodurile cu care este conenctat
    pen : QPen
        tipul de creion folosit la desenare

    Metode
    ------
    set_radius(radius)
        seteaza raza a nodului
    boundingRect()
        definește limitele exterioare ale nodului ca un dreptunghi
    paint()
        deseneaza nodul
    mousePressEvent(event)
        detecteaza click-urile adresate nodului
    mouseMoveEvent(event)
        detecteaza miscarea nodului
    mouseReleaseEvent(event)
        detecteaza eliberarea click-ului
    center()
        centrul nodului
    randomize_pos(scene_rect)
        alege o pozitie aleatorie in scene
    handle_value_changed()
        manipuleaza culoarea nodului
    """

    def __init__(self, text, engine):
        super(Node, self).__init__()
        self.setZValue(1)
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

        self.engine = engine
        self.radius = engine.node_radius
        self.text = NodeText(text, self)
        self.setPos(*self.randomize_pos(engine.view.scene.sceneRect()))
        self.connectedTo = []

        self.thickness = 2
        self.pen = QPen(Qt.white, self.thickness, Qt.SolidLine)

    def __repr__(self):
        return self.text.text()

    def __lt__(self, other):
        """Less than comparison for Node objects"""
        if isinstance(other, Node):
            return self.text.text() < other.text.text()
        return NotImplemented

    def __le__(self, other):
        """Less than or equal comparison for Node objects"""
        if isinstance(other, Node):
            return self.text.text() <= other.text.text()
        return NotImplemented

    def __gt__(self, other):
        """Greater than comparison for Node objects"""
        if isinstance(other, Node):
            return self.text.text() > other.text.text()
        return NotImplemented

    def __ge__(self, other):
        """Greater than or equal comparison for Node objects"""
        if isinstance(other, Node):
            return self.text.text() >= other.text.text()
        return NotImplemented

    def __eq__(self, other):
        """Equality comparison for Node objects"""
        if isinstance(other, Node):
            return self.text.text() == other.text.text()
        return NotImplemented

    def __ne__(self, other):
        """Not equal comparison for Node objects"""
        if isinstance(other, Node):
            return self.text.text() != other.text.text()
        return NotImplemented

    def __hash__(self):
        """Hash function for Node objects (needed for using in sets/dicts)"""
        return hash(self.text.text())

    def set_radius(self, radius):
        """Seteaza o noua raza pentru cerc"""

        if radius != self.radius:
            self.prepareGeometryChange()
            self.radius = radius

    def boundingRect(self):
        """Această funcție virtuală pură definește limitele exterioare ale elementului ca un dreptunghi

        Tot nodul trebui randat in interiorul dreptunghiului de delimitare al unui element
        """

        return QRectF(-self.radius, -self.radius,
                      self.radius * 2, self.radius * 2)

    def paint(self, painter, option, widget: QWidget = None):
        """Desenarea nodului

        Această funcție, care este de obicei numită de QGraphicsView,
        pictează conținutul unui element în coordonate locale.

        Parametrii
        ----------
        painter : QPainter
        option : QStyleOptionGraphicsItem
        widget : QWidget
        """

        painter.setPen(self.pen)
        painter.drawEllipse(self.boundingRect())

    def mousePressEvent(self, event):
        """Detecteaza click-ul adresat unui nod

        Daca un nod este apasat gravitatia este oprita
        si toate conexiunile dintre noduri sunt sterse

        Parametrii
        ----------
        event : QGraphicsSceneMouseEvent
        """

        self.engine.gravity = False
        self.engine.remove_all_connections()

        return super(Node, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Detecteaza miscarea nodului

        Nodul poate fi miscat doar in interiorul
        scene-ului, acestea nu poate iesi din scene,
        doar daca este impins de alt nod.

        Parametrii
        ----------
        event : QGraphicsSceneMouseEvent
        """

        super(Node, self).mouseMoveEvent(event)

        scene_rect = self.scene().sceneRect()
        bounding_rect = self.boundingRect()

        if self.x() - bounding_rect.width() < 0:
            self.setPos(bounding_rect.width(), self.y())
        elif self.x() + bounding_rect.width() > scene_rect.width():
            self.setPos(scene_rect.width() - bounding_rect.width(), self.y())

        if self.y() - bounding_rect.height() < 0:
            self.setPos(self.x(), bounding_rect.height())
        elif self.y() + bounding_rect.height() > scene_rect.height():
            self.setPos(self.x(), scene_rect.height() - bounding_rect.height())

    def mouseReleaseEvent(self, event):
        """Detecteaza eliberarea click-ului

        Daca nici-un nod nu mai este apasat, forta
        de gravitatie este activata.

        Parametrii
        ----------
        event : QGraphicsSceneMouseEvent
        """

        self.engine.gravity = True

        return super(Node, self).mouseReleaseEvent(event)

    def center(self):
        """Centrul nodului

        Centrul nodului este reprezentat chiar
        de coordonatele in scene ale nodului.

        Reurneaza
        ---------
        QPointF : QPointF
            centrul nodului
        """

        return QPointF(self.x(), self.y())

    def randomize_pos(self, scene_rect):
        """Alege o pozitie aleatorie in scene

        Aceasta pozitie reprezinta coordonatele de inceput
        ale nodului, cand este creeat. Pentru a se creea o
        libera a nodurilor in scene, nodul va putea fi creeat
        doar pe 'rama' scene-ului. Rama se afla pe marginile
        cene-ului de forma unei rame de tablou.
        Alegerea pozitiei se va face pe coordonatele aleatorii
        ale unei dintre cele 4 rame (sus, jos, stanga, dreapta)

        Parametrii
        ----------
        scene_rect : QRectF
            dimesiunile si pozitia scene-ului

        Returneaza
        ----------
        pos : tuple
            pozitia aleasa de coordonate (x, y)
        """

        node_radius = self.engine.node_radius
        frame_size = 20

        # Coordonatele dreptunghului scene-ului
        top_left = scene_rect.topLeft()
        top_right = scene_rect.topRight()
        bottom_left = scene_rect.bottomLeft()
        bottom_right = scene_rect.bottomRight()

        pos = random.choice([
            # RAMA DE SUS
            (random.randint(top_left.x(), top_right.x()),
             random.randint(top_left.y() + node_radius, top_left.y() + node_radius + frame_size)),
            # RAMA DIN STANGA
            (random.randint(top_left.x() + node_radius, top_left.x() + node_radius + frame_size),
             random.randint(top_left.y(), bottom_left.y())),
            # RAMA DE JOS
            (random.randint(bottom_left.x(), bottom_right.x()),
             random.randint(bottom_left.y() - node_radius - frame_size, bottom_left.y() - node_radius)),
            # RAMA DIN DREATPTA
            (random.randint(bottom_right.x() - node_radius - frame_size, bottom_right.x() - node_radius),
             random.randint(top_left.y(), bottom_left.y()))
        ])

        return pos

    def handle_value_changed(self, value):
        """Schimba culoarea nodului

        Aceasta metoda este folosita pentru shimbarea
        culorii in timpul unei animatii

        Parametrii
        ----------
        value : QColor
            noua culoare a nodului
        """

        self.pen = QPen(value, self.thickness, Qt.SolidLine)


class NodeText(QGraphicsSimpleTextItem):
    """Textul unui nod

    Textul nodului va fi mereu centrat in mijlocul
    nodului, acest lucru depinzand de dimensuine textului,
    date de boundingRect
    """

    def __init__(self, text, parent):
        super(NodeText, self).__init__(text, parent)
        self.setPen(QPen(Qt.white, 0.5, Qt.SolidLine))
        self.setBrush(QBrush(Qt.white))
        self.setFont(TEXT_FONT)
        self.setPos(-self.boundingRect().width() / 2, -self.boundingRect().height() / 2)


class Edge(QGraphicsPathItem):
    """Muchia dintre 2 noduri

    Muchia dintre 2 noduri este un path de la primul nod al
    muchiei la cel de-al doilea nod. In principiu path-ul
    este o line dreapta, dar daca un alt nod se intersecteaza
    cu aceast path, ea se va cruba pentru claritatea grafului.

    Atribute
    --------
    node1 : Node
        primul nod al muchiei
    node2 : Node
        cel de-al doilea nod al muchiei
    engine : GraphEngine
        enginu-ul aplicatiei
    cost : int, optional
        costul muchiei
    arrow_length : int, 15
        reprezinta lungimea sagetii muchiei in cazul unui graf orientat
    direct_path : QPainterPath
        path-ul direct de la primul la al doilea nod

    Metode
    ------
    create_path(start_point, end_point, directed)
        creaza path-ul muchiei dintre cele 2 noduri
    handle_value_changed(value)
        schimba culoarea muchiei
    """

    def __init__(self, node1, node2, engine, cost=None):
        super().__init__()
        self.node1 = node1
        self.node2 = node2
        self.engine = engine
        self.cost = cost

        self.arrow_length = 15
        self.setPen(self.node1.pen)

        # Crearea unui path invizibil si adaugarea lui in scene
        self.direct_path = QGraphicsPathItem()
        self.direct_path.setPen(QPen(QColor(0, 0, 0, 0)))
        self.engine.view.scene.addItem(self.direct_path)

    def create_path(self, start_point, end_point, directed):
        """Creeaza path-ul muchiei

        Path-ul muchiei este o curba Bezier. In cazul in care nici-un nod nu se intersecteaza
        cu path-ul direct dintre noduri, punctele de control ale curbei vor fi la centrul de
        greutate al dreptei date de cele 2 noduri, astfel creeandu-se o linie dreapta. In caz contrar,
        daca un nod se intersecteaza cu path-ul direct, pucntele de control ale curbei se vor situa pe
        dreapta perpendiculara pe path-ul direct, ce trece centrul de greutate al acestuia
        (dat de punctul de control initial) la o distanta egala dublul razei nodului. Aceste pucnte
        se pot situa in 2 pozitii, una la 'stanga' path-ului, iar cealalta la 'dreaptea' acestuia.
        Pozitia finala a punctului de control se determina 'trasand' 2 linii de la nodul care se
        intersecteaza la cele 2 posibile puncte de control. Verificand lungimea celor 2 linii
        se alege locatia punctului de control.

        panta dreptei : m = (y2 - y1) / (x2 - x1)
        ecuatia dreptei : y - y1 = m(x - x1)
        panta drepntei perpendiculare pe o dreapta : m' = -1 / m
        lungimea unei drepte : AB ^ 2 = (x2 - x1) ^ 2 + (y2 - y1) ^ 2

        => primul pas pentru a afla pucntele de control in cazul unei intersectii este:
        de a calula panta dreptei perpendiculara pe path-ul direct
            => m' = -1 / (node2.y - node1.y) / (node2.x - node1.x)
                => m' = -1 * (node2.x - node1.x) / (node2.y - node1.y)
        => cel de-al doilea pas este calcularea ecuatiei dreptei de panta m' ce trece prin pucntul de control (not G)
            => y - G.y = m'(x - G.x) => y = m'(x - G.x) + G.y
        => cel de-al treilea pas este inlocuirea lui y in lungimea dreptei ( lungimea dreptei dorita este dublul razei
            nodului) pentru a afla cele 2 coordonate x posibile (la 'stanga' si la 'dreapta' path-ului direct)
            => (x2 - G.x) ^ 2 + (m'(x2 - G.x) + G.y - G.y) ^ 2 = (2raza) ^ 2
            => x2 ^ 2 - 2 x2 G.x + G.x ^ 2 + (m' x2) ^ 2 - 2 (m' ^ 2) x2 G.x + (m' G.x) ^ 2 - (2raza) ^ 2 = 0
            => (x2 ^ 2)(1 + m' ^ 2) + x2(2 G.x (1 + m' ^ 2)) + (G.x ^ 2)(1 + m' ^ 2) - (2raza) ^ 2 = 0
                => cele 2 coordonate pe Ox ale punctului de control, prentu a afla cele 2 coordonate pe Oy
                se inlocuiesc valorie obtinute in ecuatia dreptei.


        Parametrii
        ----------
        start_point : QPointF
            punctul de start al path-ului
        end_point : QPointF
            punctul de final al path-ului
        directed : bool
            orientarea grafului

        Returneaza
        ----------
        path : QPainterPath
            path-ul final al muchiei
        """

        # Centrul de greutate al dreptei formata de cele 2 noduri
        control_point = QPointF((start_point.x() + end_point.x()) / 2,
                                (start_point.y() + end_point.y()) / 2)

        path = QPainterPath(start_point)
        node_radius = self.engine.node_radius
        point1 = point2 = None

        # Creearea path-ului direct
        _path = QPainterPath(start_point)
        _path.lineTo(end_point)
        self.direct_path.setPath(_path)

        # Verificarea pentru intersectii cu path-ul direct
        intersecting_items = self.engine.view.scene.collidingItems(self.direct_path)
        intersecting_items.remove(self.node1)
        intersecting_items.remove(self.node2)

        # Calcularea coordonatelor pe Ox a punctelor de control in cazul unei intersectii
        try:
            m = -1 * (self.node2.x() - self.node1.x()) / (self.node2.y() - self.node1.y())
            agent = 1 + (m ** 2)
            factors = [agent, -2 * control_point.x() * agent,
                       (control_point.x() ** 2) * agent - (node_radius * 2) ** 2]
            roots = np.roots(factors)
        # In cazul in care nodurile au acceleasi coordonate pe Ox sau Oy panta
        # dreptei nu exista. Atunci se va trata cazul de ZeroDivisionError
        except ZeroDivisionError:
            point1 = control_point + QPointF(0, node_radius * 2)
            point2 = control_point - QPointF(0, node_radius * 2)

        for item in intersecting_items:
            if isinstance(item, Node):
                # Daca exista o intersectie si exista si panta dreptei atunci se calculeaza
                # si coordonatele pe Oy ale posibilelor puncte de control
                if (point1 and point2) is None:
                    point1 = QPointF(roots[0], m * (roots[0] - control_point.x()) + control_point.y())
                    point2 = QPointF(roots[1], m * (roots[1] - control_point.x()) + control_point.y())
                # Cele 2 linii de la nod la posibilele puncte de control
                line1 = QLineF(item.pos(), point1)
                line2 = QLineF(item.pos(), point2)
                # Daca lungimea primei linii este mai mica decat lungimea celei de-a doua linie
                # inseamna ca nodul este mai aproape de prima linie deci path-ul va trebui sa se
                # curbeze in partea opusa => se alege cel de-al doilea punct
                control_point = point2 if line1.length() <= line2.length() else point1
                break

        # Creearea curbei Bezier
        path.cubicTo(control_point, control_point, end_point)

        # Daca graful este orientat se adauga la capatul muchiei o sageata pentru
        # a reprezenta orientarea acestuia
        if directed:
            pos = path.currentPosition()
            dx, dy, angle = self.engine.get_angle(control_point, end_point)

            path.lineTo(QPointF(pos.x() + self.arrow_length * math.cos(angle + 60),
                                pos.y() + self.arrow_length * math.sin(angle + 60)))
            path.moveTo(end_point)
            path.lineTo(QPointF(pos.x() + self.arrow_length * math.cos(angle - 60),
                                pos.y() + self.arrow_length * math.sin(angle - 60)))

        # In cazul in care muchia are un cost acesta va fi afisat la mijlocul muchiei
        font_metrics = QFontMetrics(TEXT_FONT)
        font_offset = QPointF(font_metrics.height(), font_metrics.horizontalAdvance(self.cost))
        path.addText(control_point - font_offset / 2, TEXT_FONT, self.cost)

        return path

    def handle_value_changed(self, value):
        """Schimba culoarea muchiei

        Aceasta metoda este folosita pentru shimbarea
        culorii in timpul unei animatii

        Parametrii
        ----------
        value : QColor
            noua culoare a muchiei
        """

        self.setPen(QPen(value, 1.5, Qt.SolidLine))


class Connection(object):
    """Conexiunea dintre 2 noduri"""

    def __init__(self, node1, node2, length):
        self.node1 = node1
        self.node2 = node2
        self.length = length

    def update(self, dx, dy):
        #node1 = connection.node1
        #node2 = connection.node2
        d = math.sqrt(dx * dx + dy * dy)
        diff = self.length - d
        percent = diff / d * 0.5
        offsetX = dx * percent
        offsetY = dy * percent

        self.node1.setPos(self.node1.x() - offsetX, self.node1.y() - offsetY)
        self.node2.setPos(self.node2.x() + offsetX, self.node2.y() + offsetY)
