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
    Block ALL rm commands for safety.
    The rm command is destructive and cannot be undone.
    Users should use safer alternatives like trash-cli or manual deletion through file managers.
    """
    # Normalize command by removing extra spaces and converting to lowercase for pattern matching
    normalized = ' '.join(command.lower().split())
    
    # Block ANY rm command - it's simply too dangerous
    if re.search(r'\brm\b', normalized):
        return True
    
    # Also block rmdir for consistency (though it's less dangerous)
    if re.search(r'\brmdir\b', normalized):
        return True
    
    # Block unlink as well (it's another way to delete files)
    if re.search(r'\bunlink\b', normalized):
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

def is_dangerous_disk_command(command):
    """
    Detect commands that could damage disks or filesystems.
    """
    normalized = ' '.join(command.lower().split())
    
    disk_patterns = [
        r'\bdd\s',  # dd command (disk destroyer)
        r'\bmkfs',  # Make filesystem
        r'\bfdisk\b',  # Partition manipulation
        r'\bparted\b',  # Partition editor
        r'\bshred\b',  # Secure deletion
        r'\bblkdiscard\b',  # Discard device blocks
        r'\bhdparm\b',  # Hard disk parameters
        r'>\s*/dev/',  # Writing to devices
        r'>\s*/proc/',  # Writing to proc
        r'>\s*/sys/',  # Writing to sys
    ]
    
    for pattern in disk_patterns:
        if re.search(pattern, normalized):
            return True
    return False

def is_download_execute_command(command):
    """
    Detect download-and-execute patterns that could run malicious code.
    """
    normalized = ' '.join(command.lower().split())
    
    # Patterns for piping downloads directly to interpreters
    pipe_patterns = [
        r'curl.*\|\s*(bash|sh|python|perl|ruby|node)',
        r'wget.*\|\s*(bash|sh|python|perl|ruby|node)',
        r'fetch.*\|\s*(bash|sh|python|perl|ruby|node)',
        r'\|\s*bash\s*$',  # Anything piped to bash
        r'\|\s*sh\s*$',  # Anything piped to sh
        r'eval\s*\(',  # eval() function
        r'exec\s*\(',  # exec() function
    ]
    
    for pattern in pipe_patterns:
        if re.search(pattern, normalized):
            return True
    return False

def is_system_control_command(command):
    """
    Detect commands that could affect system stability.
    """
    normalized = ' '.join(command.lower().split())
    
    system_patterns = [
        r'\b(shutdown|reboot|halt|poweroff)\b',  # System shutdown
        r'\bsystemctl\s+(stop|disable|mask)',  # Stopping services
        r'\bservice\s+\w+\s+stop',  # Stopping services
        r'\bkill\s+-9',  # Force kill
        r'\bkill\s+.*-KILL',  # Force kill
        r'\bkillall\b',  # Kill all processes
        r'\bpkill\b',  # Pattern kill
        r':\(\)\{:\|:&\}',  # Fork bomb
        r'fork\s*\(\s*\)\s*while',  # Fork patterns
    ]
    
    for pattern in system_patterns:
        if re.search(pattern, normalized):
            return True
    return False

def is_permission_change_command(command):
    """
    Detect dangerous permission or ownership changes.
    """
    normalized = ' '.join(command.lower().split())
    
    permission_patterns = [
        r'chmod\s+.*777',  # World writable
        r'chmod\s+.*-R.*777',  # Recursive world writable
        r'chmod\s+.*000',  # No permissions
        r'chmod\s+.*-R.*/etc',  # Changing /etc permissions
        r'chmod\s+.*-R.*/usr',  # Changing /usr permissions
        r'chmod\s+.*-R.*/var',  # Changing /var permissions
        r'chown\s+.*-R.*/etc',  # Changing /etc ownership
        r'chown\s+.*-R.*/usr',  # Changing /usr ownership
        r'chown\s+.*-R.*/var',  # Changing /var ownership
        r'chown\s+.*root',  # Changing to root ownership
        r'umask\s+000',  # Insecure umask
    ]
    
    for pattern in permission_patterns:
        if re.search(pattern, normalized):
            return True
    return False

def is_git_destructive_command(command):
    """
    Detect potentially destructive git operations.
    """
    normalized = ' '.join(command.lower().split())
    
    git_patterns = [
        r'git\s+push\s+.*--force',  # Force push
        r'git\s+push\s+.*-f\b',  # Force push shorthand
        r'git\s+reset\s+--hard\s+head',  # Hard reset
        r'git\s+clean\s+.*-fdx',  # Clean everything
        r'git\s+clean\s+.*-f.*-d',  # Force clean with directories
        r'git\s+filter-branch',  # History rewriting
        r'git\s+rebase\s+.*--force',  # Force rebase
    ]
    
    for pattern in git_patterns:
        if re.search(pattern, normalized):
            return True
    return False

def is_package_removal_command(command):
    """
    Detect removal of system packages or important tools.
    """
    normalized = ' '.join(command.lower().split())
    
    package_patterns = [
        r'apt\s+(remove|purge|autoremove)',  # Debian/Ubuntu
        r'apt-get\s+(remove|purge|autoremove)',  # Debian/Ubuntu
        r'yum\s+(remove|erase)',  # RedHat/CentOS
        r'dnf\s+(remove|erase)',  # Fedora
        r'pacman\s+-R',  # Arch
        r'npm\s+uninstall\s+.*-g',  # Global npm packages
        r'pip\s+uninstall',  # Python packages
        r'gem\s+uninstall',  # Ruby gems
    ]
    
    for pattern in package_patterns:
        if re.search(pattern, normalized):
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
            
            # Block disk/filesystem damaging commands
            if is_dangerous_disk_command(command):
                print("BLOCKED: Command could damage disk or filesystem", file=sys.stderr)
                print("Disk operations like dd, mkfs, fdisk are prohibited", file=sys.stderr)
                sys.exit(2)
            
            # Block download-and-execute patterns
            if is_download_execute_command(command):
                print("BLOCKED: Download-and-execute pattern detected", file=sys.stderr)
                print("Piping downloads directly to interpreters is prohibited", file=sys.stderr)
                sys.exit(2)
            
            # Block system control commands
            if is_system_control_command(command):
                print("BLOCKED: System control command detected", file=sys.stderr)
                print("Commands that could affect system stability are prohibited", file=sys.stderr)
                sys.exit(2)
            
            # Block dangerous permission changes
            if is_permission_change_command(command):
                print("BLOCKED: Dangerous permission change detected", file=sys.stderr)
                print("Unsafe chmod/chown operations are prohibited", file=sys.stderr)
                sys.exit(2)
            
            # Block destructive git operations
            if is_git_destructive_command(command):
                print("BLOCKED: Destructive git operation detected", file=sys.stderr)
                print("Force push, hard reset, and history rewriting are prohibited", file=sys.stderr)
                sys.exit(2)
            
            # Block package removal
            if is_package_removal_command(command):
                print("BLOCKED: Package removal command detected", file=sys.stderr)
                print("Removing system packages or tools is prohibited", file=sys.stderr)
                sys.exit(2)
        
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