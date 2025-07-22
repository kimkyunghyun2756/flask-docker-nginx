# 1. 베이스 이미지 선택
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /usr/src/app

# 3. 시스템 패키지 업데이트 (opencv 등 필요한 경우만)
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# 4. 파이썬 라이브러리 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 5. 소스코드 및 엔트리포인트 복사
COPY ./app /usr/src/app
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

CMD ["sh", "/usr/src/app/entrypoint.sh"]

