import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# خطوة 1: قراءة الملفات النصية وجمع محتوياتها
def load_text_files(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                
                texts.append(file.read())
    return texts

# خطوة 2: تقسيم النصوص إلى أجزاء صغيرة
def split_text_into_chunks(texts, chunk_size=700, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = []
    for text in texts:
        chunks.extend(text_splitter.split_text(text))
    return chunks

# خطوة 3: توليد تضمينات النصوص باستخدام نموذج Hugging Face
def generate_embeddings(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# خطوة 4: حفظ قاعدة بيانات FAISS
def save_faiss_index(vectorstore, index_path="faiss_index"):
    vectorstore.save_local(index_path)

# خطوة 5: تحميل قاعدة بيانات FAISS عند الحاجة
def load_faiss_index(index_path="faiss_index"):
    vectorstore = FAISS.load_local(index_path, embeddings=HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large"), allow_dangerous_deserialization=True)
    return vectorstore

# تنفيذ الخطوات
folder_path = "/kaggle/input/rules-data/arabic_rules"
texts = load_text_files(folder_path)
text_chunks = split_text_into_chunks(texts)
vectorstore = generate_embeddings(text_chunks)
save_faiss_index(vectorstore)
