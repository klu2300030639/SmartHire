import streamlit as st


import pandas as pd


import numpy as np


import os


import tempfile


import matplotlib.pyplot as plt


import seaborn as sns


from src.preprocessing import parse_resume, extract_email, extract_phone, extract_skills


from src.classifier import predict_category, train_classifier, CLASSIFIER_PATH


from src.recommender import get_job_recommendations, analyze_skill_gap


from src.clustering import cluster_jobs_pipeline, get_similar_jobs_in_cluster

# Set page config


st.set_page_config(


    page_title="SmartHire - AI Resume Matcher & Career Guide",


    page_icon="🤖",


    layout="wide",


    initial_sidebar_state="expanded"


)

# Custom CSS for Premium Look


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    /* Theme-adaptive base settings */
    .title-banner {
        background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    .title-banner h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #818cf8 0%, #e879f9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .title-banner p {
        font-size: 1.2rem;
        color: #a5b4fc;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    .card {
        background: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.1);
        border-radius: 1rem;
        padding: 1.8rem;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }
    .card:hover {
        border-color: rgba(139, 92, 246, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(139, 92, 246, 0.1);
    }
    .compatibility-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 0.8rem;
    }
    .compatibility-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--text-color);
    }
    .fit-badge {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .skill-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 0.5rem;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .skill-match {
        background-color: rgba(16, 185, 129, 0.12);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.25);
    }
    .skill-missing {
        background-color: rgba(239, 68, 68, 0.12);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.25);
    }
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #c084fc;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

# Helper function to reload datasets


@st.cache_data


def load_datasets_v2():

    if not os.path.exists("data/raw_resumes.csv") or not os.path.exists("data/raw_jobs.csv"):


        return None, None


    res_df = pd.read_csv("data/raw_resumes.csv")


    jobs_df = pd.read_csv("data/raw_jobs.csv")


    return res_df, jobs_df

resumes_df, jobs_df = load_datasets_v2()

# Application Layout


st.markdown("""
<div class="title-banner">
    <h1>SmartHire</h1>
    <p>AI-Powered Resume Classification, Job Recommendation, Skill-Gap Analysis, and Career Path Clustering</p>
</div>
""", unsafe_allow_html=True)

# Sidebar settings


with st.sidebar:


    st.markdown('<div class="sidebar-header">⚙️ System Control</div>', unsafe_allow_html=True)

    if resumes_df is None or jobs_df is None:


        st.error("⚠️ Datasets not detected!")


        if st.button("Generate Synthetic Datasets"):


            with st.spinner("Generating mock resumes and jobs..."):


                from src.data_generation import create_datasets


                create_datasets()


                st.rerun()


    else:


        st.success("✅ Datasets loaded successfully.")


        st.metric("Total Jobs in Database", len(jobs_df))


        st.metric("Total Resumes in Database", len(resumes_df))

    st.markdown("---")


    st.markdown("### Navigation")


    menu = st.radio("Go To:", ["🏠 Overview", "📍 Resume Matcher", "🕸️ Job Clusters", "🛠️ Model Admin"])

# 1. OVERVIEW PAGE


if menu == "🏠 Overview":


    st.header("System Overview")

    if resumes_df is None or jobs_df is None:


        st.warning("Please click 'Generate Synthetic Datasets' in the sidebar to populate the system.")


    else:


        col1, col2 = st.columns(2)

        with col1:


            st.subheader("Job Distributions by Domain")


            domain_counts = jobs_df['category'].value_counts()


            chart_data = pd.DataFrame({


                "Jobs Count": domain_counts.values


            }, index=domain_counts.index)


            st.bar_chart(chart_data, color="#818cf8")

        with col2:


            st.subheader("Overview of Career Domains")


            st.write("""


            SmartHire utilizes classical Machine Learning algorithms to facilitate career transition and recruitment:


            1. **Resume Classification**: Uses a trained **Logistic Regression** classifier on **TF-IDF features** to categorize candidates into relevant domains.


            2. **Job Recommender**: Measures content similarity using **Cosine Similarity** between resume contents and job descriptions.


            3. **Skill Gap Analysis**: Extracts matching and missing skills and queries a course recommendations mapping to direct users on bridging their career gaps.


            4. **Job Clustering**: Automatically structures jobs into logical groups using **K-Means Clustering** to identify related career paths.


            """, unsafe_allow_html=True)

        st.markdown("---")


        st.subheader("Quick Explore Jobs Database")


        search_query = st.text_input("🔍 Search jobs by keyword (e.g. Python, SQL, UI/UX):")


        if search_query:


            filtered_jobs = jobs_df[


                jobs_df['title'].str.contains(search_query, case=False) |


                jobs_df['required_skills'].str.contains(search_query, case=False) |


                jobs_df['description'].str.contains(search_query, case=False)


            ]


            st.dataframe(filtered_jobs[['job_id', 'title', 'company', 'category', 'location', 'required_skills']])


        else:


            st.dataframe(jobs_df[['job_id', 'title', 'company', 'category', 'location', 'required_skills']].head(10))

# 2. RESUME MATCHER PAGE


elif menu == "📍 Resume Matcher":


    st.header("Resume-to-Job Matching & Career Guidance")

    if resumes_df is None or jobs_df is None:


        st.warning("Please click 'Generate Synthetic Datasets' in the sidebar to populate the system.")


    else:


        st.subheader("Upload Candidate Resume")


        uploaded_file = st.file_uploader("Upload resume (PDF, DOCX, TXT, JPG, or PNG format)", type=["pdf", "docx", "txt", "jpg", "jpeg", "png"])

        # Or load a sample resume from dataset for quick demo


        st.markdown("**OR** select a sample profile from our database:")


        sample_profiles = resumes_df['name'].tolist()


        selected_sample = st.selectbox("Choose a sample candidate profile:", ["-- Select --"] + sample_profiles)

        resume_text = ""


        candidate_name = "Candidate"

        if uploaded_file is not None:


            st.info(f"ℹ️ Active Profile: Uploaded Resume ({uploaded_file.name})")


            uploaded_file.seek(0)  # Reset pointer to start of stream


            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:


                temp_file.write(uploaded_file.read())


                temp_file_path = temp_file.name

            with st.spinner("Parsing resume file..."):


                resume_text = parse_resume(temp_file_path)


                candidate_name = os.path.splitext(uploaded_file.name)[0]

            os.remove(temp_file_path)

        elif selected_sample != "-- Select --":


            st.info(f"ℹ️ Active Profile: Sample Candidate ({selected_sample})")


            profile_row = resumes_df[resumes_df['name'] == selected_sample].iloc[0]


            resume_text = profile_row['text']


            candidate_name = profile_row['name']

        # Check for empty text


        if (uploaded_file is not None or selected_sample != "-- Select --") and (not resume_text or not resume_text.strip()):


            st.warning("⚠️ No readable text could be extracted. Please ensure it is a digital (not scanned) file.")


            resume_text = ""

        if resume_text and resume_text.strip():


            st.success("Resume parsed successfully!")

            try:


                # Extract basic metadata


                email = extract_email(resume_text)


                phone = extract_phone(resume_text)


                skills = extract_skills(resume_text)

                # Classify resume


                predicted_cat, probabilities = predict_category(resume_text)


            except Exception as e:


                st.error(f"❌ Error during profile extraction or classification: {e}")


                st.stop()

            # Display profile layout


            col1, col2 = st.columns([1, 1])

            with col1:


                st.markdown(f"### Candidate Profile: {candidate_name}")


                st.write(f"📧 **Email:** {email if email else 'Not found'}")


                st.write(f"📞 **Phone:** {phone if phone else 'Not found'}")


                st.write(f"💻 **AI Classified Career Category:** `{predicted_cat}`")

                st.markdown("#### Extracted Skills")


                if skills:


                    skill_badges = "".join([f'<span class="skill-badge skill-match">{s}</span>' for s in skills])


                    st.markdown(skill_badges, unsafe_allow_html=True)


                else:


                    st.write("No skills matched from dictionary.")

            with col2:


                st.markdown("### Profile Category Probabilities")


                cats = list(probabilities.keys())


                probs = list(probabilities.values())


                chart_data = pd.DataFrame({


                    "Probability": probs


                }, index=cats)


                st.bar_chart(chart_data, color="#e879f9")

            st.markdown("---")


            st.subheader("Top Job Recommendations")

            # Get recommendations


            with st.spinner("Calculating compatibility fit scores..."):


                recs = get_job_recommendations(resume_text, jobs_df, top_n=5)

            for idx, rec in enumerate(recs):


                score = rec['compatibility_score']

                # Setup score color


                if score >= 75:


                    score_color = "#10b981" # Green


                elif score >= 50:


                    score_color = "#f59e0b" # Orange


                else:


                    score_color = "#ef4444" # Red

                st.markdown(f"""
                <div class="card">
                    <div class="compatibility-header">
                        <div>
                            <span style="font-size: 1.4rem; font-weight: 700; color: var(--text-color);">{rec['title']}</span><br/>
                            <span style="color: #a5b4fc;">{rec['company']} | 📍 {rec['location']}</span>
                        </div>
                        <div>
                            <span style="color: {score_color}; font-size: 2rem; font-weight: 800;">{score}%</span><br/>
                            <span style="font-size: 0.8rem; color: #9ca3af; text-align: right; display: block;">Compatibility Fit</span>
                        </div>
                    </div>
                    <div style="font-size: 0.9rem; color: #9ca3af; margin-bottom: 1rem;">
                        <b>Score Breakdown:</b> Content Similarity: {rec['text_similarity_score']}% | Skill Match Rate: {rec['skill_match_score']}% | Domain Classification Match: {rec['category_match_score']}%
                    </div>
                """, unsafe_allow_html=True)

                # Show skill gap


                matching = rec['matching_skills']


                missing = rec['missing_skills']

                col_match, col_miss = st.columns(2)


                with col_match:


                    st.markdown('<div class="section-title">✅ Matching Skills</div>', unsafe_allow_html=True)


                    if matching:


                        m_badges = "".join([f'<span class="skill-badge skill-match">{s}</span>' for s in matching])


                        st.markdown(m_badges, unsafe_allow_html=True)


                    else:


                        st.write("No matching skills.")

                with col_miss:


                    st.markdown('<div class="section-title">❌ Missing Skills (Gaps)</div>', unsafe_allow_html=True)


                    if missing:


                        mis_badges = "".join([f'<span class="skill-badge skill-missing">{s}</span>' for s in missing])


                        st.markdown(mis_badges, unsafe_allow_html=True)


                    else:


                        st.write("No missing skills!")

                # Actionable Career Guidance


                st.markdown('<div class="section-title">📈 Career Guidance & Upskilling Recommendations</div>', unsafe_allow_html=True)


                if rec['guidance']:


                    for g in rec['guidance']:


                        st.write(f"- {g}")


                else:


                    st.write("Excellent! You match all required skills for this job.")

                with st.expander("View Full Job Description"):


                    st.write(rec['description'])

                st.markdown("</div>", unsafe_allow_html=True)

# 3. JOB CLUSTERS PAGE


elif menu == "🕸️ Job Clusters":


    st.header("Job Cluster Map & Path Discovery (K-Means)")

    if resumes_df is None or jobs_df is None:


        st.warning("Please click 'Generate Synthetic Datasets' in the sidebar to populate the system.")


    else:


        st.subheader("Discover Job Segments via Unsupervised Learning")

        @st.cache_data


        def get_clustered_data():

            return cluster_jobs_pipeline()

        clustered_df, themes = get_clustered_data()

        # Display clusters


        col1, col2 = st.columns([1, 2])

        with col1:


            st.write("""


            **What is job clustering?**


            Using **K-Means clustering** (with K=6), the machine learning pipeline groups similar jobs together solely based on the text contents of their job descriptions. 

            By analyzing the centroid vectors, the system automatically tags each cluster with its **dominant keywords**.


            """)

            st.markdown("#### Identified Job Clusters:")


            for cluster_id, info in themes.items():


                st.markdown(f"**{info['display_name']}**")

        with col2:


            # Bar chart of cluster counts


            counts = clustered_df['cluster_display_name'].value_counts()


            chart_data = pd.DataFrame({


                "Jobs Count": counts.values


            }, index=counts.index)


            st.bar_chart(chart_data, color="#c084fc")

        st.markdown("---")


        st.subheader("Explore a Cluster")

        cluster_list = list(themes.keys())


        selected_cluster_id = st.selectbox(


            "Select cluster to view jobs:", 


            options=cluster_list,


            format_func=lambda x: themes[x]['display_name']


        )

        cluster_jobs = clustered_df[clustered_df['cluster'] == selected_cluster_id]


        st.write(f"Found **{len(cluster_jobs)}** jobs in this cluster.")


        st.dataframe(cluster_jobs[['job_id', 'title', 'company', 'category', 'location', 'required_skills']])

        st.markdown("#### Discover Similar Path Recommendations")


        job_to_compare = st.selectbox(


            "Select a job to find similar cluster roles:", 


            options=cluster_jobs['job_id'].tolist(),


            format_func=lambda x: f"{cluster_jobs[cluster_jobs['job_id']==x]['title'].values[0]} at {cluster_jobs[cluster_jobs['job_id']==x]['company'].values[0]}"


        )

        if job_to_compare:


            similar_roles = get_similar_jobs_in_cluster(job_to_compare, clustered_df, top_n=3)


            st.write("Other relevant postings in the same cluster path:")


            for _, r in similar_roles.iterrows():


                st.markdown(f"- **{r['title']}** at *{r['company']}* ({r['location']}) - Skills: `{r['required_skills']}`")

# 4. MODEL ADMIN PAGE


elif menu == "🛠️ Model Admin":


    st.header("Classifier Metrics & Job Submissions")

    if resumes_df is None or jobs_df is None:


        st.warning("Please click 'Generate Synthetic Datasets' in the sidebar to populate the system.")


    else:


        st.subheader("Resume Classifier Metrics")

        # Test training accuracy


        if st.button("🔄 Retrain Classifier Model"):


            with st.spinner("Retraining Logistic Regression model..."):


                accuracy, report = train_classifier()


                st.success(f"Model retrained! New Accuracy: {accuracy:.4f}")


                st.write("Classification Report:")


                st.json(report)


        else:


            # Load default report


            if os.path.exists(CLASSIFIER_PATH):


                accuracy, report = train_classifier()


                st.metric("Classifier Accuracy", f"{accuracy*100:.2f}%")

                # Draw confusion matrix / metrics table


                report_df = pd.DataFrame(report).transpose().round(2)


                st.markdown("#### Detailed Domain Classification Metrics:")


                st.dataframe(report_df)


            else:


                st.warning("No trained model found. Please train model using the button above.")

        st.markdown("---")


        st.subheader("Add a New Job Posting")

        with st.form("new_job_form", clear_on_submit=True):


            job_title = st.text_input("Job Title:")


            company_name = st.text_input("Company:")


            job_cat = st.selectbox("Category Domain:", [


                "Software Engineering", "Data Science", "Frontend Development", 


                "DevOps", "Product Management", "Human Resources"


            ])


            job_loc = st.text_input("Location:")


            job_skills = st.text_input("Required Skills (comma-separated):")


            min_experience = st.number_input("Minimum Experience (Years):", min_value=0, max_value=30, value=2)


            job_desc = st.text_area("Job Description:")

            submit_btn = st.form_submit_button("Post Job")

            if submit_btn:


                if job_title and company_name and job_skills and job_desc:


                    new_job_id = f"JOB_{len(jobs_df)+1:03d}"


                    new_row = {


                        "job_id": new_job_id,


                        "title": job_title,


                        "company": company_name,


                        "category": job_cat,


                        "required_skills": job_skills,


                        "min_experience": min_experience,


                        "location": job_loc,


                        "description": f"Job Title: {job_title}\nCompany: {company_name}\nLocation: {job_loc}\nDepartment: {job_cat}\n\nABOUT THE ROLE\n{job_desc}\n\nREQUIREMENTS\n- Required Skills: {job_skills}\n- Minimum {min_experience} years of experience."


                    }

                    # Append and save


                    updated_jobs_df = pd.concat([jobs_df, pd.DataFrame([new_row])], ignore_index=True)


                    updated_jobs_df.to_csv("data/raw_jobs.csv", index=False)


                    st.success(f"Job {new_job_id} ({job_title}) added successfully to the database!")


                    st.cache_data.clear() # Clear cache to refresh


                    st.rerun()


                else:


                    st.error("Please fill out all fields.")
