#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys
import re
from pathlib import Path

def is_dangerous_rm_command(command):
    """
    Comprehensive detection of dangerous rm commands.
    Matches various forms of rm -rf and similar destructive patterns.
    """
    # Normalize command by removing extra spaces and converting to lowercase
    normalized = ' '.join(command.lower().split())
    
    # Pattern 1: Standard rm -rf variations
    patterns = [
        r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf, rm -fr, rm -Rf, etc.
        r'\brm\s+.*-[a-z]*f[a-z]*r',  # rm -fr variations
        r'\brm\s+--recursive\s+--force',  # rm --recursive --force
        r'\brm\s+--force\s+--recursive',  # rm --force --recursive
        r'\brm\s+-r\s+.*-f',  # rm -r ... -f
        r'\brm\s+-f\s+.*-r',  # rm -f ... -r
    ]
    
    # Check for dangerous patterns
    for pattern in patterns:
        if re.search(pattern, normalized):
            return True
    
    # Pattern 2: Check for rm with recursive flag targeting dangerous paths
    dangerous_paths = [
        r'/',           # Root directory
        r'/\*',         # Root with wildcard
        r'~',           # Home directory
        r'~/',          # Home directory path
        r'\$HOME',      # Home environment variable
        r'\.\.',        # Parent directory references
        r'\*',          # Wildcards in general rm -rf context
        r'\.',          # Current directory
        r'\.\s*$',      # Current directory at end of command
    ]
    
    if re.search(r'\brm\s+.*-[a-z]*r', normalized):  # If rm has recursive flag
        for path in dangerous_paths:
            if re.search(path, normalized):
                return True
    
    return False

def is_env_exposure_command(command):
    """
    Detect commands that could expose sensitive environment variables.
    Blocks various forms of env variable dumping and grep patterns.
    """
    # Normalize command by removing extra spaces
    normalized = ' '.join(command.lower().split())
    
    # Dangerous environment variable exposure patterns - be more specific
    exposure_patterns = [
        r'\benv\s*\|\s*grep',  # env | grep specifically
        r'\bprintenv\s*\|\s*grep',  # printenv | grep specifically
        r'\benv\s*\|\s*head',  # env | head
        r'\bprintenv\s*\|\s*head',  # printenv | head
        r'\benv\s+.*-E',  # env with grep -E flag
        r'\bprintenv\s+.*-E',  # printenv with grep -E flag
        r'^env\s*$',  # bare env command at start (shows all vars)
        r'^printenv\s*$',  # bare printenv command at start
        r'set\s*\|\s*grep',  # set | grep (bash builtin)
        r'export\s*\|\s*grep',  # export | grep
        r'declare\s*\|\s*grep',  # declare | grep (bash)
    ]
    
    # Check for exposure patterns
    for pattern in exposure_patterns:
        if re.search(pattern, normalized):
            return True
    
    # Check for direct env var access patterns - only specific sensitive variables
    sensitive_env_patterns = [
        r'\becho\s+.*\$[A-Z_]*API[_A-Z0-9]*KEY',  # echo $API_KEY variants
        r'\becho\s+.*\$[A-Z_]*SECRET[_A-Z0-9]*',  # echo $SECRET variants
        r'\becho\s+.*\$[A-Z_]*TOKEN[_A-Z0-9]*',  # echo $TOKEN variants
        r'\becho\s+.*\$[A-Z_]*PASSWORD[_A-Z0-9]*',  # echo $PASSWORD variants
        r'\becho\s+.*\$(ELEVENLABS|OPENAI|ANTHROPIC|CLAUDE|AWS|GCP)_[A-Z_]+',  # Specific service vars
        r'\bprintf\s+.*\$[A-Z_]*API[_A-Z0-9]*KEY',  # printf equivalents
        r'\bprintf\s+.*\$[A-Z_]*SECRET[_A-Z0-9]*',
        r'\bprintf\s+.*\$[A-Z_]*TOKEN[_A-Z0-9]*',
        r'\bprintf\s+.*\$[A-Z_]*PASSWORD[_A-Z0-9]*',
        r'\bprintf\s+.*\$(ELEVENLABS|OPENAI|ANTHROPIC|CLAUDE|AWS|GCP)_[A-Z_]+',
    ]
    
    # Check for specific sensitive variable exposure
    for pattern in sensitive_env_patterns:
        if re.search(pattern, normalized):
            return True
    
    return False

def is_env_file_access(tool_name, tool_input):
    """
    Check if any tool is trying to access .env files containing sensitive data.
    """
    if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write', 'Bash']:
        # Check file paths for file-based tools
        if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write']:
            file_path = tool_input.get('file_path', '')
            if '.env' in file_path and not file_path.endswith('.env.sample'):
                return True
        
        # Check bash commands for .env file access
        elif tool_name == 'Bash':
            command = tool_input.get('command', '')
            # Pattern to detect .env file access (but allow .env.sample)
            env_patterns = [
                r'\b\.env\b(?!\.sample)',  # .env but not .env.sample
                r'cat\s+.*\.env\b(?!\.sample)',  # cat .env
                r'echo\s+.*>\s*\.env\b(?!\.sample)',  # echo > .env
                r'touch\s+.*\.env\b(?!\.sample)',  # touch .env
                r'cp\s+.*\.env\b(?!\.sample)',  # cp .env
                r'mv\s+.*\.env\b(?!\.sample)',  # mv .env
            ]
            
            for pattern in env_patterns:
                if re.search(pattern, command):
                    return True
    
    return False

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)
        
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        
        # Check for .env file access (blocks access to sensitive environment files)
        if is_env_file_access(tool_name, tool_input):
            print("BLOCKED: Access to .env files containing sensitive data is prohibited", file=sys.stderr)
            print("Use .env.sample for template files instead", file=sys.stderr)
            sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude
        
        # Check for dangerous commands
        if tool_name == 'Bash':
            command = tool_input.get('command', '')
            
            # Block rm -rf commands with comprehensive pattern matching
            if is_dangerous_rm_command(command):
                print("BLOCKED: Dangerous rm command detected and prevented", file=sys.stderr)
                sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude
            
            # Block environment variable exposure commands
            if is_env_exposure_command(command):
                print("BLOCKED: Command could expose sensitive environment variables", file=sys.stderr)
                print("Environment variable access is prohibited for security", file=sys.stderr)
                sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude
        
        # Ensure log directory exists
        log_dir = Path.cwd() / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'pre_tool_use.json'
        
        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []
        
        # Append new data
        log_data.append(input_data)
        
        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        sys.exit(0)
        
    except json.JSONDecodeError:
        # Gracefully handle JSON decode errors
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)

if __name__ == '__main__':
    main()