#!/usr/bin/env python3
"""
Launcher script for Mancala game
Starts the server and P3_bot in background, then runs P_client
"""

import subprocess
import time
import os
import signal
import sys
from pathlib import Path

def launch_mancala_game():
    """Launch the complete Mancala game setup"""
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    
    # File paths
    server_file = script_dir / "Mancala_server.pyc"
    p3_bot_file = script_dir / "P3_bot.pyc"
    client_file = script_dir / "P_client.py"
    
    # Check if files exist
    if not server_file.exists():
        print(f"Error: {server_file} not found!")
        return False
    if not p3_bot_file.exists():
        print(f"Error: {p3_bot_file} not found!")
        return False
    if not client_file.exists():
        print(f"Error: {client_file} not found!")
        return False
    
    processes = []
    
    try:
        print("Starting Mancala server...")
        # Start the server
        server_process = subprocess.Popen(
            [sys.executable, str(server_file)],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(("Server", server_process))
        
        # Wait for server to initialize
        print("Waiting for server to initialize (3 seconds)...")
        time.sleep(3)
        
        print("Starting P3_bot...")
        # Start P3_bot
        p3_process = subprocess.Popen(
            [sys.executable, str(p3_bot_file)],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(("P3_bot", p3_process))
        
        # Wait for P3_bot to connect
        print("Waiting for P3_bot to connect (2 seconds)...")
        time.sleep(2)
        
        print("Starting P_client (your bot)...")
        print("=" * 50)
        
        # Start your client (not in background - we want to see its output)
        client_process = subprocess.run(
            [sys.executable, str(client_file)],
            cwd=script_dir
        )
        
        print("=" * 50)
        print("Game completed!")
        
        return True
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return False
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
        
    finally:
        # Clean up background processes
        print("Cleaning up background processes...")
        for name, process in processes:
            try:
                if process.poll() is None:  # Process is still running
                    print(f"Terminating {name}...")
                    process.terminate()
                    # Wait up to 5 seconds for graceful termination
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        print(f"Force killing {name}...")
                        process.kill()
                        process.wait()
            except Exception as e:
                print(f"Error cleaning up {name}: {e}")
        
        print("Cleanup completed.")


def test_against_bot(bot_name):
    """Test against a specific bot (P3, P4, or P5)"""
    
    script_dir = Path(__file__).parent.absolute()
    
    # File paths
    server_file = script_dir / "Mancala_server.pyc"
    bot_file = script_dir / f"{bot_name}_bot.pyc"
    client_file = script_dir / "P_client.py"
    
    # Check if files exist
    if not server_file.exists():
        print(f"Error: {server_file} not found!")
        return False
    if not bot_file.exists():
        print(f"Error: {bot_file} not found!")
        return False
    if not client_file.exists():
        print(f"Error: {client_file} not found!")
        return False
    
    processes = []
    
    try:
        print(f"Starting Mancala server for {bot_name} match...")
        # Start the server
        server_process = subprocess.Popen(
            [sys.executable, str(server_file)],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append(("Server", server_process))
        
        # Wait for server to initialize
        print("Waiting for server to initialize (3 seconds)...")
        time.sleep(3)
        
        print(f"Starting {bot_name}_bot...")
        # Start the bot
        bot_process = subprocess.Popen(
            [sys.executable, str(bot_file)],
            cwd=script_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        processes.append((f"{bot_name}_bot", bot_process))
        
        # Wait for bot to connect
        print("Waiting for bot to connect (2 seconds)...")
        time.sleep(2)
        
        print("Starting P_client (your bot)...")
        print("=" * 50)
        
        # Start your client
        client_process = subprocess.run(
            [sys.executable, str(client_file)],
            cwd=script_dir
        )
        
        print("=" * 50)
        print(f"Match against {bot_name} completed!")
        
        return True
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return False
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
        
    finally:
        # Clean up background processes
        print("Cleaning up background processes...")
        for name, process in processes:
            try:
                if process.poll() is None:  # Process is still running
                    print(f"Terminating {name}...")
                    process.terminate()
                    try:
                        process.wait(timeout=5)
                    except subprocess.TimeoutExpired:
                        print(f"Force killing {name}...")
                        process.kill()
                        process.wait()
            except Exception as e:
                print(f"Error cleaning up {name}: {e}")
        
        print("Cleanup completed.")


if __name__ == "__main__":
    print("Mancala Game Launcher")
    print("=" * 30)
    
    if len(sys.argv) > 1:
        bot_name = sys.argv[1].upper()
        if bot_name in ["P3", "P4", "P5"]:
            print(f"Testing against {bot_name}_bot")
            success = test_against_bot(bot_name)
        else:
            print(f"Invalid bot name: {bot_name}")
            print("Usage: python launch_game.py [P3|P4|P5]")
            print("Or just: python launch_game.py (defaults to P3)")
            sys.exit(1)
    else:
        print("Testing against P3_bot (default)")
        success = launch_mancala_game()
    
    if success:
        print("Game session completed successfully!")
    else:
        print("Game session failed or was interrupted.")
        sys.exit(1)
