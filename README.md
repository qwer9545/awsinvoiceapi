# AWS_Invoice_API

[AWS Get Invoice PDF API](https://aws.amazon.com/ko/about-aws/whats-new/2025/11/get-invoice-pdf-api/)

AWS는 고객이 SDK 호출을 통해 프로그래밍 방식으로 AWS 인보이스를 다운로드할 수 있는 Get Invoice PDF API의 정식 출시를 발표했습니다.

고객은 AWS 인보이스 ID를 입력으로 사용하는 API 직접 호출을 통해 개별 인보이스 PDF 아티팩트를 검색하고, AWS 인보이스 및 추가 문서를 PDF 형식으로 즉시 다운로드할 수 있도록 미리 서명된 Amazon S3 URL을 수신할 수 있습니다. 대량 인보이스 검색의 경우 고객은 먼저 List Invoice Summaries API를 직접적으로 호출하여 특정 청구 기간의 인보이스 ID를 가져온 다음 인보이스 ID를 Get Invoice API의 입력으로 사용하여 각 인보이스 PDF 아티팩트를 다운로드할 수 있습니다.

Get Invoice PDF API는 미국 동부(버지니아 북부) 리전에서 사용할 수 있습니다. 모든 상용 리전(중국 리전 제외)의 고객이 이 서비스를 이용할 수 있습니다. Get Invoice PDF API를 시작하려면 API 설명서를 참조하세요.

## 작업 환경 (Prerequisites)

이 프로젝트를 실행하기 위해서는 다음과 같은 개발 환경이 필요합니다:

*   **OS**: Windows (본 가이드 기준), Mac, Linux 등
*   **Python**: 3.8 이상 권장
*   **AWS 계정**: 청구서(Billing) 접근 권한이 있는 IAM 사용자
*   **필수 라이브러리 (Dependencies)**:
    *   `flask` (웹 서버)
    *   `Flask-Session` (서버 사이드 세션 관리)
    *   `python-dotenv` (환경 변수 관리)
    *   `boto3` (AWS SDK for Python)

## 프로젝트 구조 (Project Structure)

보안과 유지보수를 위해 기능별로 모듈을 분리하였습니다.

*   `app.py`: 웹 라우팅 및 화면 로직 담당.
*   `aws_utils.py`: AWS API 호출 (Invoicing, STS) 관련 핵심 로직.
*   `config.py`: 보안 설정 (세션 타입, 쿠키 보안 등).
*   `.env`: **[중요]** 로컬 개발용 비밀 키 저장 (Git 업로드 제외).
*   `flask_session/`: 서버 사이드 세션 파일이 저장되는 로컬 디렉토리.

## 설치 방법 (Installation)

1. **소스 코드 다운로드**:
   ```bash
   git clone <repository-url>
   cd AWS_Invoice_API
   ```

2. **가상 환경 생성 (선택 사항)**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows Git Bash
   # 또는
   .\venv\Scripts\activate      # Windows PowerShell
   ```

3. **패키지 설치**:
   ```bash
   pip install -r requirements.txt
   ```

## 사용 방법 (Usage)

<img width="871" height="518" alt="image" src="https://github.com/user-attachments/assets/798e393f-3064-4851-a7a7-5320d24a49f2" />

앱을 실행한 후 브라우저에서 `http://localhost:5000`으로 접속합니다.
# 각자 배포 방식에 맞는 방법으로 실행하시면 됩니다.

### 1. 사전 준비 (IAM 권한)
사전에 액세스 키 발급과 Billing에 관련된 권한 정책이 필요합니다.
> **Note**: 최소 권한 원칙에 따라 인보이스 조회 및 다운로드만 가능한 권한을 가진 IAM 사용자를 생성하는 것을 추천합니다.

**필수 IAM 권한 (Permissions)**:
```json
"Action": [
    "invoicing:ListInvoiceSummaries",
    "invoicing:GetInvoicePDF"
]
```

<img width="1112" height="175" alt="image" src="https://github.com/user-attachments/assets/5f8db6c4-9c00-4877-b4f6-91bf1d18269c" />
<img width="1755" height="485" alt="image" src="https://github.com/user-attachments/assets/5a4679ba-7803-4778-ad64-b57440add304" />

### 2. 로그인 및 조회
1. 접속하고자 하는 IAM 계정의 **Access Key ID**를 입력합니다.
2. 접속하고자 하는 계정의 **Secret Access Key**를 입력합니다.
3. **청구서를 발급할 월(Billing Month)**을 선택합니다.
    *   예) 12월 청구서 = 12월 1일 ~ 12월 31일 사용분 -> 1월 초(대략 2~3일경 발행)

## 파라미터 (Parameters)

*   **Access Key**: AWS IAM 사용자 액세스 키
*   **Secret Key**: AWS IAM 사용자 시크릿 키
*   **Select Month**: 조회할 청구 월 (YYYY-MM 형식)
