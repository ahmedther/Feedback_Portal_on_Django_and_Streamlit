import streamlit as st

from support_streamlit import StreamLitAPP

# Main App
app = StreamLitAPP()


if app.check_password():
    try:
        # Side Bar
        app.side_bar()

        # Define Tabs Dashboard, "Download Excel", "Reply to Comment / Grievance", "Other"
        app.define_tabs()

        # User Comment Reply Section
        app.search_user_comments()
        app.reply_to_user_comments()

        # Get Data From Database
        app.fetch_data_from_database()

        # Define Filter Column
        app.define_filters()

        # Define Excel Data Tab
        app.excel_data_tab()

        # Define Dashboard Tab
        app.dashboard_data_tab()

        # Bar Charts
        # First Barchart Department-wise
        app.bar_chart("DEPARTMENT")
        # Second BarChart Question Wise
        app.bar_chart("QUESTION")

        with app.other:
            st.header("Save Space for the Future")

    except Exception as e:
        with app.dashboard:
            st.error(
                "Please Select Date and apply proper filters to see the full website"
            )
