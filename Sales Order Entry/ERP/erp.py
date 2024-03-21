import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json

# Define the JSON string containing Firebase service account credentials
json_data = """
{
  "type": "service_account",
  "project_id": "rpa-1-e5000",
  "private_key_id": "9183f1194ddca9b0cd5ccb9e38daeaae2c62c76c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCWM9OHx/f7W7kh\nrf2pfcglEnpW9Po32NBr48SogCkT/ew23tvRQ66PzeZnQJOLpm+Uk2c7El3vg+/V\nXye4xWqlWdpeKFZHKQif0Ww8LdQwuz3EAJN9uXJ5ZHzI3PCbrW3XG4hBAeL/o/9x\nyrGGmKoVwWI5HNsuHIvsueqSCfBb89qA0UsZCymmvQ1ro64bOVvbxbdJDWjKJbLS\nVY4eiaDZbdk/BYXrZZEnch04nnhz2ZZik6WbCAasvEwUxplQik8ZzCZCMlzLr3kD\nSGTl5a8BLjq7LjcMLe8fMTZadVS9hgGB3fYWn/tA1LDSxv3EFZDU1jum4kSDCw0g\n5tASPV+lAgMBAAECggEAB8VFn8QuJaBgqwfj1CVwOc7DaoVA/qumWLaPYYJD3cdo\ntYwBBkoAmWr3DQdvuq1RH3giwpEYMAB842aJWQtJkaVc4Tsn/4V1b0M33MMoM580\nOlQnTT1PWU1kEUYw4nTt9k9z1J0i38PdvsbUOVjjj72R9c9y3WdXq9cQdh6ygyc9\nrWUP9dUHM5vD9fP87soCF6FYHLMWZkWs0bqfCCGsFf9zNLnQSLK+5XI3zhQBp3aW\nIkU9MAGvWGTiSUbCtezVXdZFvQMhrlcMax45u6W3VkHcQzdP1SsHm9xL7n7Aks34\nEHMIBT7N1dA3728VmnYwq2PHfJ7kVz7aetCiIGBM4QKBgQDKbdUX7IZXAnVvt4D6\n6mrLzI285OdZ+kTKKot/xQ/uLTYrO1+N85jCpnzGuBJcO7z7Ohnh9n+T16BmmDCD\nM2LbOH/IZfyZBYiPRuDShIAGxwNz+cL8PvOeDJz26EQ0lHODJ39lJwGLa6LI/j9u\nK+a9PBXxvAEOfR1PssXT4fFm8QKBgQC9877mlPsjAa6ZiMyrqC9U2l6xo4UmJ1h2\n1rheQKgUU2IPemDrIZcAjJPXhJnfU518ZozobtIdbiP2PJeY8z7WU2nr03YUmrgg\np0CVrK30Vp4b4bq7nWfc9DuyMRe2hkeyYdZRyvlzwAyprZFCsGXcH2sXL4Xj+fv0\npkIi4mGL9QKBgQCNzXSqBqlwyCsl8EEtBAt96jQb76nVEQkhKb6A6bWoHgnFLRlZ\n4hvPtzrPJeDOtZZD0saQ0NE76p/VXqUVM2j7sk9pPXA+bW7lFzykm+bnWIAlvP+H\nHj4gKCvIlpo4zwlABeorHLDrTqJA9EHQ1nYTd8TTiuSelqxyyQPl0m/9sQKBgGuX\nYXz3y9wDOuNqMgvU4qJcYiCaL3Px+1CsxJdWZh3FMRj1R2pHh2FfPupnCEUP9ncd\nGxkYlFjpJuN1ZKTUurXpX2idSRfYnwyXz6Q3v/xTB5FhZUSZntfvWtTOq9DN9FRc\nyGlh37Oph0KgtlOg2ME65oymdV8xHH5xoapisb/1AoGAOmul/64wunyENXd+xCZd\nMXEGnBFc8gk7lRllkSOJSpFoh0zb2L8V405ikf/KeEU0sYHvSr1Rbhxzs7ulQ18g\nscPVTGrNqcSlozGJDlF/aoe4V3S56fPfDuIUW0d/QS1vCgF8wUCcijGUGUfaVkMU\nizPUTyRyhzmkwV20VDlEFVY=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-2uzh1@rpa-1-e5000.iam.gserviceaccount.com",
  "client_id": "101755207364690198030",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-2uzh1%40rpa-1-e5000.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""

# Load credentials from the JSON string
cred = credentials.Certificate(json.loads(json_data,strict=False))

# Initialize Firebase Admin SDK
firebase_admin.initialize_app(cred)

# Get a Firestore client
db = firestore.client()

class InvoiceGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Invoice Details")
        self.geometry("600x500")

        self.item_list = []
        self.invoice_list = []
        

        main_panel = tk.Frame(self)
        main_panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Input fields
        input_panel = tk.Frame(main_panel, borderwidth=2, relief="groove")
        input_panel.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)

        tk.Label(input_panel, text="Company Name:").grid(row=0, column=0, sticky="e")
        self.company_name_field = tk.Entry(input_panel)
        self.company_name_field.grid(row=0, column=1, sticky="w")

        tk.Label(input_panel, text="Invoice Date (yyyy-MM-dd):").grid(row=1, column=0, sticky="e")
        self.invoice_date_field = tk.Entry(input_panel)
        self.invoice_date_field.grid(row=1, column=1, sticky="w")

        tk.Label(input_panel, text="Invoice Number:").grid(row=2, column=0, sticky="e")
        self.invoice_num_field = tk.Entry(input_panel)
        self.invoice_num_field.grid(row=2, column=1, sticky="w")

        tk.Label(input_panel, text="Invoice Price:").grid(row=3, column=0, sticky="e")
        self.total_field = tk.Entry(input_panel)
        self.total_field.grid(row=3, column=1, sticky="w")

        tk.Label(input_panel, text="Item Name:").grid(row=4, column=0, sticky="e")
        self.item_name_field = tk.Entry(input_panel)
        self.item_name_field.grid(row=4, column=1, sticky="w")

        tk.Label(input_panel, text="Quantity:").grid(row=5, column=0, sticky="e")
        self.quantity_field = tk.Entry(input_panel)
        self.quantity_field.grid(row=5, column=1, sticky="w")

        tk.Label(input_panel, text="Unit Price:").grid(row=6, column=0, sticky="e")
        self.unit_price_field = tk.Entry(input_panel)
        self.unit_price_field.grid(row=6, column=1, sticky="w")

        tk.Label(input_panel, text="Total Price:").grid(row=7, column=0, sticky="e")
        self.total_field = tk.Entry(input_panel)
        self.total_field.grid(row=7, column=1, sticky="w")

        # Buttons
        button_panel = tk.Frame(main_panel)
        button_panel.pack(side=tk.BOTTOM, pady=10)

        self.add_item_button = tk.Button(button_panel, text="Add Item", command=self.add_item)
        self.add_item_button.pack(side=tk.LEFT, padx=5)

        self.add_invoice_button = tk.Button(button_panel, text="Add Invoice", command=self.add_invoice)
        self.add_invoice_button.pack(side=tk.LEFT, padx=5)

        self.send_button = tk.Button(button_panel, text="Send", command=self.send_invoices)
        self.send_button.pack(side=tk.LEFT, padx=5)

        # Added Items Text Area
        self.added_items_text_area = tk.Text(main_panel, height=10, width=1)
        self.added_items_text_area.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Invoice Details Text Area
        self.invoice_details_text_area = tk.Text(main_panel, height=10, width=1)
        self.invoice_details_text_area.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

    def add_item(self):
        item_name = self.item_name_field.get()
        quantity = (self.quantity_field.get())
        unit_price = (self.unit_price_field.get())
        total_price = (self.total_field.get())

        self.item_list.append(Item(item_name, quantity, unit_price))

        self.added_items_text_area.insert(tk.END, f"Item: {item_name}, Quantity: {quantity}, Unit Price: {unit_price}, Total Price: {total_price}\n")

        self.item_name_field.delete(0, tk.END)
        self.quantity_field.delete(0, tk.END)
        self.unit_price_field.delete(0, tk.END)
        self.total_field.delete(0, tk.END)

    def add_invoice(self):
        company_name = self.company_name_field.get()
        invoice_date = self.invoice_date_field.get()
        invoice_num = self.invoice_num_field.get()

        invoice = Invoice(company_name, invoice_date, invoice_num)

        for item in self.item_list:
            invoice.add_item(item)

        self.invoice_list.append(invoice)

        self.invoice_details_text_area.insert(tk.END, f"Company Name: {company_name}\nInvoice Date: {invoice_date}\nInvoice Number: {invoice_num}\nItems:\n")

        for item in self.item_list:
            self.invoice_details_text_area.insert(tk.END, f"- {item.get_item_name()}, Quantity: {item.get_quantity()}, Unit Price: {item.get_unit_price()}, Total Price: {item.get_total()}\n")

        self.clear_fields()

    def send_invoices(self):
        for invoice in self.invoice_list:
            company_name = invoice.get_company_name()
            invoice_date = invoice.get_invoice_date()
            invoice_num = invoice.get_invoice_num()

            invoice_data = {
                "companyName": company_name,
                "invoiceDate": invoice_date,
                "invoiceNum": invoice_num,
                "items": []
            }

            for item in invoice.get_items():
                item_data = {
                    "itemName": item.get_item_name(),
                    "quantity": item.get_quantity(),
                    "unitPrice": item.get_unit_price(),
                    "totalPrice": item.get_total()
                }
                invoice_data["items"].append(item_data)

            # Simulating sending data to Firebase
            print("Sending Invoice Data to Firebase: " + invoice.get_invoice_num())

            # Add a new document with a generated ID
            db.collection("invoices").add(invoice_data)


        # Clear invoice list after sending all invoices
        self.invoice_list.clear()

        # Display success message
        messagebox.showinfo("Success", "Invoices sent to Firebase successfully.")

    def clear_fields(self):
        self.company_name_field.delete(0, tk.END)
        self.invoice_date_field.delete(0, tk.END)
        self.invoice_num_field.delete(0, tk.END)
        self.item_name_field.delete(0, tk.END)
        self.quantity_field.delete(0, tk.END)
        self.unit_price_field.delete(0, tk.END)
        self.total_field.delete(0, tk.END)
        self.added_items_text_area.delete(1.0, tk.END)
        self.item_list.clear()


class Invoice:
    def __init__(self, company_name, invoice_date, invoice_num):
        self.company_name = company_name
        self.invoice_date = invoice_date
        self.invoice_num = invoice_num
        self.items = []

    def get_company_name(self):
        return self.company_name

    def get_invoice_date(self):
        return self.invoice_date

    def get_invoice_num(self):
        return self.invoice_num

    def add_item(self, item):
        self.items.append(item)

    def get_items(self):
        return self.items


class Item:
    def __init__(self, item_name, quantity, unit_price):
        self.item_name = item_name
        self.quantity = quantity
        self.unit_price = unit_price

    def get_item_name(self):
        return self.item_name

    def get_quantity(self):
        return self.quantity

    def get_unit_price(self):
        return self.unit_price

    def get_total(self):
        return self.quantity * self.unit_price


# Example Usage:
if __name__ == "__main__":
    app = InvoiceGUI()
    app.mainloop()
