import pandas as pd
import streamlit as st
import plotly_express as px
import os


from datetime import datetime
from postgress_config import PostgressDB


# Copied Django Wsgi File


from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "feedback_website.settings")

application = get_wsgi_application()

from django.contrib.auth import authenticate

# Django Wsgi ends here

# Rest of the App Starts here


class StreamLitAPP:
    def __init__(self):
        # Page Details
        st.set_page_config(
            page_title="Feedback Reports",
            page_icon=":chart_with_upwards_trend:",
            layout="wide",
        )

    def auth_screen(self):
        self.side_bar_header = st.sidebar.header("User Login")

    def authform(self, onclick_func):
        self.username = st.sidebar.text_input(
            "User ID",
            value="",
            max_chars=None,
            key="username",
            type="default",
            help="Please enter your Username. If you dont have one, then call on 33333 extention",
            autocomplete=None,
            on_change=None,
            args=None,
            kwargs=None,
            placeholder="username",
            disabled=False,
        )

        self.password = st.sidebar.text_input(
            "Password",
            type="password",
            on_change=onclick_func,
            key="password",
            value="",
            max_chars=None,
            help="Please enter your Password. If you forgot your password, then call on 33333 extention",
            autocomplete=None,
            args=None,
            kwargs=None,
            placeholder="password",
            disabled=False,
        )

        st.sidebar.button(
            "Login",
            key="login-button",
            help="Click to Login",
            on_click=onclick_func,
            args=None,
            kwargs=None,
            disabled=False,
        )

    def check_password(self):
        """Returns `True` if the user had a correct password."""

        st.cache()

        def password_entered():
            """Checks whether a password entered by the user is correct."""
            global user
            user = authenticate(
                username=st.session_state["username"],
                password=st.session_state["password"],
            )

            if user is not None:
                st.session_state["password_correct"] = True
                # del st.session_state["password"]  # don't store username + password
                # del st.session_state["username"]
            else:
                st.session_state["password_correct"] = False

        if "password_correct" not in st.session_state:
            # First run, show inputs for username + password.
            # st.text_input("Username", on_change=password_entered, key="username")
            # st.text_input(
            #     "Password", type="password", on_change=password_entered, key="password"
            # )

            self.authform(password_entered)

            return False
        elif not st.session_state["password_correct"]:
            # Password not correct, show input + error.
            # st.text_input("Username", on_change=password_entered, key="username")
            # st.text_input(
            #     "Password", type="password", on_change=password_entered, key="password"
            # )
            self.authform(password_entered)
            st.error("😕 User not Registered or Password incorrect")

            return False
        else:
            # Password correct.
            return True

    def define_tabs(self):
        # Define Tabs
        (
            self.dashboard,
            self.excel_data,
            self.view_user_com,
            self.other,
        ) = st.tabs(
            [
                "Dashboard",
                "Download Excel",
                "View And Reply to Patient's Comment",
                "Other",
            ]
        )

    def side_bar(self):
        # Side Bar
        self.uname = str(user)
        self.side_bar_header = st.sidebar.header(f"Welcome {self.uname.capitalize()}")
        groups = user.groups.values()
        self.auth_group = []
        for group in groups:
            self.auth_group.append(group["name"])

        st.sidebar.write(
            f"You are only authorized to view {(', '.join(self.auth_group))}, departments."
        )
        st.sidebar.header("Please Filter From Here")
        todays_day = datetime.now()
        date_range_input = st.sidebar.date_input(
            "From Date",
            value=(todays_day, todays_day),
            min_value=None,
            max_value=None,
            key=1,
            help="Please select a date range",
            on_change=None,
            args=None,
            kwargs=None,
            disabled=False,
        )
        try:
            self.from_date = date_range_input[0]
            self.to_date = date_range_input[1]
        except IndexError as error:
            if error:
                st.error("Please select a valid date range from the filter")

    # @st.experimental_memo
    def get_data_from_database(_self, _from_date, _to_date):
        try:
            db = PostgressDB()
            data, column_name = db.get_report(_from_date, _to_date)
            db.connection_close()
            pd_dframe = pd.DataFrame(data=data, columns=list(column_name))

        except Exception as errordb:
            if errordb:
                st.error("Error connecting to Database")

        return pd_dframe

    def fetch_data_from_database(self):
        # Data from Postgress DataBase
        with st.spinner(f"Wait for it...{datetime.now()}"):
            try:
                self.pd_dframe = self.get_data_from_database(
                    self.from_date, self.to_date
                )
                if self.pd_dframe.empty:
                    with self.dashboard:
                        st.warning("No Data Found")
                else:
                    with self.dashboard:
                        st.success("Connected to the Database!")
            except Exception as e:
                with self.dashboard:
                    st.error(e)

    def define_filters(self):
        # List of Filters in sidebar
        with st.form("sidebar-filter", clear_on_submit=False):
            with st.sidebar:
                filter_department = st.sidebar.multiselect(
                    "Filter Department",
                    # options=self.pd_dframe["DEPARTMENT"].unique(),
                    # default=self.pd_dframe["DEPARTMENT"].unique(),
                    options=self.auth_group,
                    default=self.auth_group,
                    key="pd_dep_filter",
                    help=None,
                    on_change=None,
                    args=None,
                    kwargs=None,
                    disabled=False,
                )

                questions_based_on_departments = self.pd_dframe.loc[
                    self.pd_dframe["DEPARTMENT"].isin(filter_department)
                ]

                filter_question = st.sidebar.multiselect(
                    "Filter Question",
                    options=questions_based_on_departments["QUESTION"].unique(),
                    # default=self.pd_dframe["QUESTION"].unique(),
                    default=None,
                    key="pd_ques_filter",
                    help=None,
                    on_change=None,
                    args=None,
                    kwargs=None,
                    disabled=False,
                )

                filter_referral = st.sidebar.multiselect(
                    "Filter Question",
                    options=self.pd_dframe["REFERRAL"].unique(),
                    default=self.pd_dframe["REFERRAL"].unique(),
                    key="pd_referral_filter",
                    help=None,
                    on_change=None,
                    args=None,
                    kwargs=None,
                    disabled=False,
                )
                filter_submit = st.form_submit_button("Search")
                if filter_submit:
                    # Dataframe Query
                    self.data_after_filter = self.pd_dframe.query(
                        """
                
                        DEPARTMENT == @filter_department & QUESTION == @filter_question & REFERRAL == @filter_referral
                    """
                    )

    def create_download_button(self, data_frame, key, message_on_button):
        todays_day = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        excel_data = data_frame.to_csv().encode("utf-8")
        st.download_button(
            message_on_button,
            excel_data,
            file_name=f"{todays_day}.csv",
            mime="text/csv",
            key=key,
            help="Click to Download 📗",
            on_click=None,
            args=None,
            kwargs=None,
            disabled=False,
        )

    def excel_data_tab(self):
        with self.excel_data:
            st.header("All data within date range without filters")
            st.dataframe(self.pd_dframe)

            # except (Exception) as errordb:
            #     if errordb:
            #         st.error("Error connecting to Database")

            # Download Button
            self.create_download_button(
                self.pd_dframe,
                "download-csv",
                "Download Excel file of the selected Date Range",
            )
            st.markdown("---")

            st.header("Data after applying filters")
            st.dataframe(self.data_after_filter)

            # Create Download Button
            self.create_download_button(
                self.data_after_filter,
                "download-csv-1",
                "Download Excel file with selected filters",
            )
            st.markdown("---")

    def dashboard_data_tab(self):
        with self.dashboard:
            # ---- Main Dashboard----#
            st.title(":chart_with_upwards_trend: Dashboard")
            st.markdown("##")

            # # Top KPI
            total_feedbacks = len(self.data_after_filter["PATIENT NAME"].unique())

            average_rating = pd.to_numeric(self.data_after_filter["RATING"])
            average_rating = round(average_rating.mean(), 1)
            average_rating = round((average_rating * 5 / 4), 1)
            star_rating = ":star:" * int(round(average_rating, 0))

            # Columns
            left_column, right_column = st.columns(2)

            with left_column:
                st.header("Total Feedback Received")
                st.subheader(f" Total Number of feedback Submitted {total_feedbacks}")

            with right_column:
                st.header("Average Ratings")
                st.subheader(f"{average_rating}     {star_rating} \n  (out of 5)")

            st.markdown("---")

    def bar_chart(
        self,
        group_by,
    ):
        with self.dashboard:
            # Bar Chart starts here

            # Convert dataframe to intigers
            self.data_after_filter = self.data_after_filter.apply(
                pd.to_numeric, errors="ignore"
            )

            # Filter data and group by department
            rating_by_group = round(
                self.data_after_filter.groupby(by=[group_by])
                .mean()[["RATING"]]
                .sort_values(by=group_by),
                1,
            )

            # increase max from 4 to 5
            rating_by_group = round((rating_by_group * 5 / 4), 1)

            # Bar Chart Details
            bar_chart_details = px.bar(
                rating_by_group,
                x="RATING",
                y=rating_by_group.index,
                orientation="h",
                title=f"<b> Average Rating By {group_by} (Max Rating 5) </b>",
                color=["#0083b8"] * len(rating_by_group),
                template="plotly_white",
            )
            # Update Bar CHart to remove background
            bar_chart_details.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=(dict(showgrid=False)),
            )
            # Display Bar chart
            st.plotly_chart(bar_chart_details)

            # can also add header {visibility : hidden;}
            hide_st_style = """
        
                <style>
                        #MainMenu {visibility : hidden;} 
                        footer {visibility : hidden;}
        
                </style>
                """
            st.markdown(hide_st_style, unsafe_allow_html=True)

    def text_box(
        self,
        label,
        key,
        placeholder=None,
        help="",
        value="",
        on_change=None,
        max_chars=None,
        disabled=False,
    ):
        text_box_data = st.text_input(
            label,
            value=value,
            max_chars=max_chars,
            key=key,
            type="default",
            help=help,
            autocomplete=None,
            on_change=on_change,
            args=None,
            kwargs=None,
            placeholder=placeholder,
            disabled=disabled,
        )

        return text_box_data

    def select__box(self, label, options, key, help, on_change=None, index=0):
        option_selected = st.selectbox(
            label=label,
            options=options,
            index=index,
            key=key,
            help=help,
            on_change=on_change,
            args=None,
            kwargs=None,
            disabled=False,
        )

        return option_selected

    def button_display(self, label, key, help, on_click):
        st.button(
            label=label,
            key=key,
            help=help,
            on_click=on_click,
            args=None,
            kwargs=None,
            disabled=False,
        )

    def text_area_display(
        self,
        label,
        key,
        help,
        placeholder=None,
        value="",
        height=None,
        on_change=None,
        disabled=False,
    ):
        text_area_value = st.text_area(
            label=label,
            value=value,
            height=height,
            max_chars=None,
            key=key,
            help=help,
            on_change=on_change,
            args=None,
            kwargs=None,
            placeholder=placeholder,
            disabled=disabled,
        )

        return text_area_value

    def search_patient_comment(self):
        try:
            db = PostgressDB()
            self.com_data = db.get_patient_comment(
                self.uhid_to_search, self.department_com, self.enconter_id_to_search
            )
            db.connection_close()
            with self.view_user_com:
                with self.left_com_column:
                    self.com_pat_del = st.write(
                        f"""The selected Patient is {self.com_data[0][0]}, for encounter id {self.com_data[0][2]}.
\nThis feedback was submitted on {self.com_data[0][3]}."""
                    )

                    self.com_pat_reply = self.text_area_display(
                        key="pat-com",
                        help=f"This is what patient has said about your department on .",
                        label=f"Patient commented this in his/her feedback on {self.department_com} Department, submitted on {self.com_data[0][3]}.",
                        disabled=True,
                        value=f"{self.com_data[0][1]}",
                    )
                    if self.com_data:
                        try:
                            if self.com_data[0][4] != None:
                                st.session_state["rep_pr_value"] = self.com_data[0][4]
                            if self.com_data[0][6] != None:
                                st.session_state[
                                    "replier-designation1"
                                ] = self.com_data[0][6]
                            if self.com_data[0][5] != None:
                                st.session_state["replier-pr-num1"] = self.com_data[0][
                                    5
                                ]
                            if self.com_data[0][2] != None:
                                st.session_state[
                                    "encounter_id_from_com"
                                ] = self.com_data[0][2]

                        except:
                            pass

        except Exception as e:
            with self.view_user_com:
                st.warning(e)

            # finally:
            #     return self.com_data

    def search_user_comments(self):
        with self.view_user_com:
            self.left_com_column, self.right_com_column = st.columns(2)
            with self.left_com_column:
                with st.form("view-com", clear_on_submit=False):
                    st.subheader("View Patient's comment on your department.")
                    self.uhid_to_search = self.text_box(
                        help="Understand how to use this call 33333 extension",
                        label="Please Enter Patient's UHID Number",
                        key="search_by_uhid",
                        max_chars=12,
                        value="KH1000",
                    )
                    self.uhid_to_search = self.uhid_to_search.upper()

                    self.enconter_id_to_search = self.text_box(
                        help="Optional, leave it black if you dont know the encounter ID",
                        label="Please Enter Patient's Encounter ID (Optional)",
                        key="search_by_encounter",
                    )

                    self.department_com = self.select__box(
                        help="Only Authorised Departments can be selected. \nIf you feel your department is not listed here, then please contact you administrator or call on 33333 extension.",
                        key="department-select",
                        label="Select The Department You Represent",
                        options=self.auth_group,
                    )

                    search_com = st.form_submit_button("Search")
                    if search_com:
                        self.search_patient_comment()

    def reply_to_user_comments(self):
        with self.view_user_com:
            with self.right_com_column:
                with st.form("reply-com", clear_on_submit=True):
                    st.subheader("Reply to Patient's comment on your department.")
                    self.replier_name = self.text_box(
                        help="Your Name (Replier Name) goes here",
                        label="Replier Name",
                        key="replier-name",
                        value=f"{self.uname.capitalize()}",
                        disabled=True,
                    )
                    if "replier-pr-num1" not in st.session_state:
                        st.session_state["replier-pr-num1"] = ""
                    self.replier_pr_name = self.text_box(
                        help="PR Number (Replier Number) goes here",
                        label="Replier PR Number",
                        key="replier-pr-num",
                        placeholder="5100",
                        value=st.session_state["replier-pr-num1"],
                    )
                    if "replier-designation1" not in st.session_state:
                        st.session_state["replier-designation1"] = ""
                    self.replier_designation = self.text_box(
                        help="You Designation (Replier Designation) goes here",
                        label="Replier (Your) Designation",
                        key="replier-designation",
                        placeholder="Write you designation here",
                        value=st.session_state["replier-designation1"],
                    )
                    if "rep_pr_value" not in st.session_state:
                        st.session_state["rep_pr_value"] = ""
                    self.deps_reply = self.text_area_display(
                        key="reply_com",
                        help=f"Your reply to the patient's concerns.",
                        label=f"Write a Reply to Patient's Comment.",
                        disabled=False,
                        placeholder="Please Write your reasons inside this box",
                        value=st.session_state["rep_pr_value"],
                    )
                    submit_com = st.form_submit_button("Submit")
                    if submit_com:
                        try:
                            db = PostgressDB()
                            db.submit_repliers_comments(
                                department=self.department_com,
                                departments_reply=self.deps_reply,
                                encounter_id=st.session_state["encounter_id_from_com"],
                                replier_designation=self.replier_designation,
                                replier_name=self.uname.capitalize(),
                                replier_pr_num=self.replier_pr_name,
                                uhid=self.uhid_to_search,
                            )
                            db.connection_close()
                            st.success(
                                "Thank you! Your comment has been successfully submitted. ✔️"
                            )
                        except Exception as e:
                            # st.error(e)
                            st.error("❌ Something Went Wrong ❌")
