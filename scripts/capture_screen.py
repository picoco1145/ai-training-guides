#!/usr/bin/env python3
"""헤드리스 브라우저 캡처 + PIL 어노테이션 (Track A)

이 스크립트는 gstack /browse 스킬의 스크린샷을 후처리하여
화살표, 하이라이트 박스, 번호 배지 등의 어노테이션을 합성합니다.

실제 캡처는 /browse 스킬이 수행하고, 이 스크립트는 어노테이션만 담당합니다.
"""

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    logging.error("Pillow 필요: pip3 install Pillow --user")
    sys.exit(1)


# 한글 폰트 경로
FONT_PATH = "/System/Library/Fonts/AppleSDGothicNeo.ttc"


def load_font(size: int = 20) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except OSError:
        return ImageFont.load_default()


def add_highlight_box(img: Image.Image, x: int, y: int, w: int, h: int,
                      label: str = "", color: str = "red") -> Image.Image:
    """이미지에 하이라이트 박스 + 라벨 추가"""
    draw = ImageDraw.Draw(img)
    outline_color = {"red": (255, 0, 0), "blue": (0, 100, 255), "green": (0, 180, 0)}.get(color, (255, 0, 0))

    # 반투명 효과를 위해 테두리만 3px
    for i in range(3):
        draw.rectangle([x - i, y - i, x + w + i, y + h + i], outline=outline_color)

    if label:
        font = load_font(18)
        # 라벨 배경
        bbox = draw.textbbox((0, 0), label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.rectangle([x, y - th - 8, x + tw + 10, y], fill=outline_color)
        draw.text((x + 5, y - th - 6), label, fill="white", font=font)

    return img


def add_arrow(img: Image.Image, x: int, y: int, label: str = "",
              direction: str = "down", color: str = "red") -> Image.Image:
    """이미지에 화살표 + 라벨 추가"""
    draw = ImageDraw.Draw(img)
    arrow_color = {"red": (255, 0, 0), "blue": (0, 100, 255)}.get(color, (255, 0, 0))
    arrow_len = 40
    head_size = 12

    # 화살표 방향별 좌표 계산
    if direction == "down":
        end_y = y + arrow_len
        draw.line([(x, y), (x, end_y)], fill=arrow_color, width=3)
        draw.polygon([(x, end_y + head_size), (x - head_size, end_y), (x + head_size, end_y)], fill=arrow_color)
    elif direction == "right":
        end_x = x + arrow_len
        draw.line([(x, y), (end_x, y)], fill=arrow_color, width=3)
        draw.polygon([(end_x + head_size, y), (end_x, y - head_size), (end_x, y + head_size)], fill=arrow_color)
    elif direction == "left":
        end_x = x - arrow_len
        draw.line([(x, y), (end_x, y)], fill=arrow_color, width=3)
        draw.polygon([(end_x - head_size, y), (end_x, y - head_size), (end_x, y + head_size)], fill=arrow_color)

    if label:
        font = load_font(16)
        draw.text((x + 15, y - 10), label, fill=arrow_color, font=font)

    return img


def add_number_badge(img: Image.Image, x: int, y: int, number: int,
                     color: str = "red") -> Image.Image:
    """이미지에 번호 배지(원형) 추가"""
    draw = ImageDraw.Draw(img)
    badge_color = {"red": (255, 0, 0), "blue": (0, 100, 255), "green": (0, 180, 0)}.get(color, (255, 0, 0))
    radius = 16

    draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=badge_color)
    font = load_font(18)
    text = str(number)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((x - tw // 2, y - th // 2), text, fill="white", font=font)

    return img


def annotate_image(input_path: Path, output_path: Path, annotations: list[dict]) -> Path:
    """스크린샷에 어노테이션 합성"""
    img = Image.open(input_path).convert("RGB")

    for ann in annotations:
        ann_type = ann.get("type")
        if ann_type == "highlight":
            img = add_highlight_box(img, ann["x"], ann["y"], ann["w"], ann["h"],
                                    ann.get("label", ""), ann.get("color", "red"))
        elif ann_type == "arrow":
            img = add_arrow(img, ann["x"], ann["y"], ann.get("label", ""),
                            ann.get("direction", "down"), ann.get("color", "red"))
        elif ann_type == "badge":
            img = add_number_badge(img, ann["x"], ann["y"], ann["number"],
                                   ann.get("color", "red"))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")
    logging.info(f"어노테이션 완료: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="스크린샷 어노테이션 합성")
    parser.add_argument("--input", required=True, help="원본 스크린샷 경로")
    parser.add_argument("--output", required=True, help="출력 경로")
    parser.add_argument("--annotations", required=True,
                        help='JSON 배열 문자열: [{"type":"highlight","x":10,"y":10,"w":200,"h":100,"label":"여기"}]')
    args = parser.parse_args()

    import json
    annotations = json.loads(args.annotations)
    annotate_image(Path(args.input), Path(args.output), annotations)


if __name__ == "__main__":
    main()
