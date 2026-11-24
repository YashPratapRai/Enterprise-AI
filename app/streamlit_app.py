
import os
import uuid
import html
from datetime import datetime

import requests
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

API_BASE = os.getenv(
    "ATLAS_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

REQUEST_TIMEOUT = 60
MAX_UPLOAD_BYTES = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = ["pdf", "docx", "txt", "md"]

st.set_page_config(
    page_title="Enterprise AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    :root {
        color-scheme: dark;
        --app-bg: #0b1020;
        --app-sidebar: #10182c;
        --app-panel: #111b30;
        --app-border: #263550;
        --app-muted: #9aaccc;
        --app-text: #e9eefb;
        --app-accent: #72e5d2;
        --app-accent-dark: #5fd5bf;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--app-bg);
        color: var(--app-text);
        font-family: Inter, Arial, sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(11, 16, 32, 0.92);
    }

    [data-testid="stSidebar"] {
        background: var(--app-sidebar);
        border-right: 1px solid #26334b;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.5rem;
    }

    .app-logo {
        color: #8de4dc;
        font-size: 25px;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 8px 0 42px 8px;
    }

    .app-logo span {
        color: white;
    }

    .app-eyebrow {
        color: #8194b2;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 8px 0 12px 4px;
    }

    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin: 4px 0 26px 0;
    }

    .app-header h1 {
        color: #e9eefb;
        font-size: 27px;
        font-weight: 700;
        margin: 0;
    }

    .app-pill {
        white-space: nowrap;
        border: 1px solid #2b655c;
        background: #15352f;
        color: #a5f4c7;
        border-radius: 30px;
        padding: 9px 15px;
        font-size: 12px;
    }

    .app-hero {
        text-align: center;
        padding: 18px 0 22px 0;
    }

    .app-spark {
        color: var(--app-accent);
        font-size: 42px;
    }

    .app-hero h2 {
        color: #e9eefb;
        font-size: 22px;
        margin: 3px 0 8px 0;
    }

    .app-hero p,
    .app-muted {
        color: var(--app-muted);
    }

    .app-hint {
        color: #758ba8;
        font-size: 11px;
        text-align: center;
        margin-top: 10px;
    }

    .app-user {
        background: #193f46;
        border: 1px solid #285b60;
        border-radius: 15px;
        padding: 14px 17px;
        margin: 12px 0 12px auto;
        max-width: 88%;
        color: #e9eefb;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }

    .app-assistant {
        background: #1a2a44;
        border: 1px solid #2b405e;
        border-radius: 15px;
        padding: 16px 18px;
        margin: 12px auto 12px 0;
        max-width: 96%;
        color: #e9eefb;
        line-height: 1.65;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }

    .app-card {
        background: #18263c;
        border: 1px solid #344d6c;
        border-radius: 14px;
        padding: 17px;
        margin: 12px 0;
    }

    .app-status {
        display: inline-block;
        border-radius: 20px;
        padding: 4px 10px;
        background: #34435d;
        color: #e9eefb;
        font-size: 12px;
        text-transform: capitalize;
    }

    .app-status.pending {
        background: #574526;
        color: #ffe6a2;
    }

    .app-status.approved {
        background: #164c3d;
        color: #adf5c9;
    }

    .app-status.rejected {
        background: #572b35;
        color: #ffc3c9;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border: 1px solid #3b516e;
        background: #202f47;
        color: #dceafa;
        border-radius: 10px;
        min-height: 40px;
        font-weight: 500;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        border-color: #6de4cf;
        color: #b8fff2;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: var(--app-accent-dark);
        border: 0;
        color: #071c24;
        font-weight: 700;
    }

    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input,
    [data-testid="stFileUploader"] section {
        background: #1a2941;
        color: #e9eefb;
        border-color: #344d6c;
        border-radius: 10px;
    }

    [data-testid="stExpander"] {
        background: #17243a;
        border: 1px solid #344d6c;
        border-radius: 10px;
    }

    [data-testid="stMetric"] {
        background: #18263c;
        border: 1px solid #344d6c;
        padding: 14px;
        border-radius: 13px;
    }

    hr {
        border-color: #263550;
    }

    footer {
        visibility: hidden;
    }

    @media (max-width: 760px) {
        .app-header {
            display: block;
        }

        .app-header h1 {
            font-size: 22px;
        }

        .app-pill {
            display: inline-block;
            margin-top: 12px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API HELPERS
# ============================================================

def api_request(method: str, path: str, *, json=None, timeout=REQUEST_TIMEOUT):
    url = f"{API_BASE}{path}"

    try:
        response = requests.request(
            method,
            url,
            json=json,
            timeout=timeout,
            headers={"Accept": "application/json"},
        )

    except requests.RequestException as exc:
        raise RuntimeError(
            f"Could not connect to Enterprise AI API at {API_BASE}. "
            "Start FastAPI first and verify ATLAS_API_URL."
        ) from exc

    try:
        data = response.json()

    except ValueError:
        data = {
            "detail": response.text or "Invalid API response."
        }

    if not response.ok:
        detail = (
            data.get("detail", f"Request failed ({response.status_code})")
            if isinstance(data, dict)
            else str(data)
        )
        raise RuntimeError(str(detail))

    return data


def format_date(value):
    if not value:
        return ""

    try:
        if isinstance(value, str):
            value = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )

        return value.strftime("%d %b %Y, %I:%M %p")

    except (TypeError, ValueError):
        return str(value)


def load_conversation():

    if st.session_state.get("conversation_loaded"):
        return

    try:
        result = api_request(
            "GET",
            f"/api/conversations/{st.session_state.conversation_id}/messages",
        )

        st.session_state.messages = [
            {
                "role": row["role"],
                "content": row["content"],
                "sources": [],
            }
            for row in result.get("messages", [])
        ]

    except Exception:
        st.session_state.messages = []

    st.session_state.conversation_loaded = True


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "page": "Knowledge chat",
    "conversation_id": str(uuid.uuid4()),
    "conversation_loaded": False,
    "messages": [],
    "composer_input": "",
    "approval_confirmation": None,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="app-logo">✦ <span>Enterprise AI</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="app-eyebrow">WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    nav_items = [
        ("◈", "Knowledge chat"),
        ("▤", "Documents"),
        ("✓", "Approvals"),
        ("◫", "Metrics"),
    ]

    for symbol, label in nav_items:

        if st.button(
            f"{symbol}   {label}",
            key=f"nav_{label}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.page == label
                else "secondary"
            ),
        ):
            st.session_state.page = label
            st.rerun()

    st.markdown("---")

    st.caption("Single-workspace demo · No login")
    st.caption(f"API: {API_BASE}")


# ============================================================
# MAIN PAGE HEADER
# ============================================================

page_titles = {
    "Knowledge chat": "Ask your organization's knowledge",
    "Documents": "Document management",
    "Approvals": "Approval requests",
    "Metrics": "Operational overview",
}

st.markdown(
    f"""
    <div class="app-header">
        <div>
            <div class="app-eyebrow">
                YOUR WORKSPACE / KNOWLEDGE
            </div>
            <h1>{page_titles[st.session_state.page]}</h1>
        </div>
        <div class="app-pill">● aws powered</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# PAGE 1: KNOWLEDGE CHAT
# ============================================================

if st.session_state.page == "Knowledge chat":

    load_conversation()

    send = False
    question = ""

    # Native Streamlit container instead of separate HTML div tags.
    with st.container(border=True):

        if not st.session_state.messages:

            st.markdown(
                """
                <div class="app-hero">
                    <div class="app-spark">✦</div>
                    <h2>What can I help you find?</h2>
                    <p>
                        Ask questions about your approved documents.
                        Every answer includes its evidence.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            suggestion_cols = st.columns(3)

            suggestions = [
                "What is our leave policy?",
                "Summarize the onboarding process",
                "What are the IT security rules?",
            ]

            for col, suggestion in zip(
                suggestion_cols,
                suggestions,
            ):

                with col:

                    if st.button(
                        suggestion + " ↗",
                        key=f"suggest_{suggestion}",
                        use_container_width=True,
                    ):
                        st.session_state.composer_input = suggestion
                        st.rerun()

        top_left, top_right = st.columns([1, 5])

        with top_left:

            if st.button(
                "＋ New conversation",
                use_container_width=True,
            ):
                st.session_state.conversation_id = str(uuid.uuid4())
                st.session_state.conversation_loaded = True
                st.session_state.messages = []
                st.session_state.composer_input = ""
                st.rerun()

        # Display conversation messages.
        for index, message in enumerate(st.session_state.messages):

            role = message.get("role", "assistant")
            content = str(message.get("content", ""))

            if role == "user":

                st.markdown(
                    f'<div class="app-user">{html.escape(content)}</div>',
                    unsafe_allow_html=True,
                )

            elif role == "assistant":

                st.markdown(
                    f'<div class="app-assistant">{html.escape(content)}</div>',
                    unsafe_allow_html=True,
                )

                sources = message.get("sources", [])

                if sources:

                    with st.expander(
                        f"Evidence and sources ({len(sources)})",
                        expanded=False,
                    ):

                        for source in sources:

                            title = source.get("title") or "Document"
                            page = source.get("page", 1)
                            excerpt = source.get("excerpt", "")

                            st.markdown(
                                f"**[{source.get('index', 1)}] "
                                f"{html.escape(str(title))} — page {page}**"
                            )

                            st.caption(excerpt)

                    feedback_col, _ = st.columns([1, 5])

                    with feedback_col:

                        if st.button(
                            "👍 Helpful",
                            key=f"feedback_{index}",
                        ):

                            try:
                                api_request(
                                    "POST",
                                    "/api/feedback",
                                    json={"rating": 1},
                                )
                                st.success("Feedback saved")

                            except Exception as exc:
                                st.error(str(exc))

        # Chat input.
        with st.form(
            "chat_form",
            clear_on_submit=True,
        ):

            question = st.text_area(
                "Question",
                placeholder="Ask a question about company knowledge...",
                height=82,
                key="composer_input",
                label_visibility="collapsed",
            )

            send = st.form_submit_button(
                "Send ↗",
                type="primary",
                use_container_width=True,
            )

        st.markdown(
            """
            <div class="app-hint">
                Answers may be inaccurate.
                Verify source passages before taking action.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Process question after form submission.
    if send:

        clean_question = (question or "").strip()

        if len(clean_question) < 3:

            st.warning(
                "Please enter a question with at least 3 characters."
            )

        else:

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": clean_question,
                    "sources": [],
                }
            )

            with st.spinner("Searching approved documents..."):

                try:

                    result = api_request(
                        "POST",
                        "/api/chat",
                        json={
                            "question": clean_question,
                            "conversation_id": st.session_state.conversation_id,
                        },
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": result.get("answer", ""),
                            "sources": result.get("sources", []),
                            "status": result.get("status", "answered"),
                        }
                    )

                    if result.get("status") == "pending_approval":

                        st.info(
                            "This request is waiting for administrator approval. "
                            "Open the Approvals tab to review it."
                        )

                except Exception as exc:

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": f"Request failed: {exc}",
                            "sources": [],
                        }
                    )

            st.rerun()


# ============================================================
# PAGE 2: DOCUMENT MANAGEMENT
# ============================================================

elif st.session_state.page == "Documents":

    with st.container(border=True):

        st.subheader("Knowledge library")

        st.markdown(
            """
            <p class="app-muted">
                Upload an approved PDF, DOCX, TXT or Markdown file.
                Use non-sensitive demo documents only.
            </p>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Choose a document",
            type=ALLOWED_EXTENSIONS,
            accept_multiple_files=False,
        )

        if uploaded_file is not None:

            if uploaded_file.size > MAX_UPLOAD_BYTES:

                st.error("Maximum file size is 10 MB.")

            elif st.button(
                "Upload document",
                type="primary",
            ):

                try:

                    with st.spinner(
                        "Uploading to S3 and indexing in Pinecone..."
                    ):

                        created = api_request(
                            "POST",
                            "/api/documents/uploads",
                            json={
                                "filename": uploaded_file.name
                            },
                        )

                        upload_response = requests.put(
                            created["upload_url"],
                            data=uploaded_file.getvalue(),
                            headers=created.get(
                                "headers",
                                {
                                    "Content-Type": "application/octet-stream"
                                },
                            ),
                            timeout=120,
                        )

                        if not upload_response.ok:

                            raise RuntimeError(
                                f"S3 upload failed "
                                f"({upload_response.status_code}): "
                                f"{upload_response.text[:300]}"
                            )

                        completed = api_request(
                            "POST",
                            "/api/documents/complete",
                            json={
                                "document_id": created["document_id"]
                            },
                            timeout=180,
                        )

                    st.success(
                        "Document indexed successfully. "
                        f"Status: {completed.get('status', 'ready')}"
                    )

                    st.rerun()

                except Exception as exc:

                    st.error(f"Upload failed: {exc}")

        st.divider()

        st.subheader("Uploaded documents")

        if st.button("Refresh documents"):
            st.rerun()

        try:

            response = api_request(
                "GET",
                "/api/documents",
            )

            documents = response.get("documents", [])

            if not documents:

                st.info(
                    "No documents found in this workspace yet."
                )

            else:

                for document in documents:

                    title = document.get(
                        "title",
                        "Untitled document",
                    )

                    status = str(
                        document.get("status", "unknown")
                    ).lower()

                    version = document.get(
                        "current_version",
                        1,
                    )

                    st.markdown(
                        f"""
                        <div class="app-card">
                            <strong>{html.escape(str(title))}</strong>
                            <span style="float:right"
                                class="app-status {html.escape(status)}">
                                {html.escape(status)}
                            </span>
                            <div class="app-muted">
                                Version {html.escape(str(version))}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

        except Exception as exc:

            st.error(
                f"Unable to load documents: {exc}"
            )


# ============================================================
# PAGE 3: APPROVALS
# ============================================================

elif st.session_state.page == "Approvals":

    with st.container(border=True):

        st.subheader("Human-in-the-loop approvals")

        st.markdown(
            """
            <p class="app-muted">
                Review pending requests. Approving records a decision only;
                no document is deleted or exported.
            </p>
            """,
            unsafe_allow_html=True,
        )

        if st.button("↻ Refresh approvals"):
            st.rerun()

        try:

            response = api_request(
                "GET",
                "/api/approvals",
            )

            approvals = response.get("approvals", [])

            pending_count = sum(
                1
                for item in approvals
                if str(item.get("status", "")).lower() == "pending"
            )

            st.caption(
                f"{pending_count} pending · "
                f"{len(approvals)} total (most recent 100)"
            )

            if not approvals:

                st.info(
                    "No approval requests yet. "
                    "Try asking the chatbot to delete a document."
                )

            for approval in approvals:

                approval_id = str(approval.get("id"))

                status = str(
                    approval.get("status", "unknown")
                ).lower()

                with st.container(border=True):

                    title_col, status_col = st.columns([5, 1])

                    with title_col:

                        st.markdown(
                            f"**{html.escape(str(approval.get('question', 'Untitled request')))}**"
                        )

                    with status_col:

                        st.markdown(
                            f'<span class="app-status {html.escape(status)}">'
                            f'{html.escape(status)}</span>',
                            unsafe_allow_html=True,
                        )

                    st.caption(
                        f"Requested by {approval.get('requester', 'unknown')} · "
                        f"{format_date(approval.get('created_at'))}"
                    )

                    if status == "pending":

                        action_cols = st.columns(2)

                        with action_cols[0]:

                            if st.button(
                                "Approve",
                                key=f"approve_{approval_id}",
                                use_container_width=True,
                            ):

                                st.session_state.approval_confirmation = {
                                    "id": approval_id,
                                    "approve": True,
                                }

                        with action_cols[1]:

                            if st.button(
                                "Reject",
                                key=f"reject_{approval_id}",
                                use_container_width=True,
                            ):

                                st.session_state.approval_confirmation = {
                                    "id": approval_id,
                                    "approve": False,
                                }

                    else:

                        st.caption(
                            f"Reviewed by {approval.get('reviewer') or 'unknown'} · "
                            f"{format_date(approval.get('reviewed_at'))} · "
                            "No action executed"
                        )

            confirmation = st.session_state.approval_confirmation

            if confirmation:

                decision = (
                    "approve"
                    if confirmation["approve"]
                    else "reject"
                )

                st.warning(
                    f"Confirm you want to {decision} this request? "
                    "This records a decision only and does not execute "
                    "the requested action."
                )

                confirm_cols = st.columns(2)

                with confirm_cols[0]:

                    if st.button(
                        "Confirm decision",
                        type="primary",
                        use_container_width=True,
                    ):

                        try:

                            outcome = api_request(
                                "POST",
                                f"/api/approvals/{confirmation['id']}/decision",
                                json={
                                    "approve": confirmation["approve"]
                                },
                            )

                            st.session_state.approval_confirmation = None

                            st.success(
                                f"Request {outcome.get('status')}. "
                                "No action executed."
                            )

                            st.rerun()

                        except Exception as exc:

                            st.error(str(exc))

                with confirm_cols[1]:

                    if st.button(
                        "Cancel",
                        use_container_width=True,
                    ):

                        st.session_state.approval_confirmation = None
                        st.rerun()

        except Exception as exc:

            st.error(
                f"Unable to load approvals: {exc}. "
                "The current API requires an admin principal for this page."
            )


# ============================================================
# PAGE 4: METRICS
# ============================================================

elif st.session_state.page == "Metrics":

    with st.container(border=True):

        st.subheader("Workspace metrics")

        try:

            metrics = api_request(
                "GET",
                "/api/admin/metrics",
            )

            document_rows = metrics.get("documents", [])
            feedback_rows = metrics.get("feedback", [])

            total_documents = sum(
                int(row.get("total", 0))
                for row in document_rows
            )

            total_feedback = sum(
                int(row.get("total", 0))
                for row in feedback_rows
            )

            metric_cols = st.columns(3)

            metric_cols[0].metric(
                "Documents",
                total_documents,
            )

            metric_cols[1].metric(
                "Feedback responses",
                total_feedback,
            )

            metric_cols[2].metric(
                "Feedback groups",
                len(feedback_rows),
            )

            with st.expander(
                "Document status breakdown",
                expanded=True,
            ):

                if document_rows:

                    st.dataframe(
                        document_rows,
                        use_container_width=True,
                        hide_index=True,
                    )

                else:

                    st.caption("No document records yet.")

            with st.expander(
                "Feedback breakdown",
                expanded=True,
            ):

                if feedback_rows:

                    st.dataframe(
                        feedback_rows,
                        use_container_width=True,
                        hide_index=True,
                    )

                else:

                    st.caption("No feedback received yet.")

        except Exception as exc:

            st.error(
                f"Unable to load workspace metrics: {exc}"
            )

        st.divider()

        st.subheader("Guardrail events")

        try:

            guardrail_data = api_request(
                "GET",
                "/api/admin/guardrails",
            )

            events = guardrail_data.get("events", [])

            if events:

                st.dataframe(
                    events,
                    use_container_width=True,
                    hide_index=True,
                )

            else:

                st.info(
                    "No guardrail events recorded yet."
                )

            st.caption(
                f"Mode: {guardrail_data.get('mode', 'unknown')} · "
                f"Managed Bedrock Guardrails: "
                f"{guardrail_data.get('managed_bedrock_guardrails', False)}"
            )

        except Exception as exc:

            st.error(
                f"Unable to load guardrail metrics: {exc}"
            )
