import os
import socket
import sys
import threading
import urllib.parse
import json
import mimetypes
import traceback # 用于打印更详细的错误信息

# --- 配置加载 ---
DEFAULT_CONFIG = {
    "ip": "127.0.0.1",
    "port": 8080,
    "static_path": "." # 默认当前目录
}
CONFIG_FILE = "config.json"

def load_config():
    """加载配置文件，如果文件不存在或无效则创建/使用默认配置"""
    config_path = os.path.abspath(CONFIG_FILE) # 获取绝对路径以增加明确性
    print(f"Attempting to load config from: {config_path}")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                print(f"Successfully loaded config file.")
                # 合并默认值，确保所有必需的键都存在
                merged_config = DEFAULT_CONFIG.copy() # Start with defaults
                merged_config.update(config_data)    # Update with loaded values
                # 验证端口是否为整数
                if not isinstance(merged_config.get("port"), int):
                    print(f"Warning: Invalid port '{merged_config.get('port')}' in config. Using default port {DEFAULT_CONFIG['port']}.")
                    merged_config["port"] = DEFAULT_CONFIG["port"]
                # 验证 static_path 是否存在 (加载后检查)
                # check moved to main block for clarity
                return merged_config
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from config file '{config_path}': {e}. Using default config.")
            return DEFAULT_CONFIG.copy() # 返回副本
        except IOError as e:
            print(f"Error reading config file '{config_path}': {e}. Using default config.")
            return DEFAULT_CONFIG.copy() # 返回副本
        except Exception as e: # Catch other potential errors
            print(f"Unexpected error loading config '{config_path}': {e}. Using default config.")
            return DEFAULT_CONFIG.copy() # 返回副本
    else:
        print(f"Config file '{config_path}' not found. Creating default config.")
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False) # ensure_ascii=False for potential non-ascii paths
            print(f"Default config file created at '{config_path}'.")
        except IOError as e:
            print(f"Error creating default config file '{config_path}': {e}. Using default config.")
        except Exception as e:
             print(f"Unexpected error creating default config file '{config_path}': {e}. Using default config.")
        return DEFAULT_CONFIG.copy() # 返回副本

# --- 图标数据 ---
# SVG Icons dictionary (Keep as is)
icons = {
    # ... (保持你的 SVG 字符串) ...
    ".zip":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M12.167 3h-3.75v2.083h1.25V8H6.333V5.083h1.25V3h-3.75a.417.417 0 0 0-.416.417v9.166c0 .23.186.417.416.417h8.334c.23 0 .416-.186.416-.417V3.417A.416.416 0 0 0 12.167 3Zm-3.334 8.333H7.167V10.5h1.666v.833ZM7.167 9.667h1.666v-.834H7.167v.834Z" fill="#5654BC"/><path fill="#FF9CAC" d="M7.167 5.917h1.667v1.25H7.167z"/></svg>',
    ".doc":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M2.5 13.5v-11A.5.5 0 0 1 3 2h10a.5.5 0 0 1 .5.5v11a.5.5 0 0 1-.5.5H3a.5.5 0 0 1-.5-.5Zm5-9h-3v3h3v-3Zm4 7h-7v-1h7v1Zm-7-2h7v-1h-7v1Zm7-2h-3v-1h3v1Zm-3-2h3v-1h-3v1Z" fill="#3965BD"/></svg>',
    ".js":'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="32" height="32" viewBox="0 0 32 32"><path fill="#f5de19" d="M2 2h28v28H2z"></path><path d="M20.809 23.875a2.866 2.866 0 0 0 2.6 1.6c1.09 0 1.787-.545 1.787-1.3c0-.9-.716-1.222-1.916-1.747l-.658-.282c-1.9-.809-3.16-1.822-3.16-3.964c0-1.973 1.5-3.476 3.853-3.476a3.889 3.889 0 0 1 3.742 2.107L25 18.128A1.789 1.789 0 0 0 23.311 17a1.145 1.145 0 0 0-1.259 1.128c0 .789.489 1.109 1.618 1.6l.658.282c2.236.959 3.5 1.936 3.5 4.133c0 2.369-1.861 3.667-4.36 3.667a5.055 5.055 0 0 1-4.795-2.691Zm-9.295.228c.413.733.789 1.353 1.693 1.353c.864 0 1.41-.338 1.41-1.653v-8.947h2.631v8.982c0 2.724-1.6 3.964-3.929 3.964a4.085 4.085 0 0 1-3.947-2.4Z"></path></svg>',
    ".json":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><g fill-rule="evenodd" clip-rule="evenodd"><path d="M5.5 3.5h-1a1 1 0 0 0-1 1v2a1 1 0 0 1-1 1H2v1h.5a1 1 0 0 1 1 1v2c0 .55.465.865 1 1h1v-1h-1V9a1 1 0 0 0-1-1 1 1 0 0 0 1-1V4.5h1v-1Zm7 1a1 1 0 0 0-1-1h-1v1h1V7a1 1 0 0 0 1 1 1 1 0 0 0-1 1v2.5h-1v1h1a1 1 0 0 0 1-1v-2a1 1 0 0 1 1-1h.5v-1h-.5a1 1 0 0 1-1-1v-2Z" fill="#89DDFF"/><path d="M6 7.5a.5.5 0 1 1 0 1 .5.5 0 0 1 0-1Zm2 0a.5.5 0 1 1 0 1 .5.5 0 0 1 0-1Zm2.5.5a.5.5 0 1 0-1 0 .5.5 0 0 0 1 0Z" fill="#FFCB6B"/></g></svg>',
    ".java":'<svg width="14" height="14" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#a)"><path d="M9.749 3.064c-1.063.32-2.214.76-2.845 1.722-.45.7-.123 1.6.404 2.158.365.359.22.948-.153 1.242-.392.342.06.282.288.117.555-.343 1.176-.97.938-1.684-.186-.54-.887-.987-.64-1.618.481-.867 1.483-1.249 2.237-1.838.29-.193-.117-.073-.23-.1ZM7.895 0l.1.464c.582 2.307-2.317 2.835-3.01 4.471-.284.836.376 1.599.905 2.17.363.368.732.742 1.157 1.048-.194-.981-1.286-1.613-1.188-2.668.195-1.013 1.257-1.457 1.866-2.188C8.736 2.174 8.96.999 7.895 0Z" fill="#FC8289"/><path d="M5 10.714c-.303.08-.845.28-.698.688.28.444.882.508 1.356.604a6.272 6.272 0 0 0 3.55-.535c-.377-.118-.73-.342-1.078-.479-1.013.207-2.094.294-3.102.023.052-.12.514-.396.128-.312L5 10.714Zm-.325-1.47c-.302.122-.84.266-.788.688.186.421.748.46 1.142.552 1.5.218 3.038.026 4.478-.423-.318-.119-.657-.231-.892-.489-1.276.253-2.624.38-3.9.11-.18-.094.184-.27.204-.366.36-.309-.125-.046-.244-.072Zm-1.818 3.104c.464-.309 1.036-.389 1.584-.313-.257-.186-.492-.397-.83-.35-.637.063-1.319.229-1.783.696-.23.27.096.58.373.612 2.354.443 4.808.508 7.173.095.617-.161 1.355-.232 1.802-.73.208-.354-.282-.612-.569-.635-.118.03.21.24.202.395-.29.32-.801.31-1.205.412-3 .39-5.964.234-6.747-.182Zm6.426-3.71c.23-.124.471-.221.66-.406-.742-.044-1.468.2-2.206.226-1.2.074-2.43.21-3.618-.017-.184-.043.15-.139.197-.176.427-.19.9-.232 1.311-.463-.17-.04-.336-.111-.514-.09-.77.044-1.564.233-2.207.663-.228.216.056.495.291.524 1.636.452 5.348.225 6.086-.261Zm1.232-1.053c-.39-.001-.764.185-.923.56-.183.248.306-.113.47-.11.52-.216 1.152.35.904.885-.257.649-.95.96-1.472 1.332-.434.356-.295.372.168.204.837-.245 1.842-.637 2.117-1.55.198-.75-.532-1.39-1.264-1.32Zm-7.283 5.736c.605.587 1.508.547 2.287.64 1.777.076 3.603.092 5.311-.443.488-.158 1.11-.542.974-1.149.04-.363-.143.115-.22.178-1.056 1.046-5.76 1.19-8.352.774Z" fill="#80CBC4"/></g><defs><clipPath id="a"><path fill="#fff" d="M0 0h14v14H0z"/></clipPath></defs></svg>',
    ".png":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><mask id="a" mask-type="alpha" maskUnits="userSpaceOnUse" x="1" y="3" width="14" height="10"><rect x="1.75" y="3" width="12.5" height="10" rx="2" fill="#00B6C2"/></mask><g mask="url(#a)"><path fill="#80CBC4" d="M1.75 3h12.5v10H1.75z"/><path d="M11.563 8 4.25 14.25l10.688-.446.562-4.018L11.562 8Z" fill="#343944"/><path d="M5.396 8.208a1.563 1.563 0 1 0 0-3.125 1.563 1.563 0 0 0 0 3.125Z" fill="#fff"/></g></svg>',
    ".ttf":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 13v-.802l1.315-.078c.155-.01.185-.055.185-.22V4H3.094c-.121 0-.155.011-.177.122L2.741 5H2V3h8v2h-.74l-.177-.878C9.06 4.01 9.027 4 8.906 4H6.5v7.9c0 .154.02.198.185.21L8 12.197V13H4Z" fill="#F07178"/><path d="M9.5 13v-.802l.815-.078c.155-.01.185-.055.185-.22V7.5H9.094c-.121 0-.155.011-.177.122l-.176.878H8v-2h6v2h-.74l-.177-.878c-.022-.111-.056-.122-.177-.122H11.5v4.4c0 .154.02.198.185.21l.815.088V13h-3Z" fill="#9883EC"/></svg>',
    "":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path opacity=".8" d="M6.6 2H2.4c-.77 0-1.393.619-1.393 1.375L1 11.625C1 12.381 1.63 13 2.4 13h11.2c.77 0 1.4-.619 1.4-1.375V4.75c0-.756-.63-1.375-1.4-1.375H8L6.6 2Z" fill="#4A616C"/></svg>', # Folder icon
    ".lnk":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M14 13.5S12 9 7.5 9v3L2 7l5.5-5v3C13 5 14 10 14 12v1.5Z" fill="#80CBC4"/></svg>',
    ".exe":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="m8 6.31 4.895-2.183L8.22 2.055c-.165-.055-.33-.055-.44 0L3.105 4.127 8 6.31Z" fill="#89DDFF"/><path d="M8.55 7.236v6.546l4.62-2.018c.22-.11.33-.273.33-.491V5.055L8.55 7.236Zm-1.1 0L2.5 5.055v6.218c0 .218.11.436.33.49l4.62 2.019V7.236Z" fill="#82AAFF"/></svg>',
    ".cpp":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="m7.87 10.269.231 1.394c-.147.08-.384.154-.7.223A5.09 5.09 0 0 1 6.263 12c-1.249-.023-2.187-.4-2.814-1.12-.633-.726-.95-1.646-.95-2.76.028-1.32.407-2.331 1.13-3.04C4.377 4.366 5.303 4 6.423 4c.424 0 .79.04 1.096.109.305.068.531.142.678.228L7.87 5.76l-.6-.194a3.214 3.214 0 0 0-.785-.086c-.656-.006-1.198.206-1.622.629-.43.417-.65 1.057-.667 1.908 0 .777.209 1.383.61 1.829.401.44.967.668 1.69.674l.752-.069c.243-.045.446-.108.622-.182Zm-.718-2.84h1.13V6.286h1.131v1.143h1.13V8.57h-1.13v1.143h-1.13V8.571h-1.13V7.43Zm5.087 0h-1.13V8.57h1.13v1.143h1.13V8.571H14.5V7.43h-1.13V6.286h-1.13v1.143Z" fill="#3965BD"/></svg>',
    ".c":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="m11.51 11.403.347 2.091c-.22.12-.574.232-1.046.335A7.557 7.557 0 0 1 9.116 14c-1.864-.034-3.263-.6-4.2-1.68C3.973 11.231 3.5 9.851 3.5 8.18c.042-1.98.607-3.497 1.687-4.56C6.3 2.549 7.683 2 9.352 2c.633 0 1.18.06 1.636.163.456.103.793.214 1.012.343l-.49 2.134-.893-.291a4.77 4.77 0 0 0-1.172-.129c-.978-.009-1.788.309-2.42.943-.641.626-.97 1.586-.995 2.863 0 1.165.312 2.074.91 2.743.6.66 1.442 1.002 2.522 1.011l1.121-.103a4.46 4.46 0 0 0 .928-.274Z" fill="#3965BD"/></svg>',
    ".bat":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 4V2.5H2.5A.5.5 0 0 0 2 3v1h2Zm10 0V3a.5.5 0 0 0-.5-.5H5V4h9Z" fill="#89DDFF"/><path fill-rule="evenodd" clip-rule="evenodd" d="M2 5v8a.5.5 0 0 0 .5.5h11a.5.5 0 0 0 .5-.5V5H2Zm4.354 4.354L4.5 11.207l-.707-.707 1.5-1.5-1.5-1.5.707-.707 1.854 1.853a.5.5 0 0 1 0 .707ZM7.5 11h3v-1h-3v1Z" fill="#3965BD"/></svg>',
    ".txt":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 3h5l2 1 1 2v7H4V3Z" fill="#A9B4CB"/><path fill-rule="evenodd" clip-rule="evenodd" d="M9 2a1 1 0 0 1 .707.293l3 3A1 1 0 0 1 13 6v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h4Zm3 4v6a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h4l3 3Z" fill="#A9B4CB"/><path d="M9 3v3h3" fill="#F5F7F9"/><path d="M10 8.5H6m4 2H6" stroke="#434F65" stroke-linecap="round" stroke-linejoin="round"/><path d="M7 6.5H6" stroke="#252D3A" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    ".md":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M8.87 10.71H7.13V8L5.814 9.733 4.5 8.001v2.708H2.76V5.293H4.5l1.315 1.812L7.13 5.293h1.74v5.416Zm2.611.437L9.316 8h1.315V5.292h1.74V8h1.316l-2.204 3.147h-.002ZM13.995 3.5H2.005a.952.952 0 0 0-.705.308c-.2.206-.3.448-.3.727v6.93a1 1 0 0 0 .3.737c.2.199.434.298.705.298h11.99c.27 0 .506-.1.706-.298a.998.998 0 0 0 .299-.737v-6.93c0-.279-.1-.521-.3-.727a.952.952 0 0 0-.705-.308Z" fill="#F78C6C"/></svg>',
    ".py":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><g fill-rule="evenodd" clip-rule="evenodd"><path d="M11.703 5.796h-.856v1.309s.046 1.561-1.41 1.561h-2.43s-1.365-.024-1.365 1.437v2.416c-.21 1.9 4.924 1.96 4.882.249l-.003-1.256H8.07v-.377h3.423c2.25.188 2.107-5.418.209-5.34ZM9.247 13.07a.502.502 0 0 1 0-.83c.293-.185.661.047.661.415s-.368.6-.661.415Z" fill="#FFCB6B"/><path d="M4.458 11.21h.856V9.9s-.046-1.56 1.41-1.56h2.43s1.365.024 1.365-1.437V4.294c-.217-1.79-5.039-1.648-4.882-.036v1.235h2.452v.377H4.667c-2.311-.053-2.064 5.34-.209 5.34Zm2.014-6.445a.502.502 0 0 1 0-.831c.293-.184.662.047.662.415s-.369.6-.662.416Z" fill="#89DDFF"/></g></svg>',
    ".xml":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M12.5 11V3.5A1.5 1.5 0 0 0 11 2H3.75A1.75 1.75 0 0 0 2 3.75V5h2.5v7.5A1.5 1.5 0 0 0 6 14h6.25A1.75 1.75 0 0 0 14 12.25V11h-1.5ZM3 4v-.25a.75.75 0 0 1 1.5 0V4H3Zm7 1.793-.707.707 1 1-1 1 .707.707 1.354-1.354a.5.5 0 0 0 0-.707L10 5.793Zm-3.854 2.06a.5.5 0 0 1 0-.707L7.5 5.793l.707.707-1 1 1 1-.707.707-1.354-1.354ZM12.25 13a.75.75 0 0 0 .75-.75V12H8v.25c0 .293-.061.54-.162.75h4.412Z" fill="#C3E88D"/></svg>',
    ".un":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M8.083 2.167H4.5a1.167 1.167 0 0 0-1.167 1.166v9.334A1.166 1.166 0 0 0 4.5 13.833h7a1.167 1.167 0 0 0 1.167-1.166V6.75H8.583a.5.5 0 0 1-.5-.5V2.167Zm4.084 3.583L9.083 2.667V5.75h3.084Z" fill="#697DA5"/></svg>', # Unknown file type
    ".ts":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M13 4a1 1 0 0 0-1-1H4a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V4Zm-4.13 6.655-.203.736c.125.06.298.115.52.167.223.052.459.078.708.078.592 0 1.03-.121 1.314-.364.285-.243.427-.531.427-.863 0-.283-.09-.52-.272-.71-.182-.192-.466-.351-.85-.48a3.674 3.674 0 0 1-.61-.26c-.126-.075-.188-.174-.188-.298 0-.104.052-.195.155-.272.103-.076.26-.115.472-.115.211 0 .393.023.545.067a2.8 2.8 0 0 1 .358.127l.22-.722a2.706 2.706 0 0 0-.468-.141 3.029 3.029 0 0 0-.639-.06c-.51 0-.911.115-1.204.343-.293.228-.44.51-.44.848 0 .287.11.526.33.717.22.191.508.346.866.465.26.08.447.162.558.246.11.084.166.186.166.305a.362.362 0 0 1-.175.312c-.116.08-.286.12-.508.12a2.41 2.41 0 0 1-.607-.075 2.292 2.292 0 0 1-.475-.17v-.002.001ZM6.54 8.238v3.398h.862V8.238h1.265v-.693H5.273v.693H6.54Z" fill="#3965BD"/></svg>',
    ".cs":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M4.474 12.571h1.743l.465-2.522h1.743l-.465 2.522h1.744l.465-2.522h1.898v-1.3h-1.588l.31-1.576h1.782v-1.3h-1.55l.504-2.444H9.82l-.503 2.444H7.573l.504-2.444H6.334l-.465 2.444H3.97v1.3h1.628l-.31 1.576h-1.86v1.3h1.55l-.504 2.522ZM8.736 8.75H6.993l.31-1.576h1.743l-.31 1.576Z" fill="#89DDFF"/></svg>',
    ".mp3":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M14 8A6 6 0 1 1 2 8a6 6 0 0 1 12 0ZM8.6 5.025c.687.084 2.372.474 2.984 2.279a.3.3 0 0 1-.437.354c-.768-.454-1.992-.54-2.547-.556V10.1c0 .827-.673 1.5-1.5 1.5s-1.5-.673-1.5-1.5.673-1.5 1.5-1.5c.339 0 .649.117.9.308V4.4h.6v.625Z" fill="#FC8289"/></svg>',
    ".mp4":'<svg width="16" height="16" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M3 5.5h10a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-.5.5H3a.5.5 0 0 1-.5-.5V6a.5.5 0 0 1 .5-.5Zm7 4-3.5-2v4l3.5-2Z" fill="#FC8289"/><path d="M2.11 4.14a.5.5 0 0 1 .39-.59l9.652-1.969a.5.5 0 1 1 .2.98L2.7 4.53a.5.5 0 0 1-.59-.39Z" fill="#FFCB6B"/></svg>',
    ".pdf":'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="32" height="32" viewBox="0 0 32 32"><path fill="#909090" d="m24.1 2.072l5.564 5.8v22.056H8.879V30h20.856V7.945L24.1 2.072"></path><path fill="#f4f4f4" d="M24.031 2H8.808v27.928h20.856V7.873L24.031 2"></path><path fill="#7a7b7c" d="M8.655 3.5h-6.39v6.827h20.1V3.5H8.655"></path><path fill="#dd2025" d="M22.472 10.211H2.395V3.379h20.077v6.832"></path><path fill="#464648" d="M9.052 4.534H7.745v4.8h1.028V7.715L9 7.728a2.042 2.042 0 0 0 .647-.117a1.427 1.427 0 0 0 .493-.291a1.224 1.224 0 0 0 .335-.454a2.13 2.13 0 0 0 .105-.908a2.237 2.237 0 0 0-.114-.644a1.173 1.173 0 0 0-.687-.65a2.149 2.149 0 0 0-.409-.104a2.232 2.232 0 0 0-.319-.026m-.189 2.294h-.089v-1.48h.193a.57.57 0 0 1 .459.181a.92.92 0 0 1 .183.558c0 .246 0 .469-.222.626a.942.942 0 0 1-.524.114m3.671-2.306c-.111 0-.219.008-.295.011L12 4.538h-.78v4.8h.918a2.677 2.677 0 0 0 1.028-.175a1.71 1.71 0 0 0 .68-.491a1.939 1.939 0 0 0 .373-.749a3.728 3.728 0 0 0 .114-.949a4.416 4.416 0 0 0-.087-1.127a1.777 1.777 0 0 0-.4-.733a1.63 1.63 0 0 0-.535-.4a2.413 2.413 0 0 0-.549-.178a1.282 1.282 0 0 0-.228-.017m-.182 3.937h-.1V5.392h.013a1.062 1.062 0 0 1 .6.107a1.2 1.2 0 0 1 .324.4a1.3 1.3 0 0 1 .142.526c.009.22 0 .4 0 .549a2.926 2.926 0 0 1-.033.513a1.756 1.756 0 0 1-.169.5a1.13 1.13 0 0 1-.363.36a.673.673 0 0 1-.416.106m5.08-3.915H15v4.8h1.028V7.434h1.3v-.892h-1.3V5.43h1.4v-.892"></path><path fill="#dd2025" d="M21.781 20.255s3.188-.578 3.188.511s-1.975.646-3.188-.511Zm-2.357.083a7.543 7.543 0 0 0-1.473.489l.4-.9c.4-.9.815-2.127.815-2.127a14.216 14.216 0 0 0 1.658 2.252a13.033 13.033 0 0 0-1.4.288Zm-1.262-6.5c0-.949.307-1.208.546-1.208s.508.115.517.939a10.787 10.787 0 0 1-.517 2.434a4.426 4.426 0 0 1-.547-2.162Zm-4.649 10.516c-.978-.585 2.051-2.386 2.6-2.444c-.003.001-1.576 3.056-2.6 2.444ZM25.9 20.895c-.01-.1-.1-1.207-2.07-1.16a14.228 14.228 0 0 0-2.453.173a12.542 12.542 0 0 1-2.012-2.655a11.76 11.76 0 0 0 .623-3.1c-.029-1.2-.316-1.888-1.236-1.878s-1.054.815-.933 2.013a9.309 9.309 0 0 0 .665 2.338s-.425 1.323-.987 2.639s-.946 2.006-.946 2.006a9.622 9.622 0 0 0-2.725 1.4c-.824.767-1.159 1.356-.725 1.945c.374.508 1.683.623 2.853-.91a22.549 22.549 0 0 0 1.7-2.492s1.784-.489 2.339-.623s1.226-.24 1.226-.24s1.629 1.639 3.2 1.581s1.495-.939 1.485-1.035"></path><path fill="#909090" d="M23.954 2.077V7.95h5.633l-5.633-5.873Z"></path><path fill="#f4f4f4" d="M24.031 2v5.873h5.633L24.031 2Z"></path><path fill="#fff" d="M8.975 4.457H7.668v4.8H8.7V7.639l.228.013a2.042 2.042 0 0 0 .647-.117a1.428 1.428 0 0 0 .493-.291a1.224 1.224 0 0 0 .332-.454a2.13 2.13 0 0 0 .105-.908a2.237 2.237 0 0 0-.114-.644a1.173 1.173 0 0 0-.687-.65a2.149 2.149 0 0 0-.411-.105a2.232 2.232 0 0 0-.319-.026m-.189 2.294h-.089v-1.48h.194a.57.57 0 0 1 .459.181a.92.92 0 0 1 .183.558c0 .246 0 .469-.222.626a.942.942 0 0 1-.524.114m3.67-2.306c-.111 0-.219.008-.295.011l-.235.006h-.78v4.8h.918a2.677 2.677 0 0 0 1.028-.175a1.71 1.71 0 0 0 .68-.491a1.939 1.939 0 0 0 .373-.749a3.728 3.728 0 0 0 .114-.949a4.416 4.416 0 0 0-.087-1.127a1.777 1.777 0 0 0-.4-.733a1.63 1.63 0 0 0-.535-.4a2.413 2.413 0 0 0-.549-.178a1.282 1.282 0 0 0-.228-.017m-.182 3.937h-.1V5.315h.013a1.062 1.062 0 0 1 .6.107a1.2 1.2 0 0 1 .324.4a1.3 1.3 0 0 1 .142.526c.009.22 0 .4 0 .549a2.926 2.926 0 0 1-.033.513a1.756 1.756 0 0 1-.169.5a1.13 1.13 0 0 1-.363.36a.673.673 0 0 1-.416.106m5.077-3.915h-2.43v4.8h1.028V7.357h1.3v-.892h-1.3V5.353h1.4v-.892"></path></svg>',
    ".download":'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24" height="24" viewBox="0 0 24 24"><path fill="#1A55E8" d="m12 16l-5-5l1.4-1.45l2.6 2.6V4h2v8.15l2.6-2.6L17 11Zm-8 4v-5h2v3h12v-3h2v5Z"></path></svg>',
    ".db":'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24" height="24" viewBox="0 0 24 24"><path fill="#ECC849" d="M21 16v3c0 1.657-4.03 3-9 3s-9-1.343-9-3v-3c0 1.657 4.03 3 9 3s9-1.343 9-3Zm-9-1c-4.97 0-9-1.343-9-3v3c0 1.657 4.03 3 9 3s9-1.343 9-3v-3c0 1.657-4.03 3-9 3Zm0-13C7.03 2 3 3.343 3 5v2c0 1.657 4.03 3 9 3s9-1.343 9-3V5c0-1.657-4.03-3-9-3Zm0 9c-4.97 0-9-1.343-9-3v3c0 1.657 4.03 3 9 3s9-1.343 9-3V8c0 1.657-4.03 3-9 3Z"></path></svg>',
    ".apk":'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="24" height="24" viewBox="0 0 24 24"><path fill="#0BB978" d="M7 19h10q-.1-1.225-.75-2.25t-1.7-1.625l.95-1.7q.05-.1.025-.225t-.15-.175q-.1-.05-.212-.025q-.113.025-.163.125l-.975 1.75q-.5-.2-1-.313q-.5-.112-1.025-.112q-.525 0-1.025.112q-.5.113-1 .313L9 13.125Q8.95 13 8.838 13q-.113 0-.238.05l-.1.375l.95 1.7q-1.05.6-1.7 1.625Q7.1 17.775 7 19Zm2.75-1.5q-.2 0-.35-.15q-.15-.15-.15-.35q0-.2.15-.35q.15-.15.35-.15q.2 0 .35.15q.15.15.15.35q0 .2-.15.35q-.15.15-.35.15Zm4.5 0q-.2 0-.35-.15q-.15-.15-.15-.35q0-.2.15-.35q.15-.15.35-.15q.2 0 .35.15q.15.15.15.35q0 .2-.15.35q-.15.15-.35.15ZM6 22q-.825 0-1.412-.587Q4 20.825 4 20V4q0-.825.588-1.413Q5.175 2 6 2h7.175q.4 0 .763.15q.362.15.637.425l4.85 4.85q.275.275.425.637q.15.363.15.763V20q0 .825-.587 1.413Q18.825 22 18 22Zm7-14q0 .425.288.712Q13.575 9 14 9h4l-5-5Z"></path></svg>'
}

def get_icons(ex:str):
    """根据文件扩展名获取对应的SVG图标"""
    ex = ex.lower()
    # Combine similar archive types
    if ex in ['.zip','.rar','.7z','.iso','.gz', '.tar', '.bz2']:
        return icons.get(".zip", icons[".un"])
    # Combine image types
    elif ex in ['.ico','.png','.gif','.jpg','.jpeg', '.bmp', '.webp', '.svg']: # Added svg here too
        return icons.get(".png", icons[".un"])
    # Combine audio types
    elif ex in ['.mp3','.ogg','.wav','.mid', '.flac', '.aac', '.m4a']:
        return icons.get(".mp3", icons[".un"])
    # Combine video types
    elif ex in ['.mp4','.avi','.flv','.rmvb', '.mov', '.wmv', '.mkv']:
        return icons.get(".mp4", icons[".un"])
    # Direct match or unknown
    else:
        # Use .get for safety, fallback to unknown
        return icons.get(ex, icons[".un"])

class BaseHeader:
    def __init__(self) -> None:
        self.headers = {}

class Request(BaseHeader):
    def __init__(self,recv_client_content:str) -> None:
        super().__init__()
        self.method = ""
        self.url = ""
        self.protocol_version = ""
        self.raw_request = recv_client_content
        self.body = "" # Store request body if needed later (e.g., for POST)

        # Separate headers and body
        header_part, *body_parts = recv_client_content.split('\r\n\r\n', 1)
        self.body = body_parts[0] if body_parts else ""

        lines = header_part.split('\r\n')
        if not lines:
            print("Warning: Received empty request.")
            return # Cannot parse further

        # Parse Request Line (First line)
        request_line = lines[0]
        parts = request_line.split(" ", maxsplit=2)
        if len(parts) >= 1:
            self.method = parts[0].upper() # Normalize method to uppercase
        if len(parts) >= 2:
            self.url = parts[1]
        if len(parts) >= 3:
            self.protocol_version = parts[2]
        else:
            # Assume HTTP/1.0 or earlier if version missing, though modern clients usually send it
            self.protocol_version = "HTTP/1.0"

        # Parse Headers (Remaining lines)
        for line in lines[1:]:
            if ':' in line:
                key, value = line.split(':', 1)
                self.headers[key.strip()] = value.strip()
            elif line: # Non-empty line without ':' is usually an error
                print(f"Warning: Malformed header line ignored: {line}")

class Response(BaseHeader):
    def __init__(self,socket) -> None:
        super().__init__()
        self.socket = socket
        self.status_line = b""
        self.body = b""

    def _build_header_str(self):
        """Builds the header part of the HTTP response as a string."""
        # Ensure required headers like Content-Length are set if body exists
        if self.body and "Content-Length" not in self.headers:
             self.headers["Content-Length"] = str(len(self.body))
        # Add Server header (optional but good practice)
        if "Server" not in self.headers:
            self.headers["Server"] = "SimplePythonHTTPServer/1.1"
        # Add Connection: close header to signal connection closure after response
        if "Connection" not in self.headers:
            self.headers["Connection"] = "close"

        header_str = ""
        for key, value in self.headers.items():
            header_str += f"{key}: {value}\r\n"
        return header_str + '\r\n' # Final blank line ending headers

    def setStatusLine(self,line:str):
        # Ensure line ends with \r\n
        if not line.endswith('\r\n'):
            line += '\r\n'
        self.status_line = line.encode("utf-8")

    def setBody(self,body):
        if isinstance(body,bytes):
            self.body = body
        else :
            try:
                # Default to UTF-8 for string bodies
                self.body = str(body).encode("utf-8")
            except Exception as e:
                print(f"Error encoding body to UTF-8: {e}")
                # Fallback or set error message
                self.body = b"Error: Could not encode response body."
                # Update headers for error response
                self.setStatusLine("HTTP/1.1 500 Internal Server Error\r\n")
                self.headers["Content-Type"] = "text/plain; charset=utf-8"


    def _toBytes(self):
        """Combines status line, headers, and body into bytes for sending."""
        # Re-calculate Content-Length just before sending, based on final body
        self.headers["Content-Length"] = str(len(self.body))
        header_bytes = self._build_header_str().encode("utf-8")
        return self.status_line + header_bytes + self.body

    def send(self):
        """Sends the complete HTTP response and closes the socket."""
        try:
            response_bytes = self._toBytes()
            # print(f"--- Sending Response ---\n{response_bytes.decode('utf-8', errors='replace')[:500]}...\n--- End Response ---") # Debug: Print response start
            self.socket.sendall(response_bytes)
        except socket.error as e:
            print(f"Socket error sending data: {e}")
        except Exception as e:
             print(f"Unexpected error sending data: {e}")
             # traceback.print_exc() # Uncomment for detailed debug info
        finally:
            try:
                # Shutdown gracefully before closing (optional but good practice)
                self.socket.shutdown(socket.SHUT_RDWR)
            except (socket.error, OSError):
                pass # Ignore errors if socket already closed/invalid
            try:
                self.socket.close()
            except (socket.error, OSError):
                pass # Ignore close errors

class HttpWebServer(object):
    def __init__(self, ip="127.0.0.1", port=8000, static_path='.'):
        self.ip = ip
        self.port = port
        # Ensure static_path is absolute and exists early on
        self.staticPath = os.path.abspath(static_path)
        if not os.path.isdir(self.staticPath):
             # This case should ideally be caught before creating the instance,
             # but double-check here.
             raise ValueError(f"Static path '{self.staticPath}' is not a valid directory.")

        self.tcp_server_socket = None
        self.running = False # Flag to control the main loop

        # Add common MIME types not guessed by default
        mimetypes.add_type('application/javascript', '.js')
        mimetypes.add_type('text/css', '.css')
        mimetypes.add_type('image/svg+xml', '.svg')
        mimetypes.add_type('font/ttf', '.ttf')
        mimetypes.add_type('application/json', '.json')
        mimetypes.add_type('text/markdown', '.md')
        # Add others if needed


    def _setup_socket(self):
        """Sets up the listening server socket."""
        try:
            self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            self.tcp_server_socket.bind((self.ip, self.port))
            self.tcp_server_socket.listen(128) # Increased backlog slightly
             # Set a timeout on the listening socket itself
             # This allows the main loop to check the self.running flag periodically
            self.tcp_server_socket.settimeout(1.0) # Check every 1 second
            print(f'Static path: "{self.staticPath}"')
            print(f'Server running at: http://{self.ip}:{self.port}/')
            print(f'Serving files from: {self.staticPath}')
            self.running = True # Set running flag
            return True
        except socket.error as e:
            print(f"Error setting up socket on {self.ip}:{self.port} - {e}")
            print("Common causes: Port already in use, invalid IP, lack of permissions.")
            self.tcp_server_socket = None
            return False
        except Exception as e:
            print(f"An unexpected error occurred during server setup: {e}")
            traceback.print_exc() # Print full traceback for unexpected errors
            self.tcp_server_socket = None
            return False

    def stop(self):
        """Signals the server to stop gracefully."""
        print("\nStopping server...")
        self.running = False # Signal the main loop to exit
        # The loop will exit after the next socket timeout or accept
        # Closing the socket here might be abrupt, let the finally block handle it.
        # if self.tcp_server_socket:
        #     self.tcp_server_socket.close()


    def handle_client_request(self, new_socket: socket, client_address):
        """Handles a single client connection."""
        # print(f"Handling connection from {client_address}") # Debug
        recv_client_data = b""
        try:
            # Set timeout for individual client socket operations
            new_socket.settimeout(30) # 30 seconds timeout for read/write

            # --- Improved Request Reading ---
            # Read headers first, then body if Content-Length is present
            # This is a simplified approach; full handling is complex.
            while b'\r\n\r\n' not in recv_client_data:
                 chunk = new_socket.recv(4096)
                 if not chunk:
                     # Connection closed by client before sending full headers
                     print(f"Connection closed by {client_address} before full request.")
                     # No response can be sent if headers weren't received. Close socket.
                     new_socket.close()
                     return
                 recv_client_data += chunk
                 # Safety break if headers get excessively large
                 if len(recv_client_data) > 16 * 1024: # 16KB limit for headers
                     print(f"Request headers too large from {client_address}.")
                     # Send 413 Payload Too Large or just close
                     response = Response(new_socket)
                     self.send_error(response, 413, "Payload Too Large", "Request headers exceed limit.")
                     return # Error sent, exit handler

        except socket.timeout:
            print(f"Socket timed out waiting for request data from {client_address}.")
            # No request fully received, just close.
            new_socket.close()
            return
        except socket.error as e:
            print(f"Socket error receiving data from {client_address}: {e}")
            # Error during receive, just close.
            new_socket.close()
            return
        except Exception as e:
             print(f"Unexpected error receiving data from {client_address}: {e}")
             traceback.print_exc()
             # Try to send a 500 error if possible, otherwise just close
             try:
                 response = Response(new_socket)
                 self.send_error(response, 500, "Internal Server Error", "Error receiving request.")
             except: # If sending error fails too
                 new_socket.close()
             return

        # --- Request Parsing ---
        try:
            # Try UTF-8 first, fallback to latin-1 for headers (common practice)
            try:
                recv_client_content = recv_client_data.decode("utf-8")
            except UnicodeDecodeError:
                recv_client_content = recv_client_data.decode("latin-1")
                print(f"Warning: Request from {client_address} decoded using latin-1 due to UTF-8 error.")

            request = Request(recv_client_content)
            # print(f"Request from {client_address}: {request.method} {request.url}") # Debug

        except Exception as e:
            print(f"Error parsing request from {client_address}: {e}")
            traceback.print_exc()
            # Send 400 Bad Request
            response = Response(new_socket)
            self.send_error(response, 400, "Bad Request", "Could not parse the request.")
            return

        # --- Routing and Response ---
        response = Response(new_socket) # Create response object linked to this client's socket
        try:
            if request.method == 'GET':
                self.on_get(request, response)
            elif request.method == 'POST':
                self.on_post(request, response)
            # Handle HEAD requests (like GET but no body)
            elif request.method == 'HEAD':
                 self.on_head(request, response) # Add a HEAD handler
            else:
                # Respond with Method Not Allowed for other unsupported methods
                self.send_error(response, 405, "Method Not Allowed", f"Method {request.method} is not supported by this server.")
        except Exception as e:
             # Catch errors during request processing (GET/POST handlers)
             print(f"!!! Internal Server Error handling {request.method} {request.url} from {client_address}: {type(e).__name__}: {e}")
             traceback.print_exc()
             # Avoid sending error if response already started/sent
             if not response.status_line: # Check if status line was already set
                 self.send_error(response, 500, "Internal Server Error", "An unexpected error occurred while processing your request.")
             else:
                  # If error happened after headers sent, can only close connection
                  print("Error occurred after response headers sent. Closing connection.")
                  try:
                      new_socket.close()
                  except: pass


    def send_error(self, response: Response, code: int, phrase: str, message: str):
        """Helper to build and send common HTML error responses."""
        try:
            response.setStatusLine(f"HTTP/1.1 {code} {phrase}\r\n")
            response.headers["Content-Type"] = "text/html; charset=UTF-8"
            # Connection: close is added automatically by Response.send() if not present
            error_body = f"""
            <!DOCTYPE html>
            <html lang="zh-cn">
            <head>
                <meta charset="UTF-8">
                <title>{code} {phrase}</title>
                 <link rel="icon" href="/server.ico" type="image/x-icon">
                 <style>
                     body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif; padding: 20px; color: #333; }}
                     .container {{ max-width: 700px; margin: auto; border: 1px solid #ddd; padding: 30px; border-radius: 5px; background-color: #f9f9f9; }}
                     h1 {{ color: #d9534f; margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 10px; font-size: 1.8em;}}
                     p {{ line-height: 1.6; }}
                     code {{ background-color: #eee; padding: 2px 5px; border-radius: 3px; }}
                     hr {{ border: 0; border-top: 1px solid #eee; margin: 20px 0; }}
                     i {{ color: #777; font-size: 0.9em;}}
                 </style>
            </head>
            <body>
                <div class="container">
                    <h1>{code} {phrase}</h1>
                    <p>{message}</p>
                    <hr>
                    <a href="/" style="text-decoration: none"><p>File Server</p></a>
                </div>
            </body>
            </html>
            """
            response.setBody(error_body)
            response.send() # Send and close
        except Exception as e:
            print(f"Error sending error response ({code}) itself: {e}")
            # If sending the error fails, try closing the socket raw
            try: response.socket.close()
            except: pass

    def on_post(self, request: Request, response: Response):
        # Basic placeholder for POST. Could implement file upload here.
        # request.body would contain the POST data.
        # request.headers['Content-Type'] would be important (e.g., multipart/form-data)
        self.send_error(response, 501, "Not Implemented", "POST requests are not currently supported by this server.")

    def on_head(self, request: Request, response: Response):
        """Handles HEAD requests. Like GET but sends only headers."""
        # Use the same logic as on_get to determine headers, but don't send body
        self.on_get(request, response, send_body=False)


    # Modified on_get to optionally skip sending body (for HEAD)
    def on_get(self, request: Request, response: Response, send_body=True):
        try:
            # --- Path Parsing and Security ---
            url_parts = urllib.parse.urlsplit(request.url)
            # Decode URL path (%20 -> space, etc.)
            decoded_path = urllib.parse.unquote(url_parts.path)

            # Normalize path, remove leading slash for joining
            relative_path = os.path.normpath(decoded_path.lstrip('/'))

            # Security: Prevent path traversal attempts
            if os.path.isabs(relative_path) or relative_path.startswith('..') or \
               any(part == '..' for part in relative_path.split(os.path.sep)):
                 raise PermissionError("Path traversal attempt detected.")

            # Construct full filesystem path
            target_path = os.path.join(self.staticPath, relative_path)
            # Final normalization and absolute path conversion
            target_path = os.path.abspath(target_path)

            # *** CRITICAL SECURITY CHECK: Ensure target is within static root ***
            # Use os.path.commonpath (Python 3.5+) or careful string comparison
            if os.path.commonpath([self.staticPath, target_path]) != self.staticPath:
                 # Handle edge case where staticPath itself is requested '' relative
                 # Allow access if target_path *is* the staticPath
                 if target_path != self.staticPath:
                    raise PermissionError("Access denied: Path is outside the allowed directory.")

            query = dict(urllib.parse.parse_qsl(url_parts.query))

            # --- Favicon Handling ---
            # Browsers request /server.ico automatically
            if url_parts.path == '/server.ico':
                favicon_fs_path = os.path.join(self.staticPath, 'server.ico')
                print(f"Favicon request. Checking for file: {favicon_fs_path}")
                if os.path.isfile(favicon_fs_path):
                    print("Serving favicon file from static directory.")
                    self._serve_file(favicon_fs_path, query, response, send_body)
                else:
                    print("Serving hardcoded default favicon.")
                    # Serve default embedded favicon
                    response.setStatusLine("HTTP/1.1 200 OK\r\n")
                    response.headers["Content-Type"] = "image/x-icon"
                    response.headers["Content-Length"] = str(len(favicon))
                    if send_body:
                        response.setBody(favicon)
                    # else: Body remains empty for HEAD
                    response.send() # Send (headers only if HEAD)
                return # Exit after handling favicon

            # --- Check if path exists ---
            if not os.path.exists(target_path):
                raise FileNotFoundError(f"Resource not found at '{target_path}'") # 404

            # --- Directory Listing ---
            if os.path.isdir(target_path):
                # Check for index.html within the directory first
                index_path = os.path.join(target_path, "index.html")
                if os.path.isfile(index_path):
                    print(f"Serving index.html for directory: {decoded_path}")
                    self._serve_file(index_path, query, response, send_body)
                else:
                     # No index.html, generate and serve directory listing
                     print(f"Serving directory listing for: {decoded_path}")
                     if not send_body: # For HEAD requests on directories
                          # Send headers indicating HTML, but no body
                          response.setStatusLine("HTTP/1.1 200 OK\r\n")
                          response.headers["Content-Type"] = "text/html; charset=UTF-8"
                          # Content-Length will be 0 implicitly or explicitly set
                          response.send()
                     else:
                         self._serve_directory_listing(target_path, decoded_path, response)


            # --- File Serving ---
            elif os.path.isfile(target_path):
                print(f"Serving file: {target_path}")
                self._serve_file(target_path, query, response, send_body)

            # --- Other Cases (Should not happen with checks above) ---
            else:
                 # e.g., Broken symlink, special file type?
                 raise RuntimeError(f"Target path is neither a file nor a directory: {target_path}") # 500


        except FileNotFoundError as e:
            print(f"404 Not Found: {request.url} -> {e}")
            self.send_error(response, 404, "Not Found", f"The requested resource <code>{urllib.parse.unquote(request.url)}</code> was not found on this server.")
        except PermissionError as e:
            print(f"403 Forbidden: {request.url} -> {e}")
            self.send_error(response, 403, "Forbidden", f"Access denied to the resource <code>{urllib.parse.unquote(request.url)}</code>.")
        except Exception as e:
            # Catch any other unexpected errors during GET processing
            print(f"!!! 500 Internal Server Error processing {request.method} {request.url}: {type(e).__name__}: {e}")
            traceback.print_exc() # Log detailed error
            # Avoid sending error if response already started
            if not response.status_line:
                self.send_error(response, 500, "Internal Server Error", "An unexpected error occurred while processing the request.")
            else:
                 print("Error occurred after response headers sent. Closing connection.")
                 try: response.socket.close()
                 except: pass


    # Modified _serve_file to optionally skip setting/sending body
    def _serve_file(self, file_path, query, response, send_body=True):
        """Prepares headers and optionally reads/sends file content."""
        response.setStatusLine("HTTP/1.1 200 OK\r\n")

        # Determine Content-Type using mimetypes
        mime_type, encoding = mimetypes.guess_type(file_path)
        if mime_type:
            content_type_header = mime_type
            # Add charset=UTF-8 for text-based types for better browser handling
            if mime_type.startswith("text/") or mime_type == "application/javascript" or mime_type == "application/json":
                content_type_header += "; charset=UTF-8"
            response.headers["Content-Type"] = content_type_header
        else:
            # Default to application/octet-stream if type unknown
            response.headers["Content-Type"] = "application/octet-stream"

        # Handle ?download=true query parameter to force download
        if "download" in query and query["download"].lower() in ['true', '1', 'yes']:
            # Ensure safe filename (remove path components)
            safe_filename = os.path.basename(file_path)
            try:
                 # Try to encode filename for header, fallback if needed
                 encoded_filename = urllib.parse.quote(safe_filename)
                 response.headers["Content-Disposition"] = f'attachment; filename="{safe_filename}"; filename*=UTF-8\'\'{encoded_filename}'
            except Exception: # Fallback for unusual filenames
                 response.headers["Content-Disposition"] = f'attachment; filename="downloaded_file"'
            # Force content type to octet-stream for downloads
            response.headers["Content-Type"] = "application/octet-stream"


        try:
            file_size = os.path.getsize(file_path)
            response.headers["Content-Length"] = str(file_size)
            # Add Last-Modified header for caching
            last_modified_time = os.path.getmtime(file_path)
            # Format according to RFC 7231 (HTTP date format)
            from datetime import datetime, timezone
            last_modified_dt = datetime.fromtimestamp(last_modified_time, tz=timezone.utc)
            response.headers["Last-Modified"] = last_modified_dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
            # Could add ETag here too based on file inode/size/mtime hash

            if send_body:
                # Read file content only if needed
                with open(file_path, "rb") as file:
                    # For very large files, consider streaming read/send in chunks
                    # For simplicity here, read all at once.
                    response.setBody(file.read())

        except IOError as e:
            print(f"IOError reading file {file_path}: {e}")
            # Raise a specific error type maybe? Or let the caller handle via 500.
            # If headers are already set, we can't easily send a 404/403 here.
            # Best to let the main handler catch this and send 500.
            raise RuntimeError(f"Could not read file content: {e}") from e
        except Exception as e:
             print(f"Unexpected error getting file metadata/content {file_path}: {e}")
             raise RuntimeError(f"Server error accessing file: {e}") from e

        response.send() # Send headers (and body if applicable)


    def _serve_directory_listing(self, dir_path, request_path, response):
        """Generates and sends an HTML directory listing."""
        response.setStatusLine("HTTP/1.1 200 OK\r\n")
        response.headers["Content-Type"] = "text/html; charset=UTF-8"
        # Prevent caching of directory listings as content changes
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"


        fileListHtml = ""
        try:
            # Ensure request_path for display ends with a slash
            display_path = request_path if request_path.endswith('/') else request_path + '/'
            escaped_display_path = urllib.parse.unquote(display_path) # Decode for display
            # Sanitize for HTML display (prevent XSS in path display)
            import html
            safe_display_path = html.escape(escaped_display_path)

            # Parent Directory Link (../)
            if display_path != '/': # Don't show ../ if already at root
                # Calculate parent URL path
                parent_url_path = '/'.join(display_path.strip('/').split('/')[:-1])
                parent_url_path = '/' + (parent_url_path + '/' if parent_url_path else '') # Add / prefix and suffix
                encoded_parent_path = urllib.parse.quote(parent_url_path)
                fileListHtml += f'<li class="dir-item parent-dir"><a href="{encoded_parent_path}"><span>{icons[""]}</span><span class="item-name">&nbsp;../</span></a></li>'

            # Get directory items and sort: directories first, then files, case-insensitive
            items = os.listdir(dir_path)
            items.sort(key=lambda x: (not os.path.isdir(os.path.join(dir_path, x)), x.lower()))

            for item_name in items:
                item_fs_path = os.path.join(dir_path, item_name)
                is_dir = os.path.isdir(item_fs_path)

                # Construct URL path for the item, ensuring no double slashes
                item_url_path = display_path + item_name
                if is_dir:
                    item_url_path += '/' # Add trailing slash for directories

                # Properly encode the item path for the URL href
                encoded_item_path = urllib.parse.quote(item_url_path)

                # Get icon based on extension (or folder icon)
                ex = os.path.splitext(item_name)[1] if not is_dir else ""
                icon_svg = get_icons(ex)

                # Sanitize item name for display in HTML
                safe_item_name = html.escape(item_name)

                # Download link (only for files)
                download_link_html = ""
                if not is_dir:
                     # Construct download URL (add ?download=true)
                     # Use encoded_item_path which is already URL-safe
                     separator = '&' if '?' in encoded_item_path else '?'
                     encoded_download_path = encoded_item_path + separator + "download=true"
                     download_link_html = f"<a href='{encoded_download_path}' class='download-link' title='Download {safe_item_name}' aria-label='Download {safe_item_name}'>{get_icons('.download')}</a>"

                # SVG preview (only for .svg files)
                svg_preview_html = ""
                if ex == '.svg':
                    # Use the encoded path directly as src
                    svg_preview_html = f"<img class='svg-preview' src='{encoded_item_path}' alt='SVG preview' loading='lazy'/>"


                # Assemble the list item HTML
                fileListHtml += f"""
                <li class="{'dir-item' if is_dir else 'file-item'}">
                    <a href='{encoded_item_path}' title='{safe_item_name}'>
                       <span class='item-icon' aria-hidden="true">{icon_svg}</span>
                       <span class='item-name'>&nbsp;{safe_item_name}</span>
                    </a>
                    {svg_preview_html}
                    {download_link_html}
                </li>
                """
        except OSError as e:
             print(f"Error listing directory {dir_path}: {e}")
             # Send 500 error instead of incomplete listing
             self.send_error(response, 500, "Internal Server Error", f"Could not list directory contents for <code>{safe_display_path}</code>.")
             return # Stop processing this request
        except Exception as e:
            print(f"Unexpected error generating directory listing for {dir_path}: {e}")
            traceback.print_exc()
            self.send_error(response, 500, "Internal Server Error", "Error generating directory listing.")
            return


        # Generate Full HTML Page
        html_body = f"""
        <!DOCTYPE html>
        <html lang="zh-cn">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="icon" href="/server.ico" type="image/x-icon">
            <title>主机 {safe_display_path}</title>
            <style>
                :root {{
                    --link-color: #1A55E8; --link-hover: #0d3dbd;
                    --hover-bg: #f0f4ff; --odd-bg: #f8f9fa;
                    --text-color: #333; --border-color: #dee2e6;
                    --icon-size: 18px; --download-icon-size: 20px;
                }}
                * {{ box-sizing: border-box; }}
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen-Sans, Ubuntu, Cantarell, "Helvetica Neue", sans-serif;
                    padding: 15px 10px; margin: 0; font-size: 15px; /* Slightly smaller base */
                    color: var(--text-color); line-height: 1.6; background-color: #fff;
                }}
                .container {{
                     max-width: 960px; margin: auto;
                     border: 1px solid var(--border-color);
                     border-radius: 6px; overflow: hidden;
                     box-shadow: 0 2px 5px rgba(0,0,0,0.05);
                }}
                h1 {{
                    font-size: 1.4em; margin: 0; padding: 12px 20px;
                    background-color: #f1f3f5; color: #495057;
                    border-bottom: 1px solid var(--border-color);
                    word-break: break-all; font-weight: 500;
                }}
                a {{ text-decoration: none; color: var(--link-color); }}
                a:hover {{ text-decoration: underline; color: var(--link-hover); }}
                ul {{ list-style: none; padding: 0; margin: 0; }}
                ul li {{
                    display: flex; align-items: center; justify-content: space-between;
                    padding: 9px 15px 9px 20px; /* Adjusted padding */
                    border-bottom: 1px solid #e9ecef; /* Lighter separator */
                    transition: background-color 0.15s ease-in-out;
                    min-height: 40px; /* Ensure consistent height */
                }}
                ul li:last-child {{ border-bottom: none; }}
                ul li:nth-child(odd):not(.parent-dir) {{ background-color: var(--odd-bg); }} /* Style odd rows, skip parent */
                ul li:hover {{ background-color: var(--hover-bg); }}
                ul li > a:first-of-type {{ /* Main link (icon + name) */
                    display: flex; align-items: center;
                    flex-grow: 1; overflow: hidden;
                    margin-right: 10px; /* Space before other icons */
                }}
                .item-icon svg, .item-icon img {{
                    vertical-align: middle; width: var(--icon-size); height: var(--icon-size);
                    flex-shrink: 0; margin-right: 10px; /* Increased space */
                    object-fit: contain; /* For img previews */
                }}
                .item-name {{
                     white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
                     flex-grow: 1; padding-top: 1px; /* Fine tune alignment */
                 }}
                .download-link, .svg-preview {{
                    flex-shrink: 0; /* Prevent shrinking */
                    margin-left: 10px; /* Space between icons */
                    display: flex; align-items: center;
                }}
                .download-link svg {{
                    width: var(--download-icon-size); height: var(--download-icon-size);
                    vertical-align: middle;
                }}
                .download-link:hover svg {{ opacity: 0.7; }}
                 .svg-preview {{
                     height: var(--icon-size); /* Match other icons */
                     width: auto; max-width: 40px; /* Limit preview width */
                     border: 1px solid #eee; padding: 1px; background-color: #fff;
                 }}
                 .parent-dir {{ background-color: #e9ecef; font-weight: 500; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>主机 {safe_display_path}</h1>
                <ul>{fileListHtml}</ul>
            </div>
        </body>
        </html>
        """
        response.setBody(html_body)
        response.send()


    def start(self):
        """Starts the server's main loop."""
        if not self._setup_socket():
             return # Exit if setup fails

        print("Server started. Press Ctrl+C to stop.")
        while self.running:
            try:
                # Wait for a connection (with timeout)
                new_socket, client_address = self.tcp_server_socket.accept()
                # print(f"Accepted connection from {client_address}") # Verbose log
                # Start a new thread to handle the client request
                client_thread = threading.Thread(
                    target=self.handle_client_request,
                    args=(new_socket, client_address),
                    daemon=True # Allows main thread to exit even if clients are active
                )
                client_thread.start()
            except socket.timeout:
                # Timeout occurred on accept(), loop continues to check self.running
                continue
            except KeyboardInterrupt:
                # User pressed Ctrl+C
                self.stop() # Signal stop
                break # Exit the loop immediately
            except socket.error as e:
                 # Handle errors during accept (e.g., socket closed by stop())
                 if self.running: # Only log if we weren't expecting to stop
                      print(f"Socket error during accept: {e}")
                 # Could add a small sleep here if accept fails repeatedly
                 # time.sleep(0.1)
            except Exception as e:
                 # Catch any other unexpected errors in the main loop
                 if self.running:
                    print(f"Unexpected error in server main loop: {e}")
                    traceback.print_exc()
                 # Consider stopping the server on critical main loop errors
                 # self.stop()
                 # break

        # --- Cleanup after loop exits ---
        print("Server loop finished.")
        if self.tcp_server_socket:
            print("Closing server socket.")
            try:
                self.tcp_server_socket.close()
            except socket.error as e:
                print(f"Error closing server socket: {e}")
        print("Server shut down gracefully.")

    # Keep start_async if needed, but start() is better for standalone script
    # def start_async(self):
    #     server_thread = threading.Thread(name="fileserver", target=self.start)
    #     server_thread.daemon = True # Allow program to exit if only this thread is running
    #     server_thread.start()
    #     return server_thread


if __name__ == '__main__':
    print("Starting HTTP File Server...")
    config = load_config()

    # Validate and prepare configuration values
    ip_addr = config.get("ip", DEFAULT_CONFIG["ip"])
    port_num = config.get("port", DEFAULT_CONFIG["port"])
    static_dir = config.get("static_path", DEFAULT_CONFIG["static_path"])

    # Validate port number
    try:
        port_num = int(port_num)
        if not (0 < port_num < 65536):
            raise ValueError("Port number must be between 1 and 65535")
    except (ValueError, TypeError) as e:
        print(f"Error: Invalid port number '{port_num}' in config or default: {e}. Using default {DEFAULT_CONFIG['port']}.")
        port_num = DEFAULT_CONFIG["port"]

    # --- Handle Command Line Argument Override for static_path ---
    if len(sys.argv) > 1:
         cmd_path_arg = sys.argv[1]
         cmd_path_abs = os.path.abspath(cmd_path_arg)
         print(f"Command line argument provided: '{cmd_path_arg}' -> '{cmd_path_abs}'")
         if os.path.isdir(cmd_path_abs):
              print(f"Overriding static path with command line argument.")
              static_dir = cmd_path_abs # Use absolute path from argument
         else:
              print(f"Warning: Command line argument '{cmd_path_abs}' is not a valid directory. Ignoring.")
    else:
         # If no command line arg, resolve config path relative to script/cwd
         static_dir = os.path.abspath(static_dir)

    # --- Final Check: Ensure the selected static directory exists ---
    print(f"Final static path configured: '{static_dir}'")
    if not os.path.isdir(static_dir):
        print(f"Error: The static directory '{static_dir}' does not exist or is not a directory.")
        print("Please create the directory, update config.json, or provide a valid path via command line.")
        sys.exit(1) # Exit if static dir is invalid

    # --- Start Server ---
    web_server = None
    try:
        web_server = HttpWebServer(ip=ip_addr, port=port_num, static_path=static_dir)
        # Use start() directly for standalone script to keep main thread alive
        web_server.start()
    except ValueError as e: # Catch specific errors like invalid static path during init
         print(f"Error initializing server: {e}")
         sys.exit(1)
    except Exception as e:
         print(f"An unexpected error occurred before starting the server: {e}")
         traceback.print_exc()
         sys.exit(1)
    finally:
         # This part might not be reached if start() runs indefinitely
         # Graceful shutdown is handled within start() via KeyboardInterrupt/stop()
         print("Main script execution finished.")
