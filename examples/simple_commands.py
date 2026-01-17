#!/usr/bin/env python3
"""
Simple Commands Example

Demonstrates running basic system commands using ftl-automation.
Shows how to execute commands and handle their output.
"""

import ftl_automation


def main():
    print("💻 Simple Commands Example")
    print("=" * 40)
    
    # Simple localhost inventory
    localhost = {
        "all": {
            "hosts": {
                "localhost": {
                    "ansible_connection": "local"
                }
            }
        }
    }
    
    with ftl_automation.automation(inventory=localhost) as ftl:
        
        ftl.debug(message="Starting command execution examples...")
        
        # Run a simple command
        ftl.debug(message="Running 'date' command...")
        result = ftl.run_module("command", cmd="date")
        
        if result.get("rc") == 0:
            ftl.debug(message=f"✅ Current date: {result.get('stdout', '').strip()}")
        else:
            ftl.debug(message="❌ Date command failed")
        
        # Check system uptime
        ftl.debug(message="Checking system uptime...")
        uptime_result = ftl.run_module("command", cmd="uptime")
        
        if uptime_result.get("rc") == 0:
            ftl.debug(message=f"✅ System uptime: {uptime_result.get('stdout', '').strip()}")
        
        # Get current user
        ftl.debug(message="Getting current user...")
        user_result = ftl.run_module("command", cmd="whoami")
        
        if user_result.get("rc") == 0:
            current_user = user_result.get('stdout', '').strip()
            ftl.debug(message=f"✅ Current user: {current_user}")
        
        # List files in current directory
        ftl.debug(message="Listing files in /tmp...")
        ls_result = ftl.run_module("command", cmd="ls -la /tmp | head -10")
        
        if ls_result.get("rc") == 0:
            ftl.debug(message="✅ Files in /tmp (first 10):")
            print(ls_result.get('stdout', ''))
        
        # Check disk usage
        ftl.debug(message="Checking disk usage...")
        df_result = ftl.run_module("command", cmd="df -h /")
        
        if df_result.get("rc") == 0:
            ftl.debug(message="✅ Root filesystem usage:")
            print(df_result.get('stdout', ''))
        
        # Example of a command that might fail
        ftl.debug(message="Testing command error handling...")
        error_result = ftl.run_module("command", cmd="ls /nonexistent-directory")
        
        if error_result.get("rc") != 0:
            ftl.debug(message="✅ Handled expected error correctly")
            ftl.debug(message=f"Error output: {error_result.get('stderr', '').strip()}")
        
        ftl.complete(message="Command execution examples completed!")


if __name__ == "__main__":
    main()