import pandas as pd
import streamlit as st

from classifier import qualify_lead


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------
st.set_page_config(
    page_title="Lead Qualification System",
    page_icon="📊",
    layout="wide",
)


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("📊 Lead Qualification System")

st.sidebar.write(
    """
    This application classifies customer enquiries into:

    🔥 Hot Leads  
    🟠 Warm Leads  
    ❄️ Cold Leads
    """
)

st.sidebar.info(
    "Classification is based on rule-based keyword matching "
    "and lead scoring."
)


# -------------------------------------------------
# MAIN TITLE
# -------------------------------------------------
st.title("📊 Lead Qualification System")

st.write(
    "Automatically classify customer enquiries as "
    "**Hot, Warm, or Cold** using rule-based text classification."
)

st.divider()


# -------------------------------------------------
# TABS
# -------------------------------------------------
single_tab, bulk_tab, validation_tab = st.tabs(
    [
        "👤 Single Lead Qualification",
        "📁 Bulk Lead Qualification",
        "✅ Validation & Accuracy",
    ]
)


# =================================================
# TAB 1 - SINGLE LEAD
# =================================================
with single_tab:

    st.subheader("Qualify a Single Lead")

    st.write(
        "Enter a customer enquiry below and click "
        "**Qualify Lead**."
    )

    enquiry = st.text_area(
        "Customer Enquiry",
        placeholder=(
            "Example: I am ready to buy today. "
            "Please send payment details."
        ),
        height=150,
    )

    if st.button(
        "Qualify Lead",
        type="primary",
        key="single_qualify",
    ):

        if not enquiry.strip():

            st.warning(
                "Please enter a customer enquiry."
            )

        else:

            result = qualify_lead(enquiry)

            qualification = result["qualification"]

            st.divider()

            # -------------------------------------
            # FINAL RESULT
            # -------------------------------------
            if qualification == "Hot":

                st.success("🔥 HOT LEAD")

            elif qualification == "Warm":

                st.warning("🟠 WARM LEAD")

            else:

                st.info("❄️ COLD LEAD")


            # -------------------------------------
            # SCORE CARDS
            # -------------------------------------
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🔥 Hot Score",
                    result["hot_score"],
                )

            with col2:
                st.metric(
                    "🟠 Warm Score",
                    result["warm_score"],
                )

            with col3:
                st.metric(
                    "❄️ Cold Score",
                    result["cold_score"],
                )


            # -------------------------------------
            # DETAILS
            # -------------------------------------
            st.subheader("Cleaned Enquiry")

            st.code(
                result["cleaned_text"]
            )

            st.subheader(
                "Final Qualification"
            )

            st.write(
                f"### {qualification}"
            )


# =================================================
# TAB 2 - BULK LEAD PROCESSING
# =================================================
with bulk_tab:

    st.subheader(
        "Upload CSV or Excel File"
    )

    st.write(
        "Your file must contain an "
        "**enquiry_text** column."
    )


    # ---------------------------------------------
    # SAMPLE FILE FORMAT
    # ---------------------------------------------
    sample_data = pd.DataFrame(
        {
            "lead_id": [
                "L001",
                "L002",
                "L003",
            ],
            "enquiry_text": [
                (
                    "I am ready to buy today "
                    "and need payment details."
                ),
                (
                    "Please send pricing and "
                    "product details."
                ),
                (
                    "I am just browsing and "
                    "maybe later."
                ),
            ],
        }
    )

    sample_csv = sample_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Sample CSV",
        data=sample_csv,
        file_name="sample_leads.csv",
        mime="text/csv",
    )


    # ---------------------------------------------
    # FILE UPLOADER
    # ---------------------------------------------
    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx"],
    )


    if uploaded_file is not None:

        try:

            # -------------------------------------
            # READ FILE
            # -------------------------------------
            if uploaded_file.name.lower().endswith(
                ".csv"
            ):

                df = pd.read_csv(
                    uploaded_file
                )

            else:

                df = pd.read_excel(
                    uploaded_file
                )


            # -------------------------------------
            # CLEAN COLUMN NAMES
            # -------------------------------------
            df.columns = [
                str(column).strip().lower()
                for column in df.columns
            ]


            st.success(
                "File uploaded successfully."
            )

            st.subheader(
                "Uploaded Data Preview"
            )

            st.dataframe(
                df.head(10),
                use_container_width=True,
            )


            # -------------------------------------
            # CHECK REQUIRED COLUMN
            # -------------------------------------
            if "enquiry_text" not in df.columns:

                st.error(
                    "The uploaded file must contain "
                    "a column named 'enquiry_text'."
                )

                st.write(
                    "Columns found:",
                    list(df.columns),
                )

            else:

                if st.button(
                    "🚀 Process Leads",
                    type="primary",
                    key="bulk_process",
                ):

                    with st.spinner(
                        "Classifying leads..."
                    ):

                        results = (
                            df["enquiry_text"]
                            .apply(qualify_lead)
                            .apply(pd.Series)
                        )


                        # Remove old generated columns
                        # if they already exist
                        generated_columns = [
                            "cleaned_text",
                            "hot_score",
                            "warm_score",
                            "cold_score",
                            "qualification",
                        ]

                        original_df = df.drop(
                            columns=[
                                column
                                for column
                                in generated_columns
                                if column in df.columns
                            ],
                            errors="ignore",
                        )


                        qualified_df = pd.concat(
                            [
                                original_df.reset_index(
                                    drop=True
                                ),
                                results.reset_index(
                                    drop=True
                                ),
                            ],
                            axis=1,
                        )


                    st.success(
                        "Lead qualification completed successfully!"
                    )


                    # ---------------------------------
                    # DASHBOARD
                    # ---------------------------------
                    st.divider()

                    st.subheader(
                        "📈 Lead Qualification Dashboard"
                    )

                    total_leads = len(
                        qualified_df
                    )

                    hot_count = (
                        qualified_df[
                            "qualification"
                        ]
                        .eq("Hot")
                        .sum()
                    )

                    warm_count = (
                        qualified_df[
                            "qualification"
                        ]
                        .eq("Warm")
                        .sum()
                    )

                    cold_count = (
                        qualified_df[
                            "qualification"
                        ]
                        .eq("Cold")
                        .sum()
                    )


                    col1, col2, col3, col4 = (
                        st.columns(4)
                    )

                    with col1:

                        st.metric(
                            "Total Leads",
                            total_leads,
                        )

                    with col2:

                        st.metric(
                            "🔥 Hot Leads",
                            hot_count,
                        )

                    with col3:

                        st.metric(
                            "🟠 Warm Leads",
                            warm_count,
                        )

                    with col4:

                        st.metric(
                            "❄️ Cold Leads",
                            cold_count,
                        )


                    # ---------------------------------
                    # CHART
                    # ---------------------------------
                    st.subheader(
                        "Lead Distribution"
                    )

                    chart_data = pd.DataFrame(
                        {
                            "Category": [
                                "Hot",
                                "Warm",
                                "Cold",
                            ],
                            "Count": [
                                hot_count,
                                warm_count,
                                cold_count,
                            ],
                        }
                    ).set_index(
                        "Category"
                    )

                    st.bar_chart(
                        chart_data
                    )


                    # ---------------------------------
                    # RESULTS TABLE
                    # ---------------------------------
                    st.subheader(
                        "Qualified Lead Results"
                    )

                    st.dataframe(
                        qualified_df,
                        use_container_width=True,
                    )


                    # ---------------------------------
                    # DOWNLOAD RESULTS
                    # ---------------------------------
                    output_csv = (
                        qualified_df
                        .to_csv(
                            index=False
                        )
                        .encode("utf-8")
                    )

                    st.download_button(
                        label=(
                            "⬇️ Download Qualified Leads"
                        ),
                        data=output_csv,
                        file_name=(
                            "qualified_leads.csv"
                        ),
                        mime="text/csv",
                    )


        except Exception as error:

            st.error(
                f"Unable to process file: {error}"
            )

# =================================================
# TAB 3 - VALIDATION & ACCURACY
# =================================================
with validation_tab:

    st.subheader("✅ Manual Validation Results")

    st.write(
        "The 30 classified leads were reviewed manually "
        "to compare the system prediction with human judgement."
    )

    # ---------------------------------------------
    # VALIDATION SUMMARY
    # ---------------------------------------------
    total_validated = 30
    correct_predictions = 27
    incorrect_predictions = 3
    accuracy = (correct_predictions / total_validated) * 100

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Validated",
            total_validated,
        )

    with col2:
        st.metric(
            "✅ Correct",
            correct_predictions,
        )

    with col3:
        st.metric(
            "❌ Incorrect",
            incorrect_predictions,
        )

    with col4:
        st.metric(
            "🎯 Accuracy",
            f"{accuracy:.0f}%",
        )

    st.divider()

    # ---------------------------------------------
    # VALIDATION CHART
    # ---------------------------------------------
    st.subheader("Validation Performance")

    validation_chart = pd.DataFrame(
        {
            "Result": [
                "Correct",
                "Incorrect",
            ],
            "Count": [
                correct_predictions,
                incorrect_predictions,
            ],
        }
    ).set_index("Result")

    st.bar_chart(validation_chart)

    st.divider()

    # ---------------------------------------------
    # INCORRECT CLASSIFICATIONS
    # ---------------------------------------------
    st.subheader("Incorrect Classification Analysis")

    error_data = pd.DataFrame(
        [
            {
                "Lead ID": "L019",
                "Enquiry": (
                    "I need details before I decide whether "
                    "to purchase in future."
                ),
                "System Label": "Hot",
                "Manual Label": "Warm",
                "Error Reason": (
                    "The word 'purchase' triggered Hot, "
                    "but the customer is still evaluating "
                    "and refers to a future purchase."
                ),
            },
            {
                "Lead ID": "L020",
                "Enquiry": (
                    "Urgent: I need a demo and quote today "
                    "before deciding."
                ),
                "System Label": "Hot",
                "Manual Label": "Warm",
                "Error Reason": (
                    "Urgent and today triggered Hot, but "
                    "the customer still wants a demo and "
                    "quote before making a decision."
                ),
            },
            {
                "Lead ID": "L029",
                "Enquiry": (
                    "I am not ready to buy today; "
                    "I am just researching."
                ),
                "System Label": "Hot",
                "Manual Label": "Cold",
                "Error Reason": (
                    "The classifier detected 'ready to buy' "
                    "and 'today' but did not understand "
                    "the negation 'not ready to buy'."
                ),
            },
        ]
    )

    st.dataframe(
        error_data,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    # ---------------------------------------------
    # OBSERVATIONS
    # ---------------------------------------------
    st.subheader("Key Observations")

    st.write(
        """
        - The system correctly classified **27 out of 30 leads**.
        - Final validation accuracy is **90%**.
        - Most clear Hot, Warm, and Cold enquiries were classified correctly.
        - Errors mainly occurred when enquiries contained conflicting intent.
        - The rule-based classifier does not fully understand negation.
        - Words such as **urgent**, **today**, and **purchase** can sometimes
          create false Hot classifications.
        """
    )

    st.info(
        "Future improvement: add negation handling, weighted keywords, "
        "and more context-aware classification rules."
    )
# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.divider()

st.caption(
    "Lead Qualification System | "
    "Python • Pandas • Streamlit"
)