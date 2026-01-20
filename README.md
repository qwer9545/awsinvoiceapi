# awsinvoiceapi
[AWS Get Invoice PDF API] (https://aws.amazon.com/ko/about-aws/whats-new/2025/11/get-invoice-pdf-api/)

오늘 AWS는 고객이 SDK 호출을 통해 프로그래밍 방식으로 AWS 인보이스를 다운로드할 수 있는 Get Invoice PDF API의 정식 출시를 발표했습니다.

고객은 AWS 인보이스 ID를 입력으로 사용하는 API 직접 호출을 통해 개별 인보이스 PDF 아티팩트를 검색하고, AWS 인보이스 및 추가 문서를 PDF 형식으로 즉시 다운로드할 수 있도록 미리 서명된 Amazon S3 URL을 수신할 수 있습니다. 대량 인보이스 검색의 경우 고객은 먼저 List Invoice Summaries API를 직접적으로 호출하여 특정 청구 기간의 인보이스 ID를 가져온 다음 인보이스 ID를 Get Invoice API의 입력으로 사용하여 각 인보이스 PDF 아티팩트를 다운로드할 수 있습니다.

Get Invoice PDF API는 미국 동부(버지니아 북부) 리전에서 사용할 수 있습니다. 모든 상용 리전(중국 리전 제외)의 고객이 이 서비스를 이용할 수 있습니다. Get Invoice PDF API를 시작하려면 API 설명서를 참조하세요.

# 사용 방법

# 파라미터
- Access Key
- Secret Key
- Select Month
