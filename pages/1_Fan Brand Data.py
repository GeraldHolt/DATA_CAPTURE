import sqlite3
import streamlit as st

# Database setup
DB_PATH = "db.sqlite"

def initialize_db():
    """Create the brands table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_brands():
    """Fetch all brand names from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM brands")
    brands = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
    conn.close()
    return brands

def add_brand(brand_name):
    """Add a new brand to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO brands (name) VALUES (?)", (brand_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        st.warning("Brand already exists!")
    conn.close()

def edit_brand(brand_id, new_name):
    """Edit an existing brand in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE brands SET name = ? WHERE id = ?", (new_name, brand_id))
        conn.commit()
    except sqlite3.IntegrityError:
        st.warning("Brand name already exists!")
    conn.close()

def delete_brand(brand_id):
    """Delete a brand from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM brands WHERE id = ?", (brand_id,))
    conn.commit()
    conn.close()

# Initialize the database
initialize_db()

# Streamlit App
st.set_page_config(layout="wide")

# App Title
st.title("Fan Brand Management")

# Fetch brands from the database
brand_options = get_brands()

# Split layout into three columns
colA, colB, colC = st.columns(3)

with colA:
    # Add a new brand
    st.subheader("Add a New Brand")
    new_brand = st.text_input("Enter New Brand Name", key="new_brand")
    if st.button("Add Brand"):
        if new_brand.strip():
            add_brand(new_brand.strip())
            st.success(f"Brand '{new_brand}' added successfully!")
            st.rerun()  # Refresh to update the brand list
        else:
            st.error("Brand name cannot be empty.")

with colB:
    # Edit an existing brand
    st.subheader("Edit an Existing Brand")
    if brand_options:
        brand_names = sorted([brand["name"] for brand in brand_options])
        selected_brand = st.selectbox("Select a Brand to Edit", options=brand_names, key="edit_brand_select")
        brand_id = next(brand["id"] for brand in brand_options if brand["name"] == selected_brand)

        # Input field to update the brand name
        updated_name = st.text_input("Enter New Name for Selected Brand", value=selected_brand, key="edit_brand_name")
        if st.button("Update Brand"):
            if updated_name.strip():
                edit_brand(brand_id, updated_name.strip())
                st.success(f"Brand '{selected_brand}' updated to '{updated_name}' successfully!")
                st.rerun()  # Refresh to update the brand list
            else:
                st.error("Updated brand name cannot be empty.")
    else:
        st.write("No brands available to edit. Please add a brand.")

with colC:
    # Delete an existing brand
    st.subheader("Delete a Brand")
    if brand_options:
        brand_names = sorted([brand["name"] for brand in brand_options])
        selected_delete_brand = st.selectbox("Select a Brand to Delete", options=brand_names, key="delete_brand_select")
        delete_brand_id = next(brand["id"] for brand in brand_options if brand["name"] == selected_delete_brand)

        if st.button("Delete Brand"):
            delete_brand(delete_brand_id)
            st.success(f"Brand '{selected_delete_brand}' deleted successfully!")
            st.rerun()  # Refresh to update the brand list
    else:
        st.write("No brands available to delete. Please add a brand.")

# Display current brands
st.subheader("Current Brands in Database")
if brand_options:
    st.write([brand["name"] for brand in brand_options])
else:
    st.write("No brands added yet.")



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
