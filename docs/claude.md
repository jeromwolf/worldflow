# All-Rounder Translation - Claude 개발 가이드

**프로젝트**: 한글→영어 PDF 문서 번역 플랫폼
**개발 방법론**: 모듈형 개발 + 안전한 배포 전략
**작성일**: 2025-10-02

---

## 🎯 핵심 개발 원칙

### 1. 모듈형 개발 (한 번에 하나씩)
- **새 기능은 항상 새 파일로 생성**
- 기존 파일(main.py, core.ts, App.tsx) 직접 수정 금지
- 각 단계마다 기존 기능 테스트 필수

### 2. 안전한 개발 전략
```bash
# 작업 전 체크리스트
□ Git 브랜치 생성 (feature/기능명)
□ 현재 작동 기능 목록 작성
□ 영향 범위 분석
□ 롤백 계획 수립
□ 독립 모듈로 개발
```

### 3. 절대 금지 사항
```bash
❌ 공통 파일 직접 수정 (main.py, App.tsx)
❌ 여러 기능 동시 작업
❌ import 경로 일괄 변경
❌ 테스트 없이 커밋
❌ 큰 단위 변경
❌ 개인정보 로그 출력
```

---

## 📁 프로젝트 구조

### 백엔드 (FastAPI)
```
backend/
├── api/
│   ├── auth.py              # 인증 API (독립)
│   ├── projects.py          # 프로젝트 API (독립)
│   ├── translation.py       # 번역 API (독립)
│   └── glossaries.py        # 용어집 API (독립, Phase 2)
│
├── services/
│   ├── pdf_parser.py        # PDF → Markdown 변환
│   ├── translator.py        # AI 번역 엔진
│   ├── pdf_generator.py     # Markdown → PDF
│   └── storage.py           # S3 파일 저장
│
├── models/
│   ├── user.py              # 사용자 모델
│   ├── project.py           # 프로젝트 모델
│   └── glossary.py          # 용어집 모델 (Phase 2)
│
├── core/
│   ├── database.py          # DB 연결 관리
│   ├── security.py          # JWT, 비밀번호 해싱
│   └── config.py            # 환경변수 설정
│
├── tasks/
│   └── celery_worker.py     # 백그라운드 작업
│
├── main.py                  # 🔒 최소 수정만
└── requirements.txt
```

### 프론트엔드 (React + TypeScript)
```
frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── dashboard/
│   │   │   ├── ProjectList.tsx
│   │   │   └── UsageStats.tsx
│   │   ├── editor/
│   │   │   ├── MarkdownEditor.tsx
│   │   │   ├── SplitView.tsx
│   │   │   └── PDFPreview.tsx
│   │   └── common/
│   │       ├── Header.tsx
│   │       └── ProgressBar.tsx
│   │
│   ├── services/
│   │   ├── authService.ts       # 인증 서비스 (독립)
│   │   ├── projectService.ts    # 프로젝트 서비스 (독립)
│   │   ├── translationService.ts # 번역 서비스 (독립)
│   │   └── apiClient.ts         # 공통 API 클라이언트
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useProject.ts
│   │   └── useTranslation.ts
│   │
│   ├── store/                   # Zustand 상태 관리
│   │   ├── authStore.ts
│   │   └── projectStore.ts
│   │
│   ├── App.tsx                  # 🔒 최소 수정만
│   └── main.tsx
│
└── package.json
```

---

## 🏗️ 기술 스택

### 백엔드
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+ (SQLAlchemy ORM)
- **Cache/Queue**: Redis 7+ (Celery)
- **Storage**: AWS S3 or Google Cloud Storage
- **PDF 처리**: PyMuPDF (파싱), WeasyPrint (생성)
- **AI**: OpenAI GPT-4 API or Anthropic Claude API

### 프론트엔드
- **Framework**: React 18 + TypeScript
- **State**: Zustand or Redux Toolkit
- **UI**: TailwindCSS + shadcn/ui
- **Editor**: Monaco Editor (Markdown)
- **Data Fetching**: React Query
- **Build**: Vite

### 인프라
- **Container**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Datadog or Prometheus
- **Payment**: Stripe

---

## 🔄 개발 워크플로우

### Phase 1: 계획 (30분)
```markdown
- [ ] 기능 요구사항 문서화
- [ ] 영향 범위 분석
- [ ] 데이터베이스 스키마 변경 필요 여부 확인
- [ ] API 엔드포인트 설계
- [ ] 컴포넌트 구조 설계
```

### Phase 2: 백엔드 구현 (2-4시간)
```markdown
- [ ] 새 API 파일 생성 (api/new_feature.py)
- [ ] 서비스 로직 구현 (services/new_service.py)
- [ ] 데이터베이스 모델 추가/수정
- [ ] 유닛 테스트 작성
- [ ] API 문서 업데이트 (Swagger)
```

### Phase 3: 프론트엔드 구현 (2-4시간)
```markdown
- [ ] 서비스 파일 생성 (services/newService.ts)
- [ ] 컴포넌트 생성 (components/NewFeature.tsx)
- [ ] React Query 훅 설정
- [ ] 라우팅 추가 (App.tsx 최소 수정)
- [ ] UI/UX 테스트
```

### Phase 4: 통합 테스트 (1-2시간)
```markdown
- [ ] E2E 테스트 실행
- [ ] 기존 기능 회귀 테스트
- [ ] 성능 테스트
- [ ] 에러 핸들링 검증
```

### Phase 5: 배포 (30분)
```markdown
- [ ] 환경변수 확인
- [ ] 마이그레이션 스크립트 준비
- [ ] 롤백 계획 수립
- [ ] 문서 업데이트
```

---

## 🔐 보안 및 개인정보 보호

### 1. 로그 관리
```python
# ❌ 절대 금지
logger.info(f"사용자 로그인: {user.email}")
logger.debug(f"비밀번호: {password}")

# ✅ 안전한 로깅
import hashlib

def safe_user_id(user_id: str) -> str:
    return hashlib.sha256(str(user_id).encode()).hexdigest()[:8]

logger.info(f"로그인 성공 (user_hash: {safe_user_id(user.id)})")
```

### 2. 비밀번호 관리
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### 3. JWT 인증
```python
from datetime import datetime, timedelta
from jose import jwt

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

### 4. XSS 방어
```python
import html
from pydantic import BaseModel, validator

class SafeInput(BaseModel):
    content: str

    @validator('content')
    def sanitize(cls, v):
        return html.escape(v.strip())
```

### 5. 환경변수 관리
```bash
# .env (절대 Git 커밋 금지)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_test_...

# .gitignore
.env
.env.local
.env.production
logs/
*.log
```

---

## 📊 API 패턴

### FastAPI 라우터 구조
```python
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from .models import Project, ProjectCreate
from .dependencies import get_current_user

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("/", response_model=Project)
async def create_project(
    file: UploadFile,
    user = Depends(get_current_user)
):
    """프로젝트 생성 (PDF 업로드)"""
    # 파일 검증
    if not file.filename.endswith('.pdf'):
        raise HTTPException(400, "PDF 파일만 지원합니다")

    # S3 업로드
    file_url = await storage.upload(file)

    # 프로젝트 생성
    project = await ProjectService.create(user.id, file_url)

    # 백그라운드 작업 시작
    celery.send_task('parse_pdf', args=[project.id])

    return project
```

### React Query 패턴
```typescript
// hooks/useProject.ts
import { useQuery, useMutation } from '@tanstack/react-query';
import { projectService } from '@/services/projectService';

export const useProjects = () => {
  return useQuery({
    queryKey: ['projects'],
    queryFn: () => projectService.getAll(),
    staleTime: 10000, // 10초 캐시
  });
};

export const useCreateProject = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (file: File) => projectService.create(file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['projects'] });
    },
  });
};
```

---

## 🧪 테스트 전략

### 백엔드 테스트
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_project(async_client: AsyncClient):
    """프로젝트 생성 테스트"""
    files = {'file': ('test.pdf', open('test.pdf', 'rb'), 'application/pdf')}

    response = await async_client.post(
        "/api/projects",
        files=files,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data['status'] == 'uploading'
```

### 프론트엔드 테스트
```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import { ProjectUpload } from '@/components/ProjectUpload';

test('파일 업로드 버튼 클릭', () => {
  render(<ProjectUpload />);

  const uploadButton = screen.getByText('PDF 업로드');
  fireEvent.click(uploadButton);

  expect(screen.getByText('파일을 선택하세요')).toBeInTheDocument();
});
```

---

## 📈 성능 최적화

### 1. 데이터베이스 인덱스
```python
class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID, primary_key=True)
    user_id = Column(UUID, index=True)  # 인덱스
    created_at = Column(DateTime, index=True)  # 인덱스
    status = Column(String, index=True)  # 인덱스
```

### 2. Eager Loading (N+1 방지)
```python
from sqlalchemy.orm import selectinload

stmt = select(User).options(
    selectinload(User.projects),  # 관계 데이터 미리 로드
)
```

### 3. Redis 캐싱
```python
from aiocache import cached

@cached(ttl=300)  # 5분 캐시
async def get_popular_projects():
    return await db.query(Project).order_by(views.desc()).limit(10)
```

---

## 🚨 에러 핸들링

### 백엔드
```python
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code

@app.exception_handler(AppException)
async def app_exception_handler(request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )
```

### 프론트엔드
```typescript
const { mutate, isError, error } = useMutation({
  mutationFn: createProject,
  onError: (error) => {
    toast.error(`번역 실패: ${error.message}`);
  },
});
```

---

## 🔄 배치 처리 (Celery)

### 작업 정의
```python
# tasks/celery_worker.py
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def parse_pdf(project_id: str):
    """PDF 파싱 백그라운드 작업"""
    project = db.get(Project, project_id)

    # 1. PDF 다운로드
    pdf_file = storage.download(project.original_file_url)

    # 2. Markdown 변환
    markdown = PDFParser.parse(pdf_file)

    # 3. DB 저장
    project.markdown_original = markdown
    project.status = "parsed"
    db.commit()

    # 4. 번역 작업 시작
    celery.send_task('translate_markdown', args=[project_id])
```

---

## 📝 Git 브랜치 전략

```bash
main           # 프로덕션 배포
  └── develop  # 개발 통합 브랜치
        ├── feature/auth         # 인증 기능
        ├── feature/pdf-parser   # PDF 파싱
        ├── feature/translator   # 번역 엔진
        └── feature/editor       # 편집기
```

### 브랜치 작업 플로우
```bash
# 1. 새 기능 브랜치 생성
git checkout develop
git pull origin develop
git checkout -b feature/기능명

# 2. 개발 및 커밋
git add .
git commit -m "feat: 기능 설명"

# 3. 원격 푸시
git push origin feature/기능명

# 4. Pull Request 생성 (GitHub)
# 리뷰 완료 후 develop에 병합

# 5. 배포 준비 시 main으로 병합
git checkout main
git merge develop
git push origin main
```

---

## 🎯 MVP 개발 체크리스트

### Week 1-2: 기반 구축
- [ ] Docker 환경 설정
- [ ] PostgreSQL + Redis 설정
- [ ] FastAPI 프로젝트 구조 생성
- [ ] React + TypeScript 프로젝트 생성
- [ ] 사용자 인증 (회원가입, 로그인, JWT)
- [ ] 대시보드 기본 레이아웃

### Week 3-4: PDF 파싱
- [ ] PyMuPDF 통합
- [ ] PDF → Markdown 변환 로직
- [ ] 레이아웃 정보 추출 (좌표, 폰트)
- [ ] S3 파일 업로드
- [ ] 파일 업로드 UI

### Week 5-6: AI 번역
- [ ] OpenAI/Claude API 통합
- [ ] 청크 단위 번역 로직
- [ ] 문맥 유지 프롬프트 최적화
- [ ] Celery 작업 큐 설정
- [ ] 번역 진행 상태 표시 (WebSocket or Polling)

### Week 7-8: 편집 및 PDF 생성
- [ ] Monaco Editor 통합
- [ ] Split View (원본/번역본)
- [ ] 자동 저장 기능
- [ ] WeasyPrint 통합
- [ ] Markdown → PDF 변환
- [ ] 레이아웃 재현 로직

### Week 9-10: 결제 및 사용량
- [ ] Stripe 연동
- [ ] 구독 플랜 설정
- [ ] 사용량 추적 시스템
- [ ] 이메일 발송 (SendGrid)

### Week 11-12: 테스트 및 출시
- [ ] 베타 테스트 (50명)
- [ ] 버그 수정
- [ ] 성능 최적화
- [ ] 랜딩 페이지 완성
- [ ] **공식 출시**

---

## 🚀 빠른 시작

### 백엔드 실행
```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일 편집 (DB, API 키 등)

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn main:app --reload
```

### 프론트엔드 실행
```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

### Docker로 실행
```bash
# 모든 서비스 시작 (DB, Redis, API, Frontend)
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down
```

---

## 📞 트러블슈팅

### 문제: PDF 파싱 실패
```bash
# PyMuPDF 재설치
pip uninstall PyMuPDF
pip install PyMuPDF==1.23.0

# PDF 파일 검증
python -c "import fitz; doc=fitz.open('test.pdf'); print(doc.page_count)"
```

### 문제: AI 번역 API 오류
```bash
# API 키 확인
echo $OPENAI_API_KEY

# 테스트 요청
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### 문제: 프론트엔드 빌드 실패
```bash
# 캐시 삭제
rm -rf node_modules package-lock.json
npm install

# TypeScript 타입 체크
npm run type-check
```

---

## 📚 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [React Query 공식 문서](https://tanstack.com/query/latest)
- [PyMuPDF 문서](https://pymupdf.readthedocs.io/)
- [OpenAI API 문서](https://platform.openai.com/docs)
- [Stripe 결제 가이드](https://stripe.com/docs)

---

**작성자**: Kelly
**최종 수정**: 2025-10-02
**버전**: 1.0
