from pathlib import Path
import os
import time
import pandas as pd
import requests
import re
from tqdm.auto import tqdm
from langchain_core.documents import Document

def fetch_movie_data(base_url, data_folder_path, pages=50):
  if os.path.exists(data_folder_path):
      return pd.read_parquet(data_folder_path)
    
  discover_endpoint = "discover/movie"

  headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjMDEyZDNlOGFiZWZhYTU3M2U1YjhkZGQ3MWFhYmU1MiIsIm5iZiI6MTc3MzE3MjQ4NS43MDg5OTk5LCJzdWIiOiI2OWIwNzcwNTJiNmFmZjZkMzcxMWVhYjIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.yQJPjdE-OtV-anwg9AhGGBhR6605TmhCe_AJLeL-QWI"
  }

  data = []

  # Get the Ids of popular movies
  for page in tqdm(range(1, pages+1), desc="Fetching movie IDs"):

    movie_params = {
        "vote_count.gte":1000,
        "page":page,
        "sort_by":"popularity.desc"
    }

    response = requests.get(base_url+discover_endpoint, headers=headers, params=movie_params).json()
    data.extend([{"id":movie["id"]} for movie in response['results']])

  print(f"Fetched the Ids of {len(data)} movies")

  # Get details of each movie
  for movie in tqdm(data, desc="Fetching movie details"):
    details_endpoint = f"movie/{movie['id']}"

    try:
      response = requests.get(base_url+details_endpoint, headers=headers).json()

    except Exception as e:
      print(f"Error fetching the movie details :{e}, ID : {movie['id']}")
      continue

    movie['genres'] = ",".join([genre["name"] for genre in response['genres']])
    movie['Duration'] = response['runtime']
    movie['Year_of_release'] = response["release_date"].split('-')[0]
    movie['Title'] = response['title']
    movie['Rating'] = response['vote_average']
    movie['Plot'] = response['overview']

    # Get cast and crew details
    credits_endpoint = f"movie/{movie['id']}/credits"

    try:
      response = requests.get(base_url+credits_endpoint, headers=headers).json()

    except Exception as e:
      print(f"Error fetching the movie details :{e}, ID : {movie['id']}")
      continue

    # Actors'/Acresses' names
    members = [member['name'] for member in response['cast'] if member["known_for_department"]=="Acting"]
    movie['Cast'] = ",".join(set(members[:5]))

    # Directors' names
    directors = {member['name'] for member in response['crew'] if member["known_for_department"]=="Directing"}
    movie['Directors'] = ",".join(directors)

    time.sleep(0.1)
	
  
  df = pd.DataFrame(data)
  # Create the directory if doesn't exist
  Path(data_folder_path).parent.mkdir(parents=True, exist_ok=True)
  df.to_parquet(data_folder_path)
    
  return df
 
def preprocess_data(df, data_folder_path):
  if os.path.exists(data_folder_path):
      return pd.read_parquet(data_folder_path)
      
  # Drop duplicate rows and reset row indices.
  df = df.drop_duplicates()
  df = df.reset_index(drop=True)

  # Combine the text info for embedding generation.
  df['combined_text_info'] = "genres:" + df['genres'] + ", title:" + df['Title'] + ", plot:" + df['Plot'] + ", cast:" + df['Cast'] + ", directors:" + df['Directors']
  df['combined_text_info'] = df['combined_text_info'].apply(lambda x : re.sub(r'\s+'," ", x)) # Remove extra white spaces

  # Normalize the case in all the text fields.
  text_fields = df.select_dtypes(exclude='number').columns
  df.loc[:, text_fields] = df[text_fields].apply(lambda x : x.str.lower())

  # Create the directory if it doesn't already exist.
  Path(data_folder_path).parent.mkdir(parents=True, exist_ok=True)    
  df.to_parquet(data_folder_path)
  return df


def create_docs(df):
    docs = []

    # Iterate through the rows and create one document per row.
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Creating Documents"):
        doc = Document(
            page_content=row['combined_text_info'],
            metadata={
                'genres':row['genres'].split(','),
                'Duration':row['Duration'],
                'Year_of_release':row['Year_of_release'],
                'Title':row['Title'],
                'Rating':row['Rating'],
                'Cast':row['Cast'].split(','),
                'Directors':row['Directors'].split(',')
            }
        )

        docs.append(doc)

    return docs
