# KVAC Paris Visa Assistant (KVAC 비자 어시스턴트)

A multilingual (French · English · Korean) AI-powered assistant for helping with KVAC visa document questions.  
This project demonstrates **production-ready MLOps practices** including Docker multi-stage, environment variables, and RAG (Retrieval-Augmented Generation) with Streamlit.

KVAC 파리 비자 관련 문서 질문을 지원하는 **다국어(French · English · 한국어) AI 어시스턴트**입니다.  
이 프로젝트는 **프로덕션 수준 MLOps**를 보여주며, Docker multi-stage, 환경 변수(.env), RAG(Retrieval-Augmented Generation), Streamlit 기반 UI를 포함합니다.

---

## 🛠 Tech Stack / 기술 스택

- **Python 3.12**
- **Streamlit**: Web UI
- **LangChain**: RAG pipeline
- **Chroma**: Vector database
- **UpstageEmbeddings / ChatGroq**: LLM embeddings & inference
- **Docker multi-stage**: Production-ready containerization
- **dotenv**: Environment variable management

---

## ⚡ Features / 기능

- PDF document loading & indexing
- Multilingual question answering (FR / EN / KO)
- Dockerized for production-ready deployment
- Environment variables management (.env)
- Lightweight runtime using Docker multi-stage

---

## 📂 Project Structure / 프로젝트 구조

agent-visa/
├── src/ # Application source code / 애플리케이션 소스
│ └── main.py
├── pdfs/ # PDF documents for RAG / RAG용 PDF 문서
├── chroma_db/ # Vector database (auto-generated) / 벡터 DB (자동 생성)
├── pyproject.toml # Python project configuration / Python 프로젝트 설정
├── uv.lock # UV dependencies lock / UV 의존성 잠금 파일
├── .venv/ # Virtual environment (optional for Docker) / 가상환경
├── start.sh # Launch script / 실행 스크립트
└── README.md


## 🚀 Quick Start / 실행 방법

### 1️⃣ Clone the repository / 레포지토리 클론
```bash
git clone https://github.com/Sylvainpons/MLOps-Projects.git
cd agent-visa
2️⃣ Prepare your environment / 환경 설정
Create a .env file with your API keys:

GROQ_API_KEY=your_groq_key
UPSTAGE_API_KEY=your_upstage_key
3️⃣ Build Docker image / Docker 이미지 빌드
bash
Copier le code
docker build -t agent-visa:multi-stage .
4️⃣ Run container / 컨테이너 실행
bash
Copier le code
docker run -p 8501:8501 --env-file .env agent-visa:multi-stage
5️⃣ Access the app / 앱 접속
Open your browser: http://<IP>:8501/

브라우저에서 열기: http://<IP>:8501/

⚙️ Notes / 참고 사항
The PDF database (chroma_db) is auto-generated at first run.

.env should never be pushed to GitHub for security.

Streamlit UI supports French, English, and Korean.

PDF DB(chroma_db)는 첫 실행 시 자동 생성됩니다.

.env 파일은 절대 GitHub에 업로드하지 마세요.

Streamlit UI는 프랑스어, 영어, 한국어를 지원합니다.

📈 Why this project is interesting / 프로젝트 가치
Demonstrates a production-ready RAG application

Shows expertise in Docker multi-stage, environment management, and Python MLOps

Portable and lightweight — can be deployed on VMs, laptops, or cloud

Excellent portfolio piece for Korean tech recruiters

프로덕션 수준 RAG 앱 구현 사례

Docker multi-stage, 환경 관리, Python MLOps 능력 증명

VM, 로컬, 클라우드 어디든 배포 가능

한국 IT 기업 채용 시 포트폴리오용 최적 프로젝트


