# src/klctool/adjustimage.py

import os
import sys
from PIL import Image, ImageColor, UnidentifiedImageError
from klctool.common import load_config, debug_print


def run(args, config):
    debug_print(args, "adjustimage サブコマンド実行")
    debug_print(args, args, header="Args:")
    debug_print(args, config, header="Initial Config:")

    paper_aspect_ratio, paper_width_px, paper_height_px, mask_strength, mask_color, output_suffix, movie_aspect_ratio, fit_mode = _prepare_adjustimage_config(args, config)

    debug_print(args, f"Mask Strength: {mask_strength}")
    debug_print(args, f"Mask Color: {mask_color}")
    debug_print(args, f"Output Suffix: {output_suffix}")
    debug_print(args, f"Movie Aspect Ratio: {movie_aspect_ratio}")
    debug_print(args, f"Paper Aspect Ratio: {paper_aspect_ratio}")
    debug_print(args, f"Paper Width (px): {paper_width_px}")
    debug_print(args, f"Paper Height (px): {paper_height_px}")

    image_files = args.input_files
    debug_print(args, f"Input Files: {image_files}")

    adjustimage_core(args, image_files, movie_aspect_ratio, paper_aspect_ratio, paper_width_px, paper_height_px, mask_strength, mask_color, output_suffix, fit_mode)


def _prepare_adjustimage_config(args, config):
    adjimg_config = config.get('adjust-image', {})
    paper_size_file_config = adjimg_config.get('paper_size_file')

    config_dir = args.config_dir_path

    paper_size_file_path = os.path.join(config_dir, paper_size_file_config)
    paper_size_config = load_config(paper_size_file_path, args)

    paper_size = args.paper_size or adjimg_config.get('paper_size')
    mask_strength = args.mask_strength or adjimg_config.get('mask_strength')
    mask_color = args.mask_color or adjimg_config.get('mask_color')
    output_suffix = args.output_suffix or adjimg_config.get('suffix')
    movie_aspect_ratio = args.movie_aspect_ratio or adjimg_config.get('movie_aspect_ratio')
    dpi = args.dpi or adjimg_config.get('dpi')
    fit_mode = args.fit_mode or adjimg_config.get('fit_mode')

    paper_width_px, paper_height_px = _get_paper_size_px(paper_size, paper_size_config, dpi)
    paper_aspect_ratio = paper_width_px / paper_height_px

    return paper_aspect_ratio, paper_width_px, paper_height_px, mask_strength, mask_color, output_suffix, movie_aspect_ratio, fit_mode


def adjustimage_core(args, image_files, movie_aspect_ratio, paper_aspect_ratio, paper_width_px, paper_height_px, mask_strength, mask_color, output_suffix, fit_mode):
    print("画像調整処理を開始します。")
    for input_file_path in image_files:
        print(f"  処理ファイル: {input_file_path}")
        output_file_path = process_image(input_file_path, movie_aspect_ratio, paper_aspect_ratio, paper_width_px, paper_height_px, mask_strength, mask_color, output_suffix, fit_mode, args)
        if output_file_path:
            print(f"  背景画像処理成功: {input_file_path} -> {output_file_path}")
        else:
            print(f"  背景画像処理失敗: {input_file_path}")
    print("画像調整処理を完了しました。")


def resize_to_paper_size(img, paper_width_px, paper_height_px):
    """画像をペーパーサイズ内に収まるようにリサイズする（アスペクト比維持）"""
    img_width, img_height = img.size
    width_scale = paper_width_px / img_width
    height_scale = paper_height_px / img_height
    scale = min(width_scale, height_scale) # 幅と高さ方向のスケールを比較して小さい方を採用（両方がペーパーサイズ内に収まるように）
    new_width_px = int(img_width * scale)
    new_height_px = int(img_height * scale)
    resized_img = img.resize((new_width_px, new_height_px), Image.LANCZOS)
    return resized_img


def apply_paper_size_resize(img, paper_width_px, paper_height_px, args):
    """画像をペーパーサイズに合わせてリサイズ処理を行う (リサイズが必要な場合のみ)"""
    debug_print(args, "【process_image】リサイズ処理開始前：padded_img サイズ", header="[DEBUG]")
    debug_print(args, f"幅: {img.width}px, 高さ: {img.height}px", header="[DEBUG] padded_img size:")
    debug_print(args, f"用紙サイズ: 幅: {paper_width_px}px, 高さ: {paper_height_px}px", header="[DEBUG] paper_size:")

    resized_img = img
    if img.width > paper_width_px or img.height > paper_height_px: # 画像がペーパーサイズより大きい場合のみリサイズ
        debug_print(args, "【process_image】リサイズ処理実行", header="[DEBUG]")
        resized_img = resize_to_paper_size(img, paper_width_px, paper_height_px)
        debug_print(args, "【process_image】リサイズ処理完了", header="[DEBUG]")
        debug_print(args, "【process_image】リサイズ後：resized_img サイズ", header="[DEBUG]")
        debug_print(args, f"幅: {resized_img.width}px, 高さ: {resized_img.height}px", header="[DEBUG] resized_img size:")
    else:
        debug_print(args, "【process_image】リサイズ不要", header="[DEBUG]")

    return resized_img


def process_image(input_file_path, movie_aspect_ratio, paper_aspect_ratio, paper_width_px, paper_height_px, mask_strength, mask_color, suffix, fit_mode, args):
    """画像処理を実行して出力ファイルパスを返す"""
    try:
        img = Image.open(input_file_path)
    except UnidentifiedImageError:
        print(f"エラー: ファイル '{input_file_path}' は画像ファイルとして認識できません。", file=sys.stderr)
        return None
    except FileNotFoundError:
        print(f"エラー: ファイル '{input_file_path}' が見つかりません。", file=sys.stderr)
        return None
    except Exception as e:
        print(f"エラー: 画像ファイル '{input_file_path}' の読み込み中にエラーが発生しました: {e}", file=sys.stderr)
        return None

    trimmed_img = trim_image_auto(img, movie_aspect_ratio)
    if trimmed_img is None:
        return None

    if args.debug:
        trim_output_file = generate_output_file_path(input_file_path, "_trimmed", args.output_dir)
        trimmed_img.save(trim_output_file)
        debug_print(args, f"トリミング後の画像を '{trim_output_file}' に保存しました。")

    masked_img = apply_mask(trimmed_img, mask_color, mask_strength)

    if args.debug:
        masked_output_file = generate_output_file_path(input_file_path, "_masked", args.output_dir)
        masked_img.save(masked_output_file)
        debug_print(args, f"マスク後の画像を '{masked_output_file}' に保存しました。")

    if fit_mode == "pad":
        fit_img = add_padding(masked_img, paper_aspect_ratio)
    else:
        fit_img = trim_image_auto(masked_img, paper_aspect_ratio)

    resized_img = apply_paper_size_resize(fit_img, paper_width_px, paper_height_px, args)

    debug_print(args, "【process_image】generate_output_file_path 呼び出し直前：args の状態", header="[DEBUG]")
    debug_print(args, args, header="[DEBUG] args:")
    debug_print(args, f"【process_image】output_dir の値: {args.output_dir}", header="[DEBUG]")
    output_file_path = generate_output_file_path(input_file_path, suffix, args.output_dir)
    resized_img.save(output_file_path)

    debug_print(args, "設定:", header="adjustimage 設定")
    debug_print(args, f"マスクの強さ: {mask_strength}")
    debug_print(args, f"マスクの色: {mask_color}")
    debug_print(args, f"サフィックス: {suffix}")
    debug_print(args, f"ムービーアスペクト比: {movie_aspect_ratio}")
    debug_print(args, f"出力画像アスペクト比: {paper_aspect_ratio}")
    debug_print(args, f"用紙幅 (px): {paper_width_px}")
    debug_print(args, f"用紙高さ (px): {paper_height_px}")
    debug_print(args, f"入力ファイル: {input_file_path}")
    debug_print(args, f"余白追加後の画像を '{output_file_path}' に保存しました。")

    return output_file_path


def _get_paper_size_px(paper_size, paper_size_config, dpi):
    if paper_size not in paper_size_config.get("paper_sizes", {}):
        print(f"エラー: 用紙サイズ '{paper_size}' は設定ファイルに定義されていません。", file=sys.stderr)
        print("設定ファイルの [adjust-image] セクションで paper_size_file が正しく設定されているか確認してください。", file=sys.stderr)
        sys.exit(1)

    paper_width_mm = paper_size_config["paper_sizes"][paper_size]["width"]
    paper_height_mm = paper_size_config["paper_sizes"][paper_size]["height"]

    # DPIに基づいてピクセル数を計算
    inches_per_mm = 1 / 25.4
    paper_width_px = int(paper_width_mm * inches_per_mm * dpi)
    paper_height_px = int(paper_height_mm * inches_per_mm * dpi)
    return paper_width_px, paper_height_px


def trim_image_auto(img, aspect_ratio):
    width, height = img.size
    player_aspect_ratio = width / height

    if not isinstance(aspect_ratio, (int, float)):
        print(f"エラー: アスペクト比 '{aspect_ratio}' は数値（floatまたはint）で指定してください。", file=sys.stderr)
        return None

    aspect_ratio_float = float(aspect_ratio)

    if player_aspect_ratio > aspect_ratio_float:
        target_width = int(height * aspect_ratio_float)
        left = (width - target_width) // 2
        right = left + target_width
        top = 0
        bottom = height
    else:
        target_height = int(width / aspect_ratio_float)
        top = (height - target_height) // 2
        bottom = top + target_height
        left = 0
        right = width

    trimmed_img = img.crop((left, top, right, bottom))
    return trimmed_img


def apply_mask(img, mask_color, mask_strength):
    try:
        if not isinstance(img, Image.Image):
            print("エラー: apply_maskに有効な画像オブジェクトが渡されませんでした。", file=sys.stderr)
            return img
        color = ImageColor.getrgb(mask_color)
    except ValueError:
        if mask_color.lower() == "white":
            color = (255, 255, 255)
        elif mask_color.lower() == "black":
            color = (0, 0, 0)
        else:
            print(f"エラー: マスクの色 '{mask_color}' の形式が不正です。", file=sys.stderr)
            return img

    img = img.convert("RGBA")
    mask = Image.new("RGBA", img.size, color)
    alpha = int(255 * mask_strength / 100)
    mask.putalpha(alpha)
    return Image.alpha_composite(img, mask)


def add_padding(img, paper_aspect_ratio):
    """画像に余白を追加する (シンプルロジック)"""
    img_aspect_ratio = img.width / img.height

    if img_aspect_ratio > paper_aspect_ratio:
        # 入力画像の方が横長: 上下に余白を追加 (入力画像の幅を基準)
        new_height_px = int(img.width / paper_aspect_ratio)
        new_img = Image.new("RGBA", (img.width, new_height_px), (0, 0, 0, 0))
        new_img.paste(img, (0, (new_height_px - img.height) // 2))
    else:
        # 目標アスペクト比の方が横長: 左右に余白を追加 (入力画像の高さを基準)
        new_width_px = int(img.height * paper_aspect_ratio)
        new_img = Image.new("RGBA", (new_width_px, img.height), (0, 0, 0, 0))
        new_img.paste(img, ((new_width_px - img.width) // 2, 0))

    return new_img


def generate_output_file_path(input_file_path, suffix, output_dir=None):
    base, ext = os.path.splitext(input_file_path)
    output_file_name = base + suffix + ".png"
    if output_dir:
        output_file_path = os.path.join(output_dir, os.path.basename(output_file_name))
    else:
        output_file_path = output_file_name

    return output_file_path
