# Product Requirements Document (PRD)
# All-Rounder Translation Platform

**문서 버전**: 1.0
**작성일**: 2025-10-02
**작성자**: Kelly
**상태**: Draft
**검토 주기**: 2주

---

## 목차

1. [Executive Summary](#1-executive-summary)
2. [Product Overview](#2-product-overview)
3. [User Personas](#3-user-personas)
4. [Use Cases & User Scenarios](#4-use-cases--user-scenarios)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [User Stories & Acceptance Criteria](#7-user-stories--acceptance-criteria)
8. [Technical Specifications](#8-technical-specifications)
9. [UI/UX Requirements](#9-uiux-requirements)
10. [API Specifications](#10-api-specifications)
11. [Data Model](#11-data-model)
12. [Security & Privacy](#12-security--privacy)
13. [Success Metrics & KPIs](#13-success-metrics--kpis)
14. [Development Roadmap](#14-development-roadmap)
15. [Risk Assessment](#15-risk-assessment)
16. [Dependencies & Constraints](#16-dependencies--constraints)
17. [Appendix](#17-appendix)

---

## 1. Executive Summary

### 1.1 제품 비전

**All-Rounder Translation**은 해외 강의 및 학술 활동을 준비하는 한국 교육자를 위한 AI 기반 문서 번역 플랫폼입니다. PDF 형식의 강의 자료를 고품질로 번역하면서 원본 레이아웃과 디자인을 완벽하게 보존하여, 사용자가 즉시 사용 가능한 결과물을 제공합니다.

### 1.2 핵심 가치 제안

- **레이아웃 완벽 보존**: 차트, 표, 이미지 위치가 그대로 유지되는 PDF 번역
- **교육 콘텐츠 특화**: 학술/교육 용어에 최적화된 번역 품질
- **편집 가능한 워크플로우**: Markdown 기반 중간 편집으로 번역 정확도 향상
- **빠른 처리 속도**: 100페이지 문서를 10분 이내 처리
- **가격 경쟁력**: 기존 솔루션 대비 30~50% 저렴

### 1.3 타겟 시장

- **1차**: 해외 강의/학회 발표 준비 대학 교수 및 연구원
- **2차**: 국제 교육 프로그램 운영 기업 및 스타트업
- **3차**: 학술 논문 영문 전환이 필요한 연구자

### 1.4 비즈니스 목표

| 기간 | 목표 |
|------|------|
| **3개월** | MVP 출시, 베타 사용자 50명 확보 |
| **6개월** | 월 구독자 100명, 손익분기점 달성 |
| **1년** | 월 구독자 500명, 월 매출 4,000만원 |
| **2년** | 월 구독자 2,000명, B2B 계약 10건 |

---

## 2. Product Overview

### 2.1 제품 개요

All-Rounder Translation은 다음 3단계 파이프라인으로 작동합니다:

```
PDF 업로드 → Markdown 변환 → AI 번역 → 사용자 편집 → PDF 생성 → 다운로드
```

### 2.2 핵심 기능 (MVP)

1. **PDF 파싱 엔진**
   - PDF를 구조화된 Markdown으로 변환
   - 텍스트, 이미지, 표, 레이아웃 정보 추출
   - 메타데이터 보존 (폰트, 색상, 위치)

2. **AI 번역 엔진**
   - GPT-4 또는 Claude API 기반 한→영 번역
   - 문맥 인식형 번역 (문서 전체 이해)
   - 교육/학술 용어 최적화

3. **편집 인터페이스**
   - 웹 기반 Markdown 에디터
   - 원본/번역본 나란히 비교
   - 실시간 미리보기

4. **PDF 재생성 엔진**
   - Markdown → PDF 변환
   - 원본과 동일한 레이아웃 재현
   - 한글 폰트 → 영문 폰트 자동 매핑

### 2.3 Phase 2 확장 기능

- OCR 지원 (스캔본 PDF)
- 용어집(Glossary) 관리
- 번역 메모리 (Translation Memory)
- 이미지 내 텍스트 번역
- 다국어 지원 (중국어, 일본어)
- 배치 처리 (여러 파일 동시 번역)

### 2.4 Out of Scope (현재 버전)

- 실시간 협업 기능
- 비디오 자막 번역
- 음성 파일 번역
- PowerPoint/Keynote 직접 지원 (→ PDF 변환 후 처리)
- 모바일 앱

---

## 3. User Personas

### Persona 1: 김교수 (해외 학회 발표자)

**기본 정보**
- 나이: 45세
- 직업: 대학교 공학 교수
- 기술 숙련도: 중급
- 언어 능력: 영어 읽기/쓰기 가능, 스피킹 보통

**니즈 & 페인포인트**
- 한글로 작성한 50페이지 강의 자료를 영어로 변환 필요
- Google Translate로 번역하면 전문용어가 부정확함
- 레이아웃이 깨져서 다시 정리하는데 2~3일 소요
- 예산 제한으로 전문 번역 서비스 이용 어려움

**목표**
- 1시간 내 번역 완료
- 전문용어 정확도 95% 이상
- 레이아웃 수정 없이 바로 사용

**사용 시나리오**
1. 학회 발표 2주 전 PDF 업로드
2. 번역 결과 확인 후 전문용어 일부 수정
3. PDF 다운로드 후 발표 자료로 사용

---

### Persona 2: 이대리 (기업 교육팀)

**기본 정보**
- 나이: 32세
- 직업: 글로벌 제조업체 교육팀
- 기술 숙련도: 고급
- 언어 능력: 영어 비즈니스 수준

**니즈 & 페인포인트**
- 월 20~30개 교육 문서 번역 필요
- 여러 번역 도구 사용 중이나 일관성 부족
- 기술 매뉴얼의 복잡한 표와 다이어그램 번역 시 깨짐
- 번역 후 재편집에 시간 소요

**목표**
- 배치 처리로 효율성 향상
- 용어집으로 회사 전문용어 일관성 유지
- 월 구독으로 예산 예측 가능

**사용 시나리오**
1. 매월 초 20개 문서 업로드
2. 용어집 적용하여 일괄 번역
3. 팀원들과 결과물 공유

---

### Persona 3: 박연구원 (박사과정)

**기본 정보**
- 나이: 28세
- 직업: 대학원 박사과정
- 기술 숙련도: 고급
- 언어 능력: 영어 논문 작성 가능

**니즈 & 페인포인트**
- 학위 논문 일부를 영문으로 전환 필요
- DeepL 사용 중이나 학술 용어 오역 발생
- 수식과 그래프가 많은 문서 처리 어려움
- 학생 예산으로 저렴한 서비스 선호

**목표**
- 학술 용어 정확도 최우선
- 수식/그래프 완벽 보존
- 페이지당 과금으로 소량 사용

**사용 시나리오**
1. 논문 일부(10~20페이지) 업로드
2. 번역 결과 꼼꼼히 검토 및 수정
3. 지도교수 리뷰용으로 제출

---

## 4. Use Cases & User Scenarios

### UC-001: 기본 PDF 번역

**Actor**: 모든 사용자

**Pre-conditions**
- 사용자 로그인 완료
- 번역 가능한 크레딧/구독 보유
- PDF 파일 준비 (최대 200페이지, 50MB)

**Main Flow**
1. 사용자가 "새 번역" 버튼 클릭
2. PDF 파일 업로드 (드래그앤드롭 or 파일 선택)
3. 시스템이 파일 유효성 검사 (형식, 크기, 보안)
4. 언어 쌍 선택 (한→영 기본값)
5. "번역 시작" 버튼 클릭
6. 시스템이 PDF 파싱 시작 (진행률 표시)
7. 시스템이 AI 번역 수행 (진행률 표시)
8. 번역 완료 알림 및 편집 화면 표시

**Post-conditions**
- 번역 결과가 편집 가능한 상태로 저장됨
- 대시보드에 프로젝트 추가됨
- 크레딧 차감 또는 사용량 기록

**Alternative Flows**
- 3a. 파일이 암호화되어 있으면 오류 메시지 표시
- 3b. 파일 크기 초과 시 업그레이드 안내
- 7a. 번역 실패 시 재시도 또는 환불 옵션

---

### UC-002: 번역 결과 편집

**Actor**: 모든 사용자

**Pre-conditions**
- UC-001 완료
- 편집 화면 진입

**Main Flow**
1. 좌측에 원본 Markdown, 우측에 번역본 Markdown 표시
2. 사용자가 번역본 텍스트 수정
3. 실시간 미리보기에 변경사항 반영
4. "저장" 버튼 클릭
5. 시스템이 자동 저장 (클라우드 동기화)

**Post-conditions**
- 수정 내용이 서버에 저장됨
- 버전 히스토리에 기록됨

---

### UC-003: PDF 다운로드

**Actor**: 모든 사용자

**Pre-conditions**
- UC-002 완료 (편집 완료)

**Main Flow**
1. "PDF 생성" 버튼 클릭
2. 시스템이 Markdown → PDF 변환 (진행률 표시)
3. 미리보기 모달 표시
4. "다운로드" 버튼 클릭
5. 브라우저 다운로드 시작

**Post-conditions**
- PDF 파일이 로컬에 저장됨
- 다운로드 히스토리 기록

**Alternative Flows**
- 2a. 변환 실패 시 오류 로그 표시 및 고객 지원 연결

---

### UC-004: 용어집 관리 (Phase 2)

**Actor**: Pro/Enterprise 사용자

**Pre-conditions**
- Pro 이상 플랜 구독
- 대시보드 진입

**Main Flow**
1. "용어집" 메뉴 클릭
2. "새 용어 추가" 버튼 클릭
3. 원어(한글), 대상어(영어) 입력
4. 카테고리 선택 (예: 기술, 의학, 교육)
5. "저장" 버튼 클릭
6. 용어집 목록에 추가됨

**Post-conditions**
- 이후 번역 시 해당 용어 자동 적용
- 용어집 데이터베이스 업데이트

---

### UC-005: 배치 번역 (Phase 2)

**Actor**: Pro/Enterprise 사용자

**Pre-conditions**
- Pro 이상 플랜 구독
- 여러 PDF 파일 준비

**Main Flow**
1. "배치 번역" 메뉴 클릭
2. 여러 PDF 파일 업로드 (최대 20개)
3. 각 파일에 용어집 적용 여부 선택
4. "일괄 번역 시작" 버튼 클릭
5. 시스템이 순차적으로 처리 (대기열 표시)
6. 완료된 파일부터 개별 확인 가능

**Post-conditions**
- 모든 파일의 번역 결과가 대시보드에 표시됨
- 이메일로 완료 알림 발송

---

## 5. Functional Requirements

### 5.1 사용자 관리

| ID | 요구사항 | 우선순위 | 비고 |
|----|----------|----------|------|
| FR-001 | 이메일 기반 회원가입 지원 | Must | 이메일 인증 필수 |
| FR-002 | 소셜 로그인 지원 (Google, Naver, Kakao) | Should | OAuth 2.0 |
| FR-003 | 비밀번호 재설정 기능 | Must | 이메일 링크 방식 |
| FR-004 | 사용자 프로필 관리 (이름, 기관, 전공) | Could | 번역 품질 개선에 활용 |
| FR-005 | 구독 플랜 변경 (Basic ↔ Pro) | Must | Stripe 연동 |

### 5.2 파일 처리

| ID | 요구사항 | 우선순위 | 비고 |
|----|----------|----------|------|
| FR-101 | PDF 파일 업로드 (최대 50MB) | Must | 드래그앤드롭 지원 |
| FR-102 | 지원 페이지 수: 1~200페이지 | Must | 초과 시 Enterprise 안내 |
| FR-103 | 암호화된 PDF 거부 | Must | 명확한 오류 메시지 |
| FR-104 | 스캔본 PDF OCR 처리 | Should | Phase 2 |
| FR-105 | 파일 형식 검증 (PDF 1.4~2.0) | Must | |
| FR-106 | 업로드 진행률 표시 | Must | 실시간 진행바 |

### 5.3 번역 엔진

| ID | 요구사항 | 우선순위 | 비고 |
|----|----------|----------|------|
| FR-201 | 한국어 → 영어 번역 | Must | GPT-4 or Claude |
| FR-202 | 문서 전체 문맥 고려 | Must | 청크 단위 처리 + 문맥 유지 |
| FR-203 | 교육/학술 용어 최적화 | Must | 프롬프트 엔지니어링 |
| FR-204 | 표/차트 내 텍스트 번역 | Must | 구조 보존 |
| FR-205 | 이미지 캡션 번역 | Should | |
| FR-206 | 수식(LaTeX) 보존 | Must | 번역 제외 처리 |
| FR-207 | 번역 품질 평가 (1~5점) | Could | 사용자 피드백 수집 |

### 5.4 편집 기능

| ID | 요구사항 | 우선순위 | 비고 |
|----|----------|----------|------|
| FR-301 | Markdown 에디터 제공 | Must | Monaco Editor |
| FR-302 | 원본/번역본 나란히 보기 | Must | Split view |
| FR-303 | 실시간 미리보기 | Should | PDF 렌더링 |
| FR-304 | 자동 저장 (30초 간격) | Must | 클라우드 동기화 |
| FR-305 | 버전 히스토리 (최근 10개) | Should | |
| FR-306 | 찾기/바꾸기 기능 | Should | Ctrl+F |
| FR-307 | 번역 취소/다시 실행 (Undo/Redo) | Must | Ctrl+Z/Y |

### 5.5 PDF 생성

| ID | 요구사항 | 우선순위 | 비고 |
|----|----------|----------|------|
| FR-401 | Markdown → PDF 변환 | Must | WeasyPrint or Pandoc |
| FR-402 | 원본 레이아웃 재현율 95%+ | Must | 핵심 품질 지표 |
| FR-403 | 폰트 자동 매핑 (한글→영문) | Must | 나눔고딕→Arial 등 |
| FR-404 | 이미지 위치 보존 | Must | |
| FR-405 | 페이지 번호 유지 | Should | |
| FR-406 | 하이퍼링크 보존 | Should | |
| FR-407 | PDF 메타데이터 설정 | Could | 작성자, 제목 등 |

### 5.6 용어집 관리 (Phase 2)

| ID | 요구사항 | 우선순위 | 비고 |
|----|----------|----------|------|
| FR-501 | 용어 추가/수정/삭제 | Should | CRUD |
| FR-502 | CSV 파일로 용어집 가져오기/내보내기 | Should | |
| FR-503 | 용어 카테고리 분류 | Could | 기술, 의학, 교육 등 |
| FR-504 | 용어집 공유 (팀 내) | Could | Enterprise 플랜 |
| FR-505 | 용어 자동 하이라이트 | Should | 편집 화면에서 표시 |

### 5.7 대시보드

| ID | 요구사항 | 우선순위 | 비고 |
|----|----------|----------|------|
| FR-601 | 프로젝트 목록 표시 | Must | 최근 순 정렬 |
| FR-602 | 프로젝트 검색 (파일명, 날짜) | Should | |
| FR-603 | 프로젝트 삭제 | Must | 소프트 삭제 (30일 보관) |
| FR-604 | 사용량 통계 (페이지 수, 크레딧) | Must | |
| FR-605 | 다운로드 히스토리 | Could | |

### 5.8 결제 시스템

| ID | 요구사항 | 우선순위 | 비고 |
|----|----------|----------|------|
| FR-701 | 구독 플랜 선택 (Basic, Pro, Enterprise) | Must | Stripe 연동 |
| FR-702 | 신용카드 결제 | Must | |
| FR-703 | 정기 결제 자동 갱신 | Must | |
| FR-704 | 구독 취소 | Must | 즉시 취소 or 기간 만료 후 |
| FR-705 | 영수증 발급 | Must | PDF 다운로드 |
| FR-706 | 환불 처리 | Should | 7일 이내 환불 정책 |

---

## 6. Non-Functional Requirements

### 6.1 성능 (Performance)

| ID | 요구사항 | 측정 기준 | 우선순위 |
|----|----------|-----------|----------|
| NFR-001 | 페이지당 번역 속도 | 1페이지 ≤ 6초 (100페이지 ≤ 10분) | Must |
| NFR-002 | PDF 파싱 속도 | 100페이지 ≤ 2분 | Must |
| NFR-003 | PDF 생성 속도 | 100페이지 ≤ 3분 | Must |
| NFR-004 | 웹페이지 로딩 시간 | 초기 로딩 ≤ 3초 | Should |
| NFR-005 | API 응답 시간 | 평균 ≤ 200ms (P95 ≤ 500ms) | Should |
| NFR-006 | 동시 사용자 지원 | 100명 동시 번역 가능 | Must |

### 6.2 확장성 (Scalability)

| ID | 요구사항 | 측정 기준 | 우선순위 |
|----|----------|-----------|----------|
| NFR-101 | 수평 확장 가능 | 서버 추가로 처리량 증가 | Must |
| NFR-102 | 대기열 시스템 | 피크 타임 대응 (Redis Queue) | Must |
| NFR-103 | 파일 저장소 확장 | S3 or GCS 무제한 저장 | Must |
| NFR-104 | 데이터베이스 샤딩 | 1M+ 사용자 지원 준비 | Could |

### 6.3 가용성 (Availability)

| ID | 요구사항 | 측정 기준 | 우선순위 |
|----|----------|-----------|----------|
| NFR-201 | 서비스 가동률 (SLA) | 99.5% uptime (월 3.6시간 다운타임 허용) | Must |
| NFR-202 | 자동 장애 복구 | 서버 다운 시 30초 이내 전환 | Should |
| NFR-203 | 데이터 백업 | 일 1회 자동 백업 | Must |
| NFR-204 | 재해 복구 계획 (DR) | RPO 24시간, RTO 4시간 | Could |

### 6.4 보안 (Security)

| ID | 요구사항 | 측정 기준 | 우선순위 |
|----|----------|-----------|----------|
| NFR-301 | HTTPS 통신 | 모든 통신 TLS 1.3 | Must |
| NFR-302 | 데이터 암호화 | 저장 데이터 AES-256 암호화 | Must |
| NFR-303 | 비밀번호 저장 | bcrypt 해싱 (cost factor 12) | Must |
| NFR-304 | API 인증 | JWT 토큰 (만료 시간 1시간) | Must |
| NFR-305 | 파일 자동 삭제 | 번역 완료 후 30일 경과 시 삭제 | Should |
| NFR-306 | XSS/CSRF 방어 | 프레임워크 기본 보안 적용 | Must |
| NFR-307 | Rate Limiting | IP당 시간당 100 요청 | Should |

### 6.5 사용성 (Usability)

| ID | 요구사항 | 측정 기준 | 우선순위 |
|----|----------|-----------|----------|
| NFR-401 | 첫 번역 완료 시간 | 신규 사용자 20분 이내 | Must |
| NFR-402 | 모바일 반응형 | 태블릿 이상 지원 (스마트폰 제외) | Should |
| NFR-403 | 다국어 UI | 한국어, 영어 지원 | Could |
| NFR-404 | 접근성 (WCAG 2.1) | Level A 준수 | Could |
| NFR-405 | 브라우저 호환성 | Chrome, Safari, Firefox, Edge 최신 2버전 | Must |

### 6.6 유지보수성 (Maintainability)

| ID | 요구사항 | 측정 기준 | 우선순위 |
|----|----------|-----------|----------|
| NFR-501 | 코드 커버리지 | 유닛 테스트 80% 이상 | Should |
| NFR-502 | 로깅 시스템 | 모든 에러 및 주요 이벤트 로깅 | Must |
| NFR-503 | 모니터링 | APM 도구 연동 (Datadog/New Relic) | Should |
| NFR-504 | 문서화 | API 문서 자동 생성 (OpenAPI 3.0) | Must |

### 6.7 규정 준수 (Compliance)

| ID | 요구사항 | 측정 기준 | 우선순위 |
|----|----------|-----------|----------|
| NFR-601 | 개인정보 보호법 준수 | 개인정보 처리방침 게시 | Must |
| NFR-602 | GDPR 준수 (향후) | EU 사용자 대응 | Could |
| NFR-603 | 이용약관 동의 | 회원가입 시 필수 동의 | Must |

---

## 7. User Stories & Acceptance Criteria

### Epic 1: 사용자 온보딩

#### US-001: 회원가입
**As a** 신규 사용자
**I want to** 이메일로 회원가입하고
**So that** 번역 서비스를 이용할 수 있다

**Acceptance Criteria**
- [ ] 이메일, 비밀번호, 이름 입력 필드 존재
- [ ] 비밀번호는 8자 이상, 영문+숫자 조합 필수
- [ ] 이메일 중복 검사 수행
- [ ] 가입 후 인증 이메일 자동 발송
- [ ] 이메일 링크 클릭 시 계정 활성화
- [ ] 이용약관 및 개인정보 처리방침 동의 체크박스

**Story Points**: 5

---

#### US-002: 소셜 로그인
**As a** 신규 사용자
**I want to** Google 계정으로 간편 로그인하고
**So that** 빠르게 서비스를 시작할 수 있다

**Acceptance Criteria**
- [ ] Google OAuth 2.0 버튼 표시
- [ ] 로그인 성공 시 프로필 정보 자동 입력
- [ ] 기존 계정과 연동 가능
- [ ] 로그인 실패 시 명확한 오류 메시지

**Story Points**: 8

---

### Epic 2: PDF 번역

#### US-003: PDF 파일 업로드
**As a** 사용자
**I want to** PDF 파일을 드래그앤드롭으로 업로드하고
**So that** 번역을 시작할 수 있다

**Acceptance Criteria**
- [ ] 드래그앤드롭 영역 표시
- [ ] 파일 선택 버튼도 제공
- [ ] 업로드 중 진행률 표시 (%)
- [ ] 최대 50MB, 200페이지 제한 검증
- [ ] 암호화된 PDF는 거부하고 오류 메시지 표시
- [ ] 업로드 완료 후 파일명, 페이지 수, 크기 표시

**Story Points**: 5

---

#### US-004: 번역 수행
**As a** 사용자
**I want to** 업로드한 PDF를 AI로 번역하고
**So that** 영문 강의 자료를 얻을 수 있다

**Acceptance Criteria**
- [ ] "번역 시작" 버튼 클릭 가능
- [ ] 번역 진행 중 단계별 상태 표시 (파싱 → 번역 → 저장)
- [ ] 진행률 % 및 예상 소요 시간 표시
- [ ] 번역 실패 시 재시도 버튼 제공
- [ ] 번역 완료 시 알림 (브라우저 알림 + 이메일)
- [ ] 100페이지 문서가 10분 이내 완료

**Story Points**: 13

---

#### US-005: 번역 결과 편집
**As a** 사용자
**I want to** 번역된 텍스트를 수정하고
**So that** 전문용어를 정확하게 교정할 수 있다

**Acceptance Criteria**
- [ ] 좌측 원본, 우측 번역본 Split View
- [ ] Markdown 문법 하이라이팅
- [ ] 실시간 미리보기 (하단 또는 별도 탭)
- [ ] 자동 저장 (30초 간격)
- [ ] Ctrl+F 찾기, Ctrl+H 바꾸기 지원
- [ ] Ctrl+Z/Y 실행 취소/다시 실행

**Story Points**: 8

---

#### US-006: PDF 다운로드
**As a** 사용자
**I want to** 편집한 번역본을 PDF로 다운로드하고
**So that** 강의 자료로 사용할 수 있다

**Acceptance Criteria**
- [ ] "PDF 생성" 버튼 클릭
- [ ] 생성 중 진행률 표시
- [ ] 생성 완료 후 미리보기 모달 표시
- [ ] 다운로드 버튼 클릭 시 브라우저 다운로드
- [ ] 원본과 레이아웃 95% 이상 일치
- [ ] 파일명 자동 생성 (예: original_translated_2025-10-02.pdf)

**Story Points**: 8

---

### Epic 3: 프로젝트 관리

#### US-007: 프로젝트 목록 보기
**As a** 사용자
**I want to** 과거 번역 프로젝트 목록을 보고
**So that** 이전 작업을 다시 확인하거나 다운로드할 수 있다

**Acceptance Criteria**
- [ ] 대시보드에 프로젝트 카드 표시
- [ ] 각 카드에 파일명, 날짜, 상태 표시
- [ ] 최근 순 정렬 (옵션: 이름순, 날짜순)
- [ ] 프로젝트 클릭 시 편집 화면 진입
- [ ] 삭제 버튼 (소프트 삭제, 30일 보관)

**Story Points**: 5

---

#### US-008: 프로젝트 검색
**As a** 사용자
**I want to** 파일명으로 프로젝트를 검색하고
**So that** 원하는 작업을 빠르게 찾을 수 있다

**Acceptance Criteria**
- [ ] 검색 입력 필드 제공
- [ ] 실시간 검색 결과 필터링
- [ ] 검색어 하이라이팅
- [ ] 검색 결과 없을 때 "결과 없음" 메시지

**Story Points**: 3

---

### Epic 4: 구독 및 결제

#### US-009: 구독 플랜 선택
**As a** 사용자
**I want to** Basic 또는 Pro 플랜을 선택하고
**So that** 필요한 기능을 사용할 수 있다

**Acceptance Criteria**
- [ ] 플랜 비교 테이블 표시 (기능, 가격)
- [ ] "구독하기" 버튼 클릭
- [ ] Stripe 결제 페이지로 이동
- [ ] 결제 완료 후 플랜 즉시 활성화
- [ ] 영수증 이메일 자동 발송

**Story Points**: 8

---

#### US-010: 사용량 확인
**As a** 사용자
**I want to** 이번 달 사용한 페이지 수를 확인하고
**So that** 플랜 한도를 관리할 수 있다

**Acceptance Criteria**
- [ ] 대시보드에 사용량 게이지 표시
- [ ] 예: "150 / 500 페이지 사용 (30% 남음)"
- [ ] 100% 도달 시 경고 메시지
- [ ] 초과 시 업그레이드 안내

**Story Points**: 3

---

### Epic 5: 용어집 관리 (Phase 2)

#### US-011: 용어 추가
**As a** Pro 사용자
**I want to** 자주 쓰는 전문용어를 용어집에 등록하고
**So that** 번역 시 자동으로 적용되도록 할 수 있다

**Acceptance Criteria**
- [ ] 용어집 페이지 진입
- [ ] "새 용어 추가" 버튼
- [ ] 한글 원어, 영어 대상어 입력 필드
- [ ] 카테고리 선택 (기술, 의학, 교육, 기타)
- [ ] 저장 버튼 클릭 시 목록에 추가
- [ ] 중복 용어 검사

**Story Points**: 5

---

#### US-012: 용어집 가져오기
**As a** Enterprise 사용자
**I want to** 기존 엑셀 용어집을 CSV로 업로드하고
**So that** 대량 용어를 한 번에 등록할 수 있다

**Acceptance Criteria**
- [ ] CSV 업로드 버튼
- [ ] 파일 형식 검증 (열: 원어, 대상어, 카테고리)
- [ ] 미리보기 테이블 표시
- [ ] "가져오기" 버튼 클릭 시 일괄 저장
- [ ] 중복 용어는 건너뛰기 or 덮어쓰기 옵션

**Story Points**: 8

---

## 8. Technical Specifications

### 8.1 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Web App    │  │  Admin Panel │  │   Mobile     │      │
│  │  (React.js)  │  │  (React.js)  │  │ (Phase 3)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                         HTTPS/WSS
                              │
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                       │
│                     (NGINX + Rate Limiting)                  │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   FastAPI    │  │  Background  │  │   WebSocket  │      │
│  │   Server     │  │   Workers    │  │   Server     │      │
│  │              │  │  (Celery)    │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Service Layer  │  │  Service Layer  │  │  Service Layer  │
│                 │  │                 │  │                 │
│  PDF Parser     │  │  Translator     │  │  PDF Generator  │
│  (PyMuPDF)      │  │  (GPT-4/Claude) │  │  (WeasyPrint)   │
└─────────────────┘  └─────────────────┘  └─────────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                       Data Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │    Redis     │  │     S3       │      │
│  │  (Metadata)  │  │   (Cache +   │  │  (Files)     │      │
│  │              │  │    Queue)    │  │              │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    External Services                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  OpenAI API  │  │  Stripe API  │  │  SendGrid    │      │
│  │              │  │              │  │  (Email)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 기술 스택

#### Frontend
- **Framework**: React 18.x + TypeScript
- **State Management**: Zustand or Redux Toolkit
- **UI Library**: TailwindCSS + shadcn/ui
- **Editor**: Monaco Editor (Markdown)
- **PDF Viewer**: react-pdf or PDF.js
- **Build Tool**: Vite
- **Testing**: Vitest + React Testing Library

#### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0
- **Task Queue**: Celery + Redis
- **Validation**: Pydantic v2
- **Authentication**: JWT (PyJWT)
- **Testing**: pytest + pytest-asyncio

#### Data & Storage
- **Database**: PostgreSQL 15+
- **Cache**: Redis 7+
- **File Storage**: AWS S3 or Google Cloud Storage
- **Search**: PostgreSQL Full-Text Search (Phase 1)

#### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (Phase 2) or AWS ECS
- **CI/CD**: GitHub Actions
- **Monitoring**: Datadog or Prometheus + Grafana
- **Logging**: ELK Stack or CloudWatch

#### External Services
- **Translation**: OpenAI GPT-4 API or Anthropic Claude API
- **Payment**: Stripe
- **Email**: SendGrid or AWS SES
- **CDN**: Cloudflare

### 8.3 핵심 라이브러리

| 용도 | 라이브러리 | 버전 | 비고 |
|------|-----------|------|------|
| PDF 파싱 | PyMuPDF (fitz) | 1.23+ | 레이아웃 정보 추출 |
| PDF 생성 | WeasyPrint | 60+ | HTML/CSS → PDF |
| Markdown 처리 | python-markdown | 3.5+ | |
| OCR (Phase 2) | pytesseract | 0.3+ | Tesseract 래퍼 |
| 이미지 처리 | Pillow | 10+ | |
| HTTP 클라이언트 | httpx | 0.25+ | Async 지원 |
| 비동기 작업 | Celery | 5.3+ | |

### 8.4 데이터베이스 스키마 (주요 테이블)

#### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    name VARCHAR(100),
    organization VARCHAR(200),
    major VARCHAR(100),
    subscription_plan VARCHAR(20) DEFAULT 'free', -- free, basic, pro, enterprise
    subscription_status VARCHAR(20) DEFAULT 'active', -- active, canceled, expired
    subscription_start_date TIMESTAMP,
    subscription_end_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### projects
```sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    original_filename VARCHAR(500) NOT NULL,
    original_file_url VARCHAR(1000), -- S3 URL
    source_language VARCHAR(10) DEFAULT 'ko',
    target_language VARCHAR(10) DEFAULT 'en',
    page_count INT,
    file_size_bytes BIGINT,
    status VARCHAR(20) DEFAULT 'uploading', -- uploading, parsing, translating, completed, failed
    progress_percent INT DEFAULT 0,
    markdown_original TEXT,
    markdown_translated TEXT,
    pdf_translated_url VARCHAR(1000),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    deleted_at TIMESTAMP -- soft delete
);
```

#### glossaries
```sql
CREATE TABLE glossaries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    source_term VARCHAR(200) NOT NULL,
    target_term VARCHAR(200) NOT NULL,
    category VARCHAR(50), -- tech, medical, education, etc.
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_glossaries_user_id ON glossaries(user_id);
CREATE INDEX idx_glossaries_source_term ON glossaries(source_term);
```

#### usage_logs
```sql
CREATE TABLE usage_logs (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    action VARCHAR(50), -- upload, translate, download
    page_count INT,
    credits_used DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_usage_logs_user_id ON usage_logs(user_id);
CREATE INDEX idx_usage_logs_created_at ON usage_logs(created_at);
```

#### payments
```sql
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    stripe_payment_id VARCHAR(255) UNIQUE,
    amount DECIMAL(10, 2),
    currency VARCHAR(3) DEFAULT 'KRW',
    status VARCHAR(20), -- succeeded, failed, refunded
    subscription_plan VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 8.5 API 엔드포인트 (RESTful)

상세한 API 사양은 [섹션 10](#10-api-specifications) 참조

---

## 9. UI/UX Requirements

### 9.1 디자인 원칙

1. **Simple & Clean**: 불필요한 요소 제거, 핵심 기능 강조
2. **Progress Visibility**: 모든 장시간 작업에 진행률 표시
3. **Error Prevention**: 명확한 가이드와 제약 조건 안내
4. **Responsive**: 태블릿(768px) 이상 지원
5. **Accessibility**: 키보드 네비게이션, 고대비 색상

### 9.2 주요 화면 구성

#### 9.2.1 랜딩 페이지
- Hero 섹션: "강의 자료 번역, 10분이면 충분합니다"
- 기능 소개 (3단 카드)
- 가격 플랜 비교 테이블
- 사용 후기 (Phase 2)
- CTA 버튼: "무료로 시작하기"

#### 9.2.2 대시보드
```
┌─────────────────────────────────────────────────────────┐
│  [Logo]  대시보드  프로젝트  용어집  설정    [Profile▼] │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  안녕하세요, 김교수님! 👋                                 │
│  이번 달 사용량: ████████░░ 80/100 페이지                │
│                                                          │
│  ┌──────────────────────────────────────────────┐       │
│  │  + 새 번역 시작                               │       │
│  │  PDF 파일을 드래그하거나 클릭하여 업로드       │       │
│  └──────────────────────────────────────────────┘       │
│                                                          │
│  최근 프로젝트                            [검색 ____]    │
│                                                          │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐           │
│  │ lecture.pdf│  │ thesis.pdf│  │ manual.pdf│           │
│  │ 완료       │  │ 번역 중   │  │ 완료       │           │
│  │ 2025-10-01│  │ 50%       │  │ 2025-09-28│           │
│  │ [편집][📥]│  │           │  │ [편집][📥]│           │
│  └───────────┘  └───────────┘  └───────────┘           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### 9.2.3 번역 진행 화면
```
┌─────────────────────────────────────────────────────────┐
│  ← 뒤로                    lecture.pdf                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  번역 중... ⏳                                            │
│                                                          │
│  ████████████████████████░░░░░░░░░░  75%                │
│                                                          │
│  현재 단계: AI 번역 수행 중 (38/50 페이지)                │
│  예상 소요 시간: 약 2분 남음                              │
│                                                          │
│  ✓ 파일 업로드 완료                                       │
│  ✓ PDF 파싱 완료 (50 페이지)                             │
│  ⏵ AI 번역 진행 중...                                    │
│  ○ 결과 저장                                             │
│                                                          │
│                     [취소]                               │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

#### 9.2.4 편집 화면 (Split View)
```
┌─────────────────────────────────────────────────────────┐
│  ← 대시보드   lecture.pdf   [저장됨 ✓]     [PDF 생성]    │
├──────────────────────┬──────────────────────────────────┤
│  원본 (한글)          │  번역본 (영어)                    │
│                      │                                  │
│  # 강의 제목          │  # Lecture Title                 │
│                      │                                  │
│  ## 1. 서론          │  ## 1. Introduction              │
│                      │                                  │
│  인공지능은...        │  Artificial intelligence is... ▂ │
│                      │                                  │
│  ...                 │  ...                             │
│                      │                                  │
├──────────────────────┴──────────────────────────────────┤
│  미리보기 [▼]                                            │
│  ┌────────────────────────────────────────────────┐     │
│  │  [PDF 렌더링 영역]                              │     │
│  │  Lecture Title                                 │     │
│  │  1. Introduction                               │     │
│  │  Artificial intelligence is...                 │     │
│  └────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

#### 9.2.5 용어집 관리 (Phase 2)
```
┌─────────────────────────────────────────────────────────┐
│  용어집                                   [+ 새 용어 추가]│
├─────────────────────────────────────────────────────────┤
│  [검색 ____]  [카테고리: 전체 ▼]  [CSV 가져오기/내보내기]│
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ 원어 (한글)  │ 대상어 (영어)    │ 카테고리 │ 삭제  │ │
│  ├────────────────────────────────────────────────────┤ │
│  │ 인공지능     │ Artificial Int..│ 기술     │ [🗑]  │ │
│  │ 머신러닝     │ Machine Learning│ 기술     │ [🗑]  │ │
│  │ 신경망       │ Neural Network  │ 기술     │ [🗑]  │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  총 324개 용어                              [1][2][3]... │
└─────────────────────────────────────────────────────────┘
```

### 9.3 컴포넌트 라이브러리

- **Button**: Primary, Secondary, Danger, Ghost
- **Input**: Text, Email, Password, File Upload
- **Progress Bar**: Linear, Circular
- **Modal**: Confirmation, Alert, Form
- **Toast**: Success, Error, Warning, Info
- **Table**: Sortable, Searchable
- **Tabs**: Horizontal, Vertical

### 9.4 Color Palette

- **Primary**: #2563EB (Blue)
- **Secondary**: #64748B (Gray)
- **Success**: #10B981 (Green)
- **Warning**: #F59E0B (Orange)
- **Danger**: #EF4444 (Red)
- **Background**: #F8FAFC (Light Gray)
- **Text**: #1E293B (Dark Gray)

### 9.5 Typography

- **Heading**: Pretendard Bold (한글), Inter Bold (영문)
- **Body**: Pretendard Regular, Inter Regular
- **Code**: JetBrains Mono

---

## 10. API Specifications

### 10.1 인증

모든 API는 JWT 기반 인증 사용

**헤더**:
```
Authorization: Bearer <JWT_TOKEN>
```

**토큰 만료**: 1시간
**Refresh 토큰**: 30일

### 10.2 에러 응답 형식

```json
{
  "error": {
    "code": "INVALID_FILE_FORMAT",
    "message": "지원하지 않는 파일 형식입니다.",
    "details": {
      "allowed_formats": ["pdf"],
      "received_format": "docx"
    }
  }
}
```

### 10.3 엔드포인트 목록

#### 인증 & 사용자

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/auth/register` | 회원가입 | No |
| POST | `/api/v1/auth/login` | 로그인 | No |
| POST | `/api/v1/auth/refresh` | 토큰 갱신 | Refresh Token |
| POST | `/api/v1/auth/logout` | 로그아웃 | Yes |
| GET | `/api/v1/users/me` | 내 프로필 조회 | Yes |
| PATCH | `/api/v1/users/me` | 프로필 수정 | Yes |
| POST | `/api/v1/auth/password-reset` | 비밀번호 재설정 요청 | No |

#### 프로젝트

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/api/v1/projects` | 새 프로젝트 생성 (파일 업로드) | Yes |
| GET | `/api/v1/projects` | 프로젝트 목록 조회 | Yes |
| GET | `/api/v1/projects/{id}` | 프로젝트 상세 조회 | Yes |
| PATCH | `/api/v1/projects/{id}` | Markdown 편집 저장 | Yes |
| DELETE | `/api/v1/projects/{id}` | 프로젝트 삭제 (소프트) | Yes |
| POST | `/api/v1/projects/{id}/translate` | 번역 시작/재시작 | Yes |
| GET | `/api/v1/projects/{id}/status` | 번역 진행 상태 조회 | Yes |
| POST | `/api/v1/projects/{id}/generate-pdf` | PDF 생성 | Yes |
| GET | `/api/v1/projects/{id}/download` | PDF 다운로드 | Yes |

#### 용어집 (Phase 2)

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/glossaries` | 용어집 목록 조회 | Yes |
| POST | `/api/v1/glossaries` | 용어 추가 | Yes |
| PATCH | `/api/v1/glossaries/{id}` | 용어 수정 | Yes |
| DELETE | `/api/v1/glossaries/{id}` | 용어 삭제 | Yes |
| POST | `/api/v1/glossaries/import` | CSV 가져오기 | Yes |
| GET | `/api/v1/glossaries/export` | CSV 내보내기 | Yes |

#### 구독 & 결제

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/api/v1/subscriptions/plans` | 플랜 목록 조회 | No |
| POST | `/api/v1/subscriptions/checkout` | Stripe 결제 세션 생성 | Yes |
| POST | `/api/v1/webhooks/stripe` | Stripe 웹훅 (결제 완료) | No |
| POST | `/api/v1/subscriptions/cancel` | 구독 취소 | Yes |
| GET | `/api/v1/usage` | 이번 달 사용량 조회 | Yes |

### 10.4 주요 API 상세 스펙

#### POST /api/v1/projects (파일 업로드 & 프로젝트 생성)

**Request**:
```http
POST /api/v1/projects
Content-Type: multipart/form-data
Authorization: Bearer <token>

file: <PDF binary>
source_language: ko
target_language: en
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "original_filename": "lecture.pdf",
  "source_language": "ko",
  "target_language": "en",
  "page_count": 50,
  "file_size_bytes": 5242880,
  "status": "uploading",
  "progress_percent": 0,
  "created_at": "2025-10-02T10:30:00Z"
}
```

**Errors**:
- `400`: Invalid file format
- `413`: File too large (>50MB)
- `429`: Rate limit exceeded

---

#### POST /api/v1/projects/{id}/translate (번역 시작)

**Request**:
```http
POST /api/v1/projects/550e8400-e29b-41d4-a716-446655440000/translate
Authorization: Bearer <token>
Content-Type: application/json

{
  "use_glossary": true,
  "glossary_ids": ["123e4567-e89b-12d3-a456-426614174000"]
}
```

**Response** (202 Accepted):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "translating",
  "progress_percent": 0,
  "estimated_time_seconds": 600
}
```

---

#### GET /api/v1/projects/{id}/status (진행 상태 조회)

**Request**:
```http
GET /api/v1/projects/550e8400-e29b-41d4-a716-446655440000/status
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "translating",
  "progress_percent": 65,
  "current_step": "AI 번역 진행 중 (33/50 페이지)",
  "estimated_time_remaining_seconds": 210,
  "updated_at": "2025-10-02T10:35:12Z"
}
```

**Status Values**:
- `uploading`: 파일 업로드 중
- `parsing`: PDF 파싱 중
- `translating`: AI 번역 중
- `completed`: 번역 완료
- `failed`: 실패

---

#### PATCH /api/v1/projects/{id} (Markdown 편집 저장)

**Request**:
```http
PATCH /api/v1/projects/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer <token>
Content-Type: application/json

{
  "markdown_translated": "# Lecture Title\n\n## 1. Introduction\n\n..."
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "markdown_translated": "# Lecture Title\n\n...",
  "updated_at": "2025-10-02T11:00:00Z"
}
```

---

#### POST /api/v1/projects/{id}/generate-pdf (PDF 생성)

**Request**:
```http
POST /api/v1/projects/550e8400-e29b-41d4-a716-446655440000/generate-pdf
Authorization: Bearer <token>
```

**Response** (202 Accepted):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "generating_pdf",
  "progress_percent": 0
}
```

---

#### GET /api/v1/projects/{id}/download (PDF 다운로드)

**Request**:
```http
GET /api/v1/projects/550e8400-e29b-41d4-a716-446655440000/download
Authorization: Bearer <token>
```

**Response** (200 OK):
```http
Content-Type: application/pdf
Content-Disposition: attachment; filename="lecture_translated_2025-10-02.pdf"

<PDF binary>
```

---

### 10.5 WebSocket API (실시간 진행 상태)

**Endpoint**: `wss://api.example.com/ws/projects/{project_id}`

**연결**:
```javascript
const ws = new WebSocket('wss://api.example.com/ws/projects/550e8400...?token=<JWT>');
```

**수신 메시지**:
```json
{
  "type": "progress_update",
  "data": {
    "status": "translating",
    "progress_percent": 75,
    "current_step": "AI 번역 진행 중 (38/50 페이지)",
    "estimated_time_remaining_seconds": 120
  }
}
```

```json
{
  "type": "translation_completed",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "markdown_translated": "..."
  }
}
```

---

## 11. Data Model

### 11.1 ERD (Entity Relationship Diagram)

```
┌──────────────┐         ┌──────────────┐
│    users     │1       *│   projects   │
│──────────────│─────────│──────────────│
│ id (PK)      │         │ id (PK)      │
│ email        │         │ user_id (FK) │
│ password_hash│         │ original_... │
│ name         │         │ status       │
│ subscription │         │ markdown_... │
│ ...          │         │ ...          │
└──────────────┘         └──────────────┘
       │1                       │1
       │                        │
       │*                       │*
┌──────────────┐         ┌──────────────┐
│  glossaries  │         │  usage_logs  │
│──────────────│         │──────────────│
│ id (PK)      │         │ id (PK)      │
│ user_id (FK) │         │ user_id (FK) │
│ source_term  │         │ project_id   │
│ target_term  │         │ page_count   │
│ ...          │         │ ...          │
└──────────────┘         └──────────────┘

       │1
       │
       │*
┌──────────────┐
│   payments   │
│──────────────│
│ id (PK)      │
│ user_id (FK) │
│ stripe_...   │
│ amount       │
│ ...          │
└──────────────┘
```

### 11.2 파일 저장 구조 (S3)

```
s3://bucket-name/
├── uploads/
│   ├── {user_id}/
│   │   ├── {project_id}/
│   │   │   ├── original.pdf
│   │   │   ├── translated.pdf
│   │   │   └── metadata.json
├── temp/
│   └── {project_id}/
│       ├── images/
│       │   ├── page_01_img_01.png
│       │   └── page_02_img_01.png
│       └── chunks/
│           ├── chunk_01.md
│           └── chunk_02.md
```

---

## 12. Security & Privacy

### 12.1 보안 요구사항

| 항목 | 구현 방법 | 우선순위 |
|------|----------|----------|
| HTTPS | TLS 1.3 인증서 (Let's Encrypt) | Must |
| 비밀번호 해싱 | bcrypt (cost factor 12) | Must |
| JWT 서명 | HS256 (Phase 1) → RS256 (Phase 2) | Must |
| API Rate Limiting | IP당 시간당 100 요청 | Should |
| CORS | 허용된 도메인만 접근 | Must |
| XSS 방어 | React 기본 이스케이핑 + CSP 헤더 | Must |
| CSRF 방어 | SameSite Cookie + CSRF 토큰 | Must |
| SQL Injection | ORM 사용 (SQLAlchemy) | Must |
| 파일 업로드 검증 | Magic number 검사, 확장자 필터 | Must |

### 12.2 개인정보 처리

- **수집 정보**: 이메일, 이름, 기관명(선택), 결제 정보(Stripe 처리)
- **보관 기간**:
  - 회원 정보: 탈퇴 후 30일
  - 프로젝트 파일: 번역 완료 후 30일 (자동 삭제)
  - 결제 기록: 5년 (세법)
- **암호화**: AES-256 (저장 데이터), TLS 1.3 (전송 데이터)

### 12.3 데이터 백업

- **빈도**: 일 1회 (자정)
- **보관**: 최근 7일
- **위치**: 별도 리전 (재해 대비)

---

## 13. Success Metrics & KPIs

### 13.1 비즈니스 메트릭

| 지표 | 목표 (3개월) | 목표 (6개월) | 측정 방법 |
|------|-------------|-------------|----------|
| 월 활성 사용자 (MAU) | 200명 | 500명 | 로그인 기록 |
| 유료 전환율 | 10% | 15% | 결제 완료 / 가입자 |
| 월 반복 매출 (MRR) | 300만원 | 1,000만원 | Stripe 데이터 |
| 고객 이탈률 (Churn) | < 10% | < 5% | 구독 취소 / 총 구독자 |
| NPS (Net Promoter Score) | 30+ | 50+ | 설문 조사 |

### 13.2 제품 메트릭

| 지표 | 목표 | 측정 방법 |
|------|------|----------|
| 평균 번역 시간 (100페이지) | < 10분 | 서버 로그 |
| 레이아웃 보존율 | > 95% | 사용자 피드백 + 자동 테스트 |
| 번역 품질 만족도 | > 4.0/5.0 | 프로젝트 완료 후 별점 |
| 첫 번역 완료율 | > 80% | 가입 → 첫 번역 완료 |
| 재방문율 (7일 이내) | > 40% | 로그인 기록 |

### 13.3 기술 메트릭

| 지표 | 목표 | 측정 도구 |
|------|------|----------|
| API 응답 시간 (P95) | < 500ms | Datadog APM |
| 서비스 가동률 (Uptime) | > 99.5% | Pingdom/UptimeRobot |
| 에러율 | < 0.5% | Sentry |
| 번역 API 성공률 | > 99% | 서버 로그 |

### 13.4 측정 도구

- **Analytics**: Google Analytics 4 or Mixpanel
- **Error Tracking**: Sentry
- **APM**: Datadog or New Relic
- **A/B Testing**: PostHog or Optimizely

---

## 14. Development Roadmap

### Phase 1: MVP (3개월)

#### Month 1: 기반 구축
**Week 1-2**
- [ ] 프로젝트 환경 설정 (Docker, CI/CD)
- [ ] 데이터베이스 스키마 설계 및 마이그레이션
- [ ] 사용자 인증 시스템 (회원가입, 로그인, JWT)
- [ ] 프론트엔드 기본 레이아웃 (React + TailwindCSS)

**Week 3-4**
- [ ] PDF 파싱 엔진 개발 (PyMuPDF)
  - 텍스트 추출
  - 레이아웃 정보 추출 (좌표, 폰트, 크기)
  - Markdown 변환 로직
- [ ] 파일 업로드 API 및 S3 연동
- [ ] 대시보드 UI (프로젝트 목록)

#### Month 2: 핵심 번역 기능
**Week 5-6**
- [ ] AI 번역 엔진 통합 (GPT-4 or Claude API)
  - 청크 단위 번역
  - 문맥 유지 로직
  - 교육/학술 용어 프롬프트 최적화
- [ ] Celery + Redis 작업 큐 설정
- [ ] 번역 진행 상태 추적 (WebSocket or Polling)

**Week 7-8**
- [ ] Markdown 편집 UI (Monaco Editor)
  - Split View (원본/번역본)
  - 자동 저장
  - 찾기/바꾸기
- [ ] PDF 생성 엔진 (WeasyPrint)
  - Markdown → HTML → PDF
  - 레이아웃 재현 로직

#### Month 3: 결제 & 출시 준비
**Week 9-10**
- [ ] Stripe 결제 연동
  - 구독 플랜 설정
  - 결제 페이지
  - 웹훅 처리
- [ ] 사용량 추적 및 제한
- [ ] 이메일 발송 (SendGrid)

**Week 11-12**
- [ ] 베타 테스트 (타겟 사용자 50명)
- [ ] 피드백 수집 및 버그 수정
- [ ] 랜딩 페이지 완성
- [ ] **공식 출시**

---

### Phase 2: 확장 기능 (3개월)

#### Month 4
- [ ] OCR 기능 추가 (Tesseract)
- [ ] 용어집 관리 UI 및 API
- [ ] 용어집 CSV 가져오기/내보내기
- [ ] 번역 시 용어집 자동 적용

#### Month 5
- [ ] 배치 번역 (여러 파일 동시 처리)
- [ ] 번역 메모리 (Translation Memory)
- [ ] 이미지 내 텍스트 번역 (OCR + 재삽입)
- [ ] 버전 히스토리 (Undo/Redo 확장)

#### Month 6
- [ ] 다국어 지원 (중국어, 일본어)
- [ ] Enterprise 플랜 기능
  - 팀 관리
  - 용어집 공유
  - API 액세스
- [ ] 성능 최적화 및 확장성 개선

---

### Phase 3: 고도화 (6개월~)

- [ ] 모바일 앱 (React Native or Flutter)
- [ ] PowerPoint/Keynote 직접 지원
- [ ] 실시간 협업 편집
- [ ] 번역 품질 AI 평가
- [ ] 커스텀 번역 모델 학습 (Fine-tuning)

---

## 15. Risk Assessment

### 15.1 기술적 리스크

| 리스크 | 영향도 | 가능성 | 완화 전략 |
|--------|-------|-------|----------|
| **PDF 레이아웃 보존 실패** | 높음 | 중간 | - 다양한 PDF 샘플로 철저한 테스트<br>- 레이아웃 보존율 < 90% 시 수동 편집 가이드 제공 |
| **AI 번역 API 장애** | 높음 | 낮음 | - 백업 API 준비 (OpenAI + Claude)<br>- 장애 시 자동 재시도 로직 |
| **대용량 파일 처리 지연** | 중간 | 중간 | - 청크 단위 처리 최적화<br>- 사용자에게 예상 시간 명확히 안내 |
| **서버 과부하** | 중간 | 중간 | - 오토 스케일링 설정<br>- 대기열 시스템으로 부하 분산 |

### 15.2 비즈니스 리스크

| 리스크 | 영향도 | 가능성 | 완화 전략 |
|--------|-------|-------|----------|
| **경쟁사 가격 인하** | 높음 | 중간 | - 교육 특화 기능으로 차별화<br>- 고객 충성도 확보 (용어집, 번역 메모리) |
| **초기 사용자 확보 실패** | 높음 | 중간 | - 타겟 커뮤니티 직접 마케팅 (교수 협회, 학회)<br>- 무료 체험 크레딧 제공 |
| **번역 품질 불만** | 중간 | 중간 | - 베타 테스트로 사전 검증<br>- 만족도 < 3.0 시 환불 정책 |
| **법적 문제 (저작권)** | 낮음 | 낮음 | - 사용자가 저작권 소유자임을 이용약관에 명시<br>- 파일 자동 삭제 (30일) |

### 15.3 규제 리스크

| 리스크 | 영향도 | 가능성 | 완화 전략 |
|--------|-------|-------|----------|
| **개인정보 유출** | 높음 | 낮음 | - AES-256 암호화<br>- 정기 보안 감사<br>- 개인정보처리방침 준수 |
| **결제 사기** | 중간 | 낮음 | - Stripe Radar (사기 탐지)<br>- 환불 정책 명확화 |

---

## 16. Dependencies & Constraints

### 16.1 외부 의존성

| 서비스 | 용도 | 비용 (추정) | 대체 방안 |
|--------|------|------------|----------|
| **OpenAI GPT-4** | AI 번역 | $0.03/1K tokens<br>(월 $3,000~) | Anthropic Claude |
| **Stripe** | 결제 처리 | 거래액의 2.9% + $0.30 | Toss Payments, Iamport |
| **AWS S3** | 파일 저장 | 월 $100~ | Google Cloud Storage |
| **SendGrid** | 이메일 발송 | 월 $15 (100 emails/day) | AWS SES |

### 16.2 기술적 제약

- **PDF 파싱 한계**: 복잡한 그래픽, 손글씨 인식 어려움
- **번역 API 비용**: 사용량 증가 시 비용 급증 → 캐싱 및 최적화 필수
- **레이아웃 재현**: 100% 완벽 불가능 → 95% 목표

### 16.3 비즈니스 제약

- **초기 자본**: 개발 + 인프라 = 약 5,000만원
- **인력**: 개발자 2명 (풀스택 1명 + 백엔드 1명)
- **출시 시기**: 3개월 내 MVP 필수 (시장 선점)

---

## 17. Appendix

### 17.1 용어 정의

- **CAT (Computer-Assisted Translation)**: 컴퓨터 보조 번역 도구
- **TM (Translation Memory)**: 번역 메모리, 과거 번역 재사용
- **OCR (Optical Character Recognition)**: 광학 문자 인식
- **SLA (Service Level Agreement)**: 서비스 수준 협약
- **MAU (Monthly Active Users)**: 월 활성 사용자
- **MRR (Monthly Recurring Revenue)**: 월 반복 매출

### 17.2 참고 문서

- [DeepL API Documentation](https://www.deepl.com/docs-api)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Stripe Integration Guide](https://stripe.com/docs)

### 17.3 변경 이력

| 버전 | 날짜 | 작성자 | 변경 내용 |
|------|------|--------|----------|
| 1.0 | 2025-10-02 | Kelly | 초안 작성 |

---

**문서 종료**

이 PRD는 살아있는 문서(Living Document)입니다. 제품 개발 과정에서 지속적으로 업데이트됩니다.
