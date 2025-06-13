import re

from PyQt5.QtCore import Qt, QObject


class InputPresenter(QObject):
    def __init__(self, view, model):
        super().__init__()
        self.input_page = view
        self.graph_model = model

        self.input_page.send_data.connect(self.handle_input)

    def handle_input(self, raw_text):
        try:
            self.graph_model.clear()

            if not raw_text:
                self.graph_model.graph_update()
                return

            lines = raw_text.split('\n')
            for line in lines:
                _line = list(filter(None, line.split(' ')))

                if not _line:
                    continue

                if len(_line) == 1 and _line[0] not in self.graph_model.nodes:
                    self.graph_model.add_node(_line[0])

                elif len(_line) > 1:
                    if _line[0] not in self.graph_model.nodes:
                        self.graph_model.add_node(_line[0])
                    if _line[1] not in self.graph_model.nodes:
                        self.graph_model.add_node(_line[1])
                    if (_line[0], _line[1]) not in self.graph_model.edges \
                            and _line[0] is not _line[1]:
                        cost = _line[2] if len(_line) >= 3 else None
                        if cost is None or not cost.isdigit():
                            self.graph_model.add_edge(_line[0], _line[1], None)
                        else:
                            self.graph_model.add_edge(_line[0], _line[1], int(cost))

            self.graph_model.graph_update()

        except Exception as e:
            print(f"ERROR in handle_input: {e}")
            import traceback
            traceback.print_exc()