import os
import cv2
import numpy as np
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename

# Flask 앱 초기화
app = Flask(__name__)

# 파일 업로드 및 결과 폴더 설정
UPLOAD_FOLDER = 'static/uploads/'
RESULT_FOLDER = 'static/results/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def transfer_color(source, style):
    """
    한 이미지의 색감(통계)을 다른 이미지로 이전하는 함수.
    LAB 색상 공간을 사용하여 밝기(L)와 색상(A, B)을 분리해 처리합니다.
    """
    # 이미지를 LAB 색상 공간으로 변환
    source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    style_lab = cv2.cvtColor(style, cv2.COLOR_BGR2LAB).astype("float32")

    # 각 채널(L, A, B)을 분리
    (s_l, s_a, s_b) = cv2.split(source_lab)
    (t_l, t_a, t_b) = cv2.split(style_lab)

    # 각 채널의 평균과 표준편차 계산
    (s_l_mean, s_l_std) = (s_l.mean(), s_l.std())
    (s_a_mean, s_a_std) = (s_a.mean(), s_a.std())
    (s_b_mean, s_b_std) = (s_b.mean(), s_b.std())
    
    (t_l_mean, t_l_std) = (t_l.mean(), t_l.std())
    (t_a_mean, t_a_std) = (t_a.mean(), t_a.std())
    (t_b_mean, t_b_std) = (t_b.mean(), t_b.std())

    # 원본 이미지의 색상 통계를 스타일 이미지의 통계와 일치시킴
    s_l -= s_l_mean
    s_a -= s_a_mean
    s_b -= s_b_mean

    s_l = (t_l_std / s_l_std) * s_l
    s_a = (t_a_std / s_a_std) * s_a
    s_b = (t_b_std / s_b_std) * s_b

    s_l += t_l_mean
    s_a += t_a_mean
    s_b += t_b_mean

    # 값 범위를 [0, 255]로 클리핑
    s_l = np.clip(s_l, 0, 255)
    s_a = np.clip(s_a, 0, 255)
    s_b = np.clip(s_b, 0, 255)

    # 채널들을 다시 병합하고 BGR 색상 공간으로 변환
    transfer = cv2.merge([s_l, s_a, s_b])
    transfer = cv2.cvtColor(transfer.astype("uint8"), cv2.COLOR_LAB2BGR)
    
    return transfer

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 파일이 없으면 메인 페이지로 리디렉션
        if 'content' not in request.files or 'style' not in request.files:
            return render_template('index.html', error="두 이미지를 모두 선택해주세요.")

        content_file = request.files['content']
        style_file = request.files['style']

        if content_file.filename == '' or style_file.filename == '':
            return render_template('index.html', error="파일을 올바르게 선택해주세요.")

        # 파일 저장
        content_filename = secure_filename(content_file.filename)
        style_filename = secure_filename(style_file.filename)
        content_path = os.path.join(app.config['UPLOAD_FOLDER'], content_filename)
        style_path = os.path.join(app.config['UPLOAD_FOLDER'], style_filename)
        content_file.save(content_path)
        style_file.save(style_path)

        # 이미지 로드 및 색상 이전 실행
        source_image = cv2.imread(content_path)
        style_image = cv2.imread(style_path)
        result_image = transfer_color(source_image, style_image)

        # 결과 이미지 저장
        result_filename = 'result_' + content_filename
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
        cv2.imwrite(result_path, result_image)

        # 템플릿에 이미지 경로 전달
        return render_template('index.html', 
                               content_img=content_path, 
                               style_img=style_path, 
                               result_img=result_path)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)