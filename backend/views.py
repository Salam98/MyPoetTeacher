from flask import Blueprint, jsonify,request,json
from ibm_token import get_valid_access_token  # استيراد دالة التوكن
import requests
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


def load_faiss_index(index_path="faiss_index"):
    vectorstore = FAISS.load_local(index_path, embeddings=HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large"), allow_dangerous_deserialization=True)
    return vectorstore

def query_faiss_index(vectorstore, query_text): 
    results = vectorstore.similarity_search(query_text, k=1)
    return [result.page_content for result in results]

# إنشاء Blueprint لإدارة المسارات (اختياري لتنظيم الكود)
bp = Blueprint('main', __name__)

@bp.route('/api/generate', methods=['POST'])
def generate_response():
    # return {"response":"تجربة ارسال جواب على السؤال \nالمرسل من قبل العميل"}

    vectorstore = load_faiss_index("./faiss_index")

    req_data = request.get_json()
    question = req_data['ques']

    grounding =""
    related_texts = query_faiss_index(vectorstore, question)
    for text in related_texts:
        grounding += "" + text
    access_token = get_valid_access_token()
    if not access_token:
        return jsonify({"error": "Failed to get access token"}), 500

    credentials = Credentials( 
         url = "https://eu-de.ml.cloud.ibm.com",
		token = access_token
          )
    parameters = {
    "decoding_method": "sample",
    "max_new_tokens": 900,
    "temperature": 0.75,
    "top_k": 50,
    "top_p": 0.8,
    "repetition_penalty": 1.5
}
    allam_model = ModelInference(
        model_id = "sdaia/allam-1-13b-instruct",
        params = parameters,
        credentials = credentials,
        project_id = "ccd9f45b-2901-4a13-903a-e17a7289d9c8"
        )
    prompt = f""" <s> [INST]

<<SYS>>
Your Goal:[اكتب من بيتين إلى خمسة أبيات من الشعر لتبسيط إجابة السؤال المطروح بشكل صحيح والتزم بنفس القافية في كل الأبيات، ووزن البسيط في كل الأبيات]

Response Example:[
Query: ماهي الأسماء الخمسة؟
Answer: 
أبوك وأخوك ثم حموك ذا مالٍ ... وفوك وذو مالٍ في العُربِ قد سالِ\n
تُرفعُ بالواو في نُطقِها عِزُّها ... وتنصبُ بالألفِ في جُمَلِ الأمثالِ\n
\n
]

Grammers information:[ {grounding} ]


Guidelines:[
استخرج الإجابة الصحيحة للسؤال من معلومات القواعد المقدمة.\
استخدم اسلوب البساطة في الإجابة و كلمات سهلة لكتابة أبيات الشعر.\
تأكد من صحة الإجابة.\
اكتب إجابة السؤال كأبيات شعرية موزونة.\
التزم بقافية موحدة لجميع الأبيات.\
التزم بوزن موحد عند كتابة الأبيات الشعرية.
]

[اكتب من بيتين إلى خمسة أبيات من الشعر للإجابة على السؤال بإسلوب بسيط و إجابة صحيحة. التزم بنفس القافية في كل الأبيات، ووزن البسيط في كل الأبيات.]

<</SYS>>

{question} [/INST]

Answer: 


"""
    
    generated_response = allam_model.generate_text(prompt=prompt, guardrails=False)



    return {"response":generated_response}
  
