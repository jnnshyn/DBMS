from PyQt5 import QtCore, QtGui, QtWidgets
from SC import Ui_Sugarcafe
from Login import Ui_MainWindow
from Dashboard import Ui_dashboard
import psycopg2
from PyQt5.QtWidgets import QInputDialog, QTableWidgetItem
import sys
import re
from datetime import datetime
import decimal  
import decimal
from PyQt5.QtWidgets import QCalendarWidget, QDialog, QDialogButtonBox, QMessageBox, QVBoxLayout
from PyQt5.QtCore import QDate


#log in window
class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #(log in btn)
        self.ui.login.clicked.connect(self.check_login)  
        self.show()

    def check_login(self):
        username = self.ui.username.text()  
        password = self.ui.password.text()  

        if username == "admin" and password == "admin123":
        # Show success message modal
            QtWidgets.QMessageBox.information(self, "Success", "Successfully logged in!")

        # Proceed to open Sugarcafe window
            self.dashboard_window = QtWidgets.QMainWindow()  # Create a QMainWindow instance
            self.dashboard_ui = Ui_dashboard()  # Initialize the dashboard UI
            self.dashboard_ui.setupUi(self.dashboard_window)  # Set up the UI
            self.dashboard_window.show()  # Show the Sugarcafe window
            self.close()  # Close the login window

        else:
        # Show error message if login fails
            QtWidgets.QMessageBox.warning(self, "Error", "Invalid username or password")
        
        # Optionally, clear the username and password fields for the user to re-enter them
            self.ui.username.clear()
            self.ui.password.clear()

        # Focus back to the username input field for convenience
            self.ui.username.setFocus()
#mainwindow(DashboardWindow)
class dashboard(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_dashboard()
        self.ui.setupUi(self)

        # Connect buttons to their respective methods
        self.ui.Inventory_DB.clicked.connect(self.inventory_page)
        self.ui.Order_DB.clicked.connect(self.order_page)
        self.ui.Report_DB.clicked.connect(self.sales_report_page)
        self.ui.Supplier_DB.clicked.connect(self.supplier_management_page)

    def inventory_page(self):
        # Navigate to the InventoryPage in the QStackedWidget
        self.ui.stackedWidget.setCurrentWidget(self.ui.InventoryPage)

    def order_page(self):
        # Navigate to the OrderPage in the QStackedWidget
        self.ui.stackedWidget.setCurrentWidget(self.ui.OrderPage)

    def sales_report_page(self):
        # Navigate to the SalesReportPage in the QStackedWidget
        self.ui.stackedWidget.setCurrentWidget(self.ui.SalesReportPage)

    def supplier_management_page(self):
        # Navigate to the SupplierManagementPage in the QStackedWidget
        self.ui.stackedWidget.setCurrentWidget(self.ui.SupplierManagementPage)




#mainwindow(SugarCafe)
class Sugarcafe(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        # Hide the maximize and close buttons
        flags = Sugarcafe.windowFlags()  # Get the current window flags
        flags &= ~QtCore.Qt.WindowMaximizeButtonHint  # Disable the maximize button
        flags &= ~QtCore.Qt.WindowCloseButtonHint     # Disable the close button
        Sugarcafe.setWindowFlags(flags)  # Apply the updated flags

        self.ui= Ui_Sugarcafe()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentWidget(self.ui.InventoryTable)
        self.show()
        self.connect_to_database()
        self.connect_buttons()
        
        #(logout btn)
        self.ui.Logout.clicked.connect(self.logout)

        #dashboard buttons
        self.ui.Inventory.clicked.connect(self.inventory_page)
        self.ui.Order.clicked.connect(self.order_page)
        self.ui.Report.clicked.connect(self.report_page)
        self.ui.Supplier.clicked.connect(self.supplier_page)
       

    def connect_buttons(self):
        #Inventory
        self.Editbutton = self.findChild(QtWidgets.QPushButton, 'Edit')
        self.Editbutton.clicked.connect(self.toggle_edit_mode)
        self.Addproductbutton = self.findChild(QtWidgets.QPushButton, 'Add')
        self.Addproductbutton.clicked.connect(self.add_product)
        self.Deletebutton = self.findChild(QtWidgets.QPushButton, 'Delete')
        self.Deletebutton.clicked.connect(self.delete_product)

        #Order
        self.Addordbutton = self.findChild(QtWidgets.QPushButton, 'Add_4')
        self.Addordbutton.clicked.connect(self.add_order)
        self.Editordbutton = self.findChild(QtWidgets.QPushButton, 'Edit_2')
        self.Editordbutton.clicked.connect(self.toggle_edit_mode_order)
        self.Deleteordbutton = self.findChild(QtWidgets.QPushButton, 'Delete_2')
        self.Deleteordbutton.clicked.connect(self.delete_order)

        #Supplier
        self.Addbutton = self.findChild(QtWidgets.QPushButton, 'Add_7')
        self.Addbutton.clicked.connect(self.add_supplier)
        self.Editsuppbutton = self.findChild(QtWidgets.QPushButton, 'Edit_5')
        self.Editsuppbutton.clicked.connect(self.toggle_edit_mode_supplier)
        self.Deletesuppbutton = self.findChild(QtWidgets.QPushButton, 'Delete_5')
        self.Deletesuppbutton.clicked.connect(self.delete_supplier)



    def connect_to_database(self): #database connection
        try:
            self.connection = psycopg2.connect(
                dbname="SugarCafe",
                user="postgres",
                password="09325365063",
                host="localhost",
                port="5432"
            )
            self.cursor = self.connection.cursor()
            print("Database Connected")
        except Exception as e:
            print(f"Error connecting to database: {e}")


    #dashboard pages
    def inventory_page(self):
        self.connect_to_database()
        self.ui.stackedWidget.setCurrentWidget(self.ui.InventoryPage)
        self.ui.Inventory.setStyleSheet(
            "QPushButton{background-color:rgb(223,203,171); border:null; border-radius:null; }")
        self.ui.Order.setStyleSheet(
            "QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.ui.Report.setStyleSheet(
            "QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.ui.Supplier.setStyleSheet(
            "QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.tableWidget = self.findChild(QtWidgets.QTableWidget, 'InventoryTable')
       
        self.refresh_product_table()

    def add_product(self):
        self.connect_to_database()

        # Loop for entering product name until it's valid
        while True:
            product_name, ok = QInputDialog.getText(self, "Input Dialog", "Enter Product Name:")
            if not ok or not product_name:
                return  # Exit if the user cancels or doesn't enter a name
            else:
                break  # Exit loop if product name is valid

        # Loop for entering product quantity on hand until it's valid
        while True:
            product_qoh, ok = QInputDialog.getInt(self, "Input Dialog", "Enter Product Quantity On Hand:")
            if not ok:
                return  # Exit if the user cancels the input
            if product_qoh < 0:
                QtWidgets.QMessageBox.warning(self, "Error", "Product Quantity On Hand cannot be negative")
                continue  # Re-prompt the user for valid quantity
            else:
                break  # Exit loop if quantity is valid

        # Loop for entering product price until it's valid
        while True:
            product_price, ok = QInputDialog.getDouble(self, "Input Dialog", "Enter Product Price:")
            if not ok:
                return  # Exit if the user cancels the input
            if product_price < 0:
                QtWidgets.QMessageBox.warning(self, "Error", "Product Price cannot be negative")
                continue  # Re-prompt the user for valid price
            else:
                break  # Exit loop if price is valid

        # Loop for entering product description until it's valid
        while True:
            product_desc, ok = QInputDialog.getText(self, "Input Dialog", "Enter Product Description:")
            if not ok or not product_desc:
                return  # Exit if the user cancels or doesn't enter a description
            else:
                break  # Exit loop if description is valid

        # Loop for entering supplier ID until it's valid
        while True:
            supp_id, ok = QInputDialog.getInt(self, "Input Dialog", "Enter Supplier ID:")
            if not ok:
                return  # Exit if the user cancels the input
            if supp_id <= 0:
                QtWidgets.QMessageBox.warning(self, "Error", "Supplier ID must be a positive integer")
                continue  # Re-prompt the user for valid supplier ID
            else:
                break  # Exit loop if supplier ID is valid

        try:
            cursor = self.connection.cursor()

            # Check if supplier ID exists
            cursor.execute("SELECT SUPP_ID FROM SUPPLIER WHERE SUPP_ID = %s", (supp_id,))
            result = cursor.fetchone()
            if not result:
                QtWidgets.QMessageBox.warning(self, "Error", "Supplier ID does not exist")
                return  # Exit if supplier ID doesn't exist

            # Check if product name already exists (case-insensitive)
            cursor.execute("SELECT PRODUCT_ID FROM PRODUCT WHERE PRODUCT_NAME ILIKE %s", (product_name,))
            if cursor.fetchone():
                QtWidgets.QMessageBox.warning(self, "Error", "Product name already exists")
                return  # Exit if product name already exists

            # Insert into the database
            cursor.execute("""
                INSERT INTO PRODUCT (PRODUCT_NAME, PRODUCT_QOH, PRODUCT_PRICE, PRODUCT_DESC, SUPP_ID)
                VALUES (%s, %s, %s, %s, %s) RETURNING PRODUCT_ID
            """, (product_name, product_qoh, product_price, product_desc, supp_id))
            product_id = cursor.fetchone()[0]
            self.connection.commit()
            print(f"Inserted product with ID: {product_id}")

            # Insert into the QTableWidget
            row_position = self.ui.InventoryTable.rowCount()
            self.ui.InventoryTable.insertRow(row_position)

            self.ui.InventoryTable.setItem(row_position, 0, QTableWidgetItem(str(product_id)))
            self.ui.InventoryTable.setItem(row_position, 1, QTableWidgetItem(product_name))
            self.ui.InventoryTable.setItem(row_position, 2, QTableWidgetItem(str(product_qoh)))
            self.ui.InventoryTable.setItem(row_position, 3, QTableWidgetItem(str(product_price)))
            self.ui.InventoryTable.setItem(row_position, 4, QTableWidgetItem(product_desc))
            self.ui.InventoryTable.setItem(row_position, 5, QTableWidgetItem(str(supp_id)))
            self.refresh_product_table()

        except Exception as e:
            print(f"Error inserting product: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to add product: {e}")


    def refresh_product_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT PRODUCT_ID, PRODUCT_NAME, PRODUCT_QOH, PRODUCT_PRICE, PRODUCT_DESC, SUPP_ID FROM PRODUCT")
            products = cursor.fetchall()

            self.ui.InventoryTable.setRowCount(0)  # Clear the table
            for row_number, row_data in enumerate(products):
                self.ui.InventoryTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    # Make all columns uneditable
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.ui.InventoryTable.setItem(row_number, column_number, item)
        except Exception as e:
            print(f"Error fetching products: {e}")

    def toggle_edit_mode(self):
        if self.Editbutton.text() == "Save":
            if self.save_edited_data():  # Save changes and check if successful
                self.Editbutton.setText("Edit")
                for row in range(self.ui.InventoryTable.rowCount()):
                    for col in range(self.ui.InventoryTable.columnCount()):
                        item = self.ui.InventoryTable.item(row, col)
                        if item:
                            # Disable editing for all columns
                            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        else:  # If the text is "Edit"
            self.Editbutton.setText("Save")
            for row in range(self.ui.InventoryTable.rowCount()):
                for col in range(self.ui.InventoryTable.columnCount()):
                    item = self.ui.InventoryTable.item(row, col)
                    if item:
                        # Enable editing for all columns except the first and last
                        if col != 0 and col != 5:
                            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    def save_edited_data(self):
        self.connect_to_database()
        try:
            edited = False  # Flag to track if any changes were saved
            for row in range(self.ui.InventoryTable.rowCount()):
                product_id = self.ui.InventoryTable.item(row, 0).text()
                product_name = self.ui.InventoryTable.item(row, 1).text()
                product_qoh = self.ui.InventoryTable.item(row, 2).text()
                product_price = self.ui.InventoryTable.item(row, 3).text()
                product_desc = self.ui.InventoryTable.item(row, 4).text()
                supp_id = self.ui.InventoryTable.item(row, 5).text()

                # Validate that the product_qoh is not negative
                if int(product_qoh) < 0:
                    QtWidgets.QMessageBox.warning(self, "Error", "Product Quantity On Hand cannot be negative")
                    return False

                # Validate that the product_price is not negative
                if float(product_price) < 0:
                    QtWidgets.QMessageBox.warning(self, "Error", "Product Price cannot be negative")
                    return False

                cursor = self.connection.cursor()
                cursor.execute("""
                    UPDATE PRODUCT
                    SET PRODUCT_NAME = %s, PRODUCT_QOH = %s, PRODUCT_PRICE = %s, 
                        PRODUCT_DESC = %s, SUPP_ID = %s
                    WHERE PRODUCT_ID = %s
                """, (product_name, product_qoh, product_price, product_desc, supp_id, product_id))
                self.connection.commit()

                # Check if any changes were actually made and saved
                if cursor.rowcount > 0:
                    edited = True

            # If any changes were saved, show success message
            if edited:
                self.refresh_product_table()
                QtWidgets.QMessageBox.information(self, "Success", "Product information updated successfully!")

            return edited

        except Exception as e:
            print(f"Error updating products: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update products: {e}")
            return False

    def delete_product(self):
        self.connect_to_database()
        
        selected_rows = self.ui.InventoryTable.selectionModel().selectedRows()
        
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a row to delete.")
            return
        
        reply = QtWidgets.QMessageBox.question(self, 'Confirm Deletion', 
                    'Are you sure you want to delete selected row(s)?',
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                for row in selected_rows:
                    product_id = self.ui.InventoryTable.item(row.row(), 0).text()
                    
                    cursor = self.connection.cursor()
                    cursor.execute("DELETE FROM PRODUCT WHERE PRODUCT_ID = %s", (product_id,))
                    self.connection.commit()
                    
                    self.ui.InventoryTable.removeRow(row.row())
                
                QtWidgets.QMessageBox.information(self, "Success", "Product(s) deleted successfully!")
                self.refresh_product_table()  # Refresh the table after deletion
                
            except Exception as e:
                print(f"Error deleting product(s): {e}")
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to delete product(s): {e}")


    def order_page(self):
        self.connect_to_database()
        self.ui.stackedWidget.setCurrentWidget(self.ui.OrderPage)
        self.ui.Order.setStyleSheet("QPushButton{background-color:rgb(223,203,171); border:null; border-radius:null; }")
        self.ui.Inventory.setStyleSheet("QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.ui.Report.setStyleSheet("QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.ui.Supplier.setStyleSheet("QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.orderTableWidget = self.findChild(QtWidgets.QTableWidget, 'OrderTable')
        self.refresh_order_table()

    def add_order(self):
        try:
            self.connect_to_database()
            # Create and configure the calendar widget dialog
            calendar_dialog = QDialog(self)
            calendar_dialog.setWindowTitle("Select Order Date")
            calendar_dialog.setStyleSheet("""
                QDialog {
                    background-color: #f2f2f2;
                    border-radius: 10px;
                    padding: 20px;
                }
                QCalendarWidget {
                    background-color: white;
                    border: 1px solid #ccc;
                    border-radius: 10px;
                }
                QDialogButtonBox {
                    padding-top: 10px;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
    
            # Calendar widget
            calendar = QCalendarWidget(calendar_dialog)
            calendar.setGridVisible(True)  # Show grid for better visibility
    
            # Buttons (OK and Cancel)
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, calendar_dialog)
            buttons.accepted.connect(calendar_dialog.accept)
            buttons.rejected.connect(calendar_dialog.reject)
    
            # Layout for the calendar and buttons
            layout = QVBoxLayout(calendar_dialog)
            layout.addWidget(calendar)
            layout.addWidget(buttons)

            # Show the dialog and check if the user selected a date and clicked OK
            if calendar_dialog.exec_() == QDialog.Accepted:
                # Get the selected date
                selected_date = calendar.selectedDate().toString("yyyy-MM-dd")

                # Validate the selected date
                try:
                    order_date_obj = datetime.strptime(selected_date, "%Y-%m-%d")
                    if order_date_obj > datetime.now():
                        QMessageBox.warning(self, "Error", "Order Date cannot be in the future.")
                        return
                    print(f"Selected Order Date: {selected_date}")
                except ValueError as e:
                    QMessageBox.warning(self, "Error", "Invalid date format. Please use YYYY-MM-DD.")
                    print(f"Date parsing error: {e}")
                    return
        
            else:
                # If calendar dialog is canceled or closed without selection
                return

            # Input dialog for product name
            product_name, ok = QInputDialog.getItem(self, "Input Dialog", "Select Product Name:", self.get_product_names(), 0, False)
            if not ok or not product_name:
                return

            # Fetch product price based on the selected product name
            product_price = self.get_product_price(product_name)
            if product_price is None:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to retrieve price for {product_name}.")
                return

            # Input dialog for quantity
            quantity, ok = QInputDialog.getInt(self, "Input Dialog", "Enter Quantity:")
            if not ok:
                return

            # Validate quantity
            if quantity <= 0:
                QtWidgets.QMessageBox.warning(self, "Error", "Quantity must be greater than 0.")
                return

            # Calculate total cost
            total_cost = quantity * product_price

            # Input dialog for payment method
            payment_method, ok = QInputDialog.getItem(self, "Input Dialog", 
                                                "Select Payment Method:", 
                                                ["Cash On Delivery", "Bank Transfer", "GCash"], 0, False)
            if not ok or not payment_method:
                return

            try:
                # Insert the new order into the database
                cursor = self.connection.cursor()
                cursor.execute("""
                INSERT INTO ORDERS (ORDER_DATE, ORDER_QUANTITY, ORDER_PAYMENT, ORDER_TOTAL, PRODUCT_ID)
                VALUES (%s, %s, %s, %s, (SELECT PRODUCT_ID FROM PRODUCT WHERE PRODUCT_NAME = %s))
                RETURNING ORDER_ID
                """, (selected_date, quantity, payment_method, decimal.Decimal(total_cost), product_name))
                order_id = cursor.fetchone()[0]

                # Update the quantity on hand in the inventory
                cursor.execute("""
                    UPDATE PRODUCT
                    SET PRODUCT_QOH = PRODUCT_QOH + %s
                    WHERE PRODUCT_NAME = %s
                """, (quantity, product_name))

                self.connection.commit()
                print(f"Inserted order with ID: {order_id}")

                # Insert the order details into the QTableWidget
                row_position = self.orderTableWidget.rowCount()
                self.orderTableWidget.insertRow(row_position)

                self.orderTableWidget.setItem(row_position, 0, QTableWidgetItem(selected_date))
                self.orderTableWidget.setItem(row_position, 1, QTableWidgetItem(str(order_id)))
                self.orderTableWidget.setItem(row_position, 2, QTableWidgetItem(product_name))
                self.orderTableWidget.setItem(row_position, 3, QTableWidgetItem(str(quantity)))
                self.orderTableWidget.setItem(row_position, 4, QTableWidgetItem(str(product_price)))
                self.orderTableWidget.setItem(row_position, 5, QTableWidgetItem(str(total_cost)))
                self.orderTableWidget.setItem(row_position, 6, QTableWidgetItem(payment_method))
                self.refresh_order_table()

            except Exception as e:
                print(f"Error inserting order: {e}")
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to add order: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")
            QtWidgets.QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")


    def toggle_edit_mode_order(self):
        if self.Editordbutton.text() == "Save":
            if self.save_edited_order_data():  # Save changes and check if successful
                self.Editordbutton.setText("Edit")
                for row in range(self.orderTableWidget.rowCount()):
                    for col in range(self.orderTableWidget.columnCount()):
                        item = self.orderTableWidget.item(row, col)
                        if item:
                            # Disable editing for all columns
                            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        else:  # If the text is "Edit"
            self.Editordbutton.setText("Save")
            for row in range(self.orderTableWidget.rowCount()):
                for col in range(self.orderTableWidget.columnCount()):
                    item = self.orderTableWidget.item(row, col)
                    if item:
                        # Enable editing for quantity and payment method columns
                        if col == 3 or col == 6:
                            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    def save_edited_order_data(self):
        self.connect_to_database()
        try:
            edited = False  # Flag to track if any changes were saved
            for row in range(self.orderTableWidget.rowCount()):
                order_id = self.orderTableWidget.item(row, 1).text()
                quantity = self.orderTableWidget.item(row, 3).text()
                payment_method = self.orderTableWidget.item(row, 6).text()

                # Fetch the product price from the corresponding product
                product_name = self.orderTableWidget.item(row, 2).text()
                product_price = self.get_product_price(product_name)
                if product_price is None:
                    QtWidgets.QMessageBox.warning(self, "Error", f"Failed to retrieve price for {product_name}.")
                    continue

                # Calculate the new total cost
                total_cost = float(quantity) * float(product_price)

                cursor = self.connection.cursor()
                cursor.execute("""
                    UPDATE ORDERS
                    SET ORDER_QUANTITY = %s, ORDER_PAYMENT = %s, ORDER_TOTAL = %s
                    WHERE ORDER_ID = %s
                """, (quantity, payment_method, decimal.Decimal(total_cost), order_id))
                self.connection.commit()

                # Check if any changes were actually made and saved
                if cursor.rowcount > 0:
                    edited = True

                    # Update the total cost in the QTableWidget
                    self.orderTableWidget.setItem(row, 5, QTableWidgetItem(str(total_cost)))

            # If any changes were saved, show success message
            if edited:
                self.refresh_order_table()
                QtWidgets.QMessageBox.information(self, "Success", "Order information updated successfully!")

            return edited

        except Exception as e:
            print(f"Error updating orders: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update orders: {e}")
            return False

    def delete_order(self):
        self.connect_to_database()
        
        selected_rows = self.orderTableWidget.selectionModel().selectedRows()
        
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a row to delete.")
            return
        
        reply = QtWidgets.QMessageBox.question(self, 'Confirm Deletion', 
                    'Are you sure you want to delete selected row(s)?',
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                for row in selected_rows:
                    order_id = self.orderTableWidget.item(row.row(), 1).text()
                    
                    cursor = self.connection.cursor()
                    cursor.execute("DELETE FROM ORDERS WHERE ORDER_ID = %s", (order_id,))
                    self.connection.commit()
                    
                    self.orderTableWidget.removeRow(row.row())
                
                QtWidgets.QMessageBox.information(self, "Success", "Order(s) deleted successfully!")
                self.refresh_order_table()  # Refresh the table after deletion
                
            except Exception as e:
                print(f"Error deleting order(s): {e}")
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to delete order(s): {e}")

    def refresh_order_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT O.ORDER_DATE, O.ORDER_ID, P.PRODUCT_NAME, O.ORDER_QUANTITY, P.PRODUCT_PRICE, 
                    O.ORDER_TOTAL, O.ORDER_PAYMENT
                FROM ORDERS O
                INNER JOIN PRODUCT P ON O.PRODUCT_ID = P.PRODUCT_ID
            """)
            orders = cursor.fetchall()

            self.orderTableWidget.setRowCount(0)  # Clear the table
            for row_number, row_data in enumerate(orders):
                self.orderTableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    item = QTableWidgetItem(str(data))
                    # Make all columns uneditable except for quantity and payment method initially
                    if column_number == 3 or column_number == 6:
                        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
                    else:
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                    self.orderTableWidget.setItem(row_number, column_number, item)
        
        except Exception as e:
            print(f"Error fetching orders: {e}")

    def get_product_names(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT PRODUCT_NAME FROM PRODUCT")
            products = cursor.fetchall()
            product_names = [product[0] for product in products]
            return product_names
        except Exception as e:
            print(f"Error fetching product names: {e}")
            return []

    def get_product_price(self, product_name):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT PRODUCT_PRICE FROM PRODUCT WHERE PRODUCT_NAME = %s", (product_name,))
            price = cursor.fetchone()
            if price:
                return price[0]
            else:
                return None
        except Exception as e:
            print(f"Error fetching product price: {e}")
            return None


    def report_page(self):
        self.connect_to_database()
        self.ui.stackedWidget.setCurrentWidget(self.ui.ReportManagement)
        self.ui.Report.setStyleSheet("QPushButton{background-color:rgb(223,203,171); border:null; border-radius:null; }")
        self.ui.Inventory.setStyleSheet("QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.ui.Order.setStyleSheet("QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.ui.Supplier.setStyleSheet("QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")

    def CSR_page(self):
        try:         
            self.connect_to_database()
            self.ui.stackedWidget.setCurrentWidget(self.ui.SalesReportPage)
            self.ui.Report.setStyleSheet("QPushButton { background-color: rgb(223, 203, 171); border: none; border-radius: none; }")
            self.ui.Inventory.setStyleSheet("QPushButton { background-color: none; border: none; } QPushButton:hover { background-color: rgba(255, 255, 255, 50); border-radius: 5px; }")
            self.ui.Order.setStyleSheet("QPushButton { background-color: none; border: none; } QPushButton:hover { background-color: rgba(255, 255, 255, 50); border-radius: 5px; }")
            self.ui.Supplier.setStyleSheet("QPushButton { background-color: none; border: none; } QPushButton:hover { background-color: rgba(255, 255, 255, 50); border-radius: 5px; }")

            # SQL query to fetch sales report data
            query = """
            SELECT 
                SR.SALES_REPORT_ID, 
                SR.SALES_DATE, 
                O.ORDER_ID,    -- Change to ORDER_ID
                P.PRODUCT_NAME, 
                S.SUPP_NAME, 
                SUM(O.ORDER_TOTAL) AS TOTAL_SALES, 
                O.ORDER_PAYMENT 
            FROM 
                SALES_REPORT SR
            JOIN 
                PRODUCT P ON SR.PRODUCT_ID = P.PRODUCT_ID
            JOIN 
                SUPPLIER S ON SR.SUPP_ID = S.SUPP_ID
            JOIN 
                ORDERS O ON SR.ORDER_ID = O.ORDER_ID   -- Change join condition
            GROUP BY 
                SR.SALES_REPORT_ID, SR.SALES_DATE, O.ORDER_ID, P.PRODUCT_NAME, S.SUPP_NAME, O.ORDER_PAYMENT
            """

            # Execute query
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                sales_reports = cursor.fetchall()

                # Populate the SalesReportTable with fetched data
                self.ui.SalesReportTable.setRowCount(len(sales_reports))
                self.ui.SalesReportTable.setColumnCount(7)
                self.ui.SalesReportTable.setHorizontalHeaderLabels(
                    ["Sales Report No.", "Date", "Order ID", "Product", "Supplier Name", "Total Spend", "Payment Method"]
                )

                for row_idx, report in enumerate(sales_reports):
                    for col_idx, data in enumerate(report):
                        item = QTableWidgetItem(str(data))
                        # Make all columns uneditable
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                        self.ui.SalesReportTable.setItem(row_idx, col_idx, item)

        except Exception as e:
            print(f"Error fetching sales reports: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to fetch sales reports: {e}")         


    def supplier_page(self):
        self.connect_to_database()
        self.ui.stackedWidget.setCurrentWidget(self.ui.SupplierManagementPage)
        self.ui.Supplier.setStyleSheet("QPushButton{background-color:rgb(223,203,171); border:null; border-radius:null; }")
        self.ui.Inventory.setStyleSheet("QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.ui.Order.setStyleSheet("QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.ui.Report.setStyleSheet("QPushButton{background-color: none; border:null} QPushButton:hover{background-color: rgba(255,255,255,50); border-radius: 5px;}")
        self.supplierTableWidget = self.findChild(QtWidgets.QTableWidget, 'SupplierManagementTable')
        self.refresh_supplier_table()

    def add_supplier(self):
        self.connect_to_database()

        while True:  # Start a loop to keep asking for valid input until all inputs are correct
            # Input dialog for supplier details
            supplier_name, ok = QInputDialog.getText(self, "Input Dialog", "Enter Supplier Name:")
            if not ok or not supplier_name:
                return  # Exit if canceled or empty name

            supplier_email, ok = QInputDialog.getText(self, "Input Dialog", "Enter Supplier Email:")
            if not ok or not supplier_email:
                return  # Exit if canceled or empty email

            # Validate email
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            while not re.match(email_pattern, supplier_email):  # Keep asking for email until valid
                QtWidgets.QMessageBox.warning(self, "Invalid Email Address", "Please enter a valid email address.")
                supplier_email, ok = QInputDialog.getText(self, "Input Dialog", "Enter Supplier Email:")
                if not ok or not supplier_email:
                    return  # Exit if canceled or empty email

            supplier_contact, ok = QInputDialog.getText(self, "Input Dialog", "Enter Supplier Contact Info:")
            if not ok or not supplier_contact:
                return  # Exit if canceled or empty contact info

            # Validate phone number
            phone_pattern = r'^(09\d{9}|\+639\d{9})$'
            while not re.match(phone_pattern, supplier_contact):  # Keep asking for contact info until valid
                QtWidgets.QMessageBox.warning(self, "Invalid Phone Number", "Phone number must be either 11 digits starting with '09' or start with '+63' followed by 9 digits.")
                supplier_contact, ok = QInputDialog.getText(self, "Input Dialog", "Enter Supplier Contact Info:")
                if not ok or not supplier_contact:
                    return  # Exit if canceled or empty contact info

            try:
                cursor = self.connection.cursor()
                # Check if the supplier name already exists (case-insensitive)
                cursor.execute("SELECT SUPP_NAME FROM SUPPLIER WHERE SUPP_NAME ILIKE %s", (supplier_name,))
                existing_supplier = cursor.fetchone()

                if existing_supplier:
                    QtWidgets.QMessageBox.warning(self, "Duplicate Supplier", "A supplier with this name already exists. Please enter a different name.")
                    continue  # If supplier name exists, restart the loop to correct it

                # Insert into the database
                cursor.execute("""
                    INSERT INTO SUPPLIER (SUPP_NAME, SUPP_EMAIL, SUPP_CONTACT)
                    VALUES (%s, %s, %s) RETURNING SUPP_ID
                """, (supplier_name, supplier_email, supplier_contact))
                supp_id = cursor.fetchone()[0]
                self.connection.commit()
                print(f"Inserted supplier with ID: {supp_id}")

                # Insert into the QTableWidget
                row_position = self.supplierTableWidget.rowCount()
                self.supplierTableWidget.insertRow(row_position)

                self.supplierTableWidget.setItem(row_position, 0, QTableWidgetItem(str(supp_id)))
                self.supplierTableWidget.setItem(row_position, 1, QTableWidgetItem(supplier_name))
                self.supplierTableWidget.setItem(row_position, 2, QTableWidgetItem(supplier_email))
                self.supplierTableWidget.setItem(row_position, 3, QTableWidgetItem(supplier_contact))
                self.refresh_supplier_table()
                break  # Exit the loop if everything is correct
            except Exception as e:
                print(f"Error inserting supplier: {e}")
                QtWidgets.QMessageBox.critical(self, "Error", f"An error occurred: {e}")
                break  # Exit the loop if an unexpected error occurs
           
    def refresh_supplier_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT SUPP_ID, SUPP_NAME, SUPP_EMAIL, SUPP_CONTACT FROM SUPPLIER")
            suppliers = cursor.fetchall()

            self.supplierTableWidget.setRowCount(0)  # Clear the table
            for row_number, row_data in enumerate(suppliers):
                self.supplierTableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.supplierTableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except Exception as e:
            print(f"Error fetching suppliers: {e}")

    def toggle_edit_mode_supplier(self):
        if self.Editsuppbutton.text() == "Save":
            if self.save_edited_supplier_data():  # Save changes and check if successful
                self.Editsuppbutton.setText("Edit")
                for row in range(self.supplierTableWidget.rowCount()):
                    for col in range(self.supplierTableWidget.columnCount()):
                        item = self.supplierTableWidget.item(row, col)
                        if item:
                            # Disable editing for all columns
                            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        else:  # If the text is "Edit"
            self.Editsuppbutton.setText("Save")
            for row in range(self.supplierTableWidget.rowCount()):
                for col in range(self.supplierTableWidget.columnCount()):
                    item = self.supplierTableWidget.item(row, col)
                    if item:
                        # Enable editing for all columns
                        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

    def save_edited_supplier_data(self):
        self.connect_to_database()
        try:
            edited = False  # Flag to track if any changes were saved
            for row in range(self.supplierTableWidget.rowCount()):
                supp_id = self.supplierTableWidget.item(row, 0).text()
                supplier_name = self.supplierTableWidget.item(row, 1).text()
                supplier_email = self.supplierTableWidget.item(row, 2).text()
                supplier_contact = self.supplierTableWidget.item(row, 3).text()

                cursor = self.connection.cursor()
                cursor.execute("""
                    UPDATE SUPPLIER
                    SET SUPP_NAME = %s, SUPP_EMAIL = %s, SUPP_CONTACT = %s
                    WHERE SUPP_ID = %s
                """, (supplier_name, supplier_email, supplier_contact, supp_id))
                self.connection.commit()

                # Check if any changes were actually made and saved
                if cursor.rowcount > 0:
                    edited = True
            
            # If any changes were saved, show success message
            if edited:
                self.refresh_supplier_table()
                QtWidgets.QMessageBox.information(self, "Success", "Supplier information updated successfully!")
            
            return edited

        except Exception as e:
            print(f"Error updating suppliers: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", f"Failed to update suppliers: {e}")
            return False

    def delete_supplier(self):
        self.connect_to_database()
        
        selected_rows = self.supplierTableWidget.selectionModel().selectedRows()
        
        if not selected_rows:
            QtWidgets.QMessageBox.warning(self, "Error", "Please select a row to delete.")
            return
        
        reply = QtWidgets.QMessageBox.question(self, 'Confirm Deletion', 
                    'Are you sure you want to delete selected row(s)?',
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                for row in selected_rows:
                    supp_id = self.supplierTableWidget.item(row.row(), 0).text()
                    
                    cursor = self.connection.cursor()
                    cursor.execute("DELETE FROM SUPPLIER WHERE SUPP_ID = %s", (supp_id,))
                    self.connection.commit()
                    
                    self.supplierTableWidget.removeRow(row.row())
                
                QtWidgets.QMessageBox.information(self, "Success", "Supplier(s) deleted successfully!")
                self.refresh_supplier_table()  # Refresh the table after deletion
                
            except Exception as e:
                print(f"Error deleting supplier(s): {e}")
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to delete supplier(s): {e}")

    #back_button
    def back(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.ReportManagement)

    #Log out
    # Log out
    def logout(self):
     # Show confirmation dialog before closing the window
        reply = QtWidgets.QMessageBox.question(self, 'Confirm Logout', 
                                           'Are you sure you want to logout?', 
                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            print("Logged out!")
            self.close()  # Close the main window
            self.login_window = MainWindow()  # Create a new instance of the login window
            self.login_window.show()  # Show the login window
        else:
            print("Logout cancelled.")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    login_window = MainWindow()
    sys.exit(app.exec_())
