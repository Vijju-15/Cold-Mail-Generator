import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://careers.nike.com/software-engineer-ii-itc/job/R-51399")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)

            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            if not jobs:
                st.error("No jobs found on the given page.")
                return

            all_skills = []
            combined_description = ""

            for job in jobs:
                role = job.get("role", "N/A")
                experience = job.get("experience", "N/A")
                skills = job.get("skills", [])
                description = job.get("description", "")

                all_skills.extend(skills)
                combined_description += f"**Role:** {role}\n**Experience:** {experience}\n**Skills:** {', '.join(skills)}\n**Description:** {description}\n\n"

            if not all_skills:
                st.error("No skills found in job listings.")
                return

            # Query links using ALL skills from all jobs
            links = portfolio.query_links(all_skills)
            # Flatten links
            flat_links = [meta.get("links") for group in links for meta in group if "links" in meta]

            # Create combined job dict
            combined_job = {
                "title": "Multiple Job Openings",
                "skills": list(set(all_skills)),
                "description": combined_description
            }

            # Generate one single mail
            email = llm.write_mail(combined_job, flat_links)
            st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
