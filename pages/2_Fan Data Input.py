import sqlite3
import streamlit as st

# Database setup
DB_PATH = "db.sqlite"


def initialize_db():
    """Create the fan_data and brands tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table for brands
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    # Table for fan data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fan_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_number TEXT UNIQUE NOT NULL,
            model_number_group TEXT NOT NULL,
            brand TEXT NOT NULL,
            speed TEXT NOT NULL,
            blade_angle TEXT NOT NULL,
            drive_train TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def get_brands():
    """Fetch all brand names from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM brands")
    brands = [{"name": row[0]} for row in cursor.fetchall()]
    conn.close()
    return brands


def get_saved_models():
    """Fetch all saved models from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, model_number FROM fan_data")
    models = [{"id": row[0], "model_number": row[1]} for row in cursor.fetchall()]
    conn.close()
    return models


def get_model_details(model_id):
    """Fetch details of a specific model by its ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT model_number, model_number_group, brand, speed, blade_angle, drive_train
        FROM fan_data WHERE id = ?
    """, (model_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "model_number": row[0],
            "model_number_group": row[1],
            "brand": row[2],
            "speed": row[3],
            "blade_angle": row[4],
            "drive_train": row[5],
        }
    return None


def save_fan_data(model_number, model_number_group, brand, speed, blade_angle, drive_train):
    """Save a new fan model into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM fan_data WHERE model_number = ?", (model_number,))
    exists = cursor.fetchone()[0]

    if exists:
        st.warning(f"Model number '{model_number}' already exists. Please use a unique model number.")
    else:
        cursor.execute("""
            INSERT INTO fan_data (model_number, model_number_group, brand, speed, blade_angle, drive_train)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (model_number, model_number_group, brand, speed, blade_angle, drive_train))
        conn.commit()
        st.success(f"Model '{model_number}' saved successfully!")
    conn.close()


def update_fan_data(model_id, model_number, model_number_group, brand, speed, blade_angle, drive_train):
    """Update an existing fan model in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE fan_data
        SET model_number = ?, model_number_group = ?, brand = ?, speed = ?, blade_angle = ?, drive_train = ?
        WHERE id = ?
    """, (model_number, model_number_group, brand, speed, blade_angle, drive_train, model_id))
    conn.commit()
    st.success(f"Model '{model_number}' updated successfully!")
    conn.close()


# Initialize database
initialize_db()

# Initialize session state
if "model_number_group" not in st.session_state:
    st.session_state["model_number_group"] = ""
if "brand" not in st.session_state:
    st.session_state["brand"] = ""
if "speed" not in st.session_state:
    st.session_state["speed"] = "720"  # Default speed
if "blade_angle" not in st.session_state:
    st.session_state["blade_angle"] = "5°"
if "drive_train" not in st.session_state:
    st.session_state["drive_train"] = "Direct Drive"

# Configure the page layout
st.set_page_config(layout="wide")

# App Title
st.title("Fan Curve Data Management")

# Retrieve saved models and brands
saved_models = get_saved_models()
brand_options = [brand["name"] for brand in get_brands()]

# Dropdown to select a saved model
st.subheader("Select or Add a Model")
model_options = ["Add New Model"] + [model["model_number"] for model in saved_models]
selected_model = st.selectbox("Choose a Model", options=model_options, key="selected_model")

# Prefill fields if a model is selected
if selected_model != "Add New Model":
    selected_id = next(model["id"] for model in saved_models if model["model_number"] == selected_model)
    model_details = get_model_details(selected_id)

    st.session_state["model_number_group"] = model_details["model_number_group"]
    st.session_state["brand"] = model_details["brand"]
    st.session_state["speed"] = model_details["speed"]
    st.session_state["blade_angle"] = model_details["blade_angle"]
    st.session_state["drive_train"] = model_details["drive_train"]
else:
    st.session_state["model_number_group"] = ""
    st.session_state["brand"] = ""
    st.session_state["speed"] = "720"
    st.session_state["blade_angle"] = "5°"
    st.session_state["drive_train"] = "Direct Drive"

# Split layout into two columns
colA, colB = st.columns(2)

with colA:
    # Input fields
    model_number_group = st.text_input("Enter Fan Model Group", value=st.session_state["model_number_group"])
    brand = st.selectbox(
        "Select Fan Brand",
        options=["Select a Brand"] + brand_options,
        index=brand_options.index(st.session_state["brand"]) + 1 if st.session_state["brand"] in brand_options else 0
    )

    # Drive Train Selection
    drive_train = st.radio(
        "Select Drive Train",
        options=["Direct Drive", "Belt Transmission"],
        index=["Direct Drive", "Belt Transmission"].index(st.session_state["drive_train"]),
        key="drive_train"
    )

    # Fan Speed
    if drive_train == "Direct Drive":
        speed = st.selectbox(
            "Fan Impeller Speed",
            ["720", "960", "1440", "2880"],
            index=["720", "960", "1440", "2880"].index(st.session_state["speed"]),
            key="speed"
        )
    else:
        speed = st.number_input(
            "Enter Impeller Speed",
            min_value=0,
            max_value=5000,
            step=1,
            value=int(st.session_state["speed"]),
            key="speed"
        )

    # Blade Angle
    blade_angle = st.selectbox(
        "Blade Angle",
        ["5°", "10°", "15°", "20°", "25°", "30°", "35°", "40°", "45°"],
        index=["5°", "10°", "15°", "20°", "25°", "30°", "35°", "40°", "45°"].index(st.session_state["blade_angle"])
    )

# Auto-generate the model number
if model_number_group and speed and blade_angle:
    model_number = f'{model_number_group}-{speed}rpm-{blade_angle}'
else:
    model_number = "Incomplete Data"

# Save or Update Button
if st.button("Save Model"):
    if selected_model == "Add New Model":
        if model_number_group and brand != "Select a Brand" and speed and blade_angle:
            save_fan_data(model_number, model_number_group, brand, speed, blade_angle, drive_train)
            st.rerun()  # Refresh to update the dropdown list
        else:
            st.error("All fields are required to save a new model!")
    else:
        if model_number_group and brand != "Select a Brand" and speed and blade_angle:
            update_fan_data(selected_id, model_number, model_number_group, brand, speed, blade_angle, drive_train)
            st.rerun()  # Refresh to update the dropdown list
        else:
            st.error("All fields are required to update the model!")

# Display the generated model number
with colB:
    st.subheader("Model Number:")
    st.subheader(f'***{model_number}***')


    # # Plot the pump curve and best-fit polynomial
    # if not updated_df.empty:
    #     flow_rates = updated_df["Flow Rate (m³/s)"]
    #     pressures = updated_df["Pressure (Pa)"]
    #
    #     # Fit a polynomial of degree 2 (quadratic) or adjust as needed
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
    #     ax.set_xlabel("Flow Rate (m³/h)")
    #     ax.set_ylabel("Pressure (bar)")
    #     ax.legend()
    #     ax.grid(True)
    #
    #     st.pyplot(fig)
    #
    #     # Display polynomial equation
    #     equation = " + ".join([f"{coeff:.2f}x^{i}" for i, coeff in enumerate(coefficients[::-1])])
    #     st.markdown(f"**Best-Fit Polynomial Equation:**\n {equation}")
    #
    # # Option to download the updated data
    # st.download_button(
    #     label="Download Updated Data",
    #     data=updated_df.to_csv(index=False),
    #     file_name="updated_pump_curve_data.csv",
    #     mime="text/csv"
    # )
