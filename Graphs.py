import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class GraphWidget(QWidget):
    """
    A QWidget for displaying a matplotlib graph, specifically designed for
    linear programming visualization.
    """

    # --- Constants for plot styling ---
    OPTIMAL_POINT_COLOR = "red"
    OPTIMAL_POINT_MARKER = "o"
    OBJECTIVE_LINE_COLOR = "green"
    OBJECTIVE_LINE_STYLE = "--"
    CONSTRAINT_LINE_STYLE = "-"
    VERTICAL_LINE_STYLE = "--"
    ANNOTATION_OFFSET_X = 10
    ANNOTATION_OFFSET_Y = -10
    GRID_ALPHA = 0.7


    def __init__(self, parent=None):
        """
        Initializes the GraphWidget, setting up the Matplotlib figure,
        canvas, and toolbar within a QVBoxLayout.
        """
        super().__init__(parent)

        self.figure = Figure(figsize=(8, 6))  # Added figsize for better control
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Initialize the axes, will be cleared on each plot
        self.ax = self.figure.add_subplot(111)


    def plot_solution(self, result, lucro_x, lucro_y, restricoes_numericas, min_x=0, max_x=50, min_y=0, max_y=50):
        """
        Draws the graph based on the results from a linear programming solution
        and numerical constraints.

        Args:
            result (dict): A dictionary containing the optimal solution,
                           e.g., {"x": val_x, "y": val_y, "z": val_z}.
            lucro_x (float): Coefficient of x in the objective function.
            lucro_y (float): Coefficient of y in the objective function.
            restricoes_numericas (list): A list of tuples, each representing a
                                         constraint: (coef_x, coef_y, operator, limit).
            min_x (float): Minimum x-axis value for the plot.
            max_x (float): Maximum x-axis value for the plot.
            min_y (float): Minimum y-axis value for the plot.
            max_y (float): Maximum y-axis value for the plot.
        """
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)

        # Define a range for x and y values for plotting lines
        # Extend the range slightly beyond max_x/max_y to ensure lines are fully drawn
        plot_x_range = np.linspace(min_x, max(max_x, result.get("x", 0) + 10), 500)
        plot_y_range = np.linspace(min_y, max(max_y, result.get("y", 0) + 10), 500)


        # Plotting the constraints as lines
        for i, (coef_x, coef_y, operador, limite) in enumerate(restricoes_numericas):
            label = f"{coef_x}x + {coef_y}y {operador} {limite}"
            if coef_y != 0:
                y_constraint = (limite - coef_x * plot_x_range) / coef_y
                self.ax.plot(plot_x_range, y_constraint,
                             label=label, linestyle=self.CONSTRAINT_LINE_STYLE)
            elif coef_x != 0:
                x_constraint = limite / coef_x
                self.ax.axvline(x=x_constraint,
                                linestyle=self.VERTICAL_LINE_STYLE,
                                label=label)
            else:
                # Handle cases where both coefficients are zero (e.g., 0x + 0y <= 5)
                # This typically means an invalid or trivial constraint, or a global bound.
                print(f"Warning: Constraint {coef_x}x + {coef_y}y {operador} {limite} is trivial or invalid.")


        # Plotting the optimal point
        optimal_x = result.get("x")
        optimal_y = result.get("y")
        optimal_z = result.get("z")

        if optimal_x is not None and optimal_y is not None and optimal_z is not None:
            self.ax.plot(optimal_x, optimal_y,
                         self.OPTIMAL_POINT_MARKER,
                         color=self.OPTIMAL_POINT_COLOR,
                         markersize=10,
                         label=f"Ótimo: Z = {optimal_z:.2f}")

            self.ax.annotate(f"({optimal_x:.2f}, {optimal_y:.2f})",
                             (optimal_x, optimal_y),
                             textcoords="offset points",
                             xytext=(self.ANNOTATION_OFFSET_X, self.ANNOTATION_OFFSET_Y),
                             ha='center')


        # Plotting the objective function line (for inclination visualization)
        if lucro_x != 0 or lucro_y != 0: # Only plot if objective function is not trivial
            if optimal_z is not None:
                if lucro_y != 0:
                    y_objective = (optimal_z - lucro_x * plot_x_range) / lucro_y
                    self.ax.plot(plot_x_range, y_objective,
                                 linestyle=self.OBJECTIVE_LINE_STYLE,
                                 color=self.OBJECTIVE_LINE_COLOR,
                                 alpha=0.6, # Slightly increased alpha for better visibility
                                 label="Linha da função objetivo")
                elif lucro_x != 0:
                    x_objective = optimal_z / lucro_x
                    self.ax.axvline(x=x_objective,
                                    linestyle=self.OBJECTIVE_LINE_STYLE,
                                    color=self.OBJECTIVE_LINE_COLOR,
                                    alpha=0.6,
                                    label="Linha da função objetivo")
        else:
            print("Warning: Objective function coefficients are both zero. Cannot plot objective line.")


        # Setting axis limits dynamically based on optimal point and default maxes
        # Ensure that optimal point is always visible and some padding is added
        x_limit = max(optimal_x if optimal_x is not None else 0, max_x) + 5
        y_limit = max(optimal_y if optimal_y is not None else 0, max_y) + 5

        self.ax.set_xlim(min_x, x_limit)
        self.ax.set_ylim(min_y, y_limit)

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_title("Gráfico da Programação Linear")
        self.ax.grid(True, alpha=self.GRID_ALPHA) # Added alpha to grid
        self.ax.legend()
        self.canvas.draw()

    def clear_plot(self):
        """
        Clears the current plot in the GraphWidget.
        """
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)
        self.canvas.draw()