import json
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Fraud Investigation Agent",
    layout="wide"
)

st.title("Fraud Investigation Agent")

page = st.sidebar.selectbox(
    "Choose Page",
    [
        "Investigate Transaction",
        "View Cases",
        "Case Details",
        "Review Case",
        "Case Statistics"
    ]
)


def show_response(response):
    if response.status_code in [200, 201]:
        st.success("Request successful")
        st.json(response.json())
    else:
        st.error(f"Error: {response.status_code}")
        st.text(response.text)


if page == "Investigate Transaction":
    st.header("Submit Transaction")

    st.info("Paste full transaction JSON below.")

    sample_json = {
        "Time": 406,
        "V1": -2.312226542,
        "V2": 1.951992011,
        "V3": -1.609850732,
        "V4": 3.997905588,
        "V5": -0.522187865,
        "V6": -1.426545319,
        "V7": -2.537387306,
        "V8": 1.391657248,
        "V9": -2.770089277,
        "V10": -2.772272145,
        "V11": 3.202033207,
        "V12": -2.899907388,
        "V13": -0.595221881,
        "V14": -4.289253782,
        "V15": 0.38972412,
        "V16": -1.14074718,
        "V17": -2.830055675,
        "V18": -0.016822468,
        "V19": 0.416955705,
        "V20": 0.126910559,
        "V21": 0.517232371,
        "V22": -0.035049369,
        "V23": -0.465211076,
        "V24": 0.320198199,
        "V25": 0.044519167,
        "V26": 0.177839798,
        "V27": 0.261145003,
        "V28": -0.143275875,
        "Amount": 0
    }

    transaction_json = st.text_area(
        "Transaction JSON",
        value=json.dumps(sample_json, indent=2),
        height=500
    )

    if st.button("Investigate Transaction"):
        try:
            payload = json.loads(transaction_json)

            response = requests.post(
                f"{API_URL}/agent/investigate",
                json=payload
            )

            show_response(response)

        except json.JSONDecodeError:
            st.error("Invalid JSON format")


elif page == "View Cases":
    st.header("View Fraud Cases")

    status = st.selectbox(
        "Filter by Status",
        [
            "ALL",
            "PENDING",
            "APPROVED",
            "REJECTED",
            "NOT_REQUIRED"
        ]
    )

    if st.button("Load Cases"):
        if status == "ALL":
            response = requests.get(f"{API_URL}/cases")
        else:
            response = requests.get(f"{API_URL}/cases?status={status}")

        show_response(response)


elif page == "Case Details":
    st.header("View Case Details")

    case_id = st.number_input(
        "Case ID",
        min_value=1,
        step=1
    )

    if st.button("Get Case"):
        response = requests.get(
            f"{API_URL}/cases/{case_id}"
        )

        show_response(response)


elif page == "Review Case":
    st.header("Human Review")

    case_id = st.number_input(
        "Case ID",
        min_value=1,
        step=1
    )

    decision = st.selectbox(
        "Decision",
        [
            "APPROVED",
            "REJECTED"
        ]
    )

    reviewed_by = st.text_input(
        "Reviewed By",
        value="Kiran"
    )

    review_notes = st.text_area(
        "Review Notes",
        value="Confirmed suspicious transaction pattern."
    )

    if st.button("Submit Review"):
        payload = {
            "decision": decision,
            "reviewed_by": reviewed_by,
            "review_notes": review_notes
        }

        response = requests.post(
            f"{API_URL}/cases/{case_id}/review",
            json=payload
        )

        show_response(response)


elif page == "Case Statistics":
    st.header("Case Statistics")

    if st.button("Load Statistics"):
        response = requests.get(
            f"{API_URL}/cases/stats"
        )

        if response.status_code == 200:
            stats = response.json()

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Cases", stats["total_cases"])
            col2.metric("Pending Cases", stats["pending_cases"])
            col3.metric("Rejected Cases", stats["rejected_cases"])

            col4, col5, col6 = st.columns(3)

            col4.metric("Approved Cases", stats["approved_cases"])
            col5.metric("High Risk Cases", stats["high_risk_cases"])
            col6.metric("Low Risk Cases", stats["low_risk_cases"])

            st.json(stats)
        else:
            st.error(f"Error: {response.status_code}")
            st.text(response.text)