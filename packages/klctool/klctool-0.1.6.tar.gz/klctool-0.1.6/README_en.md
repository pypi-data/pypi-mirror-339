# klctool - Karaoke Lyrics Card Creation Support Tool

[日本語 - Japanese](https://github.com/AmasaShiro/klctool/blob/main/README.md)

![sample image](resources/sample.jpeg)

Calling all karaoke lovers! Don't you ever want a lyrics sheet when you're practicing? But making one can be quite a hassle... This tool is here to help you with that troublesome task.  

It uses AI (Google Gemini) to convert Markdown files containing lyrics into hiragana, and then transforms them into LibreOffice Writer format so you can perform complex editing.  

Furthermore, it processes images, such as screenshots of your favorite YouTube scenes, so you can use them as background images.  

Let's create your very own personalized lyrics sheet with this tool!  

Your feedback and opinions on X (formerly Twitter) or as GitHub Issues are welcome!

## Overview

- Command-line tool: klctool
  - Hiragana conversion of lyrics: Converts lyrics to hiragana using Google Gemini.
  - Conversion to ODT format: Converts to a format editable in LibreOffice Writer using Pandoc.
  - Background image processing: Processes and adjusts images for use as lyrics card backgrounds.

## Intended Users

- Karaoke lovers
- People who enjoy creating lyrics cards
- Individuals comfortable using the command line on a PC
- Those who can laugh off occasional AI errors

## Prerequisites

- Python
- Pandoc
- LibreOffice Writer

- Google Gemini API key

## How to Use

1. Prepare Lyrics
   1. Prepare a file containing the lyrics according to the sample format. [Sample](lyrics-sample.md)
       - At the beginning of the file, within the `---` block, describe the following three properties. These will be embedded in the header section when converting to ODT format:
          - vc-title
          - vc-artist
          - vc-collab (e.g., tie-up information, anime title)
       - Markdown format header (e.g., `# Artist - Song Title`)
       - Lyrics
   2. Make the following edits as well:
       - Confirm pronunciation variations: For example, 行く(いく/ゆく) should be decided as either 「いく」 or 「ゆく」.
       - Indentation: Indent the beginning of lines with full-width spaces (using full-width spaces is for Markdown format).
       - Match actual singing: For example, 「何百年経ったって」 → 「何百年経ってたって」 (ClariS / PRIMALove).
       - Add ruby text for difficult readings or rephrased words: For example, 「自らを見失った絵画」 → 「自らを見失った[絵画] (メイク)」 (Kafu / Phony).
2. Prepare Background Images  
   Prepare image files by taking screenshots of your favorite scenes in full screen (on PC) from YouTube, etc.
3. Execute `klctool`.
   1. `klctool hiragana lyrics_file_name`  
      Adds hiragana to the prepared lyrics file using AI. If Gemini forgets to convert or makes a mistake, laugh it off and run it again.
   2. `klctool convert2odt lyrics_file_name`  
      Converts the hiragana lyrics file to ODT format, which can be handled by the word processor LibreOffice Writer.
   3. `klctool adjustimage image_file_name1 image_file_name2` (you can specify just one image file)  
      Processes and adjusts the prepared image files to match the ODT format file.
      - Trims unnecessary parts (player controls).
      - Masks with 80% opacity.
4. Edit Lyrics Files
   Edit the hiragana-converted lyrics to correct any conversion errors and add vowels or elongated sounds to make them easier to sing in karaoke. Using music-related symbols like Google Music Font might make it easier to understand.
5. Set Background Image
   Set the background image in LibreOffice Writer as the page background.
   - From the menu, select [Format]→[Page Style...]→[Background]→[Image]→[Add/Import] to specify the image.
   - Under [Options]→[Style], select [Stretch to cover] and press [Apply] or [OK].
   - To use different background images for left and right pages, set the background image in the respective page styles.
     - First page: Standard page style
     - Second page: Right page style
     - Third page: Left page style
6. Completion of Lyrics Sheet
   Export as a PDF file using LibreOffice Writer, then transfer it to your tablet or print it out for use in karaoke. It might be helpful to make notes of anything you notice while listening to your own singing recordings.

## Setup

### Prerequisite Software

Install if you haven't already.

> [!TIP]
> Please check the official websites of each software and install them appropriately.

Example: Mac: Install with Homebrew.

```zsh
brew install pandoc
brew install --cask obsidian
brew install --cask libreoffice
brew install --cask libreoffice-language-pack
```

Example: Windows: Install with winget

```cmd
winget install --id=JohnMacFarlane.Pandoc  -e
winget install --id=Obsidian.Obsidian  -e
winget install --id=TheDocumentFoundation.LibreOffice  -e
```
 
#### Google Gemini API Key

Create a Gemini API key on the following Google AI Studio website:

https://aistudio.google.com/

> [!TIP]
> You can use the free tier API key (as of March 2025).

Set the created API key in the configuration file `gemini-2.0-flash-exp.api_key.toml`. If you are concerned about storing the API key in a file, you can also specify the API key using the following methods:

- Specify the API key using a command-line option.
- Set the API key in the environment variable `GOOGLE_API_KEY`.
- Specify a file (toml) containing the API key using a command-line option.

### klctool

```zsh
pip install klctool
```

## klctool Command-line Options

### Common Options

```zsh
klctool [-h] [--debug] [--config-dir CONFIG_DIR]
     {hiragana,hira,convert2odt,odt,adjustimage,img} ...
 -h, --help                   Show help message
 --debug, -d                  Enable debug mode
 --config-dir, -c CONFIG_DIR  Specify the directory for configuration files
```

### Subcommand: Hiragana Conversion hiragana (hira)

Converts the Markdown lyrics files specified by `input_files` to hiragana. The converted files are saved in the same folder as the original files with `_hiragana` appended to the filename.

```zsh
klctool hiragana [-h] [--output-dir OUTPUT_DIR] [--output-suffix OUTPUT_SUFFIX]
                [--model-name MODEL_NAME] [--api-key-file API_KEY_FILE]
                [--api-key API_KEY] [--prompt-file PROMPT_FILE]
                input_files [input_files ...]
 input_files                          Input files (multiple can be specified)
 -h, --help                           Show help message
 --output-dir, -o OUTPUT_DIR          Output folder
 --output-suffix, -s OUTPUT_SUFFIX    Output filename suffix
 --model-name, -m MODEL_NAME          AI model name
 --api-key-file, -a API_KEY_FILE      API key filename
 --api-key, -k API_KEY                API key
 --prompt-file, -p PROMPT_FILE        Prompt filename
```

- The Google Gemini API key is used with the following priority:
  1. Option `--api-key`
  2. Environment variable `GOOGLE_API_KEY`
  3. Option `--api-key-file`
  4. The file specified by `api_key_file` in the configuration file `config.toml`

- If `--output-dir` is specified, the hiragana converted files will be saved in the specified folder.
- If `--output-suffix` is specified, the specified suffix will be added.
- If `--api-key` is specified, it will be used as the API key.
- If `--api-key-file` is specified, it will be used as the API key file.
- If `--prompt-file` is specified, it will be used as the prompt file.

### Subcommand: Convert to ODT file convert2odt (odt)

Converts the Markdown lyrics files specified by `input_files` to ODT format using Pandoc and saves them in the same folder as the lyrics files.
The ODT template embeds title, artist, and tie-up information in the header.

```zsh
klctool convert2odt [-h] [--output-dir OUTPUT_DIR] [--template-odt TEMPLATE_ODT]
                   [--lua-script LUA_SCRIPT]
                   input_files [input_files ...]
 input_files                      Input files (multiple can be specified)
 -h, --help                       Show help message
 --output-dir, -o OUTPUT_DIR      Output folder
 --template-odt, -t TEMPLATE_ODT  Template ODT filename
 --lua-script, -s LUA_SCRIPT      Lua script filename
```

- If `--output-dir` is specified, the converted ODT files will be saved in the specified folder.
- If `--template-odt` is specified, it will be used as the template file.
- If `--lua-script` is specified, it will be used as the script file.

### Subcommand: Adjust/Process Image Files adjustimage (img)

Processes the PNG files specified by `input_files`. The processed files are saved in the same folder as the original files with `_processed` appended to the filename.

```zsh
klctool adjustimage [-h] [--output-dir OUTPUT_DIR] [--paper-size PAPER_SIZE]
                   [--mask-strength MASK_STRENGTH] [--mask-color MASK_COLOR]
                   [--output-suffix OUTPUT_SUFFIX] [--movie-aspect-ratio MOVIE_ASPECT_RATIO]
                   input_files [input_files ...]
 input_files                                 Input image files (multiple can be specified)
 -h, --help                                  Show help message
 --output-dir, -o OUTPUT_DIR                 Output folder
 --paper-size, -p PAPER_SIZE                 Paper size
 --mask-strength, -m MASK_STRENGTH           Mask strength (%)
 --mask-color, -c MASK_COLOR                 Mask color
 --output-suffix, -s OUTPUT_SUFFIX           Output filename suffix
 --movie-aspect-ratio, -a MOVIE_ASPECT_RATIO Movie aspect ratio
 --dpi, -d  DPI                              Output image DPI
 --fit-mode, -f {trim,pad}                   Method to adjust aspect ratio (default: trim)
```

- If `--output-dir` is specified, the processed files will be saved in the specified folder.
- If `--paper-size` is specified, the image will be adjusted to the specified paper size.
- If `--mask-strength` is specified, the image will be masked with the specified mask strength.
- If `--mask-color` is specified, the specified color will be used as the background color for masking.
- If `--output-suffix` is specified, the specified suffix will be added.
- If `--movie-aspect-ratio` is specified, the input image will be trimmed to the specified aspect ratio, considering it as the necessary portion.
- If `--dpi` is specified, the image file size will be checked, and the image will be reduced if it's too large.
- With `--fit-mode`, you can specify whether the final adjustment should be done by trimming or adding padding. The default is trimming.

## Customization

- Configuration file location:
  - macOS / Linux: ~/.config/klctool/
  - Windows: %APPDATA%

``` zsh
.config
└── klctool
    ├── config.toml  # Default configuration values, etc.
    ├── gemini-2.0-flash-exp.api_key.toml  # API key
    ├── gemini-2.0-flash-exp.prompt.toml   # Prompt
    ├── klctool-edit.lua # Lua script for Pandoc
    ├── klctool.odt      # ODT template file
    └── paper-size.toml # Paper size definitions
```

## License

MIT License

The licenses for the libraries used are under their respective licenses.

## Development and Testing Environment

- MacBook Air Retina, 13-inch, 2018 Intel
- MacOS Sonoma 14.7.4
- Python 3.13.2
- Pandoc 3.6.4
- LibreOffice Version: 25.2.1.2 (X86_64) / LibreOffice Community / Japanese Language Pack

## Contribution

- Reports of operation in environments other than the above are welcome. Operation has not been confirmed on Linux or Windows.
- Please report bugs to Issues.

## Other

This project was created for the following learning purposes. Your opinions and questions are welcome!

- mise en place / uv
- Git / GitHub
- Python packaging
- AI programming
- nuitka

## Acknowledgements

- The code was generated by Google Gemini. It's excellent. Thanks, Gemini!
- Thank you to all OSS developers!
