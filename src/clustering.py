import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from src.preprocessing import clean_text

def cluster_jobs_pipeline(data_path="data/raw_jobs.csv", n_clusters=6):
    """Loads job dataset, runs K-Means clustering on the TF-IDF representation, and returns results and cluster themes."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Jobs dataset not found at {data_path}")
        
    df = pd.read_csv(data_path)
    
    # Preprocess descriptions
    cleaned_desc = df['description'].apply(clean_text)
    
    # TF-IDF
    vectorizer = TfidfVectorizer(max_features=1000)
    X_vec = vectorizer.fit_transform(cleaned_desc)
    
    # K-Means
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(X_vec)
    
    df['cluster'] = kmeans.labels_
    
    # Identify top keywords for each cluster to define themes
    order_centroids = kmeans.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names_out()
    
    cluster_themes = {}
    for i in range(n_clusters):
        top_terms = [terms[ind] for ind in order_centroids[i, :8]]
        formatted_terms = [t.upper() if len(t) <= 3 or t in ['ux', 'ui', 'aws', 'gcp', 'ats', 'hr'] else t.title() for t in top_terms]
        cluster_themes[i] = {
            "keywords": formatted_terms,
            "display_name": f"Cluster {i+1}: " + ", ".join(formatted_terms[:4])
        }
        
    df['cluster_display_name'] = df['cluster'].map(lambda c: cluster_themes[c]['display_name'])
    
    return df, cluster_themes

def get_similar_jobs_in_cluster(job_id, clustered_df, top_n=3):
    """Given a job ID, returns other jobs in the same cluster."""
    job_row = clustered_df[clustered_df['job_id'] == job_id]
    if job_row.empty:
        return pd.DataFrame()
        
    cluster_id = job_row['cluster'].values[0]
    similar_jobs = clustered_df[(clustered_df['cluster'] == cluster_id) & (clustered_df['job_id'] != job_id)]
    return similar_jobs.head(top_n)

if __name__ == "__main__":
    df, themes = cluster_jobs_pipeline()
    print("Clusters and Top Keywords:")
    for cluster_id, info in themes.items():
        print(f"Cluster {cluster_id}: {info['display_name']}")
