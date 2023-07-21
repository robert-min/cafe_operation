from jamo import h2j, j2hcj


def extract_korean_initial(text: str) -> str:
    result = ""
    for t in text:
        result += j2hcj(h2j(t))[0]
    return result

def make_respose(result: any) -> dict:
    return {
        "meta": {
            "code": 200,
            "message": "ok"
        },
        "data": result
    }