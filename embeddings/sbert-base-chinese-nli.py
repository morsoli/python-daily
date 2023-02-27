import torch
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from pymilvus import connections, utility, CollectionSchema, FieldSchema, DataType, Collection

MILVUS_HOST = "localhost"
MILVUS_PORT = 19530
MILVUS_DIM = 768

def encode(df):
    model = SentenceTransformer('uer/sbert-base-chinese-nli')
    sentences = df['sentence'].tolist()
    sentence_embeddings = model.encode(sentences)
    save_data(sentence_embeddings)
    return sentence_embeddings

def create_collection(collection_name):
    if not utility.has_collection(collection_name):
        text_id = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True)
        embedding = FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=MILVUS_DIM)
        text = FieldSchema(name='text', dtype=DataType.VARCHAR, max_length=500, is_primary=False, auto_id=False)
        schema = CollectionSchema(fields=[text_id, embedding, text], description="text similar search")
        collection = Collection(name=collection_name, schema=schema, using='default', \
            shards_num=2,consistency_level="Strong"
        )
    else:
        collection = Collection(collection_name)
    return collection

def insert_record(collection, entities):
    collection.insert(entities)


def create_index(collection):
    index = {
        "index_type": "IVF_FLAT",
        "metric_type": "L2",
        "params": {"nlist": 128},
        }
    collection.create_index("embedding", index)
    collection.load()

def search_text(collection, text):
    query_vector = encode([text])
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 16},
    }
    results = collection.search(
        data=query_vector,
        anns_field="embedding",
        param=search_params, 
        limit = 10
    )
    return results

def save_data(vectors):
    save_file = "data.npy"
    np.save(save_file, vectors)

def load_data(save_file):
    sentence_embeddings = np.load("data.npy")
    return sentence_embeddings

if __name__ == "__main__":
    # 创建集合
    collection_name = "test3"
    connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
    collection = create_collection(collection_name)

    # 插入向量数据
    df = pd.read_csv("output.csv", sep="#",header=None, names=["sentence"])
    vectors = encode(df)
    insert_record(collection, [np.arange(0, len(df['sentence'].tolist())), vectors, df['sentence'].tolist()])
    create_index(collection)

    # 查询数据
    text_example = '程序员'
    results = search_text(collection, text_example)
    print(results)

    # 关闭连接
    connections.remove_connection("default")
    
