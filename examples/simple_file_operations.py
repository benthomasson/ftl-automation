#!/usr/bin/env python3
"""
Simple File Operations Example

Demonstrates basic file operations using ftl-automation.
Shows how to create, copy, and manage files on localhost.
"""

import ftl_automation


def main():
    print("📁 Simple File Operations Example")
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
        
        ftl.debug(message="Starting file operations...")
        
        # Create a simple text file
        ftl.debug(message="Creating a test file...")
        result = ftl.run_module("copy",
            content="Hello from ftl-automation!\nThis is a test file.\n",
            dest="/tmp/ftl_test.txt"
        )
        
        if result.get("changed"):
            ftl.debug(message="✅ File created successfully!")
        else:
            ftl.debug(message="ℹ️  File already exists")
        
        # Check if file exists
        ftl.debug(message="Checking if file exists...")
        stat_result = ftl.run_module("stat", path="/tmp/ftl_test.txt")
        
        if stat_result.get("stat", {}).get("exists"):
            ftl.debug(message="✅ File exists!")
            size = stat_result.get("stat", {}).get("size", 0)
            ftl.debug(message=f"File size: {size} bytes")
        else:
            ftl.debug(message="❌ File does not exist")
        
        # Read the file content
        ftl.debug(message="Reading file content...")
        read_result = ftl.run_module("slurp", src="/tmp/ftl_test.txt")
        
        if read_result.get("content"):
            import base64
            content = base64.b64decode(read_result["content"]).decode('utf-8')
            ftl.debug(message=f"File content:\n{content}")
        
        # Create a directory
        ftl.debug(message="Creating a test directory...")
        dir_result = ftl.run_module("file",
            path="/tmp/ftl_test_dir",
            state="directory"
        )
        
        if dir_result.get("changed"):
            ftl.debug(message="✅ Directory created!")
        else:
            ftl.debug(message="ℹ️  Directory already exists")
        
        # Copy file to directory
        ftl.debug(message="Copying file to directory...")
        copy_result = ftl.run_module("copy",
            src="/tmp/ftl_test.txt",
            dest="/tmp/ftl_test_dir/copied_file.txt"
        )
        
        if copy_result.get("changed"):
            ftl.debug(message="✅ File copied successfully!")
        else:
            ftl.debug(message="ℹ️  File already copied")
        
        # List directory contents
        ftl.debug(message="Listing directory contents...")
        ls_result = ftl.run_module("command", cmd="ls -la /tmp/ftl_test_dir/")
        
        if ls_result.get("rc") == 0:
            ftl.debug(message=f"Directory contents:\n{ls_result.get('stdout', '')}")
        
        # Clean up (optional)
        cleanup = ftl.user_input(
            question="Clean up test files?", 
            default="yes"
        )
        
        if cleanup.lower() in ['yes', 'y']:
            ftl.debug(message="Cleaning up test files...")
            
            # Remove files and directory
            ftl.run_module("file", path="/tmp/ftl_test.txt", state="absent")
            ftl.run_module("file", path="/tmp/ftl_test_dir", state="absent")
            
            ftl.debug(message="✅ Cleanup completed!")
        else:
            ftl.debug(message="ℹ️  Files left in place")
        
        ftl.complete(message="File operations example completed!")


if __name__ == "__main__":
    main()
