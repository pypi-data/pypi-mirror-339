import os, sys, json, http.client, urllib.parse
from typing import Callable, Dict, Tuple, Union, Optional, List, Any

__version__ = "0.5"

# === Configurations ===
_registered_commands: Dict[str, Dict] = {}
_command_flags: Dict[str, Union[bool, float, None]] = {}

_memory_history: List[dict] = []

# === Provider Configuration ===
class Provider:
    """Base provider configuration"""
    OPENROUTER = "openrouter"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AISTUDIO = "aistudio"
    GROK = "grok"
    META = "meta" 
    MISTRAL = "mistral"
    
    # Provider endpoints and configurations
    ENDPOINTS = {
        OPENROUTER: "openrouter.ai",
        OPENAI: "api.openai.com",
        ANTHROPIC: "api.anthropic.com",
        AISTUDIO: "generativelanguage.googleapis.com",
        GROK: "api.grok.x",
        META: "api.meta.com",
        MISTRAL: "api.mistral.ai"
    }
    
    # Path formats for different providers
    PATHS = {
        OPENROUTER: "/api/v1/chat/completions",
        OPENAI: "/v1/chat/completions", 
        ANTHROPIC: "/v1/messages",
        AISTUDIO: "/v1beta/models/{model}:generateContent",
        GROK: "/v1/chat/completions",
        META: "/v1/chat/completions",
        MISTRAL: "/v1/chat/completions"
    }
    
    # Special handling for providers with different request formats
    @staticmethod
    def format_request(provider: str, model: str, messages: List[dict], temperature: float = 0.2, max_tokens: int = 512) -> Dict[str, Any]:
        """Format request based on provider"""
        if provider == Provider.ANTHROPIC:
            # Convert roles (system -> assistant)
            formatted_msgs = []
            system_content = ""
            
            for msg in messages:
                if msg["role"] == "system":
                    system_content += msg["content"] + "\n"
                else:
                    formatted_msgs.append({
                        "role": msg["role"],
                        "content": msg["content"]
                    })
            
            return {
                "model": model,
                "messages": formatted_msgs,
                "system": system_content.strip() if system_content else None,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
        elif provider == Provider.AISTUDIO:
            # Google AI Studio format
            content_parts = []
            for msg in messages:
                role = "user" if msg["role"] == "user" else "model"
                if msg["role"] == "system":
                    role = "system"
                content_parts.append({
                    "role": role,
                    "parts": [{"text": msg["content"]}]
                })
            
            return {
                "contents": content_parts,
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                    "topP": 0.9,
                }
            }
        else:
            # Default format (OpenAI-compatible)
            return {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
    
    @staticmethod
    def extract_response(provider: str, data: Dict[str, Any]) -> str:
        """Extract response text based on provider format"""
        if provider == Provider.ANTHROPIC:
            return data["content"][0]["text"]
        elif provider == Provider.AISTUDIO:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # Default format (OpenAI-compatible)
            return data["choices"][0]["message"]["content"]

# === Redundancy System ===
class red:
    class api:
        main = None
        provider = None
        fallbacks = []
        
        @classmethod
        def add(cls, key, provider=Provider.OPENROUTER, priority=0):
            """Add API key with priority (lower = higher priority)
            
            Use this to add fallback API keys in case the main one fails.
            
            Example:
            red.api.add("your-openai-api-key", Provider.OPENAI, priority=1)
            """
            cls.fallbacks.append({
                "key": key, 
                "provider": provider, 
                "priority": priority
            })
            cls.fallbacks.sort(key=lambda x: x["priority"])
            return cls
        
        @classmethod
        def set_main(cls, key, provider=Provider.OPENROUTER):
            """Set main API key (primary, not fallback)
            
            Example:
            red.api.set_main("your-openai-api-key", Provider.OPENAI)
            """
            cls.main = key
            cls.provider = provider
            return cls
    
    class mdl:
        main = None
        fallbacks = []
        
        @classmethod
        def add(cls, name, provider=Provider.OPENROUTER, priority=0):
            """Add model with priority (lower = higher priority)
            
            Use this to add fallback models in case the main one fails.
            
            Example:
            red.mdl.add("gpt-4-turbo", Provider.OPENAI, priority=1)  
            """
            cls.fallbacks.append({
                "name": name, 
                "provider": provider, 
                "priority": priority
            })
            cls.fallbacks.sort(key=lambda x: x["priority"])
            return cls
        
        @classmethod
        def set_main(cls, name, provider=Provider.OPENROUTER):
            """Set main model (primary, not fallback)
            
            Example:
            red.mdl.set_main("gpt-4-turbo", Provider.OPENAI)
            """
            cls.main = {"name": name, "provider": provider, "priority": -1}
            return cls
    
    class meminit:
        @staticmethod
        def init(mem_file="qexec_mem.json"):
            """Initialize memory management"""
            global _memory_history
            if os.path.isfile(mem_file):
                try:
                    with open(mem_file, "r") as f:
                        _memory_history = json.load(f)
                except Exception as e:
                    print(f"[WARN] Memory file loading failed: {e}")
                    _memory_history = []
            else:
                _memory_history = []
            return _memory_history
    
    @staticmethod
    def memsv(mem_file="qexec_mem.json"):
        """Save memory to file"""
        try:
            with open(mem_file, "w") as f:
                json.dump(_memory_history, f)
            return True
        except Exception as e:
            print(f"[ERROR] Memory save failed: {e}")
            return False
    
    @staticmethod
    def memclr():
        """Clear memory history"""
        global _memory_history
        _memory_history = []
        return True
    
    @staticmethod
    def bind():
        """Bind current configuration to a dict that can be used in configure()
        
        Use after setting up with red.api.set_main() and red.mdl.set_main()
        
        Example:
        red.api.set_main("your-api-key", Provider.OPENAI)
        red.mdl.set_main("gpt-4-turbo", Provider.OPENAI)
        configure(red.bind())
        """
        return {
            'api': red.api.main,
            'provider': red.api.provider,
            'model': red.mdl.main['name'] if red.mdl.main else None
        }

# Initialize default fallback models
red.mdl.add("quasaralph", Provider.OPENROUTER, 0)
red.mdl.add("gemini-1.5-pro", Provider.AISTUDIO, 1)

# === Setup functions ===

def config(config_dict=None, model=None, api_key=None, provider=Provider.OPENROUTER):
    """Set the model name, API key, and provider
    
    Two ways to configure:
    
    1. Direct configuration (single model, no redundancy):
       configure(model="gpt-4-turbo", api_key="your-api-key", provider=Provider.OPENAI)
    
    2. Using red binding (supports redundancy):
       # First set up with red classes
       red.api.set_main("your-api-key", Provider.OPENAI)
       red.mdl.set_main("gpt-4-turbo", Provider.OPENAI)
       # Then optionally add fallbacks
       red.api.add("your-anthropic-key", Provider.ANTHROPIC, 1)
       red.mdl.add("claude-3-opus-20240229", Provider.ANTHROPIC, 1)
       # Finally configure with bind
       configure(red.bind())
    
    Provider can be one of:
    - Provider.OPENROUTER
    - Provider.OPENAI
    - Provider.ANTHROPIC
    - Provider.AISTUDIO
    - Provider.GROK
    - Provider.META
    - Provider.MISTRAL
    
    Or combined with comma separation:
    - "openrouter,openai,anthropic"
    """
    if config_dict is not None:
        if isinstance(config_dict, dict):
            model = config_dict.get('model')
            api_key = config_dict.get('api')
            provider = config_dict.get('provider', Provider.OPENROUTER)
        else:
            raise ValueError("config_dict must be a dictionary")
    
    # Process comma-separated providers
    if isinstance(provider, str) and "," in provider:
        providers = [p.strip() for p in provider.split(",")]
        main_provider = providers[0]
        
        # Set main provider
        if model and api_key:
            red.mdl.set_main(model, main_provider)
            red.api.set_main(api_key, main_provider)
        
        # Add fallbacks for additional providers
        for i, p in enumerate(providers[1:], 1):
            if p == main_provider:
                continue
            fallback_key = os.environ.get(f"{p.upper()}_API_KEY")
            if fallback_key:
                red.api.add(fallback_key, p, i)
                # Add a default model for this provider if we know one
                default_models = {
                    Provider.OPENAI: "gpt-4-turbo",
                    Provider.ANTHROPIC: "claude-3-opus-20240229",
                    Provider.AISTUDIO: "gemini-1.5-pro",
                    Provider.GROK: "grok-0",
                    Provider.META: "llama-3-70b-chat",
                    Provider.MISTRAL: "mistral-large-latest"
                }
                if p in default_models:
                    red.mdl.add(default_models[p], p, i)
    else:
        # Single provider
        if model:
            red.mdl.set_main(model, provider)
        if api_key:
            red.api.set_main(api_key, provider)
    
    # Initialize memory
    red.meminit.init()

def regexec(
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

# === LLM call with redundancy ===

def llm(user_instructions: str) -> str:
    if not (red.mdl.main and red.api.main):
        raise RuntimeError("Call configure() first to set model and API key")

    prompt = compose_prompt(user_instructions)
    _memory_history.append({"role": "user", "content": user_instructions})
    msgs = _memory_history.copy()
    msgs.append({"role": "system", "content": _generate_instructions()})

    # Try main model first
    response = _try_api_call(
        red.mdl.main["name"], 
        red.api.main, 
        red.mdl.main["provider"], 
        msgs
    )
    
    # If main fails, try fallbacks
    if not response:
        # Try alternative models with same API
        for model in red.mdl.fallbacks:
            response = _try_api_call(
                model["name"], 
                red.api.main, 
                model["provider"], 
                msgs
            )
            if response:
                print(f"[INFO] Using fallback model: {model['name']} ({model['provider']})")
                break
        
        # If model fallbacks fail, try API fallbacks
        if not response:
            for api in red.api.fallbacks:
                # Try with main model
                response = _try_api_call(
                    red.mdl.main["name"],
                    api["key"],
                    api["provider"],
                    msgs
                )
                if response:
                    print(f"[INFO] Using fallback API: {api['provider']}")
                    break
                
                # Try with compatible fallback models
                for model in red.mdl.fallbacks:
                    if model["provider"] == api["provider"]:
                        response = _try_api_call(
                            model["name"],
                            api["key"],
                            api["provider"],
                            msgs
                        )
                        if response:
                            print(f"[INFO] Using fallback: {model['name']} + {api['provider']}")
                            break
    
    if not response:
        raise RuntimeError("All API calls failed")
    
    _memory_history.append({"role": "assistant", "content": response})
    red.memsv()  # Auto-save memory after each response
    return response

def _try_api_call(model_name: str, api_key: str, provider: str, messages: List[dict]) -> Optional[str]:
    """Try to call the API with the given model, key and provider"""
    
    # Check if provider endpoint is configured
    if provider not in Provider.ENDPOINTS:
        print(f"[ERROR] Unknown provider: {provider}")
        return None
    
    endpoint = Provider.ENDPOINTS[provider]
    path = Provider.PATHS[provider]
    
    # For Google AI Studio, include model in path
    if provider == Provider.AISTUDIO:
        path = path.format(model=model_name)
    
    # Format request based on provider
    req_data = Provider.format_request(provider, model_name, messages)
    
    # Handle auth header differences
    headers = {"Content-Type": "application/json"}
    
    if provider == Provider.AISTUDIO:
        # Google uses query param
        path += f"?key={api_key}"
    else:
        # Most providers use Bearer token
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        # Make the API call
        if provider == Provider.ANTHROPIC:
            conn = http.client.HTTPSConnection(endpoint)
        else:
            conn = http.client.HTTPSConnection(endpoint)
            
        conn.request("POST", path, json.dumps(req_data), headers)
        resp = conn.getresponse()
        data = resp.read()
        conn.close()

        if resp.status != 200:
            print(f"[WARN] API error with {provider}/{model_name}: {resp.status}")
            print(data.decode()[:200])
            return None

        # Parse and extract response based on provider
        try:
            js = json.loads(data)
            return Provider.extract_response(provider, js)
        except Exception as e:
            print(f"[ERROR] Failed to parse {provider} response: {e}")
            return None
            
    except Exception as e:
        print(f"[ERROR] API call failed for {provider}/{model_name}: {e}")
        return None

# === Command Extract and Execute ===

def pne(response: str):
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

# Example usage:
"""
# Method 1: Direct configuration (no redundancy)
configure(
    model="gpt-4-turbo", 
    api_key="your-openai-api-key", 
    provider=Provider.OPENAI
)

# Method 2: Using red binding (supports redundancy)
# Set main API and model
red.api.set_main("your-openai-api-key", Provider.OPENAI)
red.mdl.set_main("gpt-4-turbo", Provider.OPENAI)

# Add fallback API and models (optional)
red.api.add("your-anthropic-api-key", Provider.ANTHROPIC, priority=1)
red.mdl.add("claude-3-opus-20240229", Provider.ANTHROPIC, priority=1)

# Configure with binding
configure(red.bind())

# After configuration, call the LLM:
response = call_llm("What's the weather like today?")
print(response)

# Process commands in the response
parse_and_execute(response)
"""