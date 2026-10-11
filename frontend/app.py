import streamlit as st
import requests
import base64
import html

st.set_page_config(page_title="Banking Portal", layout="wide")

API_URL = "http://127.0.0.1:8000"
IMAGE_PATH = r"C:\Users\admin\banking-multi-Aiagent\frontend\assets\Screenshot 2026-10-11 160637.png"
DASHBOARD_CSS_PATH = r"C:\Users\admin\banking-multi-Aiagent\frontend\dashboard.css"


def get_background_image():
    with open(IMAGE_PATH, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


if "token" not in st.session_state:
    st.session_state["token"] = None
if "account_number" not in st.session_state:
    st.session_state["account_number"] = ""
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "dashboard_section" not in st.session_state:
    st.session_state["dashboard_section"] = "Transfer Money"


def sign_out():
    st.session_state["token"] = None
    st.session_state["account_number"] = ""
    st.session_state["chat_history"] = []
    st.session_state["dashboard_section"] = "Transfer Money"


def set_dashboard_section(section):
    st.session_state["dashboard_section"] = section


background_image = get_background_image()

if st.session_state["token"] is None:
    page_background = f"""
        background-image:
            linear-gradient(rgba(5, 10, 28, 0.25), rgba(5, 10, 28, 0.40)),
            url("data:image/png;base64,{background_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    """
else:
    page_background = """
        background:
            radial-gradient(ellipse at top left, rgba(76, 29, 149, 0.30), transparent 45%),
            radial-gradient(ellipse at bottom right, rgba(6, 182, 212, 0.18), transparent 45%),
            linear-gradient(135deg, #050A1C, #0B1230, #080D20);
        background-attachment: fixed;
    """

st.markdown(f"""

<style>



/* Background: login image or dashboard gradient */

.stApp {{

    {page_background}

    color: #E5EEFF;

}}



.block-container {{

    padding-top: 1.8rem;

    padding-bottom: 3rem;

    max-width: 1400px;

}}



/* Main title */

.stApp h1 {{

    color: #FFFFFF;

    text-align: center;

    font-size: 48px;

    font-weight: 800;

    letter-spacing: 1.5px;

    text-shadow: 0 0 22px rgba(34, 211, 238, 0.45);

}}



.stApp h2, .stApp h3 {{

    color: #FFFFFF;

    font-weight: 700;

}}



/* Authentication form - transparent */

div[data-testid="stForm"] {{

    background: transparent !important;

    border: none !important;

    border-radius: 0 !important;

    padding: 24px 0 !important;

    box-shadow: none !important;

}}



/* Plain black typing boxes - no border */

[data-testid="stForm"] input,

.stTextInput input,

.stNumberInput input {{

    background: #000000 !important;

    color: #FFFFFF !important;

    font-size: 22px !important;

    min-height: 54px;

    border: none !important;

    outline: none !important;

    box-shadow: none !important;

    border-radius: 6px !important;

}}



/* Input labels */

[data-testid="stForm"] label {{

    color: #FFFFFF !important;

    font-size: 22px !important;

    font-weight: 700 !important;

}}



/* Placeholder */

[data-testid="stForm"] input::placeholder {{

    color: #CBD5E1 !important;

    opacity: 1;

}}



/* Sign in and Create account buttons */

[data-testid="stForm"] button {{

    font-size: 23px !important;

    font-weight: 800 !important;

    min-height: 56px;

    border-radius: 10px !important;

}}



/* Other buttons */

.stButton button,

.stFormSubmitButton button {{

    background: linear-gradient(100deg, #0891B2, #6D28D9);

    color: #FFFFFF;

    border: 1px solid rgba(103, 232, 249, 0.5);

    border-radius: 11px;

    font-size: 20px;

    font-weight: 700;

    min-height: 48px;

}}



.stButton button:hover,

.stFormSubmitButton button:hover {{

    border-color: #67E8F9;

    box-shadow: 0 0 18px rgba(34, 211, 238, 0.28);

    color: #FFFFFF;

}}



/* Dashboard metric cards */

div[data-testid="stMetric"] {{

    background: rgba(15, 23, 50, 0.82);

    border: 1px solid rgba(103, 232, 249, 0.24);

    border-radius: 16px;

    padding: 20px;

    box-shadow: 0 0 20px rgba(8, 145, 178, 0.08);

}}



div[data-testid="stMetricLabel"] {{

    color: #A5B4FC;

}}



div[data-testid="stMetricValue"] {{

    color: #67E8F9;

    font-weight: 800;

}}



/* Sign in and Register tabs */

button[data-baseweb="tab"] {{

    color: #FFFFFF !important;

    font-size: 23px !important;

    font-weight: 800 !important;

    padding: 12px 20px !important;

}}



button[data-baseweb="tab"][aria-selected="true"] {{

    color: #67E8F9 !important;

}}



/* Dividers and captions */

hr {{

    border-color: rgba(103, 232, 249, 0.3);

}}



.stCaption, [data-testid="stCaptionContainer"] {{

    color: #FFFFFF;

    font-size: 18px;

}}



/* Chat bubbles */

div[data-testid="stChatMessage"] {{

    background: rgba(15, 23, 50, 0.82);

    border: 1px solid rgba(129, 140, 248, 0.18);

    border-radius: 14px;

    padding: 12px;

}}

/* FORCE larger login fonts */

div[data-testid="stForm"] label p,

div[data-testid="stForm"] label,

div[data-testid="stTextInput"] label p {{

    font-size: 25px !important;

    font-weight: 600 !important;

}}



/* Sign in / Register tabs */

.stTabs button[data-baseweb="tab"] div p {{

    font-size: 25px !important;

    font-weight: 600 !important;

}}



/* Phone number and Password typing fields */

div[data-testid="stTextInput"] input {{

    font-size: 25px !important;

    height: 64px !important;

}}



/* Login / Register submit buttons */

div[data-testid="stFormSubmitButton"] button p,

div[data-testid="stFormSubmitButton"] button{{

    font-size: 25px !important;

    font-weight: 600 !important;

    min-height: 45px !important;

}}

/* Transaction text */

.stMarkdown, .stJson {{

    color: #E2E8F0;

}}



/* Sidebar */

section[data-testid="stSidebar"] {{

    background: #080D20;

    border-right: 1px solid rgba(103, 232, 249, 0.20);

}}

/* Phone number and Password labels */

[data-testid="stForm"] label {{

    font-size: 30px !important;

    font-weight: 700 !important;

}}



/* Sign in and Register tabs */

button[data-baseweb="tab"] {{

    font-size: 30px !important;

    font-weight: 800 !important;

}}



/* Input boxes */

[data-testid="stForm"] input,

.stTextInput input {{

    font-size: 25px !important;

    min-height: 60px !important;

}}



/* Sign in and Register submit buttons */

[data-testid="stForm"] button {{

    font-size: 30x !important;

    font-weight: 800 !important;

    min-height: 64px !important;

}}

/* Mild black input background */

div[data-testid="stTextInput"] input,

[data-testid="stForm"] input {{

    background-color: #303038 !important;

    color: #FFFFFF !important;

    font-size: 28px !important;

    border: none !important;

    box-shadow: none !important;

    border-radius: 8px !important;

}}

</style>

""", unsafe_allow_html=True)

st.title("ComfyBank AI")
st.caption("Smart Banking. Simplified with AI.")

# -------------------- LOGIN / REGISTER (UNCHANGED FLOW) --------------------
if st.session_state["token"] is None:
    login_tab, register_tab = st.tabs(["Sign in", "Register"])

    with login_tab:
        st.markdown(
            "<h2 style='text-align:center; color:white; font-size:36px;'>Welcome Back</h2>",
            unsafe_allow_html=True,
        )
        with st.form("login_form"):
            login_phone = st.text_input("Phone number")
            login_password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Sign in", use_container_width=True)

        if login_submitted:
            if not login_phone.strip() or not login_password:
                st.warning("Enter your phone number and password.")
            else:
                try:
                    response = requests.post(
                        f"{API_URL}/login",
                        data={"username": login_phone.strip(), "password": login_password},
                        timeout=10,
                    )
                    if response.status_code == 200:
                        login_data = response.json()
                        st.session_state["token"] = login_data["access_token"]
                        st.session_state["account_number"] = login_data.get("account_number", "")
                        st.session_state["chat_history"] = []
                        st.session_state["dashboard_section"] = "Transfer Money"
                        st.rerun()
                    elif response.status_code == 401:
                        st.error("Invalid phone number or password.")
                    else:
                        st.error(f"Sign-in failed: {response.text}")
                except requests.RequestException:
                    st.error("Unable to connect to the banking server. Check whether the backend is running.")

    with register_tab:
        st.subheader("Create your account")
        with st.form("register_form"):
            customer_name = st.text_input("Full name")
            new_account_number = st.text_input("Account number")
            register_phone = st.text_input("Phone number")
            ifsc_code = st.text_input("IFSC code")
            new_password = st.text_input("Create password", type="password")
            confirm_password = st.text_input("Confirm password", type="password")
            register_submitted = st.form_submit_button("Create account", use_container_width=True)

        if register_submitted:
            if not all([customer_name.strip(), new_account_number.strip(), register_phone.strip(), ifsc_code.strip(), new_password, confirm_password]):
                st.warning("Complete all fields.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            elif len(new_password) < 8:
                st.error("Password must contain at least 8 characters.")
            else:
                try:
                    response = requests.post(
                        f"{API_URL}/register",
                        json={
                            "customer_name": customer_name.strip(),
                            "account_number": new_account_number.strip(),
                            "phone": register_phone.strip(),
                            "password": new_password,
                            "ifsc_code": ifsc_code.strip(),
                        },
                        timeout=10,
                    )
                    if response.status_code in (200, 201):
                        st.success("Account created successfully. You can now sign in.")
                    elif response.status_code == 409:
                        st.error("This account number or phone is already registered.")
                    else:
                        st.error(f"Registration failed: {response.text}")
                except requests.RequestException:
                    st.error("Unable to connect to the banking server. Check whether the backend is running.")

# -------------------- DASHBOARD (AFTER LOGIN ONLY) --------------------
else:
    token = st.session_state["token"]
    account_number = st.session_state["account_number"]
    headers = {"Authorization": f"Bearer {token}"}

    try:
        with open(DASHBOARD_CSS_PATH, "r", encoding="utf-8") as css_file:
            st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
    except OSError:
        pass

    heading_col, logout_col = st.columns([4, 1])
    with heading_col:
        st.markdown(
            "<h1 style='text-align:left; font-size:34px; margin-bottom:0;'>ComfyBank <span style='color:#67E8F9;'>AI</span></h1>",
            unsafe_allow_html=True,
        )
        st.caption("AI-Powered Digital Banking · Your financial overview")
    with logout_col:
        st.write("")
        st.button("Sign out", on_click=sign_out, use_container_width=True)

    # Load balance independently so an endpoint 404 does not hide the three dashboard buttons.
    customer_name = "Customer"
    balance = None
    balance_error = None
    try:
        balance_response = requests.get(
            f"{API_URL}/agent/balance/{account_number}", headers=headers, timeout=10
        )
        if balance_response.status_code == 200:
            account_data = balance_response.json()
            customer_name = account_data.get("customer_name", account_data.get("name", "Customer"))
            balance = float(account_data.get("balance", 0))
        elif balance_response.status_code == 401:
            sign_out()
            st.warning("Your session has expired. Please sign in again.")
            st.stop()
        else:
            balance_error = f"Unable to load account details: {balance_response.text}"
    except requests.RequestException:
        balance_error = "Unable to connect to the banking server. Check whether the backend is running."

    st.markdown(
        f"<div style='padding:12px 0 20px 0;'><div style='color:#A5B4FC;font-size:14px;letter-spacing:2px;'>WELCOME BACK</div><div style='color:#FFFFFF;font-size:30px;font-weight:750;margin-top:5px;'>Hello, {html.escape(str(customer_name))}</div><div style='color:#94A3B8;font-size:15px;margin-top:5px;'>Here's your banking overview.</div></div>",
        unsafe_allow_html=True,
    )

    balance_col, account_col = st.columns(2, gap="large")
    with balance_col:
        st.metric("💰 Available Balance", f"₹{balance:,.2f}" if balance is not None else "Unavailable")
    with account_col:
        st.metric("🏦 Account Number", account_number or "Unavailable")
    if balance_error:
        st.warning(balance_error)

    st.divider()
    st.subheader("Choose an action")
    action1, action2, action3 = st.columns(3, gap="medium")
    with action1:
        st.button("💸 Transfer Money", key="nav_transfer", use_container_width=True,
                  type="primary" if st.session_state["dashboard_section"] == "Transfer Money" else "secondary",
                  on_click=set_dashboard_section, args=("Transfer Money",))
    with action2:
        st.button("📄 Transaction History", key="nav_history", use_container_width=True,
                  type="primary" if st.session_state["dashboard_section"] == "Transaction History" else "secondary",
                  on_click=set_dashboard_section, args=("Transaction History",))
    with action3:
        st.button("🤖 AI Assistant", key="nav_ai", use_container_width=True,
                  type="primary" if st.session_state["dashboard_section"] == "AI Assistant" else "secondary",
                  on_click=set_dashboard_section, args=("AI Assistant",))

    st.divider()
    selected_section = st.session_state["dashboard_section"]

    # 1) Transfer Money section
    if selected_section == "Transfer Money":
        st.subheader("Transfer Money")
        st.caption("Send money to another account")
        with st.form("transfer_form"):
            receiver_account = st.text_input("Receiver account number")
            transfer_amount = st.number_input("Transfer amount (₹)", min_value=1.0, step=100.0)
            transfer_submitted = st.form_submit_button("Transfer Money", use_container_width=True)

        if transfer_submitted:
            if not receiver_account.strip():
                st.warning("Enter the receiver account number.")
            elif receiver_account.strip() == account_number:
                st.error("You cannot transfer to your own account.")
            else:
                try:
                    transfer_response = requests.post(
                        f"{API_URL}/transfer",
                        headers=headers,
                        json={"receiver_account": receiver_account.strip(), "amount": transfer_amount},
                        timeout=10,
                    )
                    if transfer_response.status_code == 200:
                        st.success("Transfer successful!")
                        st.json(transfer_response.json())
                        st.rerun()
                    elif transfer_response.status_code == 401:
                        sign_out()
                        st.warning("Your session has expired. Please sign in again.")
                        st.stop()
                    else:
                        st.error(f"Transfer failed: {transfer_response.text}")
                except requests.RequestException:
                    st.error("Unable to connect to the banking server.")

    # 2) Transaction History section
    elif selected_section == "Transaction History":
        st.subheader("Recent Transactions")
        try:
            transaction_response = requests.get(
                f"{API_URL}/transactions/{account_number}", headers=headers, timeout=10
            )
            if transaction_response.status_code == 200:
                transaction_data = transaction_response.json()
                if isinstance(transaction_data, dict):
                    transactions = transaction_data.get("transactions", [])
                elif isinstance(transaction_data, list):
                    transactions = transaction_data
                else:
                    transactions = []

                if not transactions:
                    st.info("No transactions available yet.")
                else:
                    for transaction in transactions:
                        if not isinstance(transaction, dict):
                            continue
                        with st.container(border=True):
                            transaction_col, amount_col = st.columns([3, 1])
                            with transaction_col:
                                st.caption("Date: " + str(transaction.get("date", "Date unavailable")))
                                st.write(transaction.get("description", "Transaction"))
                                st.caption(transaction.get("transaction_type", "Transaction"))
                            with amount_col:
                                amount = float(transaction.get("amount", 0))
                                st.write(f"₹{amount:,.2f}")
            elif transaction_response.status_code == 401:
                sign_out()
                st.warning("Your session has expired. Please sign in again.")
                st.stop()
            else:
                st.warning(f"Unable to load transaction history: {transaction_response.text}")
        except requests.RequestException:
            st.warning("Unable to connect to the banking server.")

    # 3) AI Assistant section
    elif selected_section == "AI Assistant":
        st.subheader("AI Banking Assistant")
        st.caption("Ask questions about your balance, transactions, or loan EMI.")

        for chat in st.session_state["chat_history"]:
            with st.chat_message(chat["role"]):
                st.write(chat["content"])

        user_message = st.chat_input("Ask about your account...", key="banking_chat_input")
        if user_message:
            st.session_state["chat_history"].append({"role": "user", "content": user_message})
            answer = "I could not process that request."
            try:
                chat_response = requests.post(
                    f"{API_URL}/agent/chat", headers=headers,
                    json={"message": user_message}, timeout=10,
                )
                if chat_response.status_code == 200:
                    chat_data = chat_response.json()
                    if "result" in chat_data:
                        agent_result = chat_data["result"]
                        if isinstance(agent_result, dict):
                            if "balance" in agent_result:
                                name = agent_result.get("customer_name", agent_result.get("name", "Customer"))
                                amount = float(agent_result.get("balance", 0))
                                answer = f"NAME: {name}\n\nBALANCE: ₹{amount:,.2f}"
                            elif "transactions" in agent_result:
                                transactions = agent_result["transactions"]
                                if not transactions:
                                    answer = "No transactions found."
                                else:
                                    lines = ["TRANSACTION DETAILS"]
                                    for transaction in transactions:
                                        if isinstance(transaction, dict):
                                            amount = float(transaction.get("amount", 0))
                                            transaction_type = transaction.get("type", transaction.get("transaction_type", "Transaction"))
                                            transaction_date = transaction.get("date", "Date unavailable")
                                            description = transaction.get("description", "-")
                                            lines.append(f"Date: {transaction_date}\nType: {transaction_type}\nAmount: ₹{amount:,.2f}\nDescription: {description}")
                                        else:
                                            lines.append(str(transaction))
                                    answer = "\n\n".join(lines)
                            elif "monthly_emi" in agent_result:
                                answer = (
                                    f"MONTHLY EMI: ₹{float(agent_result['monthly_emi']):,.2f}\n\n"
                                    f"TOTAL INTEREST: ₹{float(agent_result.get('total_interest', 0)):,.2f}\n\n"
                                    f"TOTAL PAYMENT: ₹{float(agent_result.get('total_payment', 0)):,.2f}"
                                )
                            else:
                                answer = "\n".join(f"{key.replace('_', ' ').title()}: {value}" for key, value in agent_result.items())
                        else:
                            answer = str(agent_result)
                    elif "message" in chat_data:
                        answer = str(chat_data["message"])
                elif chat_response.status_code == 401:
                    answer = "Your session has expired. Please sign in again."
                else:
                    answer = f"Request failed: {chat_response.text}"
            except requests.RequestException:
                answer = "Unable to connect to the banking server."

            st.session_state["chat_history"].append({"role": "assistant", "content": answer})
            st.rerun()
