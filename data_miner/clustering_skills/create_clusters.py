from dataclasses import dataclass
from typing import List 
from pathlib import Path 
import numpy as np
import json
import os
from tqdm import tqdm
from datetime import datetime

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from wordcloud import WordCloud, STOPWORDS

from data_miner.db.base_table import DB_Creds
from data_miner.db.clusters import SkillsClustersTable
from data_miner.llm.name_skills_cluster import SkillGroupTagger
from data_miner.db.skills_cluster_tag import SkillsClusterTagTable


@dataclass
class ClusterConfig:
    
    # db config
    db_creds: DB_Creds
    
    # cluster config
    num_of_dimensions: int = 25     # after PCA
    num_of_clusters: int = 88
    
    # pre_generated_txt_embeddings
    embeddings_path: str = Path('../mount/top_skills_embeddings/embeddings.npy')
    embeddings_metadata: str = Path('../mount/top_skills_embeddings/metadata.json')
    
    # top skills wordcloud
    wordcloud_save_dir: str = Path('../mount/top_skills_wordclouds')
    wordcloud_threshold: int = 0.4
    
    # skill group tagger
    skill_group_tagger_config: str = Path('../llm_configs/skill_cluster_namer.json')
    
    # run save dir
    run_save_dir: str = Path('../mount/skill_clustering_run_details')
    
    
    def __post_init__(self):
        self.wordcloud_save_dir.mkdir(parents=True, exist_ok=True)
        self.run_save_dir.mkdir(parents=True, exist_ok=True)
    
    
    
class ClusterSkills:
    def __init__(self, config: ClusterConfig):
        self.config = config
        self.db_creds = config.db_creds
        self._load_data()
        self.kmeans = KMeans(n_clusters=self.config.num_of_clusters)
        self.pca = PCA(n_components=self.config.num_of_dimensions)
        self.clustering_score = None
        self.skill_group_tagger = SkillGroupTagger(self.config.skill_group_tagger_config)
        self.cluster_table = SkillsClustersTable(self.db_creds)
        self.individual_skills_table = SkillsClusterTagTable(self.db_creds)
    
    
    def _load_data(self):
        self.X = np.load(self.config.embeddings_path)
        with open(self.config.embeddings_metadata, 'r') as f:
            metadatas = json.load(f)
        self.metadata = {v['array_index']: v for v in metadatas}
        self.clusters = {}
        
    
    def _get_silhoutte_score(self, X_pca):
        return silhouette_score(X_pca, self.kmeans.labels_, metric='cosine')
    
    
    def decompose_n_cluster(self):
        X_pca = self.pca.fit_transform(self.X)
        self.kmeans.fit(X_pca)
        self.clustering_score = self._get_silhoutte_score(X_pca)
        
        # get clusters and their tags
        for i, l in enumerate(self.kmeans.labels_):
            self.metadata[i]['cluster'] = int(l)
            if int(l) not in self.clusters:
                self.clusters[int(l)] = {'data':[self.metadata[i]]}
            else:
                self.clusters[int(l)]['data'].append(self.metadata[i])
                
    
    def get_top_skills_using_wordcloud(self):
        for cluster_id, cluster_data in self.clusters.items():
            skills = ' '.join([d['skill'] for d in cluster_data['data']])
            wordcloud = WordCloud(width = 800, height = 800, 
                                  background_color ='white', 
                                  stopwords = set(STOPWORDS), 
                                  min_font_size = 10).generate(skills)
            wordcloud.to_file(self.config.wordcloud_save_dir / f"cluster_{cluster_id}.png")
            top_tags = [k for k, v in wordcloud.words_.items() if v > self.config.wordcloud_threshold]
            self.clusters[cluster_id]['top_tags'] = top_tags
            
            
    def tag_clusters(self):
        for cluster_id, cluster_data in tqdm(desc="Tagging Clusters", iterable=self.clusters.items()):
            self.clusters[cluster_id]['tag'] = self.skill_group_tagger.tag(cluster_data['top_tags'])
            
    
    def save_to_db(self):
        self.cluster_table.delete_all_data()
        for cluster_id, cluster_data in tqdm(desc="Saving to db", iterable=self.clusters.items()):
            self.cluster_table.insert_data({
                "cluster_id": cluster_id,
                "cluster_tags": json.dumps(cluster_data['top_tags']),
                "cluster_head_tag": cluster_data['tag']
            })
        
        self.individual_skills_table.delete_all_data()
        for cluster_id, cluster_data in tqdm(desc="Saving to db", iterable=self.clusters.items()):
            for data in cluster_data['data']:
                self.individual_skills_table.insert_data({
                    "cluster_id": cluster_id,
                    "job_id": data['job_id'],
                    "skill": data['skill'],
                    "skill_rank": data['skill_rank']
                })
    
    
    def save_run_details(self):
        sv_path = os.path.join(self.config.run_save_dir, Path(f'run_details.json'))
        with open(sv_path, 'w') as f:
            json.dump({
                'clustering_score': float(self.clustering_score),
                'clusters': self.clusters
            }, f, indent=4)
    
    
    def run(self):
        print(f" ||>> Running clustering with {self.config.num_of_clusters} clusters ...")
        self.decompose_n_cluster()
        print(f" ||>> Clustering score: {self.clustering_score}")
        self.get_top_skills_using_wordcloud()
        print(f" ||>> Tagging clusters ...")
        self.tag_clusters()
        print(f" ||>> Saving to db ...")
        self.save_run_details()
        self.save_to_db()
        