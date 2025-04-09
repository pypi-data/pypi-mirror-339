# src/klctool/common.py

import toml
import sys
import os
import platform
import shutil

from pathlib import Path

def initialize_config_directory(args):
    """
    設定ファイルの初期化処理を行う関数。
    """
    if args.config_dir is not None:
        # コマンドラインオプションで設定ファイルのパスが指定されている場合はそのまま使用
        config_dir_path = os.path.expanduser(args.config_dir)
    else:
        # OSを判別してデフォルトの設定ファイル格納先を決定
        system = platform.system()
        if system == 'Darwin' or system == 'Linux':  # macOSまたはLinux
            default_config_dir = os.path.expanduser('~/.config')
        elif system == 'Windows':
            default_config_dir = os.environ.get('APPDATA')
            if not default_config_dir:
                # %APPDATA%が設定されていない場合のフォールバック
                default_config_dir = os.path.expanduser('~/.config') # 一応設定
        else:
            # その他のOSの場合は~/.configを使用
            default_config_dir = os.path.expanduser('~/.config')

        config_dir_path = os.path.join(default_config_dir, 'klctool')

        # 設定ファイル用フォルダが存在しない場合は作成
        if not os.path.exists(config_dir_path):
            os.makedirs(config_dir_path, exist_ok=True)

            # config/klctoolフォルダの内容をコピー
            package_config_dir = Path(__file__).parent.parent / 'config' / 'klctool' # パッケージ化した場合のフォルダ指定
            debug_print(args, f"コピー元フォルダ: {package_config_dir}")
            if package_config_dir.is_dir():
                for item in package_config_dir.iterdir():
                    dst_path = Path(config_dir_path) / item.name
                    if not dst_path.exists():
                        if item.is_file():
                            shutil.copy2(item, dst_path)
                        elif item.is_dir():
                            shutil.copytree(item, dst_path)

    return config_dir_path


def load_config(config_path, args):
    debug_print(args, f"Config Path: {config_path}")
    try:
        with open(config_path, 'r') as f:
            config = toml.load(f)
        return config
    except FileNotFoundError:
        print(f"設定ファイルが見つかりません: {config_path}", file=sys.stderr)
        print("オプション '--config-dir' で設定ファイルのディレクトリを指定してください。", file=sys.stderr)
        sys.exit(1)
    except toml.TomlDecodeError as e:
        print(f"設定ファイルの形式が不正です: {config_path}", file=sys.stderr)
        print(f"TOML パースエラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"設定ファイルの読み込み中に予期せぬエラーが発生しました: {config_path}", file=sys.stderr)
        print(f"エラー内容: {e}", file=sys.stderr)
        sys.exit(1)


def debug_print(args, message, header=None):
    if args.debug:
        if header:
            print(f"[DEBUG] {header}")
        print(f"[DEBUG] {message}")
