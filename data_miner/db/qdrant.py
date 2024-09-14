from dataclasses import dataclass 
import uuid

from qdrant_client.models import Distance, VectorParams
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

@dataclass
class QdrantConfig:
    
    collection_name: str = "top_skills"
    vector_size: int = 384
    distance_measure: Distance = Distance.COSINE
    
    host_url: str = "http://localhost:6333"
    
    
@dataclass
class TopSkillsPayload:
    
    job_id: str
    skill: str
    rank: int
    
    
class VectorDB:
    def __init__(self, config: QdrantConfig):
        self.config = config
        self.client = QdrantClient(url=self.config.host_url)
        
        if not self.client.collection_exists(collection_name=self.config.collection_name):
            self._create_collection()
    
    
    def _create_collection(self):
        self.client.create_collection(
            collection_name=self.config.collection_name,
            vectors_config=VectorParams(size=self.config.vector_size, 
                                        distance=self.config.distance_measure),
        )
        
        
    def insert_vectors(self, vectors: list[dict]) -> dict:
        """
        
        :param vectors: list[dict]. Each dict should have the following keys - 
            "vector": np.array (of shape (self.config.vector_size,)),
            "payload": TopSkillsPayload
            
        :return: dict. The operation info
        """
        
        points = [PointStruct(id=uuid.uuid4().__str__(), 
                              vector=point['vector'], 
                              payload=point['payload']) 
                  for point in vectors]
        
        operation_info = self.client.upsert(
            collection_name=self.config.collection_name,
            wait=True,
            points=points,
        )
        
        return operation_info.__dict__
    
    