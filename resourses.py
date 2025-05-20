import os  
from dotenv import load_dotenv
load_dotenv()
    
import huggingface_hub
huggingface_hub.login(token=os.environ["HUGGINGFACE_TOKEN"])


def get_llm():
    from llama_index.llms.google_genai import GoogleGenAI
    try:
        gemini_llm = GoogleGenAI(model="gemini-2.0-flash")
        # Thử gọi một request nhỏ để kiểm tra rate limit
        gemini_llm.complete("test")
        return gemini_llm
    except Exception as e:
        print(f"Falling back to Ollama due to: {str(e)}")
        from llama_index.llms.ollama import Ollama
        return Ollama(model="qwen2.5:0.5b", request_timeout=120.0)
    

def get_embed_model(model_path="khanglt0004/ltk_embedding"):
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    return HuggingFaceEmbedding(
        model_name=model_path
    )
    
    
def get_index(local = True, _embed_model = None):
    import os
    from llama_index.core.indices.vector_store.base import VectorStoreIndex
    from llama_index.vector_stores.qdrant import QdrantVectorStore
    import qdrant_client
    qdrant_collection_name = "local_law_documents" if local else "law_db"
    _embed_model = _embed_model if _embed_model else get_embed_model(model_path="bkai-foundation-models/vietnamese-bi-encoder")
    loaded_index = VectorStoreIndex.from_vector_store(
        QdrantVectorStore(
            client=qdrant_client.QdrantClient(
                "https://08838c4e-e0ad-488e-a2a9-b217fa55c19a.us-east-1-0.aws.cloud.qdrant.io",
                api_key=os.environ["QDRANT_API_KEY"],
            ) if not local else qdrant_client.QdrantClient(
                "http://localhost:6333",
            ),
            collection_name=qdrant_collection_name,
            enable_hybrid=True,
            fastembed_sparse_model="Qdrant/bm25",
            batch_size=20,
        ),
        embed_model=_embed_model,
    )
    return loaded_index
    
def get_query_engine(loaded_index=None,llm=None,top_k_sparse=10,top_k_similarity=2):
    
    from llama_index.core.prompts import RichPromptTemplate
    from llama_index.core.postprocessor import SimilarityPostprocessor
    
    loaded_index = loaded_index if loaded_index else get_index(local=True)
    llm = llm if llm else get_llm()
    # Postprocessor: Cutoff node if similarity is under threshold
    sim_postprocessor = SimilarityPostprocessor(similarity_cutoff=0.4)
    qa_prompt_tmpl_str = (
        "Bạn là trợ lý tư vấn pháp luật cho nhiệm vụ hỏi đáp với người dùng.\n"
        "Sử dụng các phần sau của bối cảnh được truy xuất để trả lời câu hỏi.\n"
        "Nếu bạn không biết câu trả lời, đừng cố tạo câu trả lời..\n"
        "Ngữ cảnh cung cấp:\n"
        "---------------------\n"
        "{{ context_str }}\n"
        "Hãy trả lời câu hỏi sau với phong cách của một luật sư.\n"
        "Người dùng hỏi: {{ query_str }}\n"
        "Trả lời: "
    )
    qa_prompt_tmpl = RichPromptTemplate(qa_prompt_tmpl_str)
    
    query_engine = loaded_index.as_query_engine(
        text_qa_template=qa_prompt_tmpl,
        llm=llm,
        similarity_top_k=top_k_similarity,
        sparse_top_k=top_k_sparse,
        vector_store_query_mode="hybrid",
        node_postprocessors=[sim_postprocessor],
    )
    return query_engine

def get_chat_engine(query_engine=None,llm=None):
    from llama_index.core.chat_engine import CondenseQuestionChatEngine
    from llama_index.core import PromptTemplate
    from llama_index.core.llms import ChatMessage, MessageRole
    llm = llm if llm else get_llm()
    loaded_index = get_index(local=True)
    query_engine = query_engine if query_engine else get_query_engine(loaded_index,llm)
    
    custom_prompt ="""\
    Cho đoạn hội thoại(Giữa người dùng và trợ lý) và một câu hỏi tiếp theo từ người dùng, \
    vui lòng viết lại câu hỏi để nó trở thành một câu hỏi độc lập, \
    có thể hiểu được toàn bộ ngữ cảnh đoạn hội thoại. \

    <Đoạn hội thoại>
    {chat_history}

    <Câu hỏi tiếp theo>
    {question}

    <Câu hỏi độc lập>
    """
    
    custom_chat_history = [
        ChatMessage(
            role=MessageRole.USER,
            content="Chào bạn, tôi cần sự giúp đỡ của bạn về một vấn đề pháp lý, lĩnh vực hôn nhân gia đình.",
        ),
        ChatMessage(
            role=MessageRole.ASSISTANT, content="Được thôi! Tôi có thể giúp gì cho bạn?"
        ),
    ]
    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=query_engine,
        condense_question_prompt= PromptTemplate(custom_prompt),
        chat_history=custom_chat_history,
        verbose=True,
        llm=llm,
    )
    return chat_engine
