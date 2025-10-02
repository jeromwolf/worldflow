# Railway 배포 가이드

## Railway Persistent Volume 설정

### 1. Railway 프로젝트 생성
```bash
# Railway CLI 설치
npm i -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
railway init
```

### 2. Persistent Volume 추가

Railway 대시보드에서:
1. 프로젝트 선택
2. **Settings** → **Volumes** 탭
3. **+ New Volume** 클릭
4. 설정:
   - **Mount Path**: `/data`
   - **Size**: 1GB (무료 플랜 포함, 이후 $0.25/GB/월)

### 3. 환경 변수 설정

Railway 대시보드 → **Variables**:

```bash
# Database
DATABASE_URL=postgresql://user:password@railway-postgres-url/dbname

# Security
SECRET_KEY=your-secret-key-min-32-characters-here

# File Storage (자동 감지됨)
RAILWAY_ENVIRONMENT=production

# File Limits
MAX_FILE_SIZE_MB=50
MAX_PAGES=200

# AI APIs (선택사항)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### 4. 배포

```bash
# Git push로 자동 배포
git push

# 또는 Railway CLI로 배포
railway up
```

## 스토리지 동작 방식

### 개발 환경
```python
# ./storage/ 폴더 사용 (로컬)
storage/
  ├── uploads/
  │   └── users/{user_id}/originals/
  └── translated/
      └── users/{user_id}/
```

### Railway 환경
```python
# /data/ 볼륨 사용 (영구 저장)
/data/
  ├── uploads/
  │   └── users/{user_id}/originals/
  └── translated/
      └── users/{user_id}/
```

**자동 전환**: `RAILWAY_ENVIRONMENT` 환경변수가 있으면 `/data/` 사용

## 비용 예상

### Railway 무료 플랜
- 볼륨: 1GB 무료
- 실행 시간: $5 크레딧/월
- 메모리: 512MB
- vCPU: 공유

### 유료 사용 시
- 추가 스토리지: **$0.25/GB/월**
- 예) 10GB 사용 → $2.5/월
- 예) 100GB 사용 → $25/월

**비교 (AWS S3):**
- 저장: $0.023/GB/월 (10GB → $0.23/월)
- 전송: $0.09/GB (다운로드 시 과금)
- Railway가 **관리 편의성** 면에서 우수

## 볼륨 관리

### 사용량 확인
Railway 대시보드 → **Metrics** → **Volume Usage**

### 백업
```bash
# Railway CLI로 접속
railway run bash

# 데이터 확인
ls -lh /data

# 압축 백업
tar -czf backup.tar.gz /data
```

### 정리
오래된 파일 자동 삭제 (향후 구현 예정):
- 30일 이상 접근 없는 파일
- 삭제된 프로젝트의 파일
- 크론 작업으로 정리

## 모니터링

```python
# backend/api/admin.py (향후 추가)
@router.get("/storage/stats")
async def get_storage_stats():
    """스토리지 사용량 통계"""
    return {
        "total_files": count_files(),
        "total_size_mb": get_total_size(),
        "users": get_user_breakdown()
    }
```
