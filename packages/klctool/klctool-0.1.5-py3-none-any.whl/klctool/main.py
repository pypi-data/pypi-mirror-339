# src/klctool/main.py

import argparse
import os

from klctool.common import initialize_config_directory, load_config, debug_print

import klctool.hiragana
import klctool.convert2odt
import klctool.adjustimage

# デバッグモード: args.debugを参照
# 設定ファイル格納ディレクトリ: args.config_dir_pathを参照

def main():
    parser = argparse.ArgumentParser(description="歌詞カード作成支援ツール")
    parser.add_argument("--debug", "-d", action="store_true", help="デバッグモードを有効にする")
    parser.add_argument("--config-dir", "-c", type=str, help="設定ファイルのディレクトリを指定する")

    subparsers = parser.add_subparsers(title="サブコマンド", dest="subcommand")

    # サブコマンド定義
    subcommands_config = {
        "hiragana": {
            "aliases": ["hira"],
            "help": "歌詞ファイルにひらがなを追加",
            "module": klctool.hiragana.run,
            "arguments": [
                {"name": "input_files", "nargs": "+", "help": "入力ファイル  複数指定可能"},
                {"name": "--output-dir", "type": str, "help": "出力フォルダ", "short": "-o"},
                {"name": "--output-suffix", "type": str, "help": "出力ファイル名サフィックス", "short": "-s"},
                {"name": "--model-name", "type": str, "help": "AIモデル名", "short": "-m"},
                {"name": "--api-key-file", "type": str, "help": "APIキーファイル名", "short": "-a"},
                {"name": "--api-key", "type": str, "help": "APIキー", "short": "-k"},
                {"name": "--prompt-file", "type": str, "help": "プロンプト格納ファイル名", "short": "-p"},
            ],
        },
        "convert2odt": {
            "aliases": ["odt"],
            "help": "歌詞ファイルをODTに変換",
            "module": klctool.convert2odt.run,
            "arguments": [
                {"name": "input_files", "nargs": "+", "help": "入力ファイル 複数指定可能"},
                {"name": "--output-dir", "type": str, "help": "出力フォルダ", "short": "-o"},
                {"name": "--template-odt", "type": str, "help": "テンプレートODTファイルパス","short": "-t"},
                {"name": "--lua-script", "type": str, "help": "Luaスクリプトファイルパス", "short": "-s"},
            ],
        },
        "adjustimage": {
            "aliases": ["img"],
            "help": "画像を歌詞カード用に調整",
            "module": klctool.adjustimage.run,
            "arguments": [
                {"name": "input_files", "nargs": "+", "help": "入力画像ファイル 複数指定可能"},
                {"name": "--output-dir", "type": str, "help": "出力フォルダ", "short": "-o"},
                {"name": "--paper-size", "type": str, "help": "用紙サイズ", "short": "-p"},
                {"name": "--mask-strength", "type": int, "default": 80, "help": "マスク強度 単位 %%", "short": "-m"},
                {"name": "--mask-color", "type": str, "default": "white", "help": "マスク色", "short": "-c"},
                {"name": "--output-suffix", "type": str, "help": "出力ファイル名サフィックス", "short": "-s"},
                {"name": "--movie-aspect-ratio", "type": float, "help": "アスペクト比", "short": "-a"},
                {"name": "--dpi", "type": int, "help": "出力画像のDPI", "short": "-d"},
                {"name": "--fit_mode", "type": str, "choices": ["trim", "pad"], "default": "trim", "help": "アスペクト比を合わせる方法 (trim: 切り抜き, pad: 余白追加)", "short": "-f"},
            ],
        },
    }

    # サブコマンド設定
    for name, config in subcommands_config.items():
        subparser = subparsers.add_parser(name, help=config.get("help"), aliases=config.get("aliases"))
        for arg in config.get("arguments",):
            kwargs = {k: v for k, v in arg.items() if k not in ("name", "short")}
            short = arg.get("short")
            if short:
                subparser.add_argument(arg["name"], short, **kwargs)
            else:
                subparser.add_argument(arg["name"], **kwargs)
        subparser.set_defaults(func=config["module"])

    # コマンドラインパース
    args = parser.parse_args()

    # 設定ファイルのフォルダ準備と指定
    config_dir_path = initialize_config_directory(args)
    args.config_dir_path = config_dir_path

    # 設定ファイルパス確定
    config_path = os.path.join(config_dir_path, "config.toml")

    debug_print(args, f"config_dir_path: {args.config_dir_path}")
    debug_print(args, f"config_path: {config_path}")

    # 設定ファイル読み込み
    config = load_config(config_path, args)

    debug_print(args, args)
    debug_print(args, config, "Loaded Config:")

    # サブコマンド実行
    if args.subcommand is not None:
        args.func(args, config)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
