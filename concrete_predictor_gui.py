"""
Concrete Mixture Prediction System
Interactive GUI for predicting Cost, Compressive Strength, and CO2 Emissions
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import joblib
import numpy as np
import pandas as pd
import os
import sys

class ConcretePredictorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Otsile Lame Mateise, 202103314")
        self.root.geometry("1100x650")
        self.root.resizable(True, True)
        
        # Load model registry
        try:
            # Show current working directory for debugging
            current_dir = os.getcwd()
            model_path = os.path.join('trained_models', 'model_registry.pkl')
            
            if not os.path.exists('trained_models'):
                messagebox.showerror("Error", 
                    f"'trained_models' folder not found!\n\n"
                    f"Current directory: {current_dir}\n\n"
                    f"Please create a 'trained_models' folder in the same directory as this script "
                    f"and place your model_registry.pkl file inside it.")
                sys.exit(1)
            
            if not os.path.exists(model_path):
                messagebox.showerror("Error", 
                    f"'model_registry.pkl' file not found!\n\n"
                    f"Looking in: {os.path.join(current_dir, model_path)}\n\n"
                    f"Please ensure model_registry.pkl is in the trained_models folder.")
                sys.exit(1)
            
            self.model_registry = joblib.load(model_path)
            self.ash_types = self.model_registry['ash_types']
            self.target_variables = self.model_registry['target_variables']
            self.input_variables = self.model_registry['input_variables']
            self.models = self.model_registry['models']
            
            # Fix XGBoost compatibility issues
            self._fix_xgboost_models()
        except Exception as e:
            messagebox.showerror("Error", 
                f"Failed to load models: {str(e)}\n\n"
                f"Current directory: {os.getcwd()}\n\n"
                f"Please ensure 'trained_models/model_registry.pkl' exists.")
            sys.exit(1)
        
        # Variables
        self.selected_ash_type = tk.StringVar()
        self.input_values = {}
        
        # Setup GUI
        self.setup_gui()
        
    def _fix_xgboost_models(self):
        """Fix XGBoost models for compatibility with newer versions"""
        try:
            import xgboost
            for ash_type in self.models:
                for target_var in self.models[ash_type]:
                    model = self.models[ash_type][target_var]['model']
                    # Check if it's an XGBoost model
                    if hasattr(model, '__class__') and 'XGB' in model.__class__.__name__:
                        # Remove deprecated parameters
                        deprecated_params = ['gpu_id', 'predictor', 'n_gpus']
                        for param in deprecated_params:
                            if hasattr(model, param):
                                try:
                                    delattr(model, param)
                                except:
                                    pass
        except Exception as e:
            print(f"Warning: Could not fix XGBoost models: {e}")
        
    def setup_gui(self):
        """Setup the main GUI layout"""
        
        # Main container with less padding
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title - smaller font
        title_label = ttk.Label(main_frame, text="Concrete Mixture Prediction System", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Subtitle - smaller font
        subtitle_label = ttk.Label(main_frame, text="Predict Cost, Compressive Strength, and CO₂ Emissions", 
                                  font=('Arial', 9))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 5))
        
        # Left Panel - Input Section
        left_panel = ttk.LabelFrame(main_frame, text="Input Parameters", padding="5")
        left_panel.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 3))
        left_panel.columnconfigure(0, weight=1)
        
        # Ash Type Selection - more compact
        ash_frame = ttk.LabelFrame(left_panel, text="Select Ash Type", padding="5")
        ash_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        ash_frame.columnconfigure(0, weight=1)
        
        # Create buttons for ash types - smaller
        self.ash_buttons = []
        button_frame = ttk.Frame(ash_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        for i, ash_type in enumerate(self.ash_types):
            ash_display = ash_type.replace(' 1', '')
            btn = ttk.Button(button_frame, text=ash_display, 
                           command=lambda a=ash_type: self.select_ash_type(a),
                           width=10)
            btn.grid(row=i//3, column=i%3, padx=2, pady=2, sticky=(tk.W, tk.E))
            self.ash_buttons.append(btn)
            button_frame.columnconfigure(i%3, weight=1)
        
        # Pozzolan Type Selection - more compact
        pozzolan_frame = ttk.Frame(left_panel)
        pozzolan_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        pozzolan_frame.columnconfigure(1, weight=1)
        
        ttk.Label(pozzolan_frame, text="Pozzolan:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        pozzolan_types = ['None', 'Fly Ash', 'Silica Fume', 'Metakaolin', 'Other']
        self.pozzolan_var = tk.StringVar(value='Fly Ash')
        pozzolan_dropdown = ttk.Combobox(pozzolan_frame, textvariable=self.pozzolan_var, 
                                        values=pozzolan_types, state='readonly', width=15)
        pozzolan_dropdown.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Input Variables - more compact
        input_frame = ttk.LabelFrame(left_panel, text="Mixture Parameters", padding="5")
        input_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 5))
        input_frame.columnconfigure(1, weight=1)
        left_panel.rowconfigure(2, weight=1)
        
        # Create scrollable frame for inputs with reduced height
        canvas = tk.Canvas(input_frame, height=250)
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        input_frame.rowconfigure(0, weight=1)
        input_frame.columnconfigure(0, weight=1)
        
        # Input variable labels and descriptions
        input_info = {
            'replacement_pct': ('Replacement %', 'Percentage of cement replaced (0-100)'),
            'cement_kg_m3': ('Cement (kg/m³)', 'Cement content in kg per cubic meter'),
            'ash_kg_m3': ('Ash (kg/m³)', 'Ash content in kg per cubic meter'),
            'fine_aggregate_kg_m3': ('Fine Aggregate (kg/m³)', 'Fine aggregate content'),
            'coarse_aggregate_kg_m3': ('Coarse Aggregate (kg/m³)', 'Coarse aggregate content'),
            'pozzolan added(Fly Ash) kgm3': ('Pozzolan Added (kg/m³)', 'Additional pozzolan content'),
            'superplasticizer_kg_m3': ('Superplasticizer (kg/m³)', 'Superplasticizer content'),
            'water kg_m3': ('Water (kg/m³)', 'Water content in kg per cubic meter'),
            'curing_days': ('Curing Days', 'Number of days for curing (e.g., 7, 28, 90)')
        }
        
        row = 0
        for var in self.input_variables:
            if var in input_info:
                label_text, tooltip = input_info[var]
                
                # Label - smaller font
                label = ttk.Label(scrollable_frame, text=label_text + ":", font=('Arial', 8))
                label.grid(row=row, column=0, sticky=tk.W, pady=2, padx=(0, 5))
                
                # Entry - smaller
                entry_var = tk.StringVar(value="0")
                self.input_values[var] = entry_var
                entry = ttk.Entry(scrollable_frame, textvariable=entry_var, width=20)
                entry.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2)
                
                # Tooltip
                tooltip_label = ttk.Label(scrollable_frame, text="ℹ", foreground="blue", cursor="question_arrow")
                tooltip_label.grid(row=row, column=2, padx=(3, 0))
                self.create_tooltip(tooltip_label, tooltip)
                
                row += 1
        
        scrollable_frame.columnconfigure(1, weight=1)
        
        # Buttons - more compact
        button_panel = ttk.Frame(left_panel)
        button_panel.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        button_panel.columnconfigure(0, weight=1)
        button_panel.columnconfigure(1, weight=1)
        button_panel.columnconfigure(2, weight=1)
        
        predict_btn = ttk.Button(button_panel, text="Predict", command=self.predict, style='Accent.TButton')
        predict_btn.grid(row=0, column=0, padx=2, sticky=(tk.W, tk.E))
        
        clear_btn = ttk.Button(button_panel, text="Clear", command=self.clear_inputs)
        clear_btn.grid(row=0, column=1, padx=2, sticky=(tk.W, tk.E))
        
        example_btn = ttk.Button(button_panel, text="Load Example", command=self.load_example)
        example_btn.grid(row=0, column=2, padx=2, sticky=(tk.W, tk.E))
        
        # Right Panel - Results Section - more compact
        right_panel = ttk.LabelFrame(main_frame, text="Prediction Results", padding="5")
        right_panel.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(3, 0))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        
        # Results text area - smaller font
        self.results_text = scrolledtext.ScrolledText(right_panel, wrap=tk.WORD, 
                                                      width=45, height=25, 
                                                      font=('Courier', 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status Bar - smaller
        self.status_bar = ttk.Label(main_frame, text="Ready", relief=tk.SUNKEN, anchor=tk.W, font=('Arial', 8))
        self.status_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Initial message
        self.show_welcome_message()
        
    def create_tooltip(self, widget, text):
        """Create tooltip for widget"""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = ttk.Label(tooltip, text=text, background="lightyellow", 
                            relief=tk.SOLID, borderwidth=1, padding=3, font=('Arial', 8))
            label.pack()
            widget.tooltip = tooltip
            
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                
        widget.bind('<Enter>', on_enter)
        widget.bind('<Leave>', on_leave)
    
    def select_ash_type(self, ash_type):
        """Handle ash type selection"""
        self.selected_ash_type.set(ash_type)
        
        # Update button styles
        for btn in self.ash_buttons:
            btn.state(['!pressed'])
        
        # Find and highlight selected button
        ash_display = ash_type.replace(' 1', '')
        for btn in self.ash_buttons:
            if btn['text'] == ash_display:
                btn.state(['pressed'])
                break
        
        self.status_bar.config(text=f"Selected: {ash_display}")
        
    def validate_inputs(self):
        """Validate all input values"""
        if not self.selected_ash_type.get():
            messagebox.showerror("Error", "Please select an ash type.")
            return False
        
        try:
            values = []
            for var in self.input_variables:
                if var in self.input_values:
                    val = float(self.input_values[var].get())
                    if val < 0:
                        messagebox.showerror("Error", f"{var} cannot be negative.")
                        return False
                    values.append(val)
            return True
        except ValueError:
            messagebox.showerror("Error", "All input values must be valid numbers.")
            return False
    
    def predict(self):
        """Make predictions using the trained models"""
        if not self.validate_inputs():
            return
        
        ash_type = self.selected_ash_type.get()
        
        # Check if models exist for this ash type
        if ash_type not in self.models or not self.models[ash_type]:
            messagebox.showerror("Error", f"No models available for {ash_type.replace(' 1', '')}")
            return
        
        # Prepare input data
        X_input = []
        for var in self.input_variables:
            if var in self.input_values:
                X_input.append(float(self.input_values[var].get()))
            else:
                X_input.append(0.0)
        X_input = np.array(X_input).reshape(1, -1)
        
        # Clear results
        self.results_text.delete(1.0, tk.END)
        
        # Header - more compact
        self.results_text.insert(tk.END, "="*55 + "\n")
        self.results_text.insert(tk.END, "PREDICTION RESULTS\n".center(55))
        self.results_text.insert(tk.END, "="*55 + "\n\n")
        
        self.results_text.insert(tk.END, f"Ash Type: {ash_type.replace(' 1', '')}\n")
        self.results_text.insert(tk.END, f"Pozzolan: {self.pozzolan_var.get()}\n")
        self.results_text.insert(tk.END, "-"*55 + "\n\n")
        
        # Input summary - more compact
        self.results_text.insert(tk.END, "INPUT PARAMETERS:\n")
        self.results_text.insert(tk.END, "-"*55 + "\n")
        
        for var in self.input_variables:
            value = self.input_values[var].get()
            display_name = var.replace('_', ' ').replace('kg m3', '(kg/m³)').title()
            self.results_text.insert(tk.END, f"  {display_name:<35} {value:>15}\n")
        
        self.results_text.insert(tk.END, "\n" + "="*55 + "\n\n")
        
        # Make predictions
        self.results_text.insert(tk.END, "PREDICTED OUTPUT:\n")
        self.results_text.insert(tk.END, "-"*55 + "\n\n")
        
        predictions = {}
        for target_var in self.target_variables:
            if target_var in self.models[ash_type]:
                model_info = self.models[ash_type][target_var]
                model = model_info['model']
                scaler = model_info['scaler']
                model_name = model_info['name']
                
                # Get features used by this model
                model_features = model_info['features']
                
                # Prepare input with correct features
                X_model = []
                for feat in model_features:
                    idx = self.input_variables.index(feat)
                    X_model.append(X_input[0, idx])
                
                # Convert to DataFrame with proper feature names to avoid warnings
                X_model_df = pd.DataFrame([X_model], columns=model_features)
                
                # Scale and predict
                X_scaled = scaler.transform(X_model_df)
                prediction = model.predict(X_scaled)[0]
                predictions[target_var] = prediction
                
                # Format output
                if 'cost' in target_var.lower():
                    self.results_text.insert(tk.END, f"  💰 Cost per m³:\n")
                    self.results_text.insert(tk.END, f"     ${prediction:,.2f} USD\n")
                elif 'strength' in target_var.lower():
                    self.results_text.insert(tk.END, f"  💪 Compressive Strength:\n")
                    self.results_text.insert(tk.END, f"     {prediction:.2f} MPa\n")
                elif 'co2' in target_var.lower():
                    self.results_text.insert(tk.END, f"  🌍 CO₂ Emissions:\n")
                    self.results_text.insert(tk.END, f"     {prediction:.4f} kgCO₂e/kg\n")
                else:
                    # Skip slump and other variables
                    continue
                
                self.results_text.insert(tk.END, f"     (Model: {model_name})\n\n")
        
        self.results_text.insert(tk.END, "="*55 + "\n")
        
        # Summary
        if predictions:
            self.results_text.insert(tk.END, "\nSUMMARY:\n")
            self.results_text.insert(tk.END, "-"*55 + "\n")
            self.results_text.insert(tk.END, f"  ✓ Predicted 3 parameters\n")
            self.results_text.insert(tk.END, f"  ✓ Best performing models used\n")
            self.results_text.insert(tk.END, "="*55 + "\n")
        
        self.status_bar.config(text=f"Prediction completed for {ash_type.replace(' 1', '')}")
        
    def clear_inputs(self):
        """Clear all input fields"""
        for var in self.input_values:
            self.input_values[var].set("0")
        
        self.selected_ash_type.set("")
        self.pozzolan_var.set("Fly Ash")
        
        for btn in self.ash_buttons:
            btn.state(['!pressed'])
        
        self.results_text.delete(1.0, tk.END)
        self.show_welcome_message()
        self.status_bar.config(text="Inputs cleared")
    
    def load_example(self):
        """Load example values"""
        example_values = {
            'replacement_pct': '20',
            'cement_kg_m3': '320',
            'ash_kg_m3': '80',
            'fine_aggregate_kg_m3': '700',
            'coarse_aggregate_kg_m3': '1100',
            'pozzolan added(Fly Ash) kgm3': '30',
            'superplasticizer_kg_m3': '5',
            'water kg_m3': '180',
            'curing_days': '28'
        }
        
        for var, value in example_values.items():
            if var in self.input_values:
                self.input_values[var].set(value)
        
        # Select first ash type as example
        if self.ash_types:
            self.select_ash_type(self.ash_types[0])
        
        self.status_bar.config(text="Example values loaded")
        messagebox.showinfo("Example Loaded", "Example concrete mixture parameters loaded.\nClick 'Predict' to see results.")
    
    def show_welcome_message(self):
        """Show welcome message in results area"""
        self.results_text.insert(tk.END, "="*55 + "\n")
        self.results_text.insert(tk.END, "CONCRETE PREDICTOR\n".center(55))
        self.results_text.insert(tk.END, "="*55 + "\n\n")
        self.results_text.insert(tk.END, "Instructions:\n")
        self.results_text.insert(tk.END, "-"*55 + "\n")
        self.results_text.insert(tk.END, "1. Select an ash type button\n")
        self.results_text.insert(tk.END, "2. Choose pozzolan type\n")
        self.results_text.insert(tk.END, "3. Enter mixture parameters\n")
        self.results_text.insert(tk.END, "4. Click 'Predict' for results\n")
        self.results_text.insert(tk.END, "5. Use 'Load Example' for sample\n\n")
        
        self.results_text.insert(tk.END, "Available Ash Types:\n")
        self.results_text.insert(tk.END, "-"*55 + "\n")
        for i, ash in enumerate(self.ash_types, 1):
            self.results_text.insert(tk.END, f"  {i}. {ash.replace(' 1', '')}\n")
        
        self.results_text.insert(tk.END, "\n" + "="*55 + "\n")

def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    
    # Set theme
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure custom styles
    style.configure('Accent.TButton', foreground='white', background='#0078d7', 
                   font=('Arial', 9, 'bold'))
    
    app = ConcretePredictorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()