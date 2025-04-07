import os, sys, json, http.client
from typing import Callable, Dict, Tuple, Union, Optional, List
from cryptography.fernet import Fernet

__version__ = "0.2"

# === Configurations ===
_registered_commands: Dict[str, Dict] = {}
_command_flags: Dict[str, Union[bool, float, None]] = {}

_api_key: Optional[str] = None
_model_name: Optional[str] = None
_memory_history: List[dict] = []

# Encryption key setup
if "QEXEC_MEM_KEY" in os.environ:
    _mem_key = os.environ["QEXEC_MEM_KEY"].encode()
else:
    _mem_key = Fernet.generate_key()
    print("[Warn] New encryption key generated. Save it via QEXEC_MEM_KEY env var for persistence.")

_mem_cipher = Fernet(_mem_key)

# === Setup functions ===

def configure(model: str, api_key: str):
    """Set the model name and API key"""
    global _model_name, _api_key
    _model_name = model
    _api_key = api_key

def save_memory(filename="qexec_mem.json.enc"):
    data = json.dumps(_memory_history).encode()
    encrypted = _mem_cipher.encrypt(data)
    with open(filename, "wb") as f:
        f.write(encrypted)

def load_memory(filename="qexec_mem.json.enc"):
    global _memory_history
    if not os.path.isfile(filename):
        return
    with open(filename, "rb") as f:
        decrypted = _mem_cipher.decrypt(f.read())
    _memory_history = json.loads(decrypted.decode())

def clear_memory():
    global _memory_history
    _memory_history = []

def register_exec(
    label: str,
    func: Callable,
    *,
    description: str,
    type: str = "action",
    value_range: Optional[Tuple[float, float]] = None
):
    """Register a command with label, function, description, and type
    
    Types:
    - switch: True/False value (on/off)
    - button: Toggle function (no parameters)
    - range: Numeric value within a range
    """
    if not description:
        raise ValueError("Description required")
    if label in _registered_commands:
        raise ValueError(f"{label} already registered")
    
    if type not in ["switch", "button", "range"]:
        raise ValueError(f"Invalid type: {type}. Must be one of: switch, button, range")
    
    if type == "range" and value_range is None:
        raise ValueError("value_range is required for type 'range'")

    _registered_commands[label] = {
        "func": func,
        "description": description,
        "type": type,
        "range": value_range,
    }

    attr = f'cmd_{label.replace("-","_").replace(" ","_")}'
    init_val = False if type == "switch" else None
    _command_flags[attr] = init_val
    setattr(sys.modules[__name__], attr, init_val)

# === Prompt generator with explicit examples ===

def _generate_instructions() -> str:
    base = '''
You are an AI assistant that can both engage in conversation and control home devices via IR signals.

IMPORTANT RULES:
1. For normal conversation or questions (e.g., "how are you?", "what's your name?"), respond naturally WITHOUT using any command markers.

2. ONLY use device control commands (#@$QEXEC#@$) when:
   - The user explicitly asks to control a device
   - The request is clearly about device manipulation
   - Examples of when to use commands:
     * "turn on the lights"
     * "set fan speed to 50%"
     * "toggle the lights please"

3. NEVER use device commands for:
   - General conversation
   - Questions about your status
   - Questions about capabilities
   - Any request not explicitly about device control

Command Format (ONLY for device control requests):
#@$QEXEC#@$ YOUR_COMMAND #@$QEXEC#@$ 

Examples:
User: "how are you?"
Assistant: I'm doing well, thank you! How are you?

User: "turn on the lights"
Assistant: I'll turn on the lights for you.
#@$QEXEC#@$ lights-on-ir=true #@$QEXEC#@$ 

User: "what can you do?"
Assistant: I can help you control various home devices like lights and fans, and I can also chat with you about other topics. Would you like to know about specific device controls?

### Available device control commands:
'''

    lines = []
    for label, meta in _registered_commands.items():
        desc = meta['description']
        cmd_type = meta['type']
        
        if cmd_type == "range":
            rng = meta.get('range', (0,100))
            example = f"#@$QEXEC#@$ {label}={rng[1]} #@$QEXEC#@$"
            lines.append(f"- **{label}**: {desc} (range {rng[0]} to {rng[1]})")
        elif cmd_type == "switch":
            example = f"#@$QEXEC#@$ {label}=true #@$QEXEC#@$"
            lines.append(f"- **{label}**: {desc} (switch: true/false)")
        else:  # button type
            example = f"#@$QEXEC#@$ {label} #@$QEXEC#@$"
            lines.append(f"- **{label}**: {desc} (button: toggle)")

    return base + "\n".join(lines)

def compose_prompt(user_instructions: str) -> str:
    return f"{user_instructions}\n\n{_generate_instructions()}"

# === LLM call ===

def call_llm(user_instructions: str) -> str:
    if not (_model_name and _api_key):
        raise RuntimeError("Call configure() first to set model and API key")

    prompt = compose_prompt(user_instructions)

    headers = {
        "Authorization": f"Bearer {_api_key}",
        "Content-Type": "application/json"
    }

    # Add conversation history
    _memory_history.append({"role": "user", "content": user_instructions})
    msgs = _memory_history.copy()
    msgs.append({"role": "system", "content": _generate_instructions()})

    req = {
        "model": _model_name,
        "messages": msgs,
        "temperature": 0.2,
        "max_tokens": 512
    }

    conn = http.client.HTTPSConnection("openrouter.ai")
    conn.request("POST", "/api/v1/chat/completions", json.dumps(req), headers)
    resp = conn.getresponse()
    data = resp.read()
    conn.close()

    if resp.status != 200:
        raise RuntimeError(f"API error {resp.status}: {data.decode()}")

    js = json.loads(data)
    out = js['choices'][0]['message']['content']
    _memory_history.append({"role": "assistant", "content": out})
    return out

# === Command Extract and Execute ===

def parse_and_execute(response: str):
    # Reset all command flags
    for label, meta in _registered_commands.items():
        attr = f'cmd_{label.replace("-","_").replace(" ","_")}'
        init_val = False if meta['type'] == "switch" else None
        _command_flags[attr] = init_val
        setattr(sys.modules[__name__], attr, init_val)

    # Find commands inside markers
    parts = response.split("#@$QEXEC#@$")

    for idx in range(1, len(parts), 2):
        cmd = parts[idx].strip()
        if '=' in cmd:
            k, v = cmd.split('=', 1)
            k, v = k.strip(), v.strip()
            meta = _registered_commands.get(k)
            if not meta:
                continue
            try:
                if meta['type'] == "switch":
                    val = v.lower() == "true"
                elif meta['type'] == "range":
                    val = float(v)
                    if meta['range'] and (val < meta['range'][0] or val > meta['range'][1]):
                        print(f"[WARN] Value {val} out of range {meta['range']} for {k}")
                        continue
                else:
                    continue  # button type doesn't use =value format
                
                attr = f'cmd_{k.replace("-","_").replace(" ","_")}'
                _command_flags[attr] = val
                setattr(sys.modules[__name__], attr, val)
                meta['func'](val)
            except Exception as e:
                print(f"[ERR] Executing command {k}: {e}")
        else:
            k = cmd.strip()
            meta = _registered_commands.get(k)
            if not meta:
                continue
            try:
                if meta['type'] == "button":
                    meta['func']()
                else:
                    print(f"[WARN] Command {k} requires a value for type {meta['type']}")
            except Exception as e:
                print(f"[ERR] Executing command {k}: {e}")
