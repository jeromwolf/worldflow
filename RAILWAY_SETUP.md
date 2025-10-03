# Railway 배포 가이드

## 🚂 필수 환경 변수 설정

Railway 대시보드 → worldflow 서비스 → **Variables 탭**에서 다음 변수들을 추가하세요:

### 1️⃣ PostgreSQL 연결 (필수)
```bash
DATABASE_URL=${{Postgres.DATABASE_URL}}
```
**설정 방법**:
- "+ New Variable" 클릭
- Variable name: `DATABASE_URL`
- Value: `${{Postgres.DATABASE_URL}}` (Variable Reference 선택)

### 2️⃣ Redis 연결 (필수)
```bash
REDIS_URL=${{Redis.REDIS_URL}}
```
**설정 방법**:
- "+ New Variable" 클릭
- Variable name: `REDIS_URL`
- Value: `${{Redis.REDIS_URL}}` (Variable Reference 선택)

### 3️⃣ JWT 시크릿 키 (필수)
```bash
SECRET_KEY=랜덤-32자-이상-문자열-여기에-입력
```
**예시**:
```
SECRET_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567
```

### 4️⃣ AI API 키 (필수 - 하나만 선택)
```bash
OPENAI_API_KEY=sk-your-actual-openai-key-here
AI_PROVIDER=openai
```
**또는**:
```bash
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
AI_PROVIDER=anthropic
```

### 5️⃣ 기타 설정
```bash
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEBUG=false
ENVIRONMENT=production
LOG_LEVEL=INFO
```

---

## ⚠️ 주의사항

### PostgreSQL과 Redis가 추가되어 있는지 확인
왼쪽 사이드바에서:
- **Postgres** 서비스 있어야 함
- **Redis** 서비스 있어야 함

없으면:
```bash
railway add -d postgres
railway add -d redis
```

---

## ✅ 배포 확인

Variables 설정 후:
1. 자동으로 재배포 시작 (1-2분 소요)
2. **Deployments** 탭에서 상태 확인
3. **Logs** 탭에서 에러 확인
4. 성공하면 **초록색 체크마크** ✅

---

**문서 작성일**: 2025-10-03
