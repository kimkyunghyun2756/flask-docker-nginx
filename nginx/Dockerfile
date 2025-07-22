FROM nginx:1.25-alpine

# 기존 설정 제거 (선택적)
RUN rm /etc/nginx/conf.d/default.conf

# custom default.conf 복사
COPY default.conf /etc/nginx/conf.d/default.conf