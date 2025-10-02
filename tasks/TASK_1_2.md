# Task 1.2: 데이터베이스 설계 및 구축

**담당자**: 백엔드 개발자
**예상 소요 시간**: 6시간
**우선순위**: 🔴 High
**상태**: 📅 예정
**선행 작업**: TASK_1_1 완료 필수

---

## 📋 목표

PostgreSQL 데이터베이스 스키마를 설계하고 Alembic 마이그레이션을 설정합니다.

---

## ✅ 체크리스트

### 1. Alembic 초기 설정
- [ ] Alembic 초기화
  ```bash
  cd backend
  alembic init alembic
  ```
- [ ] alembic.ini 수정
  ```ini
  # sqlalchemy.url 주석 처리 (환경변수 사용)
  # sqlalchemy.url = driver://user:pass@localhost/dbname
  ```
- [ ] alembic/env.py 수정
  ```python
  from core.config import settings
  from models.base import Base

  config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
  target_metadata = Base.metadata
  ```

### 2. 데이터베이스 모델 설계

#### models/base.py
- [ ] Base 모델 생성
  ```python
  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy import Column, DateTime
  from datetime import datetime
  import uuid

  Base = declarative_base()

  class TimestampMixin:
      created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
      updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
  ```

#### models/user.py
- [ ] User 모델 생성
  ```python
  from sqlalchemy import Column, String, Boolean, DateTime, Enum
  from sqlalchemy.dialects.postgresql import UUID
  from models.base import Base, TimestampMixin
  import uuid
  import enum

  class SubscriptionPlan(str, enum.Enum):
      FREE = "free"
      BASIC = "basic"
      PRO = "pro"
      ENTERPRISE = "enterprise"

  class User(Base, TimestampMixin):
      __tablename__ = "users"

      id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
      email = Column(String(255), unique=True, nullable=False, index=True)
      password_hash = Column(String(255), nullable=False)
      name = Column(String(100))
      organization = Column(String(200))
      major = Column(String(100))

      # 구독 정보
      subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
      subscription_status = Column(String(20), default="active")
      subscription_start_date = Column(DateTime)
      subscription_end_date = Column(DateTime)

      # 인증
      is_active = Column(Boolean, default=True)
      is_verified = Column(Boolean, default=False)
      email_verified_at = Column(DateTime)

      # 관계
      projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
      glossaries = relationship("Glossary", back_populates="user", cascade="all, delete-orphan")
  ```

#### models/project.py
- [ ] Project 모델 생성
  ```python
  from sqlalchemy import Column, String, Integer, BigInteger, Text, ForeignKey, Enum
  from sqlalchemy.dialects.postgresql import UUID
  from sqlalchemy.orm import relationship
  from models.base import Base, TimestampMixin
  import uuid
  import enum

  class ProjectStatus(str, enum.Enum):
      UPLOADING = "uploading"
      PARSING = "parsing"
      TRANSLATING = "translating"
      COMPLETED = "completed"
      FAILED = "failed"

  class Project(Base, TimestampMixin):
      __tablename__ = "projects"

      id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
      user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

      # 파일 정보
      original_filename = Column(String(500), nullable=False)
      original_file_url = Column(String(1000))
      pdf_translated_url = Column(String(1000))

      # 언어
      source_language = Column(String(10), default="ko")
      target_language = Column(String(10), default="en")

      # 문서 정보
      page_count = Column(Integer)
      file_size_bytes = Column(BigInteger)

      # 진행 상태
      status = Column(Enum(ProjectStatus), default=ProjectStatus.UPLOADING, index=True)
      progress_percent = Column(Integer, default=0)
      error_message = Column(Text)

      # Markdown 콘텐츠
      markdown_original = Column(Text)
      markdown_translated = Column(Text)

      # 소프트 삭제
      deleted_at = Column(DateTime, index=True)

      # 관계
      user = relationship("User", back_populates="projects")
      usage_logs = relationship("UsageLog", back_populates="project")
  ```

#### models/glossary.py (Phase 2용, 스키마만 준비)
- [ ] Glossary 모델 생성
  ```python
  from sqlalchemy import Column, String, ForeignKey, Index
  from sqlalchemy.dialects.postgresql import UUID
  from sqlalchemy.orm import relationship
  from models.base import Base, TimestampMixin
  import uuid

  class Glossary(Base, TimestampMixin):
      __tablename__ = "glossaries"

      id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
      user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

      source_term = Column(String(200), nullable=False)
      target_term = Column(String(200), nullable=False)
      category = Column(String(50))

      # 관계
      user = relationship("User", back_populates="glossaries")

      __table_args__ = (
          Index('idx_glossary_source_term', 'source_term'),
      )
  ```

#### models/usage_log.py
- [ ] UsageLog 모델 생성
  ```python
  from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric
  from sqlalchemy.dialects.postgresql import UUID
  from sqlalchemy.orm import relationship
  from models.base import Base
  from datetime import datetime

  class UsageLog(Base):
      __tablename__ = "usage_logs"

      id = Column(Integer, primary_key=True, autoincrement=True)
      user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
      project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id", ondelete="SET NULL"))

      action = Column(String(50))  # upload, translate, download
      page_count = Column(Integer)
      credits_used = Column(Numeric(10, 2))

      created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

      # 관계
      user = relationship("User")
      project = relationship("Project", back_populates="usage_logs")
  ```

#### models/payment.py
- [ ] Payment 모델 생성
  ```python
  from sqlalchemy import Column, String, ForeignKey, DateTime, Numeric
  from sqlalchemy.dialects.postgresql import UUID
  from sqlalchemy.orm import relationship
  from models.base import Base
  from datetime import datetime
  import uuid

  class Payment(Base):
      __tablename__ = "payments"

      id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
      user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

      stripe_payment_id = Column(String(255), unique=True)
      amount = Column(Numeric(10, 2))
      currency = Column(String(3), default="KRW")
      status = Column(String(20))  # succeeded, failed, refunded
      subscription_plan = Column(String(20))

      created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

      # 관계
      user = relationship("User")
  ```

### 3. Database 연결 설정

#### core/database.py
- [ ] 비동기 DB 연결 생성
  ```python
  from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
  from sqlalchemy.orm import sessionmaker
  from core.config import settings

  engine = create_async_engine(
      settings.DATABASE_URL,
      echo=settings.DEBUG,
      pool_size=20,
      max_overflow=40,
      pool_pre_ping=True,
  )

  AsyncSessionLocal = sessionmaker(
      engine,
      class_=AsyncSession,
      expire_on_commit=False,
      autocommit=False,
      autoflush=False,
  )

  async def get_db():
      async with AsyncSessionLocal() as session:
          try:
              yield session
          finally:
              await session.close()
  ```

#### core/config.py
- [ ] 환경변수 설정 클래스 생성
  ```python
  from pydantic_settings import BaseSettings
  from pydantic import validator

  class Settings(BaseSettings):
      # Database
      DATABASE_URL: str

      # JWT
      SECRET_KEY: str
      ALGORITHM: str = "HS256"
      ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

      # Redis
      REDIS_URL: str

      # AWS
      AWS_ACCESS_KEY_ID: str
      AWS_SECRET_ACCESS_KEY: str
      AWS_REGION: str = "ap-northeast-2"
      S3_BUCKET_NAME: str

      # AI APIs
      OPENAI_API_KEY: str
      ANTHROPIC_API_KEY: str

      # Stripe
      STRIPE_SECRET_KEY: str
      STRIPE_PUBLISHABLE_KEY: str

      # Email
      SENDGRID_API_KEY: str
      FROM_EMAIL: str

      # App
      DEBUG: bool = False
      LOG_LEVEL: str = "INFO"

      class Config:
          env_file = ".env"
          case_sensitive = True

  settings = Settings()
  ```

### 4. 마이그레이션 생성 및 실행
- [ ] 초기 마이그레이션 생성
  ```bash
  alembic revision --autogenerate -m "Initial migration"
  ```
- [ ] 생성된 마이그레이션 파일 검토
  - `alembic/versions/xxxx_initial_migration.py` 확인
  - 모든 테이블과 인덱스가 포함되었는지 검증
- [ ] 마이그레이션 실행
  ```bash
  alembic upgrade head
  ```
- [ ] 데이터베이스 스키마 확인
  ```bash
  docker exec -it <postgres_container> psql -U user -d translation_db
  \dt  # 테이블 목록
  \d users  # users 테이블 스키마
  ```

### 5. 시드 데이터 생성 (개발용)
- [ ] scripts/seed_data.py 생성
  ```python
  import asyncio
  from sqlalchemy import select
  from core.database import AsyncSessionLocal
  from models.user import User
  from core.security import get_password_hash

  async def create_test_user():
      async with AsyncSessionLocal() as session:
          # 테스트 사용자 생성
          test_user = User(
              email="test@example.com",
              password_hash=get_password_hash("password123"),
              name="Test User",
              organization="Test Org",
              is_verified=True,
          )
          session.add(test_user)
          await session.commit()
          print(f"✅ Test user created: {test_user.email}")

  if __name__ == "__main__":
      asyncio.run(create_test_user())
  ```
- [ ] 시드 데이터 실행
  ```bash
  python scripts/seed_data.py
  ```

---

## 🧪 검증 방법

### 1. 데이터베이스 연결 확인
```python
# test_db_connection.py
import asyncio
from core.database import engine
from sqlalchemy import text

async def test_connection():
    async with engine.begin() as conn:
        result = await conn.execute(text("SELECT version()"))
        print(f"✅ PostgreSQL version: {result.scalar()}")

asyncio.run(test_connection())
```

### 2. 모델 CRUD 테스트
```python
# test_models.py
import asyncio
from core.database import AsyncSessionLocal
from models.user import User
from core.security import get_password_hash

async def test_create_user():
    async with AsyncSessionLocal() as session:
        user = User(
            email="test@example.com",
            password_hash=get_password_hash("password"),
            name="Test User"
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        print(f"✅ User created: {user.id}")

asyncio.run(test_create_user())
```

### 3. 마이그레이션 롤백 테스트
```bash
alembic downgrade -1  # 이전 버전으로 롤백
alembic upgrade head  # 다시 최신으로
```

---

## 📝 완료 조건

- [ ] 모든 테이블이 정상적으로 생성됨
  - users
  - projects
  - glossaries (Phase 2)
  - usage_logs
  - payments
- [ ] 인덱스가 정상적으로 생성됨
- [ ] Foreign Key 제약 조건이 정상 작동함
- [ ] Alembic 마이그레이션이 정상 작동함
- [ ] 테스트 사용자가 정상 생성됨

---

## 🚨 주의사항

- **절대 프로덕션 DB를 직접 수정하지 말 것**
- 마이그레이션은 항상 Alembic을 통해서만
- 개인정보 컬럼(email, password_hash)은 절대 로그에 남기지 않기
- UUID는 항상 `uuid.uuid4()` 사용

---

## 📚 참고 자료

- [SQLAlchemy Async 가이드](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic 공식 문서](https://alembic.sqlalchemy.org/)
- [PostgreSQL 인덱스 가이드](https://www.postgresql.org/docs/current/indexes.html)

---

**작성일**: 2025-10-02
**최종 수정**: 2025-10-02
