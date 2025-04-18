import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Create Function"

# Menu bar with buttons
st.markdown("""
    <style>
        .menu {
            display: flex;
            gap: 20px;
            padding: 10px 0;
            border-bottom: 1px solid #ccc;
            margin-bottom: 20px;
        }
        .menu-button {
            background-color: #f0f2f6;
            border: none;
            color: #333;
            padding: 10px 20px;
            cursor: pointer;
            font-weight: bold;
        }
        .menu-button:hover {
            background-color: #e0e2e6;
        }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    if st.button("Create Function"):
        st.session_state.page = "Create Function"
with col2:
    if st.button("List Functions"):
        st.session_state.page = "List Functions"
with col3:
    if st.button("Delete Function"):
        st.session_state.page = "Delete Function"
with col4:
    if st.button("Update Function"):
        st.session_state.page = "Update Function"
with col5:
    if st.button("Execute Function"):
        st.session_state.page = "Execute Function"
with col6:
    if st.button("Monitoring Dashboard"):
        st.session_state.page = "Monitoring Dashboard"

# Main content
st.title("Lambda Serverless Function Manager")

# Create Function Page
if st.session_state.page == "Create Function":
    st.subheader("Deploy New Function")

    name = st.text_input("Function Name")
    language = st.selectbox("Language", ["python", "javascript"])
    route = st.text_input("Filename (e.g., hello.py)")
    timeout = st.number_input("Timeout (seconds)", min_value=1, max_value=30, value=5)

    if st.button("Deploy"):
        payload = {
            "name": name,
            "language": language,
            "route": route,
            "timeout": timeout
        }
        response = requests.post(f"{API_URL}/functions", json=payload)
        if response.status_code == 200:
            st.success("Function deployed successfully!")
        else:
            st.error(f"Failed: {response.text}")

# List Functions Page
elif st.session_state.page == "List Functions":
    st.subheader("All Functions")
    response = requests.get(f"{API_URL}/functions")
    if response.ok:
        for func in response.json():
            st.json(func)
    else:
        st.error("Could not fetch functions.")

# Delete Function Page
elif st.session_state.page == "Delete Function":
    st.subheader("Delete Function")
    response = requests.get(f"{API_URL}/functions")
    if response.ok:
        functions = response.json()
        choices = {f"{f['name']} (ID: {f['id']})": f['id'] for f in functions}
        selected = st.selectbox("Select Function to Delete", list(choices.keys()))
        if st.button("Delete"):
            fid = choices[selected]
            del_res = requests.delete(f"{API_URL}/functions/{fid}")
            if del_res.status_code == 200:
                st.success("Deleted successfully!")
            else:
                st.error("Delete failed.")
    else:
        st.error("Could not load functions.")

# Update Function Page
elif st.session_state.page == "Update Function":
    st.subheader("✏️ Update Existing Function")

    response = requests.get(f"{API_URL}/functions")
    if response.ok:
        functions = response.json()
        choices = {f"{f['name']} (ID: {f['id']})": f for f in functions}
        selected = st.selectbox("Select Function to Update", list(choices.keys()))

        func_data = choices[selected]
        updated_name = st.text_input("New Name", value=func_data["name"])
        updated_lang = st.selectbox("Language", ["python", "javascript"], index=["python", "javascript"].index(func_data["language"]))
        updated_route = st.text_input("Filename", value=func_data["route"])
        updated_timeout = st.number_input("Timeout", min_value=1, max_value=30, value=func_data["timeout"])

        if st.button("Update"):
            payload = {
                "name": updated_name,
                "language": updated_lang,
                "route": updated_route,
                "timeout": updated_timeout
            }
            res = requests.put(f"{API_URL}/functions/{func_data['id']}", json=payload)
            if res.status_code == 200:
                st.success("Function updated successfully!")
            else:
                st.error(f"Update failed: {res.text}")
    else:
        st.error("Could not fetch functions.")
# Execute Function Page
elif st.session_state.page == "Execute Function":
    st.subheader("⚡ Execute Function")

    function_id = st.number_input("Function ID", min_value=1, step=1)
    raw_args = st.text_input("Arguments (comma-separated)", value="")
    use_gvisor = st.checkbox("Use gVisor Runtime", value=False)

    if st.button("Execute"):
        args = [arg.strip() for arg in raw_args.split(",") if arg.strip()]
        payload = {
            "id": int(function_id),
            "args": args,
            "use_gvisor": use_gvisor
        }
        response = requests.post(f"{API_URL}/functions/execute", json=payload)
        if response.status_code == 200:
            data = response.json()
            st.success("✅ Function Executed!")
            st.code(data.get("output", ""), language="text")
            if data.get("error"):
                st.error(data["error"])
        else:
            st.error("Function execution failed.")
            
# Dashboard Page
elif st.session_state.page == "Monitoring Dashboard":
    st.subheader(" Monitoring Dashboard")

    try:
        response = requests.get(f"{API_URL}/metrics/summary")
        if response.status_code != 200:
            st.warning("Could not load metrics.")
        else:
            summary = response.json()
            if not summary:
                st.info("No metrics available yet.")
            else:
                df = pd.DataFrame(summary)
                df["function"] = df["function_id"].astype(str)

                # System-wide overview
                st.write("## System-wide Metrics")
                total_calls = df["total_calls"].sum()
                total_errors = df["error_count"].sum()
                avg_exec_time = round((df["avg_time"] * df["total_calls"]).sum() / total_calls, 3) if total_calls else 0

                col1, col2, col3 = st.columns(3)
                col1.metric("Total Calls", total_calls)
                col2.metric("Total Errors", total_errors)
                col3.metric("Avg Exec Time", f"{avg_exec_time} sec")

                # Charts
                st.write("###  Total Calls per Function")
                st.bar_chart(df.set_index("function")["total_calls"])

                st.write("###  Error Count per Function")
                st.bar_chart(df.set_index("function")["error_count"])

                st.write("###  Average Execution Time (sec)")
                st.line_chart(df.set_index("function")["avg_time"])

                # Expanders for individual functions
                st.write("## Per-Function Metrics")
                for item in summary:
                    with st.expander(f"Function ID: {item['function_id']}"):
                        st.write(f"Total Calls: {item['total_calls']}")
                        st.write(f"Average Time: {item['avg_time']} sec")
                        st.write(f"Error Count: {item['error_count']}")

    except Exception as e:
        st.error(f"Failed to load dashboard: {e}")
