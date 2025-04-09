# src/klctool/hiragana.py

import os
import sys
import google.generativeai as genai
import re
from klctool.common import load_config, debug_print

def run(args, config):
    debug_print(args, "hiragana サブコマンド実行")
    debug_print(args, args, header="Command Line Args:")
    debug_print(args, config, header="Initial Config:")

    # 設定値の決定: コマンドラインオプションと設定ファイルをマージ
    output_suffix, model_name = _merge_configurations(args, config)
    # APIキーを決定: 1.コマンドラインオプション 2.環境変数 3.コマンドラインオプション(ファイル指定) 4.APIキーファイル(設定ファイル記載のファイル)
    api_key = _load_api_key(args, config)
    # プロンプト読み込み: 1.コマンドラインプション(ファイル名) 2.設定ファイル記載のファイル
    prompt_hiragana = _load_prompt_content(args, config)

    debug_print(args, f"Output Suffix: {output_suffix}")
    debug_print(args, f"Model Name: {model_name}")
    debug_print(args, f"Output Directory: {args.output_dir}")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    input_files = args.input_files
    debug_print(args, f"Input Files: {input_files}")

    hiragana_core(args, model, prompt_hiragana, output_suffix, args.output_dir)

    print("hiragana サブコマンド 完了 (AIによるひらがな変換処理を実行しました)")

def _merge_configurations(args, config):
    """コマンドラインオプションと設定ファイルの値をマージする"""
    hiragana_config = config.get('hiragana', {})
    output_suffix = args.output_suffix or hiragana_config.get('output_suffix')
    model_name = args.model_name or hiragana_config.get('model_name')
    return output_suffix, model_name


def _load_api_key(args, config):
    """APIキーをロードする"""
    hiragana_config = config.get('hiragana', {})
    api_key_file_config = hiragana_config.get('api_key_file')
    api_key_file_cli = args.api_key_file

    api_key = None
    api_key_source = "設定なし"

    if args.api_key:
        api_key = args.api_key
        api_key_source = "コマンドラインオプション --api-key"
    elif os.environ.get('GOOGLE_API_KEY'):
        api_key = os.environ.get('GOOGLE_API_KEY')
        api_key_source = "環境変数 GOOGLE_API_KEY"
    elif api_key_file_cli:
        api_key_path_cli = api_key_file_cli
        if not os.path.isabs(api_key_file_cli):
            api_key_path_cli = os.path.join('.', api_key_file_cli)
        if not os.path.exists(api_key_path_cli):
            print(f"エラー：APIキーファイルが見つかりません: {api_key_path_cli}", file=sys.stderr)
            sys.exit(1)
        debug_print(args, f"API Key File Path (CLI): {api_key_path_cli}")
        api_key_config_cli = load_config(api_key_path_cli, args)
        api_key = api_key_config_cli.get('api_key')
        api_key_source = f"コマンドライン指定APIキーファイル: {api_key_file_cli}"
    elif api_key_file_config:
        api_key_path_config = os.path.join(args.config_dir_path, api_key_file_config)
        debug_print(args, f"API Key File Path (Config): {api_key_path_config}")
        api_key_config_config = load_config(api_key_path_config, args)
        api_key = api_key_config_config.get('api_key')
        api_key_source = f"設定ファイル指定APIキーファイル: {api_key_file_config}"

    debug_print(args, f"API Key Source: {api_key_source}")
    debug_print(args, f"API Key: {api_key}")

    return api_key


def _load_prompt_content(args, config):
    """プロンプトファイルの読み込みとプロンプト内容の取得を行う"""
    hiragana_config = config.get('hiragana', {})
    prompt_file_config = hiragana_config.get('prompt_file')
    prompt_file_cli = args.prompt_file

    prompt_path = None

    if prompt_file_cli:
        prompt_path = prompt_file_cli
    elif prompt_file_config:
        prompt_path = os.path.join(args.config_dir_path, prompt_file_config)

    if prompt_path:
        debug_print(args, f"Prompt File Path (Before Process): {prompt_path}")
        if not os.path.isabs(prompt_path):
            prompt_path = os.path.join('.', prompt_path)
        if os.path.exists(prompt_path):
            debug_print(args, f"Prompt File Path: {prompt_path}")
            prompt_config = load_config(prompt_path, args)
            prompt_content = prompt_config.get('prompt_hiragana')
            if args.debug and prompt_content:
                debug_print(args, f"Prompt Content: {prompt_content}")
        else:
            debug_print(args, f"警告：プロンプトファイルが見つかりません: {prompt_path}")
    else:
        debug_print(args, "プロンプトファイル: 設定なし")

    return prompt_content


def hiragana_core(args, model, prompt_hiragana, output_suffix, output_dir):
    """ひらがな化のコア処理を実行する
    Args:
        args: argparse.Namespace - コマンドライン引数
        config: dict - 設定ファイルの内容
        model: google.generativeai.GenerativeModel - Gemini API モデル
        prompt_hiragana: str - ひらがな化プロンプト
        output_suffix: str - 出力ファイルサフィックス
        output_dir: str - 出力ディレクトリ
    """
    for lyrics_file_path in args.input_files:
        debug_print(args, f"ひらがな化処理を実行: {lyrics_file_path}")

        try:
            with open(lyrics_file_path, 'r', encoding='utf-8') as f:
                lyrics_markdown = f.read()
        except FileNotFoundError:
            print(f"エラー: 歌詞ファイルが見つかりませんでした: {lyrics_file_path}")
            continue

        yaml_part, heading_part, lyrics_body = parse_markdown_lyrics(lyrics_markdown)
        lyrics_body = re.sub(r'!\[.*?\]\(.*?\)', '', lyrics_body)

        hiragana_lyrics = generate_hiragana_lyrics_with_gemini(model, prompt_hiragana, lyrics_body)

        if hiragana_lyrics:
            output_file_path = generate_output_file_path(lyrics_file_path, output_suffix, output_dir)
            output_markdown = create_output_markdown(yaml_part, heading_part, hiragana_lyrics, lyrics_body)

            try:
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(output_markdown)
                print(f"ひらがな化された歌詞を保存しました: {output_file_path}")
            except Exception as e:
                print(f"エラー: ファイル保存に失敗しました: {output_file_path} - {e}")
        else:
            print(f"エラー: ひらがな歌詞の生成に失敗しました: {lyrics_file_path}")


def parse_markdown_lyrics(markdown_text):
    """マークダウン形式の歌詞ファイルを解析する"""
    parts = re.split(r'^---$', markdown_text, maxsplit=2, flags=re.MULTILINE)
    yaml_part = parts[1].strip() if len(parts) > 1 else ""
    content_after_yaml = parts[-1].strip()

    heading_match = re.match(r'^(# .+?)\n', content_after_yaml, re.MULTILINE)
    heading_part = heading_match.group(1).strip() if heading_match else ""

    lyrics_body_start = heading_match.end() if heading_match else 0
    lyrics_body = content_after_yaml[lyrics_body_start:].strip()

    return yaml_part, heading_part, lyrics_body


def generate_hiragana_lyrics_with_gemini(model, prompt, lyrics_body):
    """Gemini API を使用して歌詞をひらがな化する"""
    try:
        response = model.generate_content(prompt + "\n" + lyrics_body)
        hiragana_text = response.text
        hiragana_text = re.sub(r"^(.*)(?<!  )$", r"\1  ", hiragana_text, flags=re.MULTILINE)
#        hiragana_text = re.sub(r"^(\S+)(.*)$", r"\1\2  ", hiragana_text, flags=re.MULTILINE)

        return hiragana_text
    except Exception as e:
        print(f"Gemini API エラー: {e}")
        return None


def generate_output_file_path(input_file_path, suffix, output_dir=None):
    """出力ファイルのパスを生成する"""
    base, ext = os.path.splitext(input_file_path)
    output_file_name = base + suffix + ext
    if output_dir:
        output_file_path = os.path.join(output_dir, os.path.basename(output_file_name))
    else:
        output_file_path = output_file_name
    return output_file_path


def create_output_markdown(yaml_part, heading_part, hiragana_lyrics, original_lyrics):
    """ひらがな歌詞を挿入したマークダウンテキストを生成する"""

    output_markdown = ""
    if yaml_part:
        output_markdown += "---\n" + yaml_part + "\n---\n"
    if heading_part:
        output_markdown += heading_part + "\n\n"
    if hiragana_lyrics:
        output_markdown += hiragana_lyrics + "\n\n\n"
    if original_lyrics:
        output_markdown += original_lyrics
    return output_markdown
