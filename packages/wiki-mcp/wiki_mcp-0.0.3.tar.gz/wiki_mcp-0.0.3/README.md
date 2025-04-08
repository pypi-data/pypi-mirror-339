# Wiki-MCP 서버

Wiki 서비스를 위한 MCP(Model Context Protocol) 서버입니다.

## 설치 및 설정

### 사전 요구사항
- Python 3.10 이상
- [uv](https://github.com/astral-sh/uv) 설치
- [fastmcp](https://github.com/jlowin/fastmcp) 설치

### 설치 방법

1. 저장소를 클론합니다:
```
git clone <repository-url>
cd wiki-mcp
```

2. uv를 사용하여 가상 환경을 생성하고 의존성을 설치합니다:
```
uv venv
uv pip install -r requirements.txt
```

개발 의존성도 설치하려면:
```
uv pip install -e ".[dev]"
```

## 환경 변수 설정

`.env` 파일을 루트 디렉토리에 생성하고 필요한 환경 변수를 설정합니다:

```
API_KEY=your_api_key_here
DEBUG=True
```

## MCP 서버 실행 방법

### 개발 모드에서 실행 (권장)
MCP Inspector를 사용하여 서버를 테스트하고 디버그할 수 있습니다:

```
fastmcp dev server.py
```

### Claude Desktop에 설치
서버가 준비되면 Claude Desktop에 설치하여 사용할 수 있습니다:

```
fastmcp install server.py
```

환경 변수 설정과 함께 설치:
```
fastmcp install server.py -e API_KEY=abc123 -e DEBUG=True
```

또는 .env 파일에서 환경 변수 로드:
```
fastmcp install server.py -f .env
```

### 직접 실행
고급 시나리오용:

```
fastmcp run server.py
# 또는
python server.py
```

## MCP 서버 구성하기

서버는 도구(tools), 리소스(resources), 프롬프트(prompts)로 구성됩니다:

### 도구 추가하기
```python
@mcp.tool()
def my_tool(param1: str, param2: int) -> str:
    """도구 설명"""
    return f"결과: {param1}, {param2}"
```

### 리소스 추가하기
```python
@mcp.resource("my-resource://{param}")
def my_resource(param: str) -> str:
    """리소스 설명"""
    return f"리소스 데이터: {param}"
```

### 프롬프트 추가하기
```python
@mcp.prompt()
def my_prompt(query: str) -> str:
    """프롬프트 설명"""
    return f"다음 정보를 처리해주세요: {query}"
```

## 개발

### 코드 포맷팅

```
black .
isort .
```

### 린팅

```
ruff check .
```

### 타입 체크

```
mypy .
```

## 테스트

```
pytest
``` 