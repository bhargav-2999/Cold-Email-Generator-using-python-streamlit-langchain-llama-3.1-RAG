# import streamlit as st
# from langchain_community.document_loaders import WebBaseLoader

# from chains import Chain
# from portfolio import Portfolio
# from utils import clean_text


# def create_streamlit_app(llm, portfolio, clean_text):
#     st.title("📧 Cold Mail Generator")
#     url_input = st.text_input("Enter a URL:", value="https://careers.nike.com/data-engineer/job/R-51131")
#     submit_button = st.button("Submit")

#     if submit_button:
#         try:
#             loader = WebBaseLoader([url_input])
#             data = clean_text(loader.load().pop().page_content)
#             portfolio.load_portfolio()
#             jobs = llm.extract_jobs(data)
#             for job in jobs:
#                 skills = job.get('skills', [])
#                 links = portfolio.query_links(skills)
#                 email = llm.write_mail(job, links)
#                 st.code(email, language='markdown')
#         except Exception as e:
#             st.error(f"An Error Occurred: {e}")


# if __name__ == "__main__":
#     chain = Chain()
#     portfolio = Portfolio()
#     st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
#     create_streamlit_app(chain, portfolio, clean_text)
















import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, portfolio, clean_text):
    # Custom CSS for styling
    st.markdown(
        """
        <style>
        /* Overall background gradient */
        .reportview-container {
            background: linear-gradient(to bottom right, #f7f9fc, #e3e7f0);
        }
        /* Header styling */
        .main-header {
            background: linear-gradient(90deg, #0072ff, #00c6ff);
            padding: 1.5rem;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 2rem;
        }
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background: #f0f2f6;
        }
        /* Input container styling */
        .input-container {
            background: #ffffff;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        /* Result container styling */
        .result-container {
            background: #ffffff;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            margin-top: 2rem;
            border-left: 5px solid #0072ff;
        }
        /* Footer styling */
        .footer {
            text-align: center;
            font-size: 0.8rem;
            color: #777777;
            margin-top: 2rem;
            padding: 1rem;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Header banner
    st.markdown("<div class='main-header'>Cold Mail Generator</div>", unsafe_allow_html=True)

    # Sidebar for input settings
    st.sidebar.header("Job URL Input")
    url_input = st.sidebar.text_input("Enter the job posting URL:", value="https://careers.nike.com/data-engineer/job/R-51131")
    submit_button = st.sidebar.button("Generate Emails")

    # Expandable instructions section
    with st.expander("How It Works"):
        st.markdown("""
            1. **Enter the URL:** Provide the URL of the job posting.
            2. **Scrape Data:** The system scrapes the job details from the webpage.
            3. **Extract & Generate:** It extracts key details and generates a personalized cold email.
            4. **Review:** The generated email is displayed below for your review.
        """)

    if submit_button:
        with st.spinner("Processing your request..."):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                if jobs:
                    for job in jobs:
                        skills = job.get('skills', [])
                        links = portfolio.query_links(skills)
                        email = llm.write_mail(job, links)

                        st.markdown("<div class='result-container'>", unsafe_allow_html=True)
                        st.subheader("Generated Email")
                        st.code(email, language='markdown')
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.warning("No job postings found.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Footer
    st.markdown("<div class='footer'>Powered by Your Cold Email Generator App</div>", unsafe_allow_html=True)


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator By Bhargav", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
