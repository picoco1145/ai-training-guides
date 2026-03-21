#!/usr/bin/env python3
"""Notion File Upload API 래퍼

이미지 파일을 Notion에 직접 업로드하고 file_upload ID를 반환합니다.
이 ID를 image 블록의 file_upload 타입에 사용합니다.

제한:
- 20MB 이하: single_part 업로드
- 업로드 후 1시간 내 블록에 첨부 필수
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

import requests

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

NOTION_API_VERSION = "2022-06-28"


def get_api_key() -> str:
    """NOTION_API_KEY 환경변수에서 API 키 로드"""
    key = os.environ.get("NOTION_API_KEY")
    if not key:
        logging.error("NOTION_API_KEY 환경변수가 설정되지 않았습니다.")
        sys.exit(1)
    return key


def upload_file(file_path: Path, api_key: str) -> dict:
    """Notion File Upload API로 파일 업로드 → file_upload 객체 반환"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_API_VERSION,
    }

    # Step 1: 업로드 생성
    create_resp = requests.post(
        "https://api.notion.com/v1/file-uploads",
        headers={**headers, "Content-Type": "application/json"},
        json={"mode": "single_part", "filename": file_path.name},
    )
    create_resp.raise_for_status()
    upload_obj = create_resp.json()
    upload_id = upload_obj["id"]
    upload_url = upload_obj["upload_url"]

    # Step 2: 파일 전송
    with open(file_path, "rb") as f:
        send_resp = requests.put(
            upload_url,
            headers={"Authorization": f"Bearer {api_key}", "Notion-Version": NOTION_API_VERSION},
            files={"file": (file_path.name, f, "image/png")},
        )
    send_resp.raise_for_status()

    logging.info(f"업로드 완료: {file_path.name} → ID: {upload_id}")
    return {"id": upload_id, "filename": file_path.name}


def upload_images(image_dir: Path) -> list[dict]:
    """디렉토리 내 모든 PNG 이미지를 Notion에 업로드"""
    api_key = get_api_key()
    results = []

    png_files = sorted(image_dir.glob("*.png"))
    if not png_files:
        logging.warning(f"PNG 파일 없음: {image_dir}")
        return results

    for img_path in png_files:
        try:
            result = upload_file(img_path, api_key)
            results.append(result)
        except requests.HTTPError as e:
            logging.error(f"업로드 실패 ({img_path.name}): {e}")
            logging.error(f"응답: {e.response.text if e.response else 'N/A'}")

    return results


def main():
    parser = argparse.ArgumentParser(description="이미지를 Notion에 직접 업로드")
    parser.add_argument("--dir", required=True, help="이미지 디렉토리 경로")
    parser.add_argument("--output-json", help="결과 JSON 저장 경로 (선택)")
    args = parser.parse_args()

    results = upload_images(Path(args.dir))

    if args.output_json:
        with open(args.output_json, "w") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logging.info(f"결과 저장: {args.output_json}")

    # stdout에도 출력
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
