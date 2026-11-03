import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="BI Canvas Dashboard",
    page_icon="📊",
    layout="wide"
)

# Enhanced Modern CSS for Vibrant Cards and Theme
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E1B4B;
        color: #E2E8F0;
    }
    [data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
    }
    
    /* Modern Power BI Style Metric Cards */
    div.stMetric {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #4338CA; /* Left accent bar */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div.stMetric:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(67, 56, 202, 0.1), 0 4px 6px -2px rgba(67, 56, 202, 0.05);
    }
    /* Make metric labels and values high contrast */
    div.stMetric label {
        color: #64748B !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    div.stMetric [data-testid="stMetricValue"] {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 1.8rem !important;
    }
    </style>
""", unsafe_allow_html=True)
# Custom CSS matching Enterprise Indigo Theme
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
    }
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E1B4B;
        color: #E2E8F0;
    }
    [data-testid="stSidebar"] label {
        color: #E2E8F0 !important;
    }
    /* Metric Cards */
    div.stMetric {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar Controls & Data Upload
st.sidebar.title("BI Canvas")
st.sidebar.markdown("---")
st.sidebar.subheader("Data Source")

uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

# Sample Dataset Option if no file is uploaded
if uploaded_file is not None:
    @st.cache_data
    def load_data(file):
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    df = load_data(uploaded_file)
else:
    st.sidebar.info("Using default sample data. Upload your file above.")
    data = {
        "Order ID": [121891, 134912, 175384, 175925, 182391, 194821],
        "Customer Name": ["Jones Smith", "Marix Walter", "Jame Martier", "Jonny Colm", "Sarah Connor", "John Doe"],
        "Product Category": ["Technology", "Furniture", "Furniture", "Office Supplies", "Technology", "Furniture"],
        "Region": ["West", "East", "Central", "South", "Europe", "APAC"],
        "Revenue": [636.00, 450.00, 300.00, 99.00, 1200.00, 540.00],
        "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    }
    df = pd.DataFrame(data)

# 3. Dynamic Chart Builder Options in Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("Chart Customization")
columns = list(df.columns)

chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"])
x_axis = st.sidebar.selectbox("X-Axis / Category Column", columns, index=columns.index("Month") if "Month" in columns else 0)
y_axis = st.sidebar.selectbox("Y-Axis / Metric Column", columns, index=columns.index("Revenue") if "Revenue" in columns else 1)
color_column = st.sidebar.selectbox("Group/Color By (Optional)", [None] + columns)

# 4. Main Dashboard Layout
st.title("Dashboard Overview")
st.markdown("Customize your visual charts and inspect tabular data dynamically.")

# KPI Summary Cards
total_metric = df[y_axis].sum() if pd.api.types.is_numeric_dtype(df[y_axis]) else 0
total_rows = len(df)
avg_metric = df[y_axis].mean() if pd.api.types.is_numeric_dtype(df[y_axis]) else 0

col1, col2, col3 = st.columns(3)
col1.metric(f"Total {y_axis}", f"₹ {total_metric:,.2f}" if isinstance(total_metric, (int, float)) else total_metric, "+15.2%")
col2.metric("Total Records", f"{total_rows:,}", "+8.1%")
col3.metric(f"Avg {y_axis} / Row", f"₹ {avg_metric:,.2f}" if isinstance(avg_metric, (int, float)) else "N/A", "-1.9%")

st.markdown("---")

# 5. Dynamic Chart Rendering Section
st.subheader(f"Visualizing: {chart_type} ({y_axis} by {x_axis})")

try:
    if chart_type == "Bar Chart":
        fig = px.bar(df, x=x_axis, y=y_axis, color=color_column, color_discrete_sequence=["#6366F1", "#10B981", "#F59E0B", "#EC4899"])
    elif chart_type == "Line Chart":
        fig = px.line(df, x=x_axis, y=y_axis, color=color_column, markers=True, color_discrete_sequence=["#6366F1"])
    elif chart_type == "Scatter Plot":
        fig = px.scatter(df, x=x_axis, y=y_axis, color=color_column, color_discrete_sequence=["#6366F1"])
    elif chart_type == "Pie Chart":
        fig = px.pie(df, names=x_axis, values=y_axis, color_discrete_sequence=px.colors.qualitative.Plotly)

    fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", margin=dict(t=20, b=20, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True)
except Exception as e:
    st.error(f"Could not generate chart with selected columns: {e}")

# 6. Interactive Data Table View with Column Filter
st.markdown("---")
st.subheader("Data Table View & Filtering")

selected_columns = st.multiselect("Select columns to display in table", columns, default=columns)
if selected_columns:
    st.dataframe(df[selected_columns], use_container_width=True)
else:
    st.dataframe(df, use_container_width=True)