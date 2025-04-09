# src/klctool/convert2odt.py

import os
import subprocess
from klctool.common import debug_print


def run(args, config):
    debug_print(args, "convert2odt サブコマンド実行")
    debug_print(args, args, header="Args:")
    debug_print(args, config, header="Initial Config:")

    template_odt_path, lua_script_path, output_dir = _prepare_convert2odt_config(args, config)

    debug_print(args, f"Template ODT Path: {template_odt_path}")
    debug_print(args, f"Lua Script Path: {lua_script_path}")
    debug_print(args, f"Output Directory: {output_dir}")

    convert2odt_core(args, template_odt_path, lua_script_path, output_dir)

    print("convert2odt サブコマンド 完了 (ODT変換処理を実行しました)")


def _prepare_convert2odt_config(args, config):
    """convert2odt サブコマンドの設定を準備する (設定マージ、パス解決)"""
    odt_config = config.get('odt', {})
    config_dir = args.config_dir_path

    lua_script_name = odt_config.get('lua_script_name', "klctool-edit.lua")
    template_name = odt_config.get('template_name', "klctool.odt")

    lua_script_path = args.lua_script or os.path.join(config_dir, lua_script_name)
    template_odt_path = args.template_odt or os.path.join(config_dir, template_name)
    output_dir = args.output_dir

    return template_odt_path, lua_script_path, output_dir


def convert2odt_core(args, template_odt_path, lua_script_path, output_dir):
    """convert2odt のコア処理を実行する

    Args:
        args: argparse.Namespace - コマンドライン引数
        config: dict - 設定ファイルの内容
        template_odt_path: str - テンプレート ODT ファイルパス
        lua_script_path: str - Lua スクリプトファイルパス
        output_dir: str - 出力ディレクトリ
    """
    lyrics_files = args.input_files

    print("ODT変換処理を開始します。")

    for input_file_path in lyrics_files:

        output_file_path = generate_output_file_path(input_file_path, template_odt_path, output_dir, args)
        if not output_file_path:
            print(f"  エラー: 出力ファイルパスの生成に失敗しました: {input_file_path}")
            continue

        if not os.path.exists(template_odt_path):
            print(f"  エラー: テンプレート ODT ファイルが見つかりません: {template_odt_path}")
            print(f"  設定ファイル ({args.config_file_path}) の [odt] セクションで template_name が正しく設定されているか確認してください。")
            continue

        if not os.path.exists(lua_script_path):
            print(f"  エラー: Lua フィルタースクリプトが見つかりません: {lua_script_path}")
            print(f"  設定ファイル ({args.config_file_path}) の [odt] セクションで lua_script_name が正しく設定されているか確認してください。")
            continue

        result = convert_markdown_to_odt_with_pandoc(input_file_path, output_file_path, lua_script_path, template_odt_path, args)

        if result:
            print(f"  ODT 変換成功: {output_file_path}")
        else:
            print(f"  ODT 変換失敗: {input_file_path} -> {output_file_path}")

    print("ODT変換処理を完了しました。")


def generate_output_file_path(input_file_path, template_odt_path, output_dir=None, args=None): # 引数に args を追加
    """出力ファイルのパスを生成する (convert-odt 用)"""
    debug_print(args, f"● カレントディレクトリ: {os.getcwd()}", header="[generate_output_file_path]")
    debug_print(args, f"input_file_path: {input_file_path}", header="[generate_output_file_path]")
    debug_print(args, f"output_dir: {output_dir}", header="[generate_output_file_path]")
    debug_print(args, f"template_odt_path: {template_odt_path}", header="[generate_output_file_path]")

    base, ext = os.path.splitext(input_file_path)
    if base.endswith("_hiragana"):
        base = base[:-len("_hiragana")]

    output_file_name = os.path.basename(base) + ".odt"


    if output_dir:
        output_file_path = os.path.join(output_dir, os.path.basename(output_file_name))
    else:
        absolute_input_file_path = os.path.abspath(input_file_path)
        input_dir = os.path.dirname(absolute_input_file_path)
        output_file_path = os.path.join(input_dir, output_file_name)

    debug_print(args, f"output_file_path: {output_file_path}", header="[generate_output_file_path]")

    return output_file_path


def convert_markdown_to_odt_with_pandoc(input_file_path, output_file_path, lua_script_path, template_odt_path, args): # ★ args を引数に追加 ★
    """Pandoc を使用して Markdown ファイルを ODT 形式に変換する"""
    command = [
        "pandoc",
        "-f", "markdown+hard_line_breaks+yaml_metadata_block+raw_attribute",
        "-s", # スタンドアロンな ODT ファイルを生成
        "-o", output_file_path, # 出力ファイルパスを指定
        "--reference-doc", template_odt_path, # テンプレート ODT ファイルを指定
        "--lua-filter", lua_script_path, # Lua フィルタースクリプトを指定
        input_file_path, # 入力ファイルパス
    ]

    try:
        debug_print(args, f"{' '.join(command)}", header="Pandoc コマンド:")
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{e}", header="Pandoc エラー:")
        return False
    except FileNotFoundError:
        print("  エラー: Pandoc コマンドが見つかりません。Pandoc がインストールされているか、PATH が通っているか確認してください。")
        return False
