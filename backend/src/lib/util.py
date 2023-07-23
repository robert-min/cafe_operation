"""Util library

Functions:
    - extract_korean_initial: 초성 검색을 위해 아이템 이름의 초성을 추출합니다.
    - make_respose: 공통된 API 응답을 위해 response를 생성합니다.
"""
from jamo import h2j, j2hcj

def extract_korean_initial(text: str) -> str:
    """Extract korean initial for searching."""
    result = ""
    for t in text:
        result += j2hcj(h2j(t))[0]
    return result

def make_respose(result: any) -> dict:
    """Make api response format."""
    return {
        "meta": {
            "code": 200,
            "message": "ok"
        },
        "data": result
    }
