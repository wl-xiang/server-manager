#!/usr/bin/env python3
import signal
import sys
import time
import argparse

running = True

def signal_handler(signum, frame):
    global running
    sig_name = signal.Signals(signum).name
    print(f"Received {sig_name}, shutting down gracefully...")
    running = False

def main():
    parser = argparse.ArgumentParser(description='Test Server Application')
    parser.add_argument('--message', '-m', default='Test Server', 
                        help='Custom message to display')
    parser.add_argument('--interval', '-i', type=int, default=5,
                        help='Log interval in seconds')
    args = parser.parse_args()
    
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"{args.message} started (PID: {sys.argv[0]})")
    print("Press Ctrl+C or send SIGTERM to stop")
    
    counter = 0
    while running:
        counter += 1
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {args.message} - Heartbeat #{counter}")
        sys.stdout.flush()
        
        for _ in range(args.interval):
            if not running:
                break
            time.sleep(1)
    
    print(f"{args.message} stopped")

if __name__ == "__main__":
    main()
