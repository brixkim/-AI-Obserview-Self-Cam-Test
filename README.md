# [AI Obserview] Self Cam Test
AI Obserview 내부망을 Test하기 위한 Repo

## 개요
이 프로젝트는 `YOLOv12n-face`를 내부망에서 테스트 하기 위한 프로젝트입니다.

## 실행 방법
### 1. 가상환경 설정
```
python -m venv {venv_name}
source {venv_name}/bin/activate
pip install -r requirements.txt
cd src
```

### 2. SSL 인증서 발급

HTTPS 통신을 사용하려면 서버는 신뢰 가능한 SSL 인증서를 통해 자신ㅇ르 증명해야합니다.<br/>
인증서는 서버가 신뢰할 수 있는 주체임을 증명하고, 클라이언트와 서버 간 전송되는 데이터를 암호화하여 제3자가 내용을 볼 수 없도록 보호하는 역할을 합니다.<br/>
<br/>
특히 웹캠, 마이크 등 민감한 사용자 자원에 접근하기 위해서는 브라우저 정책상 반드시 HTTPS 환경이 요구됩니다.<br/>
따라서 사용자의 카메라 영상 스트림을 암호화되지 않은 HTTP 통신을 통해 전송될 경우 브라우저는 보안상의 이유로 접근 자체를 차단합니다.<br/>
사용자의 캠에 접근하기 위해서는 아래 인증서와 개인 키를 서버에 올바르게 연결하기 위해 필요합니다.<br/>

```
--ssl-certfile <인증서 파일 경로>
--ssl-keyfile <개인 키 파일 경로>
```

### 3. FastAPI 서버 실행
```
uvicorn server:app \
  --host 0.0.0.0 --port 8000 \
  --ssl-certfile <CERT_PATH.pem> \
  --ssl-keyfile  <KEY_PATH.pem>
```

### 4. Web 예시
![web example](/assets/images/example_web.png)<br/>

`시작`버튼을 누르면 추론을 시작합니다.<br/>
`정지`버튼을 누르면 추론을 정지합니다.<br/>