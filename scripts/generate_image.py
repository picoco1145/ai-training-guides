#!/usr/bin/env python3
"""Gemini Imagen API로 개념도/흐름도 이미지 생성 (Track B)"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def load_api_key() -> str:
    """vocab_cards config에서 Gemini API 키 로드"""
    config_path = Path.home() / "vocab_cards" / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"config.json 없음: {config_path}")
    with open(config_path) as f:
        config = json.load(f)
    return config["gemini"]["api_key"]


def generate_image(prompt: str, style: str, output_path: Path) -> Path:
    """Gemini Imagen API로 이미지 생성. 3회 재시도."""
    from google import genai
    from google.genai import types

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)
    model = "gemini-3.1-flash-image-preview"

    # 스타일별 프롬프트 보강
    style_prefix = {
        "diagram": "Clean flat-design diagram. Minimal text, use icons and shapes. ",
        "concept": "Clean concept illustration. Simple flat design, no complex textures. ",
        "workflow": "Workflow flowchart with arrows. Clean layout, minimal text. ",
    }
    full_prompt = style_prefix.get(style, "") + prompt
    full_prompt += "\nOutput as a single 1024x768 image. White background."

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=model,
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"]
                ),
            )
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, "wb") as f:
                        f.write(part.inline_data.data)
                    logging.info(f"이미지 저장: {output_path}")
                    return output_path

            raise ValueError("API 응답에 이미지 데이터 없음")
        except Exception as e:
            logging.warning(f"생성 실패 (시도 {attempt + 1}/3): {e}")
            if attempt < 2:
                time.sleep(5)

    logging.error("이미지 생성 3회 모두 실패")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Gemini Imagen으로 이미지 생성")
    parser.add_argument("--prompt", required=True, help="이미지 프롬프트")
    parser.add_argument("--style", default="diagram", choices=["diagram", "concept", "workflow"])
    parser.add_argument("--output", required=True, help="출력 경로 (PNG)")
    args = parser.parse_args()

    generate_image(args.prompt, args.style, Path(args.output))


if __name__ == "__main__":
    main()
