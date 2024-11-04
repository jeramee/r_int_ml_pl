# mongo_integration.py

from pymongo import MongoClient
from project_config import BASE_URL
from mongo_setup import connect_mongo, get_collections

# Connect to MongoDB and get collections
db = connect_mongo()
collections = get_collections(db)

# Access specific collections
deseq2_results_collection = collections["deseq2_results"]
samples_collection = collections["samples"]
projects_collection = collections.get("projects")  # Optional

# Insert DESeq2 results into MongoDB
def insert_deseq2_results(results, sample_id):
    """
    Inserts DESeq2 analysis results into the 'deseq2_results' collection.
    
    Parameters:
    - results (list of dict): List of DESeq2 result dictionaries, each representing a gene's results.
    - sample_id (str): Identifier for the sample, added to each result entry.
    """
    for result in results:
        result["sample_id"] = sample_id
    deseq2_results_collection.insert_many(results)
    print(f"Inserted {len(results)} DESeq2 results into 'deseq2_results' collection.")

# Insert sample metadata into MongoDB
def insert_sample_metadata(sample_metadata):
    """
    Inserts metadata for a sample into the 'samples' collection.
    
    Parameters:
    - sample_metadata (dict): Metadata dictionary containing details about the sample.
    """
    samples_collection.insert_one(sample_metadata)
    print(f"Inserted sample metadata for {sample_metadata['sample_id']} into 'samples' collection.")

# Insert project metadata (optional)
def insert_project_metadata(project_metadata):
    """
    Inserts metadata for a project into the 'projects' collection.
    
    Parameters:
    - project_metadata (dict): Metadata dictionary containing details about the project.
    """
    if projects_collection:
        projects_collection.insert_one(project_metadata)
        print(f"Inserted project metadata for {project_metadata['project_id']} into 'projects' collection.")
    else:
        print("Projects collection is not defined.")

# Retrieve DESeq2 results from MongoDB
def get_deseq2_results(sample_id):
    """
    Retrieves DESeq2 results from the 'deseq2_results' collection for a given sample_id.
    
    Parameters:
    - sample_id (str): Identifier for the sample whose DESeq2 results are to be retrieved.
    
    Returns:
    - list of dict: List of dictionaries containing DESeq2 results for the sample.
    """
    results = list(deseq2_results_collection.find({"sample_id": sample_id}))
    print(f"Retrieved {len(results)} DESeq2 results for sample {sample_id}.")
    return results

# Retrieve all samples
def get_all_samples():
    """
    Retrieves all sample metadata from the 'samples' collection.
    
    Returns:
    - list of dict: List of dictionaries containing metadata for each sample.
    """
    samples = list(samples_collection.find({}))
    print(f"Retrieved {len(samples)} samples.")
    return samples

# Retrieve all projects (optional)
def get_all_projects():
    """
    Retrieves all project metadata from the 'projects' collection, if available.
    
    Returns:
    - list of dict: List of dictionaries containing metadata for each project.
    """
    if projects_collection:
        projects = list(projects_collection.find({}))
        print(f"Retrieved {len(projects)} projects.")
        return projects
    else:
        print("Projects collection is not defined.")
        return []
