
import sys
import json
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, QMainWindow, QStackedWidget, \
QLineEdit, QHBoxLayout, QComboBox, QTableWidget, QTableWidgetItem, QMessageBox


USER_DATA_FILE = "users.json"


def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            data = json.load(file)
        return data["users"]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_user_data(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump({"users": users}, file, indent=4) # stores users


class BasePage(QWidget):
    def __init__(self):
        super().__init__() # inheritance
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


class LoginPage(BasePage):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.setWindowTitle("Login") # title for page

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.username_input.setPlaceholderText("Enter your username") # shows text in box for user to see where to put username
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.authenticate)

        self.register_button = QPushButton("Register") # allows user to switch to register page
        self.register_button.clicked.connect(self.go_to_registration_page)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("Color:Red;") # changes error message to red

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.error_label) # widgets so all info is on screen to interact and see

        self.setLayout(self.layout) # sets page layout

    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()
        users = load_user_data()
        for user in users:
            if user["username"] == username and user["password"] == password:
                print("Login successful") # checks on login page the username and password match one in the files
                self.main_window.transition_to_main_screen()
                return
        self.error_label.setText("Invalid username or password")
        self.username_input.clear()
        self.password_input.clear()

    def go_to_registration_page(self):
        self.main_window.transition_to_registration_page()


class RegistrationPage(BasePage):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Registration")

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.register_button)
        self.setLayout(self.layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            print("Please fill the required boxes")
            return
        users = load_user_data()
        if any(user['username'] == username for user in users): # checks if user already exists
            print("Username already taken")
        new_user = {"username": username, "password": password}
        users.append(new_user) # adds new user details
        save_user_data(users)
        print("Registration is complete")

        self.main_window.transition_to_the_login_page()


class MainScreen(BasePage):
    def __init__(self, main_window):
        super().__init__() # inheritance
        self.main_window = main_window

        self.setWindowTitle("welcome to Greener Bikes") # title

        self.production_button = QPushButton("production workflow")
        self.production_button.clicked.connect(self.go_to_production)

        self.inventory_button = QPushButton("Inventory Management")
        self.inventory_button.clicked.connect(self.go_to_inventory)

        self.order_button = QPushButton("Order management")
        self.order_button.clicked.connect(self.go_to_order_management)

        self.reports_button = QPushButton("Reports")
        self.reports_button.clicked.connect(self.go_to_report_page) # when button clicked triggers correct action

        self.layout.addWidget(self.production_button)
        self.layout.addWidget(self.inventory_button)
        self.layout.addWidget(self.order_button)
        self.layout.addWidget(self.reports_button) # layout for main screen buttons

    def go_to_production(self):
        print("Going to production workflow")
        self.main_window.transition_to_production_workflow() # makes page transition to correct page

    def go_to_inventory(self):
        print("going to inventory")
        self.main_window.transition_to_inventory_page()

    def go_to_order_management(self):
        self.main_window.transition_to_order_management_page()

    def go_to_report_page(self):
        print("Going to reports")
        self.main_window.transition_to_report_page()


class ProductionWorkflowPage(BasePage):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Production workflow")

        self.components = {
            'steel': 20, # number of components which will show next to name from code directly below
            'frame': 20,
            'fork': 50,
            'painting': 20,
            'pedal': 30,
            'wheel': 10,
            'chain': 3,
            'brakes': 6,
            'lights': 7,
            'seats': 4,

        }

        self.frame_welding_stock_label = QLabel(f" Frame: {self.components['frame']}")
        self.fork_welding_stock_label = QLabel(f"Fork: {self.components['fork']}")
        self.painting_stock_label = QLabel(f" paint: {self.components['painting']}")
        self.pedal_stock_label = QLabel(f"pedal stock: {self.components['pedal']}")
        self.wheel_stock_label = QLabel(f" Wheel stock:{self.components['wheel']}")
        self.chain_stock_label = QLabel(f"Chain stock: {self.components['chain']}")
        self.brake_stock_label = QLabel(f"brake stock: {self.components['brakes']}")
        self.light_stock_label = QLabel(f"light stock: {self.components['lights']}")
        self.seat_stock_label = QLabel(f"Seat stock: {self.components['seats']}")

        self.frame_welding_button = QPushButton("Record frame assembly station")
        self.frame_welding_button.clicked.connect(self.record_frame_welding) # button and confirmation its clicked to reduce stock

        self.fork_welding_button = QPushButton("Record fork assembly station")
        self.fork_welding_button.clicked.connect(self.record_fork_welding)

        self.painting_button = QPushButton("Record painting process")
        self.painting_button.clicked.connect(self.record_painting)

        self.pedal_button = QPushButton("Record addition of pedals")
        self.pedal_button.clicked.connect(self.record_pedal_addition)

        self.wheel_button = QPushButton("Record wheels being added")
        self.wheel_button.clicked.connect(self.record_wheel_addition)

        self.chain_button = QPushButton("Record addition of chain")
        self.chain_button.clicked.connect(self.record_chain_addition)

        self.brake_button = QPushButton("Record brake addition")
        self.brake_button.clicked.connect(self.record_brake_addition)

        self.light_button = QPushButton("Record addition of lights")
        self.light_button.clicked.connect(self.record_light_addition)

        self.seat_button = QPushButton("Record seat addition")
        self.seat_button.clicked.connect(self.record_seat_addition)

        self.back_button = QPushButton("Back to home page")
        self.back_button.clicked.connect(self.back_button_clicked)

        self.layout.addWidget(QLabel("frame station"))
        self.layout.addWidget(self.frame_welding_stock_label)
        self.layout.addWidget(self.frame_welding_button)

        self.layout.addWidget(QLabel("Fork station")) # widgets for all stations
        self.layout.addWidget(self.fork_welding_stock_label)
        self.layout.addWidget(self.fork_welding_button)

        self.layout.addWidget(QLabel("Painting station"))
        self.layout.addWidget(self.painting_stock_label)
        self.layout.addWidget(self.painting_button)

        self.layout.addWidget(QLabel("Assembly station"))
        self.layout.addWidget(self.pedal_stock_label)
        self.layout.addWidget(self.pedal_button)
        self.layout.addWidget(self.wheel_stock_label)
        self.layout.addWidget(self.wheel_button)
        self.layout.addWidget(self.chain_stock_label)
        self.layout.addWidget(self.chain_button)
        self.layout.addWidget(self.brake_stock_label)
        self.layout.addWidget(self.brake_button)
        self.layout.addWidget(self.light_stock_label)
        self.layout.addWidget(self.light_button)
        self.layout.addWidget(self.seat_stock_label)
        self.layout.addWidget(self.seat_button)

        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)
        self.setFixedSize(800, 600) # fixed size for page layout of buttons


    def update_stock_label(self):
        self.frame_welding_stock_label.setText(f"frame welding stock available {self.components['frame']}")
        self.fork_welding_stock_label.setText(f" fork welding stock available {self.components['fork']}")
        self.painting_stock_label.setText(f"paint stock available {self.components['painting']}")
        self.pedal_stock_label.setText(f"pedal stock available{self.components['pedal']}")
        self.wheel_stock_label.setText(f"wheel stock available {self.components['wheel']}")
        self.chain_stock_label.setText(f"Chain stock available{self.components['chain']}")
        self.brake_stock_label.setText(f"brake stock available {self.components['brakes']}")
        self.light_stock_label.setText(f"lights stock available{self.components['lights']}")
        self.seat_stock_label.setText(f"Seat stock available {self.components['seats']}")

    def check_component_levels(self, component_name):
        """Check if a components levels exceeds our threshold."""
        if self.components[component_name] > 3: # trgiggers warning
            print(f"Warning {component_name} does not meet warning threshold level")

    def record_frame_welding(self):
        if self.components['steel'] >= 1: # checks previous component can be completed if not this one cant
            self.components['frame'] -= 1 # minus one once button clicked same for others
            print("Frame welding completed")
            self.check_component_levels('frame')
            self.update_stock_label()
        else:
            print("Not enough steel from frame welding")

    def record_fork_welding(self):
        if self.components['steel'] >= 1:
            self.components['fork'] -= 1
            print("Fork welding complete")
            self.check_component_levels('fork')
            self.update_stock_label()
        else:
            print("Not enough steel to complete fork welding")

    def record_painting(self):
        if self.components['frame'] > 0 and self.components['fork'] > 0:
            self.components['painting'] -= 1
            print("Painting process complete")
            self.check_component_levels('painting')
            self.update_stock_label()
        else:
            print("Not enough frames or forks available for painting to start")

    def record_pedal_addition(self):
        if self.components['painting'] > 0:
            self.components['pedal'] -= 1
            print("Pedal has been added")
            self.update_stock_label()
        else:
            print("No painted frames to move onto pedal addition")

    def record_wheel_addition(self):
        if self.components['pedal'] > 0:
            self.components['wheel'] -= 1
            print("Wheel addition complete")
            self.update_stock_label()
        else:
            print("No pedals available to begin wheel addition")

    def record_chain_addition(self):
        if self.components['wheel'] > 0:
            self.components['chain'] -= 1
            print("Chain and gear installed")
            self.update_stock_label()
        else:
            print("No wheels available for chain and gear addition")

    def record_brake_addition(self):
        if self.components['chain'] > 0:
            self.components['brakes'] -= 1
            print("Brakes have been added")
            self.update_stock_label()
        else:
            print("No chains available to complete brake addition")

    def record_light_addition(self):
        if self.components['brakes'] > 0:
            self.components['lights'] -= 1
            print("Lights have been added")
            self.update_stock_label()
        else:
            print("No brakes available for light addition")

    def record_seat_addition(self):
        if self.components['lights'] > 0:
            self.components['seats'] -= 1
            print("Seat has been added")
            self.update_stock_label()
        else:
            print("seat cannot be added as no lights available")
    def back_button_clicked(self): # back button on every page for better navigation
        self.main_window.transition_to_main_screen()



class InventoryManagementPage(BasePage):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Inventory Management")
        self.back_button = QPushButton("Back to home page")
        self.back_button.clicked.connect(self.back_button_clicked)
        self.layout.addWidget(self.back_button)

        self.components = {
            "steel": 20,
            "frame": 20,
            "fork": 50,
            "painting": 20,
            "pedal": 30,
            "wheel": 10,
            "chain": 3,
            "brakes": 6,
            "lights": 1,
            "seats": 4,
        }
        self.components_widgets = {}

        for component, stock in self.components.items():
            self.create_component_ui(component, stock)

        self.warning_label = QLabel("")
        self.warning_label.setStyleSheet("color: red; font-weight: bold;") # error for components below threshold of 3
        self.layout.addWidget(self.warning_label)

        self.update_inventory_display()

    def create_component_ui(self, component, stock):
        label = QLabel(f"{component.capitalize()}stock: {stock}")
        reorder_button = QPushButton(f"reorder {component}")
        reorder_button.clicked.connect(lambda: self.reorder_component(component))

        component_layout = QHBoxLayout()
        component_layout.addWidget(label)
        component_layout.addWidget(reorder_button)

        self.layout.addLayout(component_layout)
        self.components_widgets[component] = label

    def reorder_component(self, component):
        self.components[component] += 1 # components go up by one when reorder clicked but only correct one not all
        print(f"{component.capitalize()}")
        self.update_inventory_display()

    def update_inventory_display(self):
        for component, stock in self.components.items():
            self.components_widgets[component].setText(f"{component.capitalize()} stock: {stock}")

            warnings = []
            for component, stock in self.components.items():
                if stock < 3: #for loop to check when stock goes below or above threshold message appears and disappears
                    warnings.append(f"{component.capitalize()} needs a reorder asap!") # the arning message in bold and red
            if warnings:
                self.warning_label.setText("\n".join(warnings))
            else:
                self.warning_label.setText("")
    def back_button_clicked(self):
        self.main_window.transition_to_main_screen()


class OrderMangementPage(BasePage):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Order management")

        self.orders = []

        self.model_label = QLabel("Bike model")
        self.model_input = QLineEdit()

        self.size_label = QLabel("Size:")
        self.size_input = QComboBox() # crates the drop box style
        self.size_input.addItems(["small", "medium", "Large", "Extra large"])

        self.colour_label = QLabel("Colour:")
        self.colour_input = QComboBox()
        self.colour_input.addItems(["Red", "Black", "White", "Yellow", "Orange"])

        self.wheel_size_label = QLabel("Wheel size:")
        self.wheel_size_input = QComboBox()
        self.wheel_size_input.addItems(["Standard", "Premium"])

        self.brake_type_label = QLabel("Brake type:")
        self.brake_type_input = QComboBox()
        self.brake_type_input.addItems(["Standard(Disk)", "Premium(Rim)"])

        self.light_type_label = QLabel("Light type:")
        self.light_type_input = QComboBox()
        self.light_type_input.addItems(["Standard", "Premium (LED)"])

        self.customer_name_label = QLabel("Customer name:")
        self.customer_name_input = QLineEdit()

        self.contact_label = QLabel("Contact information:")
        self.contact_input = QLineEdit()

        self.delivery_address_label = QLabel(" Customer Delivery address")
        self.delivery_address_input = QLineEdit()

        self.submit_order_button = QPushButton("Submit customer order")
        self.submit_order_button.clicked.connect(self.submit_order)

        self.back_button = QPushButton("Back to home page")
        self.back_button.clicked.connect(self.back_button_clicked)

        self.layout.addWidget(self.model_label)
        self.layout.addWidget(self.model_input)
        self.layout.addWidget(self.size_label)
        self.layout.addWidget(self.size_input)
        self.layout.addWidget(self.colour_label)
        self.layout.addWidget(self.colour_input)
        self.layout.addWidget(self.wheel_size_label)
        self.layout.addWidget(self.wheel_size_input)
        self.layout.addWidget(self.brake_type_label)
        self.layout.addWidget(self.brake_type_input)
        self.layout.addWidget(self.light_type_label)
        self.layout.addWidget(self.light_type_input)
        self.layout.addWidget(self.customer_name_label)
        self.layout.addWidget(self.customer_name_input)
        self.layout.addWidget(self.contact_label)
        self.layout.addWidget(self.contact_input)
        self.layout.addWidget(self.delivery_address_label)
        self.layout.addWidget(self.delivery_address_input)
        self.layout.addWidget(self.submit_order_button)

        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def submit_order(self):
        bike_model = self.model_input.text()
        size = self.size_input.currentText()
        colour = self.colour_input.currentText()
        wheel_size = self.wheel_size_input.currentText()
        brake_type = self.brake_type_input.currentText()
        light_type = self.light_type_input.currentText()

        customer_name = self.customer_name_input.text()
        contact_info = self.contact_input.text()
        delivery_address = self.delivery_address_input.text()

        if not (customer_name and contact_info and delivery_address and bike_model and size and colour and wheel_size and brake_type and light_type):
            QMessageBox.warning(
                self,
                "Caution",
                "Please fill out all of the fields before clicking submit" # tells user not filled all fields
            )
            self.rest_form() # rests any progress made as all fields bnot filled
            return

        order = {
              f"Customer name": customer_name,
              f"Contact information": contact_info,
              f"Delivery address": delivery_address,
              f"Bike model": bike_model,
              f"Size": size,
              f"Colour": colour,
              f"Wheel size": wheel_size,
              f"Brake type": brake_type,
              f"Light type": light_type,
        }
        self.orders.append(order)
        print(F"current orders: {self.orders}")

        QMessageBox.information(
            self,
            "Order submitted",
            "Now head to production workflow to fufill order"
        ) # pop up only when order finished

        self.rest_form() # rests whole form after completion
        return




    def rest_form(self):
        self.model_input.clear()
        self.size_input.setCurrentIndex(0)
        self.colour_input.setCurrentIndex(0)
        self.wheel_size_input.setCurrentIndex(0)
        self.brake_type_input.setCurrentIndex(0)
        self.light_type_input.setCurrentIndex(0)
        self.customer_name_input.clear()
        self.contact_input.clear()
        self.delivery_address_input.clear()

    def back_button_clicked(self):
        self.main_window.transition_to_main_screen()

class ReportsPage(BasePage): # isnt currently working
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("customer Order reports")
        self.layout = QVBoxLayout()

        self.title_label = QLabel("Customer order reports")
        self.layout.addWidget(self.title_label)

        self.reports_table = QTableWidget()
        self.layout.addWidget(self.title_label)

        self.reports_table = QTableWidget()
        self.reports_table.setColumnCount(9)
        self.reports_table.setHorizontalHeaderLabels([
            "Customer Name", "Contact Information", "Delivery Address", "Bike Model", "Size", "Colour", "Wheel Size", "Brake Type", "Light Type"
        ])
        self.layout.addWidget(self.reports_table)

        self.back_button = QPushButton("Back to home page")
        self.back_button.clicked.connect(self.back_button_clicked)

        self.setLayout(self.layout)

        self.orders()
    def orders(self):
        orders = [
            {
                "Customer Name": "Zac",
                "Contact Information": "123",
                "Delivery Address": "123 bob street",
                "Bike Model": "Mountain",
                "Size": "Medium",
                "Colour": "Black",
                "Wheel Size": "Standard",
                "Brake Type": "Disk",
                "Light Type": "Standard"
            }
        ]
        self.reports_table.setRowCount(len(orders))
        for row, order in enumerate(orders):
            self.reports_table.setItem(row, 0, QTableWidgetItem(order["Customer Name"]))
            self.reports_table.setItem(row, 1, QTableWidgetItem(order["Contact Information"]))
            self.reports_table.setItem(row, 2, QTableWidgetItem(order["Delivery Address"]))
            self.reports_table.setItem(row, 3, QTableWidgetItem(order["Bike Model"]))
            self.reports_table.setItem(row, 4, QTableWidgetItem(order["Size"]))
            self.reports_table.setItem(row, 5, QTableWidgetItem(order["Colour"]))
            self.reports_table.setItem(row, 6, QTableWidgetItem(order["Wheel Size"]))
            self.reports_table.setItem(row, 7, QTableWidgetItem(order["Brake Type"]))
            self.reports_table.setItem(row, 8, QTableWidgetItem(order["Light Type"]))

    def back_button_clicked(self):
        self.main_window.transition_to_main_screen()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Greener Bikes Bicycle Factory") # title for pages
        self.setGeometry(200, 200, 400, 600) #size

        self.login_page = LoginPage(self)
        self.registration_page = RegistrationPage(self)
        self.main_screen = MainScreen(self)
        self.production_workflow_page = ProductionWorkflowPage(self)
        self.inventory_management_page = InventoryManagementPage(self)
        self.order_management_page = OrderMangementPage(self)
        self.reports_page = ReportsPage(self)

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.registration_page)
        self.stacked_widget.addWidget(self.main_screen)
        self.stacked_widget.addWidget(self.production_workflow_page)
        self.stacked_widget.addWidget(self.inventory_management_page)
        self.stacked_widget.addWidget(self.order_management_page)
        self.stacked_widget.addWidget(self.reports_page) # widget for all pages

        self.setCentralWidget(self.stacked_widget)

    def transition_to_main_screen(self): # transtion to the page same for all
        self.stacked_widget.setCurrentWidget(self.main_screen)

    def transition_to_registration_page(self):
        self.stacked_widget.setCurrentWidget(self.registration_page)

    def transition_to_the_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def transition_to_production_workflow(self):
        self.stacked_widget.setCurrentWidget(self.production_workflow_page)
        print("Going to production workflow")

    def transition_to_inventory_page(self):
        self.stacked_widget.setCurrentWidget(self.inventory_management_page)
        print("Going to inventory mangement")

    def transition_to_order_management_page(self):
        self.stacked_widget.setCurrentWidget(self.order_management_page)
    def transition_to_report_page(self):
        self.stacked_widget.setCurrentWidget(self.reports_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


