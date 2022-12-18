# FastAPI 프레임워크 API 사용방법

### 가상환경 생성
```sh
# FastAPI 상위폴더에서 생성 추천
python -m venv [venv_name]
cd [venv_name] #venv 폴더로 이동
.\Scripts\Activate.ps1 # Powershell인 경우 
```
### 가상환경에서 필요 라이브러리 설치
```python
pip install -r requirements.txt
```
### FastAPI 폴더로 이동하여 FastAPI 실행
```python
python ./main.py
```

### Web UI 실행
```
http://127.0.0.1:8000에 접속
드래그 앤 드랍을 통해 파일을 업로드 하거나,
Camera On 버튼을 통해 opencv를 이용하여 캠으로 환부 캡쳐
```

### 이미지 캡쳐 방법
```
opencv를 이용하여 카메라가 나오면 키보드 "c"를 눌러 이미지 캡쳐
키보드 "q"를 누르면 opencv가 종료되며 이미지 분류가 실행됨
```

### FastAPI 종료 방법
```
터미널에서 ctrl+c를 눌러 종료
```