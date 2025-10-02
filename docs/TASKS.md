# All-Rounder Translation - 개발 태스크 관리

**프로젝트**: 한글→영어 PDF 문서 번역 플랫폼
**개발 기간**: 3개월 (MVP)
**시작일**: 2025-10-02

---

## 📊 전체 진행 현황

### Phase 1: MVP 개발 (12주)
- **Week 1-2**: 기반 구축 ✅
- **Week 3-4**: PDF 파싱 엔진 ✅
- **Week 5-6**: AI 번역 엔진 ✅
- **Week 7-8**: 편집 및 PDF 생성 📅
- **Week 9-10**: 결제 시스템 📅
- **Week 11-12**: 테스트 및 출시 📅

### Phase 2: 확장 기능 (3개월)
- OCR 지원, 용어집, 배치 처리 📅

---

## 🎯 Phase 1: MVP 개발 (12주)

### Week 1-2: 기반 구축 ✅
**목표**: 개발 환경 설정 및 인증 시스템 구현

#### ✅ 완료된 작업
- [x] 프로젝트 기획 (PRD, 벤치마킹)
- [x] 개발 가이드 작성 (claude.md)
- [x] **Task 1.1**: 프로젝트 환경 설정
  - Git 초기화, 프로젝트 구조 생성
  - Docker & docker-compose 설정
  - requirements.txt, package.json
  - Railway 배포 설정
- [x] **Task 1.2**: 데이터베이스 설계 및 구축
  - PostgreSQL + SQLAlchemy 설정
  - User, Project, Glossary, UsageLog, Payment 모델
  - Alembic 마이그레이션 설정
- [x] **Task 1.3**: 사용자 인증 시스템
  - JWT 기반 인증 (bcrypt 암호화)
  - 회원가입, 로그인, 토큰 갱신 API
  - 인증 의존성 (get_current_user)
- [x] **Task 1.4**: 프론트엔드 기본 레이아웃
  - React 18 + TypeScript + Vite
  - TailwindCSS 설정
  - Header, Footer, Layout 컴포넌트
  - 랜딩 페이지 (Home.tsx)

---

### Week 3-4: PDF 파싱 엔진 ✅
**목표**: PDF를 Markdown으로 변환하는 파싱 엔진 개발

#### ✅ 완료된 작업
- [x] **Task 2.1**: PDF 파싱 엔진 개발
  - ODIN-AI 검증된 멀티 파서 전략
  - pdfplumber → PyMuPDF → PyPDF2 자동 폴백
  - 텍스트, 테이블, 메타데이터 추출
  - Markdown 변환 (테이블 포함)
- [x] **Task 2.2**: 파일 저장소 연동
  - Railway Persistent Volume 사용
  - 로컬: ./storage/, Railway: /data/
  - 자동 환경 감지 (RAILWAY_ENVIRONMENT)
- [x] **Task 2.3**: 파일 업로드 API
  - POST /api/projects/upload
  - 파일 검증 (PDF, 크기, 페이지 제한)
  - 프로젝트 CRUD API (목록, 상세, 수정, 삭제)

#### 📅 예정된 작업
- [ ] **Task 2.4**: 대시보드 UI 개발 (프론트엔드)

---

### Week 5-6: AI 번역 엔진 ✅
**목표**: GPT-4/Claude를 활용한 AI 번역 시스템 구축

#### ✅ 완료된 작업
- [x] **Task 3.1**: AI 번역 API 통합
  - OpenAI GPT-4 & Anthropic Claude 지원
  - translate_text() - 단일 텍스트 번역
  - translate_markdown() - 청크 기반 문서 번역
  - 문맥 보존, 용어집 지원
- [x] **Task 3.2**: 백그라운드 작업 (FastAPI BackgroundTasks)
  - 비동기 번역 처리
  - 상태 업데이트 (translating → completed/failed)
  - TODO: Celery로 마이그레이션 예정
- [x] **Task 3.3**: 번역 진행 상태 추적
  - POST /api/translation/projects/{id}/translate
  - GET /api/translation/projects/{id}/status
  - 진행률 추적 (0% → 100%)

#### 📅 예정된 작업
- [ ] **Task 3.4**: 번역 UI 개발 (프론트엔드)

---

### Week 7-8: 편집 및 PDF 생성
**목표**: Markdown 편집기 및 PDF 재생성 시스템

#### 📅 예정된 작업
- [ ] **Task 4.1**: Markdown 편집기 개발 → [TASK_4_1.md](./tasks/TASK_4_1.md)
- [ ] **Task 4.2**: PDF 생성 엔진 → [TASK_4_2.md](./tasks/TASK_4_2.md)
- [ ] **Task 4.3**: 편집 UI (Split View) → [TASK_4_3.md](./tasks/TASK_4_3.md)
- [ ] **Task 4.4**: PDF 다운로드 기능 → [TASK_4_4.md](./tasks/TASK_4_4.md)

---

### Week 9-10: 결제 시스템
**목표**: Stripe 결제 연동 및 사용량 관리

#### 📅 예정된 작업
- [ ] **Task 5.1**: Stripe 결제 연동 → [TASK_5_1.md](./tasks/TASK_5_1.md)
- [ ] **Task 5.2**: 구독 플랜 관리 → [TASK_5_2.md](./tasks/TASK_5_2.md)
- [ ] **Task 5.3**: 사용량 추적 시스템 → [TASK_5_3.md](./tasks/TASK_5_3.md)
- [ ] **Task 5.4**: 이메일 발송 시스템 → [TASK_5_4.md](./tasks/TASK_5_4.md)

---

### Week 11-12: 테스트 및 출시
**목표**: 베타 테스트, 버그 수정, 공식 출시

#### 📅 예정된 작업
- [ ] **Task 6.1**: E2E 테스트 작성 → [TASK_6_1.md](./tasks/TASK_6_1.md)
- [ ] **Task 6.2**: 베타 테스트 진행 → [TASK_6_2.md](./tasks/TASK_6_2.md)
- [ ] **Task 6.3**: 성능 최적화 → [TASK_6_3.md](./tasks/TASK_6_3.md)
- [ ] **Task 6.4**: 랜딩 페이지 완성 → [TASK_6_4.md](./tasks/TASK_6_4.md)
- [ ] **Task 6.5**: 배포 및 출시 → [TASK_6_5.md](./tasks/TASK_6_5.md)

---

## 🎯 Phase 2: 확장 기능 (3개월)

### Month 4: OCR 및 용어집
#### 📅 예정된 작업
- [ ] **Task 7.1**: OCR 엔진 통합 (Tesseract)
- [ ] **Task 7.2**: 용어집 관리 시스템
- [ ] **Task 7.3**: 용어집 CSV 가져오기/내보내기
- [ ] **Task 7.4**: 번역 시 용어집 자동 적용

### Month 5: 배치 처리 및 번역 메모리
#### 📅 예정된 작업
- [ ] **Task 8.1**: 배치 번역 시스템
- [ ] **Task 8.2**: 번역 메모리 (TM)
- [ ] **Task 8.3**: 이미지 내 텍스트 번역
- [ ] **Task 8.4**: 버전 히스토리 확장

### Month 6: 다국어 및 Enterprise 기능
#### 📅 예정된 작업
- [ ] **Task 9.1**: 다국어 지원 (중국어, 일본어)
- [ ] **Task 9.2**: 팀 관리 기능 (Enterprise)
- [ ] **Task 9.3**: 용어집 공유 기능
- [ ] **Task 9.4**: API 액세스 제공

---

## 📝 태스크 작업 규칙

### 1. 태스크 시작 전
```markdown
- [ ] 관련 문서 읽기 (PRD, claude.md)
- [ ] Git 브랜치 생성 (feature/태스크명)
- [ ] 영향 범위 분석
- [ ] 롤백 계획 수립
```

### 2. 태스크 진행 중
```markdown
- [ ] 독립 파일로 개발 (기존 파일 수정 최소화)
- [ ] 단위 테스트 작성
- [ ] 코드 리뷰 요청
- [ ] 문서 업데이트
```

### 3. 태스크 완료 시
```markdown
- [ ] 기존 기능 회귀 테스트
- [ ] Pull Request 생성
- [ ] 리뷰 완료 후 병합
- [ ] 체크박스 체크 (✅)
```

---

## 🚨 긴급 이슈 트래커

### 현재 이슈
_현재 긴급 이슈 없음_

### 해결된 이슈
_없음_

---

## 📊 주간 진행 리포트

### Week 0 (2025-10-02)
**완료된 작업**:
- [x] PRD 작성
- [x] 벤치마킹 분석
- [x] 개발 가이드 작성 (claude.md, REUSABLE_PATTERNS.md)
- [x] 태스크 관리 문서 생성
- [x] **Week 1-2 완료**: 기반 구축
  - 프로젝트 환경 설정 (Docker, Railway)
  - 데이터베이스 모델 (PostgreSQL + SQLAlchemy)
  - 사용자 인증 시스템 (JWT)
  - 프론트엔드 레이아웃 (React + TailwindCSS)
- [x] **Week 3-4 완료**: PDF 파싱 엔진
  - 멀티 파서 전략 (pdfplumber/PyMuPDF/PyPDF2)
  - Railway 볼륨 스토리지
  - 파일 업로드 & 프로젝트 API
- [x] **Week 5-6 완료**: AI 번역 엔진
  - OpenAI/Anthropic 번역 서비스
  - 백그라운드 작업 처리
  - 번역 상태 추적 API

**다음 계획**:
- [ ] Week 7-8: Markdown 편집기 및 PDF 생성

---

## 📞 도움이 필요한 경우

### 기술 문제
- **백엔드**: FastAPI, PostgreSQL, Celery 관련
- **프론트엔드**: React, TypeScript, React Query 관련
- **인프라**: Docker, AWS, CI/CD 관련

### 비즈니스 문제
- **기획**: 기능 우선순위, UX 개선
- **마케팅**: 타겟 고객, 가격 전략

---

**문서 최종 수정**: 2025-10-02
**다음 업데이트**: 매주 월요일
