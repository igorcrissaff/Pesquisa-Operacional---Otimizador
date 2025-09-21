from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic

from Graphs import GraphWidget
import MessageBox as msg
import Models

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"ui/main.ui", self)

        self.msg = msg.Msg()
        self.grafico = GraphWidget()
        self.widget_2.layout().addWidget(self.grafico)
        self.solve_btn.clicked.connect(lambda: self.read_model())

        self.model = {
            "sense": None,
            "objective": None,
            "restrictions": []
        }

    def read_model(self):
        lucro_x = self.lucro_x.value()
        lucro_y = self.lucro_y.value()
        consumo_1_x = self.consumo_1_x.value()
        consumo_1_y = self.consumo_1_y.value()
        materia_1 = self.materia_1.value()
        consumo_2_x = self.consumo_2_x.value()
        consumo_2_y = self.consumo_2_y.value()
        materia_2 = self.materia_2.value()
        demanda_min_x = self.demanda_min_x.value()
        demanda_max_x = self.demanda_max_x.value()
        demanda_min_y = self.demanda_min_y.value()
        demanda_max_y = self.demanda_max_y.value()

        objective = lucro_x * Models.x + lucro_y * Models.y

        restrictions = [
            consumo_1_x * Models.x + consumo_1_y * Models.y <= materia_1,
            consumo_2_x * Models.x + consumo_2_y * Models.y <= materia_2,

            Models.x >= demanda_min_x,
            Models.x <= demanda_max_x,

            Models.y >= demanda_min_y,
            Models.y <= demanda_max_y
        ]
    
        result = Models.solve(objective, restrictions)
        if result is None:
            self.x_value.setText("Inviável")
            self.y_value.setText("Inviável")
            self.z_value.setText("Inviável")
            self.grafico.clear_plot()
            self.msg.show_error("Não foi possível encontrar uma solução viável para o problema.")

        else:
            self.x_value.setText(str(result['x']))
            self.y_value.setText(str(result['y']))
            self.z_value.setText(str(result['z']))
        
            restricoes_numericas = [
            (consumo_1_x, consumo_1_y, "<=", materia_1),
            (consumo_2_x, consumo_2_y, "<=", materia_2),

            (1, 0, ">=", demanda_min_x),
            (1, 0, "<=", demanda_max_x),

            (0, 1, ">=", demanda_min_y),
            (0, 1, "<=", demanda_max_y)
            ]

            # Plotando no widget de gráfico
            self.grafico.plot_solution(
                result, 
                lucro_x, 
                lucro_y, 
                restricoes_numericas,
                min_x=demanda_min_x,
                max_x=demanda_max_x,
                min_y=demanda_min_y,
                max_y=demanda_max_y)
            self.msg.show_info("Solução encontrada com sucesso!")
    
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    app.exec()