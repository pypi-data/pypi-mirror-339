#!/usr/bin/env python
"""
Generate shell completion scripts for AMAUTA.

This script generates completion scripts for various shells.
It uses the typer completion generation functionality.

Usage:
    python -m amauta_ai.scripts.completion bash > ~/.bash_completion.d/amauta.sh
    python -m amauta_ai.scripts.completion zsh > ~/.zsh/completion/_amauta
    python -m amauta_ai.scripts.completion fish > ~/.config/fish/completions/amauta.fish
    python -m amauta_ai.scripts.completion powershell > C:\Users\Username\Documents\WindowsPowerShell\amauta.ps1
"""

import sys


def main() -> int:
    """Generate shell completion script for the specified shell."""
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <shell>")
        print("Where <shell> is one of: bash, zsh, fish, powershell")
        return 1

    shell = sys.argv[1].lower()

    # Get completion script
    if shell == "bash":
        completion_script = """
# amauta bash completion script

_amauta_completion() {
    local IFS=$'\\n'
    local response

    response=$(env COMP_WORDS="${COMP_WORDS[*]}" COMP_CWORD=$COMP_CWORD _AMAUTA_COMPLETE=bash_complete amauta)

    for completion in $response; do
        IFS=',' read type value <<< "$completion"
        if [[ $type == 'dir' ]]; then
            COMPREPLY=( $(compgen -d -- "$value") )
        elif [[ $type == 'file' ]]; then
            COMPREPLY=( $(compgen -f -- "$value") )
        elif [[ $type == 'plain' ]]; then
            COMPREPLY+=($value)
        fi
    done

    return 0
}

_amauta_completion_setup() {
    complete -o nosort -F _amauta_completion amauta
}

_amauta_completion_setup;
"""
    elif shell == "zsh":
        completion_script = """
#compdef amauta

_amauta_completion() {
    local -a completions
    local -a completions_with_descriptions
    local -a response
    
    response=("${(@f)$(env _AMAUTA_COMPLETE=zsh_complete amauta)}")
    
    for type value in ${(ps: :)response}; do
        if [[ $type == 'dir' ]]; then
            _path_files -/
        elif [[ $type == 'file' ]]; then
            _path_files -f
        elif [[ $type == 'plain' ]]; then
            if [[ -n $value ]]; then
                completions+=($value)
            fi
        fi
    done
    
    if [ -n "$completions" ]; then
        _describe -t values 'amauta' completions
    fi
}

compdef _amauta_completion amauta
"""
    elif shell == "fish":
        completion_script = """
function __fish_amauta_complete
    set -l response
    
    for i in (commandline -cop)
        set -a cmd $i
    end
    
    set -l completions (env _AMAUTA_COMPLETE=fish_complete amauta)
    
    for completion in $completions
        set -l name_value (string split "," $completion)
        
        if test $name_value[1] = "dir"
            __fish_complete_directories $name_value[2]
        else if test $name_value[1] = "file"
            __fish_complete_path $name_value[2]
        else if test $name_value[1] = "plain"
            echo $name_value[2]
        end
    end
end

complete --no-files -c amauta -a "(__fish_amauta_complete)"
"""
    elif shell == "powershell":
        completion_script = """
# AMAUTA PowerShell completion script

function _amautaCompletion {
    param($wordToComplete, $commandAst, $cursorPosition)
    
    # Get current command line
    $line = $commandAst.ToString()
    
    # Generate the completion data from AMAUTA
    $env:_AMAUTA_COMPLETE = 'powershell_complete'
    $completions = @(amauta $line) | ForEach-Object {
        $type, $value = $_.Split(',')
        
        if ($type -eq 'plain') {
            if ($value -like "$wordToComplete*") {
                [System.Management.Automation.CompletionResult]::new(
                    $value, 
                    $value, 
                    'ParameterValue',
                    $value
                )
            }
        }
        elseif ($type -eq 'dir') {
            $matches = Get-ChildItem -Directory -Path $value* -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "$wordToComplete*" }
            foreach ($match in $matches) {
                $completionText = $match.FullName
                if ($match.PSIsContainer) {
                    $completionText += '\'
                }
                
                [System.Management.Automation.CompletionResult]::new(
                    $completionText, 
                    $match.Name, 
                    'ParameterValue',
                    $match.Name
                )
            }
        }
        elseif ($type -eq 'file') {
            $matches = Get-ChildItem -File -Path $value* -ErrorAction SilentlyContinue | Where-Object { $_.Name -like "$wordToComplete*" }
            foreach ($match in $matches) {
                [System.Management.Automation.CompletionResult]::new(
                    $match.FullName, 
                    $match.Name, 
                    'ParameterValue',
                    $match.Name
                )
            }
        }
    }
    
    return $completions
}

# Register the completion function
Register-ArgumentCompleter -Native -CommandName amauta -ScriptBlock $function:_amautaCompletion

Write-Output "AMAUTA PowerShell completion has been loaded."
Write-Output "To make this permanent, add this script to your PowerShell profile:"
Write-Output '1. Run $PROFILE to see your profile path'
Write-Output '2. Create the profile file if it does not exist'
Write-Output '3. Add the line: . path\\to\\amauta_completion.ps1'
"""
    else:
        print(f"Error: Unsupported shell '{shell}'")
        print("Supported shells: bash, zsh, fish, powershell")
        return 1

    # Print the completion script to stdout
    print(completion_script)
    return 0


if __name__ == "__main__":
    sys.exit(main())
