# UI/UX 설계 문서
# All-Rounder Translation Platform

**작성일**: 2025-10-02
**참고**: iLovePDF, PDFAid

---

## 🎨 디자인 철학

### 핵심 원칙
1. **Simple & Clean** - 3단계만으로 완료 (업로드 → 선택 → 변환)
2. **Progress Visibility** - 모든 진행 상태 실시간 표시
3. **Familiar Pattern** - iLovePDF 스타일의 친숙한 UI
4. **Professional Look** - 교육/학술 사용자를 위한 전문적 디자인

---

## 📱 메인 페이지 (랜딩)

### 레이아웃
```
┌─────────────────────────────────────────────────────────────┐
│  [Logo] All-Rounder Translation              [로그인] [시작] │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│              📄→📝→🌐                                         │
│                                                              │
│        강의 자료 번역, 10분이면 충분합니다                      │
│                                                              │
│     PDF 업로드 → 언어 선택 → AI 번역 → 편집 → 다운로드          │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │                                                    │     │
│  │    PDF 파일을 드래그하거나 클릭하여 업로드           │     │
│  │                                                    │     │
│  │              📁 파일 선택                          │     │
│  │                                                    │     │
│  │   또는 Google Drive, Dropbox에서 가져오기           │     │
│  │                                                    │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│                 최대 200페이지, 50MB까지                      │
│                                                              │
│  ───────────────────────────────────────────────────────    │
│                                                              │
│  ✅ 레이아웃 완벽 보존    ✅ 교육 용어 최적화                   │
│  ✅ 10분 내 완료         ✅ 편집 가능한 결과물                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 주요 요소
- **Hero Section**: 간단한 메시지 + 3단계 프로세스
- **Upload Zone**: 드래그 앤 드롭 (iLovePDF 스타일)
  - 테두리: 점선 (Drag 시 하이라이트)
  - 아이콘: 큰 폴더 아이콘
  - 버튼: "PDF 파일 선택" (Primary Blue)
- **클라우드 연동**: Google Drive, Dropbox 아이콘 (작게)
- **제약 조건**: 회색 작은 글씨로 명시

---

## 📤 업로드 & 언어 선택 화면

### Step 1: 파일 업로드 완료
```
┌─────────────────────────────────────────────────────────────┐
│  ← 뒤로                All-Rounder Translation               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📄 lecture_notes.pdf  ✅                                     │
│  50 페이지 · 5.2 MB · 업로드 완료                             │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  📝 번역 설정                                                │
│                                                              │
│  원본 언어                                                   │
│  ┌──────────────────────┐                                   │
│  │  🇰🇷 한국어  ▼      │  (자동 감지)                       │
│  └──────────────────────┘                                   │
│                                                              │
│  번역 언어                                                   │
│  ┌──────────────────────┐                                   │
│  │  🇺🇸 English  ▼     │                                   │
│  └──────────────────────┘                                   │
│                                                              │
│  고급 옵션 (선택)                                            │
│  ☐ 용어집 적용 (Pro 플랜)                                     │
│  ☐ 표/차트 우선 번역                                          │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│                          [번역 시작] →                       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 주요 요소
- **파일 정보 카드**: 파일명, 페이지 수, 크기, 체크 아이콘
- **언어 선택**:
  - Dropdown (국기 + 언어명)
  - 자동 감지 레이블
- **고급 옵션**:
  - 체크박스 (Pro 기능은 배지 표시)
- **CTA 버튼**:
  - "번역 시작" (크고 눈에 띄게)
  - Primary 색상, 우측 하단 고정

---

## ⏳ 번역 진행 화면

### Step 2: 번역 중
```
┌─────────────────────────────────────────────────────────────┐
│  All-Rounder Translation                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                   🔄 번역 진행 중...                          │
│                                                              │
│  lecture_notes.pdf → English                                │
│                                                              │
│  ████████████████████████████░░░░░░░░  75%                  │
│                                                              │
│  현재 단계: AI 번역 수행 중 (38/50 페이지)                     │
│  예상 소요 시간: 약 2분 30초                                   │
│                                                              │
│  ✓ 파일 업로드 완료 (5.2 MB)                                  │
│  ✓ PDF 파싱 완료 (50 페이지, 3개 표)                          │
│  ⏵ AI 번역 진행 중... (38/50)                                │
│  ○ 번역 결과 저장                                             │
│  ○ PDF 생성 준비                                              │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  💡 팁: 번역 중에도 다른 작업을 계속하실 수 있습니다.           │
│      완료되면 알림을 보내드립니다.                              │
│                                                              │
│                         [취소]                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 주요 요소
- **Progress Bar**:
  - 두께감 있는 바 (12px)
  - 퍼센트 숫자 표시
  - Animated (부드러운 애니메이션)
- **단계별 상태**:
  - ✓ 완료 (Green)
  - ⏵ 진행 중 (Blue, 애니메이션)
  - ○ 대기 (Gray)
- **예상 시간**:
  - 실시간 업데이트
  - 페이지 진행 표시
- **취소 버튼**:
  - 하단 중앙, Ghost 스타일

---

## ✏️ 편집 화면 (Split View)

### Step 3: 번역 완료 → 편집
```
┌─────────────────────────────────────────────────────────────┐
│  ← 대시보드   lecture_notes.pdf   [저장됨 ✓]    [PDF 생성] → │
├──────────────────────┬──────────────────────────────────────┤
│  원본 (한글) 📄        │  번역본 (English) 🌐                  │
│                      │                                      │
│  # 강의 제목          │  # Lecture Title                     │
│                      │                                      │
│  ## 1. 서론          │  ## 1. Introduction                  │
│                      │                                      │
│  인공지능은 현대      │  Artificial intelligence is a       │
│  사회에서...          │  technology in modern society... ▂   │
│                      │                                      │
│  ...                 │  ...                                 │
│                      │                                      │
│ [도구] 🔍 찾기        │ [도구] 📝 서식  💾 자동저장 (30초)     │
├──────────────────────┴──────────────────────────────────────┤
│  미리보기 [▼]                                                │
│  ┌────────────────────────────────────────────────────┐     │
│  │  [PDF 렌더링 영역]                                  │     │
│  │                                                    │     │
│  │  Lecture Title                                     │     │
│  │  1. Introduction                                   │     │
│  │  Artificial intelligence is...                     │     │
│  │                                                    │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 주요 요소
- **Split View (50:50)**:
  - 좌: 원본 (읽기 전용, 배경 연한 회색)
  - 우: 번역본 (편집 가능, Monaco Editor)
- **상단 툴바**:
  - 뒤로가기 버튼
  - 파일명 표시
  - 저장 상태 (✓ 아이콘)
  - PDF 생성 버튼 (Primary)
- **에디터 기능**:
  - 찾기/바꾸기 (Ctrl+F)
  - Markdown 문법 하이라이팅
  - 자동 저장 표시
- **미리보기 (접기 가능)**:
  - PDF 스타일 렌더링
  - 실시간 반영
  - 스크롤 동기화 (선택 사항)

---

## 📥 PDF 생성 & 다운로드

### Step 4: PDF 생성
```
┌─────────────────────────────────────────────────────────────┐
│  All-Rounder Translation                                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│                   🎉 번역 완료!                               │
│                                                              │
│  lecture_notes_EN.pdf                                       │
│  50 페이지 · 5.8 MB                                          │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │                                                    │     │
│  │          [PDF 미리보기 썸네일]                      │     │
│  │                                                    │     │
│  │  Lecture Title                                     │     │
│  │  1. Introduction                                   │     │
│  │  Artificial intelligence...                        │     │
│  │                                                    │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  레이아웃 보존율: 97% ✅                                       │
│  번역 소요 시간: 8분 32초                                      │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│     [⬇️ PDF 다운로드]        [✏️ 다시 편집]                  │
│                                                              │
│  ─────────────────────────────────────────────────────────  │
│                                                              │
│  💡 이 파일은 30일간 보관됩니다                                │
│     대시보드에서 언제든 다시 다운로드 가능합니다                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 주요 요소
- **완료 메시지**:
  - 축하 아이콘 (🎉)
  - 파일명 자동 생성 (원본명_언어코드.pdf)
- **미리보기 카드**:
  - PDF 첫 페이지 썸네일
  - 그림자 효과
- **통계 정보**:
  - 레이아웃 보존율
  - 소요 시간
- **액션 버튼**:
  - Primary: "PDF 다운로드" (파란색, 크게)
  - Secondary: "다시 편집" (회색 테두리)
- **보관 안내**:
  - 작은 정보 박스 (아이콘 + 텍스트)

---

## 🎯 대시보드

### 프로젝트 관리 화면
```
┌─────────────────────────────────────────────────────────────┐
│  [Logo]  대시보드  프로젝트  용어집  설정       [Profile ▼]   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  안녕하세요, 김교수님! 👋                                      │
│                                                              │
│  이번 달 사용량                                               │
│  ████████░░░░░░  80/100 페이지  [Pro 업그레이드 →]           │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  + 새 번역 시작                                       │   │
│  │  PDF 파일을 드래그하거나 클릭하여 업로드               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  최근 프로젝트                              [검색 🔍]         │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │📄           │  │📄           │  │📄           │         │
│  │lecture.pdf  │  │thesis.pdf   │  │manual.pdf   │         │
│  │             │  │             │  │             │         │
│  │✅ 완료       │  │⏳ 번역 중    │  │✅ 완료       │         │
│  │2025-10-01   │  │50%          │  │2025-09-28   │         │
│  │             │  │             │  │             │         │
│  │[편집] [📥]   │  │[보기]       │  │[편집] [📥]   │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                              │
│  ──────────────────────────────────────────────────────     │
│                                                              │
│  📊 통계                                                     │
│  - 총 번역 문서: 12개                                         │
│  - 총 번역 페이지: 580 페이지                                 │
│  - 평균 레이아웃 보존율: 96%                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 주요 요소
- **사용량 게이지**:
  - Progress bar
  - 숫자 표시
  - 업그레이드 CTA (100% 도달 시 강조)
- **빠른 업로드 존**:
  - 대시보드 상단 고정
  - 항상 접근 가능
- **프로젝트 카드**:
  - 그리드 레이아웃 (3열)
  - 썸네일 + 상태 + 액션
  - Hover 효과 (살짝 올라감)
- **통계 위젯**:
  - 간단한 숫자 요약

---

## 🎨 디자인 시스템

### Color Palette
```css
/* Primary Colors */
--primary-blue: #2563EB;      /* 주 CTA 버튼 */
--primary-dark: #1E40AF;      /* Hover */
--primary-light: #DBEAFE;     /* Background */

/* Status Colors */
--success-green: #10B981;     /* 완료 상태 */
--warning-orange: #F59E0B;    /* 경고 */
--error-red: #EF4444;         /* 에러 */
--progress-blue: #3B82F6;     /* 진행 중 */

/* Neutral Colors */
--gray-50: #F8FAFC;           /* Background */
--gray-100: #F1F5F9;          /* Card Background */
--gray-300: #CBD5E1;          /* Border */
--gray-600: #475569;          /* Secondary Text */
--gray-900: #1E293B;          /* Primary Text */
```

### Typography
```css
/* 한글 */
font-family: 'Pretendard', -apple-system, sans-serif;

/* 영문 */
font-family: 'Inter', -apple-system, sans-serif;

/* 코드 (Markdown 에디터) */
font-family: 'JetBrains Mono', monospace;

/* Size Scale */
--text-xs: 0.75rem;    /* 12px - 보조 정보 */
--text-sm: 0.875rem;   /* 14px - 일반 텍스트 */
--text-base: 1rem;     /* 16px - 본문 */
--text-lg: 1.125rem;   /* 18px - 소제목 */
--text-xl: 1.25rem;    /* 20px - 제목 */
--text-2xl: 1.5rem;    /* 24px - 큰 제목 */
--text-3xl: 1.875rem;  /* 30px - Hero */
```

### Components

#### Button Styles
```tsx
// Primary Button
<button className="bg-primary-blue text-white px-6 py-3 rounded-lg
                   font-semibold hover:bg-primary-dark
                   transition-colors shadow-md">
  번역 시작
</button>

// Secondary Button
<button className="bg-white text-gray-700 px-6 py-3 rounded-lg
                   font-semibold border-2 border-gray-300
                   hover:border-primary-blue hover:text-primary-blue
                   transition-colors">
  다시 편집
</button>

// Ghost Button
<button className="text-gray-600 px-4 py-2 rounded-lg
                   hover:bg-gray-100 transition-colors">
  취소
</button>
```

#### Card Styles
```tsx
<div className="bg-white rounded-xl shadow-lg p-6
                border border-gray-200
                hover:shadow-xl transition-shadow">
  {/* 카드 내용 */}
</div>
```

#### Progress Bar
```tsx
<div className="w-full bg-gray-200 rounded-full h-3">
  <div className="bg-primary-blue h-3 rounded-full
                  transition-all duration-500 ease-out"
       style={{ width: `${progress}%` }}>
  </div>
</div>
```

---

## 📱 반응형 디자인

### Breakpoints
```css
/* Mobile First */
sm: 640px   /* 모바일 가로 */
md: 768px   /* 태블릿 */
lg: 1024px  /* 데스크톱 */
xl: 1280px  /* 큰 데스크톱 */
```

### 모바일 (< 768px)
- Split View → 탭 전환 (원본/번역본)
- 3열 그리드 → 1열
- 사이드바 → 햄버거 메뉴

### 태블릿 (768px ~ 1024px)
- Split View 유지 (비율 조정 가능)
- 2열 그리드
- 터치 최적화

---

## ⚡ 사용자 경험 최적화

### 1. 로딩 상태
```tsx
// Skeleton Loading
<div className="animate-pulse">
  <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
  <div className="h-4 bg-gray-200 rounded w-1/2"></div>
</div>
```

### 2. 에러 처리
```tsx
// Toast Notification
<div className="fixed top-4 right-4 bg-red-50 border border-red-200
                text-red-800 px-6 py-4 rounded-lg shadow-lg">
  <div className="flex items-center">
    <span className="mr-3">❌</span>
    <div>
      <p className="font-semibold">번역 실패</p>
      <p className="text-sm">PDF 파일이 손상되었습니다</p>
    </div>
  </div>
</div>
```

### 3. 성공 피드백
```tsx
// Success Animation
<div className="flex flex-col items-center">
  <div className="text-6xl animate-bounce">🎉</div>
  <h2 className="text-2xl font-bold mt-4">번역 완료!</h2>
</div>
```

### 4. 드래그 앤 드롭 피드백
```tsx
// On Drag Over
<div className="border-4 border-dashed border-primary-blue
                bg-primary-light/50 rounded-xl p-12
                transition-all duration-200">
  <p className="text-primary-blue font-semibold">
    📁 파일을 여기에 놓으세요
  </p>
</div>
```

---

## 🔄 인터랙션 플로우

### Flow Diagram
```
[랜딩 페이지]
    ↓ (파일 선택)
[업로드 & 언어 선택]
    ↓ (번역 시작)
[진행 상태 화면]
    ↓ (완료)
[편집 화면] ←→ [미리보기]
    ↓ (PDF 생성)
[다운로드 화면]
    ↓
[대시보드] (프로젝트 관리)
```

### WebSocket 실시간 업데이트
```typescript
// 번역 진행 상태 실시간 수신
ws.onmessage = (event) => {
  const { progress, current_step, eta } = JSON.parse(event.data);

  // Progress Bar 업데이트
  setProgress(progress);
  setCurrentStep(current_step);
  setETA(eta);
};
```

---

## 🎁 추가 기능 (Phase 2)

### 1. 용어집 관리 (Pro)
```
┌─────────────────────────────────────────────────────────────┐
│  용어집                                   [+ 새 용어 추가]     │
├─────────────────────────────────────────────────────────────┤
│  [검색 🔍]  [카테고리: 전체 ▼]  [CSV 가져오기/내보내기]       │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │ 원어 (한글)  │ 대상어 (영어)    │ 카테고리 │ 삭제  │     │
│  ├────────────────────────────────────────────────────┤     │
│  │ 인공지능     │ Artificial Int..│ 기술     │ [🗑]  │     │
│  │ 머신러닝     │ Machine Learning│ 기술     │ [🗑]  │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### 2. 배치 번역 (Pro/Enterprise)
```
[여러 파일 업로드]
    ↓
[일괄 설정 (언어, 용어집)]
    ↓
[대기열 처리] (순차적)
    ↓
[완료된 파일부터 다운로드]
```

---

## 🚀 구현 우선순위

### Phase 1 (MVP)
1. ✅ 랜딩 페이지
2. ✅ 업로드 & 언어 선택
3. ✅ 번역 진행 화면
4. ✅ 편집 화면 (Split View)
5. ✅ PDF 다운로드
6. ✅ 기본 대시보드

### Phase 2
1. 용어집 관리
2. 배치 번역
3. 고급 에디터 기능
4. 협업 기능 (공유)

---

## 📊 성공 지표

### UX Metrics
- **First Translation Time**: < 20분 (신규 사용자)
- **Bounce Rate**: < 30% (랜딩 페이지)
- **Conversion Rate**: > 15% (무료 → 유료)
- **NPS Score**: > 50

### 성능 목표
- **Page Load**: < 2초
- **Upload Speed**: 5MB/s 이상
- **Translation Time**: 100페이지 < 10분

---

**작성일**: 2025-10-02
**참고**: iLovePDF, PDFAid
**디자인 도구**: Figma (프로토타입 제작 예정)
