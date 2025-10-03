# WorldFlow

AI 기반 PDF 문서 번역 플랫폼 (한글 ↔ 영어)

## 🎯 프로젝트 개요

해외 강의 및 학술 활동을 준비하는 한국 교육자를 위한 고품질 문서 번역 서비스입니다.

### 주요 기능
- **🚀 Quick Mode**: 3단계로 빠른 번역 (3-5분)
- **👨‍🏫 Pro Mode**: 전문가용 고품질 번역 + 편집
- **📊 레이아웃 보존**: 표, 차트, 이미지 위치 유지
- **✏️ 편집 가능**: Markdown 기반 실시간 편집
- **🔧 용어집**: 전문용어 일관성 유지

## 🛠️ 기술 스택

### Backend
- FastAPI (Python 3.11+)
- PostgreSQL 15+
- Redis 7+
- Celery (백그라운드 작업)
- PyMuPDF, pdfplumber (PDF 파싱)
- OpenAI GPT-4 / Anthropic Claude (AI 번역)

### Frontend
- React 18 + TypeScript
- Vite
- TailwindCSS
- React Query
- Zustand (상태 관리)

### 인프라
- Docker + Docker Compose
- Railway (배포 + Persistent Volume)
- Stripe (결제 - Phase 2)

## 🚀 빠른 시작

### 사전 요구사항
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL 15+ (or Docker)
- Redis 7+ (or Docker)

### 1. 저장소 클론
\`\`\`bash
git clone <repository-url>
cd worldflow
\`\`\`

### 2. 환경 변수 설정
\`\`\`bash
cp .env.example .env
# .env 파일 편집 (API 키, DB 설정 등)
\`\`\`

### 3. Docker로 실행 (권장)
\`\`\`bash
docker-compose up -d
\`\`\`

서비스 접속:
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Frontend: http://localhost:5173

### 4. 로컬 개발 환경

#### Backend
\`\`\`bash
cd backend

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
python main.py
# or
uvicorn main:app --reload
\`\`\`

#### Frontend
\`\`\`bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
\`\`\`

## 📁 프로젝트 구조

\`\`\`
worldflow/
├── backend/                 # FastAPI 백엔드
│   ├── api/                # API 라우터
│   ├── services/           # 비즈니스 로직
│   │   └── pdf/           # PDF 파싱/변환
│   ├── models/             # 데이터베이스 모델
│   ├── core/               # 설정, DB, 보안
│   ├── tasks/              # Celery 작업
│   ├── tests/              # 테스트
│   ├── main.py             # 메인 앱
│   └── requirements.txt
│
├── frontend/                # React 프론트엔드
│   ├── src/
│   │   ├── components/    # React 컴포넌트
│   │   ├── services/      # API 클라이언트
│   │   ├── hooks/         # Custom hooks
│   │   ├── store/         # 상태 관리
│   │   └── utils/         # 유틸리티
│   └── package.json
│
├── storage/                 # 파일 저장소
│   ├── uploads/            # 업로드된 PDF
│   └── temp/               # 임시 파일
│
├── docs/                    # 문서
│   ├── PRD.md              # 제품 요구사항
│   ├── BENCHMARKING.md     # 경쟁사 분석
│   ├── UI_UX_DESIGN.md     # UI/UX 설계
│   └── UI_DUAL_MODE_STRATEGY.md  # 듀얼 모드 전략
│
├── docker-compose.yml
├── .env.example
└── README.md
\`\`\`

## 🧪 테스트

\`\`\`bash
# Backend 테스트
cd backend
pytest

# Frontend 테스트
cd frontend
npm run test
\`\`\`

## 📚 API 문서

서버 실행 후 http://localhost:8000/api/docs 에서 확인

## 🚂 Railway 배포

\`\`\`bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 생성 및 배포
railway init
railway up
\`\`\`

환경변수는 Railway Dashboard에서 설정:
- DATABASE_URL (자동 생성)
- REDIS_URL (자동 생성)
- SECRET_KEY
- OPENAI_API_KEY
- 기타 .env.example 참고

## 📊 개발 진행 상황

**MVP 핵심 기능: 85% 완료**

- [x] 프로젝트 기획 (PRD, 벤치마킹, UI/UX 설계)
- [x] 개발 환경 설정 (Docker, Railway)
- [x] 데이터베이스 설계 (PostgreSQL + SQLAlchemy)
- [x] 사용자 인증 시스템 (JWT)
- [x] PDF 파싱 엔진 (멀티 파서: pdfplumber → PyMuPDF → PyPDF2)
- [x] AI 번역 엔진 (OpenAI GPT-4 / Anthropic Claude)
- [x] Markdown 편집 인터페이스 (Monaco Editor, Split View)
- [x] PDF 생성 엔진 (WeasyPrint)
- [x] 프로젝트 대시보드 (업로드, 목록, 상태 추적)
- [ ] 테스트 & 최적화
- [ ] Railway 배포
- [ ] 결제 시스템 (Phase 2)

**전체 워크플로우:**
1. PDF 업로드 → 2. 파싱 (PDF → Markdown) → 3. AI 번역 → 4. 편집 → 5. PDF 생성 & 다운로드

상세 진행 상황: [docs/TASKS.md](./docs/TASKS.md)

## 🤝 기여

1. Fork the repository
2. Create your feature branch (\`git checkout -b feature/amazing-feature\`)
3. Commit your changes (\`git commit -m 'Add amazing feature'\`)
4. Push to the branch (\`git push origin feature/amazing-feature\`)
5. Open a Pull Request

## 📝 라이선스

This project is licensed under the MIT License.

## 📞 문의

- 이메일: contact@worldflow.ai
- 이슈: GitHub Issues

---

**Made with ❤️ by Kelly**
