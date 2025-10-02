# Task 1.1: 프로젝트 환경 설정

**담당자**: 개발팀
**예상 소요 시간**: 4시간
**우선순위**: 🔴 High
**상태**: 📅 예정

---

## 📋 목표

개발 환경을 구축하고 Docker, Git, CI/CD 파이프라인을 설정합니다.

---

## ✅ 체크리스트

### 1. Git 저장소 설정
- [ ] GitHub 저장소 생성
  - 저장소명: `all-rounder-translation`
  - Private 저장소로 설정
- [ ] README.md 작성
  - 프로젝트 소개
  - 기술 스택
  - 로컬 실행 방법
- [ ] .gitignore 설정
  ```
  # Python
  __pycache__/
  *.py[cod]
  venv/
  .env

  # Node
  node_modules/
  dist/
  .env.local

  # Logs
  logs/
  *.log

  # IDE
  .vscode/
  .idea/

  # OS
  .DS_Store
  ```
- [ ] Git 브랜치 전략 설정
  - `main` 브랜치 보호 설정
  - `develop` 브랜치 생성

### 2. 백엔드 환경 설정
- [ ] Python 가상환경 생성
  ```bash
  python3.11 -m venv venv
  source venv/bin/activate
  ```
- [ ] requirements.txt 작성
  ```txt
  fastapi==0.104.1
  uvicorn[standard]==0.24.0
  sqlalchemy==2.0.23
  asyncpg==0.29.0
  alembic==1.12.1
  python-jose[cryptography]==3.3.0
  passlib[bcrypt]==1.7.4
  python-multipart==0.0.6
  pydantic==2.5.0
  pydantic-settings==2.1.0
  python-dotenv==1.0.0
  redis==5.0.1
  celery==5.3.4
  boto3==1.29.7
  PyMuPDF==1.23.8
  weasyprint==60.1
  openai==1.3.7
  anthropic==0.7.7
  pytest==7.4.3
  pytest-asyncio==0.21.1
  httpx==0.25.2
  ```
- [ ] .env.example 파일 작성
  ```bash
  # Database
  DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/translation_db

  # JWT
  SECRET_KEY=your-secret-key-change-in-production
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=60

  # Redis
  REDIS_URL=redis://localhost:6379/0

  # AWS S3
  AWS_ACCESS_KEY_ID=your-access-key
  AWS_SECRET_ACCESS_KEY=your-secret-key
  AWS_REGION=ap-northeast-2
  S3_BUCKET_NAME=translation-files

  # AI APIs
  OPENAI_API_KEY=sk-...
  ANTHROPIC_API_KEY=sk-ant-...

  # Stripe
  STRIPE_SECRET_KEY=sk_test_...
  STRIPE_PUBLISHABLE_KEY=pk_test_...

  # Email
  SENDGRID_API_KEY=SG...
  FROM_EMAIL=noreply@example.com

  # App
  DEBUG=true
  LOG_LEVEL=INFO
  ```
- [ ] 프로젝트 디렉토리 구조 생성
  ```bash
  mkdir -p backend/{api,services,models,core,tasks,tests}
  touch backend/__init__.py
  touch backend/main.py
  ```

### 3. 프론트엔드 환경 설정
- [ ] React + TypeScript 프로젝트 생성
  ```bash
  npm create vite@latest frontend -- --template react-ts
  cd frontend
  ```
- [ ] 주요 패키지 설치
  ```bash
  npm install
  npm install @tanstack/react-query
  npm install zustand
  npm install react-router-dom
  npm install axios
  npm install @monaco-editor/react
  npm install tailwindcss postcss autoprefixer
  npm install -D @types/react @types/react-dom
  ```
- [ ] TailwindCSS 설정
  ```bash
  npx tailwindcss init -p
  ```
- [ ] 프로젝트 디렉토리 구조 생성
  ```bash
  mkdir -p src/{components,services,hooks,store,types,utils}
  ```

### 4. Docker 환경 설정
- [ ] Dockerfile (백엔드) 작성
  ```dockerfile
  FROM python:3.11-slim

  WORKDIR /app

  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt

  COPY . .

  CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
- [ ] Dockerfile (프론트엔드) 작성
  ```dockerfile
  FROM node:18-alpine

  WORKDIR /app

  COPY package*.json ./
  RUN npm install

  COPY . .

  CMD ["npm", "run", "dev", "--", "--host"]
  ```
- [ ] docker-compose.yml 작성
  ```yaml
  version: '3.8'

  services:
    db:
      image: postgres:15
      environment:
        POSTGRES_DB: translation_db
        POSTGRES_USER: user
        POSTGRES_PASSWORD: password
      ports:
        - "5432:5432"
      volumes:
        - postgres_data:/var/lib/postgresql/data

    redis:
      image: redis:7
      ports:
        - "6379:6379"

    backend:
      build: ./backend
      ports:
        - "8000:8000"
      environment:
        - DATABASE_URL=postgresql+asyncpg://user:password@db:5432/translation_db
        - REDIS_URL=redis://redis:6379/0
      depends_on:
        - db
        - redis
      volumes:
        - ./backend:/app

    frontend:
      build: ./frontend
      ports:
        - "5173:5173"
      volumes:
        - ./frontend:/app
        - /app/node_modules

  volumes:
    postgres_data:
  ```

### 5. GitHub Actions CI/CD 설정
- [ ] .github/workflows/ci.yml 작성
  ```yaml
  name: CI

  on:
    push:
      branches: [ main, develop ]
    pull_request:
      branches: [ main, develop ]

  jobs:
    backend-test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Set up Python
          uses: actions/setup-python@v4
          with:
            python-version: '3.11'
        - name: Install dependencies
          run: |
            cd backend
            pip install -r requirements.txt
        - name: Run tests
          run: |
            cd backend
            pytest

    frontend-test:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - name: Set up Node
          uses: actions/setup-node@v3
          with:
            node-version: '18'
        - name: Install dependencies
          run: |
            cd frontend
            npm install
        - name: Run tests
          run: |
            cd frontend
            npm run test
  ```

### 6. 개발 도구 설정
- [ ] VSCode 설정 (.vscode/settings.json)
  ```json
  {
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true
    }
  }
  ```
- [ ] .editorconfig 설정
  ```ini
  root = true

  [*]
  charset = utf-8
  end_of_line = lf
  insert_final_newline = true
  trim_trailing_whitespace = true

  [*.py]
  indent_style = space
  indent_size = 4

  [*.{js,ts,tsx,json}]
  indent_style = space
  indent_size = 2
  ```

---

## 🧪 검증 방법

### 1. Git 저장소 확인
```bash
git remote -v
git branch -a
```

### 2. 백엔드 실행 테스트
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# http://localhost:8000/docs 접속 확인
```

### 3. 프론트엔드 실행 테스트
```bash
cd frontend
npm install
npm run dev
# http://localhost:5173 접속 확인
```

### 4. Docker 실행 테스트
```bash
docker-compose up -d
docker-compose ps
# 모든 서비스가 Up 상태인지 확인
```

---

## 📝 완료 조건

- [ ] GitHub 저장소가 정상적으로 생성됨
- [ ] 백엔드가 http://localhost:8000 에서 실행됨
- [ ] 프론트엔드가 http://localhost:5173 에서 실행됨
- [ ] Docker Compose로 모든 서비스가 실행됨
- [ ] GitHub Actions CI가 정상 작동함

---

## 🚨 주의사항

- **절대 .env 파일을 Git에 커밋하지 말 것**
- AWS, OpenAI, Stripe 키는 테스트용만 사용
- Docker 볼륨은 개발 중 데이터 보존 확인

---

## 📚 참고 자료

- [FastAPI 프로젝트 구조](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [Vite React TypeScript](https://vitejs.dev/guide/)
- [Docker Compose 가이드](https://docs.docker.com/compose/)

---

**작성일**: 2025-10-02
**최종 수정**: 2025-10-02
