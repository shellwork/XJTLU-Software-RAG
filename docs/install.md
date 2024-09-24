# Set up and Installation

#### 1. Clone the repository:
```bash
git clone https://github.com/XJTLU-Software-iGEM/2024-project.git
cd 2024-project
```
<br/>

#### 2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
<br/>

#### 3. Set up environment variables in the `config.py` file:
```python
DATA_PATH = "data/uploads"
CHROMA_PATH = "chroma"
```
<br/>

#### 4. Run the backend API:
```bash
uvicorn server.api:app --reload
```
<br/>

#### 5. Run the frontend (Streamlit):
```bash
streamlit run frontend_streamlit/knowledge_base.py
```
