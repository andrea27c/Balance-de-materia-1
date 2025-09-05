import streamlit as st

def calculate_sugar_needed(initial_mass_kg, initial_brix, final_brix):
    """
    Calculates the amount of sugar needed to reach a target Brix level.
    Args:
        initial_mass_kg (float): The initial mass of the pulp in kg.
        initial_brix (float): The initial Brix value in degrees.
        final_brix (float): The target Brix value in degrees.
    Returns:
        float: The mass of sugar needed in kg.
    """
    # Convert Brix to a decimal concentration
    initial_concentration = initial_brix / 100.0
    final_concentration = final_brix / 100.0

    # Ensure valid inputs
    if initial_concentration >= final_concentration:
        return 0  # No sugar needed if initial Brix is already higher or equal

    # Mass balance formula:
    # final_concentration = (initial_solids + added_sugar) / (initial_mass + added_sugar)
    # Solve for added_sugar (X)
    # X = initial_mass * (final_concentration - initial_concentration) / (1 - final_concentration)
    sugar_needed = (initial_mass_kg * (final_concentration - initial_concentration)) / (1 - final_concentration)
    return sugar_needed

# --- Streamlit UI ---

# Page configuration
st.set_page_config(
    page_title="Calculadora de Balance de Masa",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("Calculadora de Balance de Masa")
st.markdown("---")
st.header("Problema")
st.markdown("""
Luego de procesar 50 kg de pulpa de fruta con 7 °Brix, necesitamos ajustar la concentración a 10 °Brix agregando azúcar.
Esta aplicación te ayudará a calcular la cantidad exacta que debes agregar.
""")

# Input section
st.sidebar.header("Parámetros de Entrada")
initial_mass = st.sidebar.number_input(
    "Masa de pulpa inicial (kg)",
    min_value=0.0,
    value=50.0,
    step=0.1
)
initial_brix = st.sidebar.number_input(
    "°Brix inicial",
    min_value=0.0,
    value=7.0,
    step=0.1
)
final_brix = st.sidebar.number_input(
    "°Brix objetivo",
    min_value=0.0,
    value=10.0,
    step=0.1
)

# Calculation button
if st.sidebar.button("Calcular Cantidad de Azúcar"):
    if initial_brix > final_brix:
        st.error("Los °Brix objetivo deben ser mayores que los °Brix iniciales para agregar azúcar.")
    else:
        # Perform calculation
        sugar_to_add = calculate_sugar_needed(initial_mass, initial_brix, final_brix)
        
        # Display results
        st.subheader("Resultado")
        st.success(f"Para ajustar la pulpa, debe agregar **{sugar_to_add:.4f} kg** de azúcar.")
        st.markdown("---")
        st.subheader("Análisis de la Solución")
        st.info(f"""
        **Masa inicial de pulpa:** {initial_mass} kg
        **Sólidos iniciales:** {initial_mass} kg * ({initial_brix/100:.2f}) = {initial_mass * (initial_brix/100):.2f} kg de sólidos.

        **Masa de azúcar a agregar:** {sugar_to_add:.4f} kg
        **Nueva masa total de pulpa:** {initial_mass + sugar_to_add:.4f} kg
        **Nueva masa de sólidos:** {initial_mass * (initial_brix/100) + sugar_to_add:.4f} kg

        **Verificación de los °Brix finales:**
        ({initial_mass * (initial_brix/100) + sugar_to_add:.4f} kg de sólidos) / ({initial_mass + sugar_to_add:.4f} kg de pulpa) = **{((initial_mass * (initial_brix/100) + sugar_to_add) / (initial_mass + sugar_to_add)) * 100:.2f} °Brix**
        """)
