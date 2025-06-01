class Styles:
    DARK_MAIN_COLOR = "#23272a"
    DARK_OTHER_COLOR = "#63676e"
    LIGHT_MAIN_COLOR = "#d1d0cf"
    LIGHT_OTHER_COLOR = "#81a1a3"
    BUTTON_HOVER_COLOR = "#2c2f33"
    dark_central_widget_style = "background-color: %s;" % DARK_MAIN_COLOR
    dark_frames_style = "\n    QFrame{ background-color: %s; border-radius: 10px; }\n    " % DARK_OTHER_COLOR
    dark_graphics_view_style = "\n    QGraphicsView{ background-color: %s; border-radius: 10px; }\n    " % DARK_OTHER_COLOR
    light_central_widget_style = "background-color: %s;" % LIGHT_MAIN_COLOR
    light_frames_style = "\n    QFrame{ background-color: %s; border-radius: 10px; }\n    " % LIGHT_OTHER_COLOR
    light_graphics_view_style = "\n    QGraphicsView{ background-color: %s; border-radius: 10px; }\n    " % LIGHT_OTHER_COLOR
    btn_directed_undirected_clicked = "\n    QPushButton{ background-color: transparent; border-radius: 10px; color: white; }\n    QPushButton::hover{ background-color: %s; }" % BUTTON_HOVER_COLOR
    btn_directed_undirected_non_clicked = "border: 2px solid white; border-radius: 15px; color: white;"
