import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import os

class StockManagementGUI:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        self.root.title("Supplify Stock Management")
        self.root.configure(background="#F0F0F0")
        self.root.pack_propagate(0)  # Disable automatic resizing
        self.logo = tk.Label(self.root, text="Supplify Egypt", font=("Arial", 20), bg="#F0F0F0")
        self.logo.place(x=10, y=10)
        # Search option
        self.search_label = tk.Label(self.root, text="Search:", bg="#F0F0F0")
        self.search_label.place(x=20, y=310)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.place(x=80, y=310)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_items)
        self.search_button.place(x=220, y=310)
        
        self.item_name_label = tk.Label(self.root, text="Item Name:", bg="#F0F0F0")
        self.item_name_label.place(x=20, y=60)
        self.item_name_entry = tk.Entry(self.root)
        self.item_name_entry.place(x=150, y=60)
        
        self.purchase_price_label = tk.Label(self.root, text="Purchase Price:", bg="#F0F0F0")
        self.purchase_price_label.place(x=20, y=90)
        self.purchase_price_entry = tk.Entry(self.root)
        self.purchase_price_entry.place(x=150, y=90)
        
        self.sale_price_label = tk.Label(self.root, text="Sale Price:", bg="#F0F0F0")
        self.sale_price_label.place(x=20, y=120)
        self.sale_price_entry = tk.Entry(self.root)
        self.sale_price_entry.place(x=150, y=120)
        
        self.quantity_purchased_label = tk.Label(self.root, text="Quantity Purchased:", bg="#F0F0F0")
        self.quantity_purchased_label.place(x=20, y=150)
        self.quantity_purchased_entry = tk.Entry(self.root)
        self.quantity_purchased_entry.place(x=150, y=150)
        
        self.quantity_sold_label = tk.Label(self.root, text="Quantity Sold:", bg="#F0F0F0")
        self.quantity_sold_label.place(x=20, y=180)
        self.quantity_sold_entry = tk.Entry(self.root)
        self.quantity_sold_entry.place(x=150, y=180)
        
        self.date_added_label = tk.Label(self.root, text="Date Added:", bg="#F0F0F0")
        self.date_added_label.place(x=20, y=210)
        self.date_added_entry = tk.Entry(self.root, state="disabled")
        self.date_added_entry.place(x=150, y=210)
        
        self.date_modified_label = tk.Label(self.root, text="Date Modified:", bg="#F0F0F0")
        self.date_modified_label.place(x=20, y=240)
        self.date_modified_entry = tk.Entry(self.root, state="disabled")
        self.date_modified_entry.place(x=150, y=240)
        
        self.add_button = tk.Button(self.root, text="Add Item", command=self.add_item)
        self.add_button.place(x=20, y=280)
        
        self.update_button = tk.Button(self.root, text="Update Item", command=self.update_item)
        self.update_button.place(x=110, y=280)
        
        self.delete_button = tk.Button(self.root, text="Delete Item", command=self.delete_item)
        self.delete_button.place(x=210, y=280)
        
        self.save_button = tk.Button(self.root, text="Save", command=self.save_data)
        self.save_button.place(x=20, y=530)
        
        self.import_button = tk.Button(self.root, text="Import", command=self.import_data)
        self.import_button.place(x=90, y=530)
        
        self.export_button = tk.Button(self.root, text="Export", command=self.export_data)
        self.export_button.place(x=160, y=530)
        
        self.item_list_label = tk.Label(self.root, text="Item List:", font=("Arial", 16), bg="#F0F0F0")
        self.item_list_label.place(x=330, y=10)
        self.item_list = tk.Listbox(self.root, height=15, width=45)
        self.item_list.place(x=330, y=50)
        self.item_list.bind('<<ListboxSelect>>', self.display_item_details)
        
        self.details_label = tk.Label(self.root, text="Item Details:", font=("Arial", 16), bg="#F0F0F0")
        self.details_label.place(x=330, y=270)
        
        self.item_details = tk.Label(self.root, text="", font=("Arial", 12), bg="#F0F0F0", justify="left")
        self.item_details.place(x=330, y=310)
        
        self.plot_button = tk.Button(self.root, text="Plot Sales", command=self.plot_sales)
        self.plot_button.place(x=300, y=530)
        
        self.load_data()
        self.load_item_list()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def get_script_path(self):
        if getattr(sys, 'frozen', False):
            # Executable frozen with PyInstaller
            return os.path.dirname(sys.executable)
        else:
            # Script executed directly
            return os.path.dirname(os.path.abspath(sys.argv[0]))
    
    def load_data(self):
        script_dir = self.get_script_path()
        file_path = os.path.join(script_dir, "stock_data.xlsx")
        try:
            self.data = pd.read_excel(file_path)
        except FileNotFoundError:
            self.data = pd.DataFrame(columns=["Item Name", "Purchase Price", "Sale Price", "Quantity Purchased",
                                            "Quantity Sold", "Date Added", "Date Modified"])
    
    def save_data(self):
        script_dir = self.get_script_path()
        file_path = os.path.join(script_dir, "stock_data.xlsx")
        try:
            self.data.to_excel(file_path, index=False)
            messagebox.showinfo("Save", "Data saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data. Error: {str(e)}")

    
    def import_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                self.data = pd.read_excel(file_path)
                self.load_item_list()
                messagebox.showinfo("Import", "Data imported successfully!")
            except:
                messagebox.showerror("Error", "Failed to import data.")
    
    def export_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                self.data.to_excel(file_path, index=False)
                messagebox.showinfo("Export", "Data exported successfully!")
            except:
                messagebox.showerror("Error", "Failed to export data.")
    
    def load_item_list(self):
        self.item_list.delete(0, tk.END)
        items = self.data["Item Name"].tolist()
        for item in items:
            self.item_list.insert(tk.END, item)
    def search_items(self):
        search_query = self.search_entry.get().strip()
        if search_query:
            search_results = self.data[self.data["Item Name"].str.contains(search_query, case=False)]
            if not search_results.empty:
                self.item_list.delete(0, tk.END)
                items = search_results["Item Name"].tolist()
                for item in items:
                    self.item_list.insert(tk.END, item)
                self.item_details.config(text="")
                self.clear_fields()
                messagebox.showinfo("Search", f"{len(search_results)} item(s) found.")
            else:
                messagebox.showinfo("Search", "No items found.")
        else:
            messagebox.showwarning("Search", "Please enter a search query.")

        self.search_entry.delete(0, tk.END)
    
    def add_item(self):
        item_name = self.item_name_entry.get().strip()
        purchase_price = self.purchase_price_entry.get().strip()
        sale_price = self.sale_price_entry.get().strip()
        quantity_purchased = self.quantity_purchased_entry.get().strip()
        quantity_sold = self.quantity_sold_entry.get().strip()
        
        if not item_name or not purchase_price or not sale_price or not quantity_purchased or not quantity_sold:
            messagebox.showerror("Error", "Please enter all fields.")
            return
        
        try:
            purchase_price = float(purchase_price)
            sale_price = float(sale_price)
            quantity_purchased = int(quantity_purchased)
            quantity_sold = int(quantity_sold)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for numeric fields.")
            return
        
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_item = pd.DataFrame({
            "Item Name": [item_name],
            "Purchase Price": [purchase_price],
            "Sale Price": [sale_price],
            "Quantity Purchased": [quantity_purchased],
            "Quantity Sold": [quantity_sold],
            "Date Added": [current_date],
            "Date Modified": [current_date]
        })
        
        self.data = pd.concat([self.data, new_item], ignore_index=True)
        self.clear_fields()
        self.load_item_list()
        self.save_data()
        messagebox.showinfo("Add Item", "Item added successfully!")
        self.root.update()  # Update window size after adding item
    
    def update_item(self):
        selected_item = self.item_list.curselection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return
        
        index = selected_item[0]
        
        item_name = self.item_name_entry.get().strip()
        purchase_price = self.purchase_price_entry.get().strip()
        sale_price = self.sale_price_entry.get().strip()
        quantity_purchased = self.quantity_purchased_entry.get().strip()
        quantity_sold = self.quantity_sold_entry.get().strip()
        
        if not item_name or not purchase_price or not sale_price or not quantity_purchased or not quantity_sold:
            messagebox.showerror("Error", "Please enter all fields.")
            return
        
        try:
            purchase_price = float(purchase_price)
            sale_price = float(sale_price)
            quantity_purchased = int(quantity_purchased)
            quantity_sold = int(quantity_sold)
        except ValueError:
            messagebox.showerror("Error", "Invalid input for numeric fields.")
            return
        
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.data.at[index, "Item Name"] = item_name
        self.data.at[index, "Purchase Price"] = purchase_price
        self.data.at[index, "Sale Price"] = sale_price
        self.data.at[index, "Quantity Purchased"] = quantity_purchased
        self.data.at[index, "Quantity Sold"] = quantity_sold
        self.data.at[index, "Date Modified"] = current_date
        
        self.clear_fields()
        self.load_item_list()
        self.save_data()
        messagebox.showinfo("Update Item", "Item updated successfully!")
    
    def delete_item(self):
        selected_item = self.item_list.curselection()
        if not selected_item:
            messagebox.showerror("Error", "No item selected.")
            return
        
        index = selected_item[0]
        self.data.drop(index, inplace=True)
        self.clear_fields()
        self.load_item_list()
        self.save_data()
        messagebox.showinfo("Delete Item", "Item deleted successfully!")
    
    def display_item_details(self, event):
        selected_item = self.item_list.curselection()
        if not selected_item:
            return
        
        index = selected_item[0]
        item = self.data.loc[index]
        details = f"Item Name: {item['Item Name']}\n"
        details += f"Purchase Price: {item['Purchase Price']}\n"
        details += f"Sale Price: {item['Sale Price']}\n"
        details += f"Quantity Purchased: {item['Quantity Purchased']}\n"
        details += f"Quantity Sold: {item['Quantity Sold']}\n"
        details += f"Date Added: {item['Date Added']}\n"
        details += f"Date Modified: {item['Date Modified']}"
        
        self.item_details.config(text=details)
        
        self.item_name_entry.delete(0, tk.END)
        self.item_name_entry.insert(tk.END, item['Item Name'])
        self.purchase_price_entry.delete(0, tk.END)
        self.purchase_price_entry.insert(tk.END, item['Purchase Price'])
        self.sale_price_entry.delete(0, tk.END)
        self.sale_price_entry.insert(tk.END, item['Sale Price'])
        self.quantity_purchased_entry.delete(0, tk.END)
        self.quantity_purchased_entry.insert(tk.END, item['Quantity Purchased'])
        self.quantity_sold_entry.delete(0, tk.END)
        self.quantity_sold_entry.insert(tk.END, item['Quantity Sold'])
        self.date_added_entry.config(state="normal")
        self.date_added_entry.delete(0, tk.END)
        self.date_added_entry.insert(tk.END, item['Date Added'])
        self.date_added_entry.config(state="disabled")
        self.date_modified_entry.config(state="normal")
        self.date_modified_entry.delete(0, tk.END)
        self.date_modified_entry.insert(tk.END, item['Date Modified'])
        self.date_modified_entry.config(state="disabled")
    
    def clear_fields(self):
        self.item_name_entry.delete(0, tk.END)
        self.purchase_price_entry.delete(0, tk.END)
        self.sale_price_entry.delete(0, tk.END)
        self.quantity_purchased_entry.delete(0, tk.END)
        self.quantity_sold_entry.delete(0, tk.END)
        self.date_added_entry.config(state="normal")
        self.date_added_entry.delete(0, tk.END)
        self.date_added_entry.config(state="disabled")
        self.date_modified_entry.config(state="normal")
        self.date_modified_entry.delete(0, tk.END)
        self.date_modified_entry.config(state="disabled")
        self.item_details.config(text="")
    
    def plot_sales(self):
        if len(self.data) == 0:
            messagebox.showerror("Error", "No data available to plot.")
            return
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(self.data["Date Added"], self.data["Quantity Sold"], marker="o", linestyle="-", color="blue")
        ax.set_xlabel("Date")
        ax.set_ylabel("Quantity Sold")
        ax.set_title("Sales over Time")
        ax.grid(True)        
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().place(x=600, y=350)
    
    def on_closing(self):
        self.save_data()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StockManagementGUI(root)
    root.mainloop()
