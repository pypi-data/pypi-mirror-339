"""
Main entry point for SpeedClick Pro
"""

import sys
import os

def main():
    """
    Launch the SpeedClick Pro application
    """
    from .auto_clicker import AutoClicker
    
    # Create the application instance
    app = AutoClicker()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
