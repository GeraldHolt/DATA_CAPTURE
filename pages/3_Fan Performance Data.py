import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
import json

# Database setup
DB_PATH = "db.sqlite"


def initialize_db():
    """Ensure the database schema is correct."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure fan_data table exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fan_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_number TEXT UNIQUE NOT NULL,
            brand TEXT NOT NULL,
            speed TEXT NOT NULL,
            blade_angle TEXT NOT NULL,
            drive_train TEXT NOT NULL
        )
    """)

    # Ensure performance_data table exists with the required columns
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fan_id INTEGER NOT NULL,
            flow_pressure_data TEXT NOT NULL,
            curve_image BLOB,
            polynomial_function TEXT,
            FOREIGN KEY (fan_id) REFERENCES fan_data (id) ON DELETE CASCADE
        )
    """)

    # Check and add missing columns if necessary
    try:
        cursor.execute("SELECT curve_image FROM performance_data LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE performance_data ADD COLUMN curve_image BLOB")

    try:
        cursor.execute("SELECT polynomial_function FROM performance_data LIMIT 1")
    except sqlite3.OperationalError:
        cursor.execute("ALTER TABLE performance_data ADD COLUMN polynomial_function TEXT")

    conn.commit()
    conn.close()


def get_saved_models():
    """Fetch all saved models from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, model_number FROM fan_data")
    models = [{"id": row[0], "model_number": row[1]} for row in cursor.fetchall()]
    conn.close()
    return models


def get_performance_data(fan_id):
    """Fetch performance data for a specific fan model."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT flow_pressure_data FROM performance_data WHERE fan_id = ?", (fan_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return []


def save_performance_data(fan_id, performance_data, curve_image=None, polynomial_function=None):
    """Save performance data, curve image, and polynomial function into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    serialized_data = json.dumps(performance_data)

    # Check if performance data already exists for the fan
    cursor.execute("SELECT COUNT(*) FROM performance_data WHERE fan_id = ?", (fan_id,))
    exists = cursor.fetchone()[0]

    if exists:
        # Update existing data
        cursor.execute("""
            UPDATE performance_data
            SET flow_pressure_data = ?, curve_image = ?, polynomial_function = ?
            WHERE fan_id = ?
        """, (serialized_data, curve_image, polynomial_function, fan_id))
    else:
        # Insert new data
        cursor.execute("""
            INSERT INTO performance_data (fan_id, flow_pressure_data, curve_image, polynomial_function)
            VALUES (?, ?, ?, ?)
        """, (fan_id, serialized_data, curve_image, polynomial_function))

    conn.commit()
    conn.close()


# Initialize database
initialize_db()

# Configure the page layout
st.set_page_config(layout="wide")

# App Title
st.title("Fan Performance Data Management")

# Fetch saved models
models = get_saved_models()

if models:
    # Dropdown to select a fan model
    selected_model = st.selectbox(
        "Select a Fan Model",
        options=[model["model_number"] for model in models],
        key="model_selector"
    )
    model_id = next((model["id"] for model in models if model["model_number"] == selected_model), None)

    # Load existing data when a model is selected
    if "performance_df" not in st.session_state or st.session_state.get("current_model") != selected_model:
        existing_data = get_performance_data(model_id)
        st.session_state["performance_df"] = pd.DataFrame(existing_data or [], columns=["flow_rate", "pressure"])
        st.session_state["current_model"] = selected_model

    # Input fields for adding new data
    st.subheader(f"Add Performance Data for Model: {selected_model}")
    col1, col2, col3 = st.columns([3, 3, 1])
    with col1:
        flow_rate = st.number_input("Flow Rate (m³/s)", step=0.1, key="new_flow")
    with col2:
        pressure = st.number_input("Pressure (Pa)", step=1.0, key="new_pressure")
    with col3:
        if st.button("Add", key="add_button"):
            # Validate that at least one row exists
            new_row = {"flow_rate": flow_rate, "pressure": pressure}
            st.session_state["performance_df"] = pd.concat(
                [st.session_state["performance_df"], pd.DataFrame([new_row])],
                ignore_index=True,
            )
            st.rerun()

    # Editable performance data table
    st.subheader("Performance Data Table")
    edited_df = st.data_editor(
        st.session_state["performance_df"],
        num_rows="dynamic",
        use_container_width=True,
        key="performance_data_editor"
    )

    # Update session state with edits
    st.session_state["performance_df"] = edited_df

    # Plot the pump curve and best-fit polynomial
    if not edited_df.empty:
        edited_df["flow_rate"] = pd.to_numeric(edited_df["flow_rate"], errors="coerce")
        edited_df["pressure"] = pd.to_numeric(edited_df["pressure"], errors="coerce")
        edited_df = edited_df.dropna(subset=["flow_rate", "pressure"])

        flow_rates = edited_df["flow_rate"].values
        pressures = edited_df["pressure"].values

        if len(flow_rates) > 1:
            degree = st.slider("Polynomial Degree", 1, 7, 2, key="degree_slider")
            coefficients = np.polyfit(flow_rates, pressures, degree)
            polynomial = np.poly1d(coefficients)

            # Generate best-fit curve
            flow_range = np.linspace(flow_rates.min(), flow_rates.max(), 500)
            fitted_pressures = polynomial(flow_range)

            fig, ax = plt.subplots(figsize=(8, 6))
            ax.scatter(flow_rates, pressures, color="blue", label="Data Points")
            ax.plot(flow_range, fitted_pressures, color="red", label=f"Best-Fit Polynomial (Degree {degree})")
            ax.set_title("Pump Curve")
            ax.set_xlabel("Flow Rate (m³/s)")
            ax.set_ylabel("Pressure (Pa)")
            ax.legend()
            ax.grid(True)

            st.pyplot(fig)

            equation = " + ".join([f"{coeff:.2f}x^{i}" for i, coeff in enumerate(coefficients[::-1])])
            st.markdown(f"**Best-Fit Polynomial Equation:** {equation}")

            # Save button
            if st.button("Save Performance Data and Curve", key="save_button"):
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                curve_image = buf.getvalue()
                save_performance_data(model_id, edited_df.to_dict(orient="records"), curve_image, equation)
                st.success("Performance data and curve saved successfully!")
        else:
            st.warning("At least two data points are required to plot the pump curve.")
else:
    st.warning("No fan models available. Please add a fan model first.")

#
# # Generate polynomial equation
# if not edited_df.empty:
#     flow_rates = edited_df["flow_rate"]
#     pressures = edited_df["pressure"]
#
#     degree = st.slider("Polynomial Degree", 1, 7, 2)  # Slider to choose polynomial degree
#     coefficients = np.polyfit(flow_rates, pressures, degree)
#     polynomial = np.poly1d(coefficients)
#
#     # Generate best-fit curve
#     flow_range = np.linspace(flow_rates.min(), flow_rates.max(), 500)
#     fitted_pressures = polynomial(flow_range)
#
#     # Plotting
#     fig, ax = plt.subplots()
#     ax.scatter(flow_rates, pressures, color="blue", label="Data Points")  # Data points
#     ax.plot(flow_range, fitted_pressures, color="red", label=f"Best-Fit Polynomial (Degree {degree})")  # Best-fit curve
#     ax.set_title("Pump Curve")
#     ax.set_xlabel("Flow Rate (m³/s)")
#     ax.set_ylabel("Pressure (Pa)")
#     ax.legend()
#     ax.grid(True)
#
#     # Save the figure as a PNG file
#     buf = io.BytesIO()
#     fig.savefig(buf, format="png")
#     buf.seek(0)
#
#     st.pyplot(fig)
#
#     # Generate polynomial equation
#     polynomial_equation = " + ".join([f"{coeff:.2f}x^{i}" for i, coeff in enumerate(coefficients[::-1])])
#     st.markdown(f"**Best-Fit Polynomial Equation:**\n {polynomial_equation}")
#
#     # Save button to store data in the database
#     if st.button("Save Performance Data"):
#         if not st.session_state["performance_df"].empty:
#             performance_data = st.session_state["performance_df"].to_dict(orient="records")
#             save_performance_data(model_id, performance_data, buf.read(), polynomial_equation)  # Save performance data, curve image, and polynomial equation
#             st.success(f"Performance data, curve, and polynomial saved for model {selected_model}!")
#         else:
#             st.warning("No data to save! Please add entries to the table.")
