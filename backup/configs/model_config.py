import os

model_root_path = ''
model_path = {
    'embed_model' : {
        'text-embedding-3-small' : os.getenv('API_KEY')
    },
    'llm_model' : {
        'GPT-3.5-turbo': os.getenv('API_KEY')
    }
}

embedding_model = 'text-embedding-3-small'
embedding_device = 'auto'

llm_model = 'GPT-3.5-turbo'
llm_device = 'auto'

len_history = 8
temperature = 0.5

langchain_llm_model = {
    'OpenAI' : {
        'model_name' : 'GPT-3.5-turbo',
        'api_base_url': 'https://api.openai.com/v1',
        'api_key' : os.getenv('API_KEY'),
        'openai_proxy': ''
    }
}

nltk_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")
