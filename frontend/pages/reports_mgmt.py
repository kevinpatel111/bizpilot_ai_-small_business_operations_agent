import streamlit as st
import os
import json
import re
from tools.reporting_tools import generate_pdf_report, export_excel_report
from agents.advisor import run_advisor_agent
from utils.logger import logger

def extract_score(advisor_text: str) -> int:
    """Try to extract a health score from the advisor text, default to 75."""
    match = re.search(r"health\s*score:?\s*(\d+)", advisor_text, re.IGNORECASE)
    if match:
        try:
            return int(match.group(1))
        except Exception:
            pass
    return 75

def render_reports_mgmt():
    st.title("📋 Business Reports & Exports")
    st.write("Generate professional PDF reports and export consolidated Excel sheets of your operations.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Generate PDF Performance Audit")
        st.write("This PDF will compile your sales KPIs, low stock notices, profit margins, and include custom AI Advisor recommendations.")
        
        if st.button("Generate Performance PDF"):
            with st.spinner("Advisor Agent is compiling metrics & creating PDF..."):
                # Run advisor agent first
                audit_text = run_advisor_agent("Compile a business performance summary and highlight the top 3 weekly recommendations.")
                score = extract_score(audit_text)
                
                # Split audit text into summary and recommendations
                summary = audit_text.split("Recommendations")[0] if "Recommendations" in audit_text else audit_text
                
                recs_match = re.findall(r"-\s*(.*)", audit_text)
                recs = recs_match[:5] if recs_match else ["Review stock levels", "Control operating expenses", "Identify high-performing channels"]
                
                summary_data = {
                    "health_score": score,
                    "summary": summary,
                    "recommendations": recs
                }
                
                pdf_path = generate_pdf_report(summary_data)
                
                if pdf_path and os.path.exists(pdf_path):
                    st.success("✅ PDF Report Generated!")
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download Performance PDF",
                            data=f,
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf"
                        )
                else:
                    st.error("Failed to generate PDF report. Check logs for details.")
                    
    with col2:
        st.subheader("Export Excel Ledger")
        st.write("Export your consolidated sales, inventory, and expense tables into a clean multi-tab Excel spreadsheet.")
        
        if st.button("Compile & Export Excel"):
            with st.spinner("Generating Excel sheets..."):
                excel_path = export_excel_report()
                if excel_path and os.path.exists(excel_path):
                    st.success("✅ Excel Workbook Compiled!")
                    with open(excel_path, "rb") as f:
                        st.download_button(
                            label="Download Excel Workbook",
                            data=f,
                            file_name=os.path.basename(excel_path),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.error("Failed to compile Excel workbook.")
                    
    st.markdown("---")
    
    # Expose a direct support draft capability here as well, because "Customer Support Agent" needs visibility
    st.subheader("✉️ Customer Support Reply Drafts")
    st.write("Generate email/chat replies for customer inquiries, returns, refunds, or product availability.")
    
    from agents.support import run_support_agent
    support_query = st.text_input("Describe the customer issue/query:", placeholder="e.g. Customer is asking for a refund on a broken item.")
    if st.button("Generate Draft Reply"):
        if support_query:
            with st.spinner("Drafting response..."):
                reply = run_support_agent(support_query)
                st.info("Here is the suggested draft reply:")
                st.code(reply, language="text")
        else:
            st.warning("Please enter customer query details.")
