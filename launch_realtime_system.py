"""
Main System Launcher for Real-time Demo

This script starts all components needed for the real-time elderly monitoring system demo.
Includes WebSocket server, sensor simulation, ML integration, and web server.
"""

import asyncio
import threading
import time
import signal
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from src.core.websocket_api import start_websocket_server, get_websocket_manager
from src.core.realtime_system_integration import initialize_system_integration, start_realtime_system
from sensors.advanced_sensor_simulator import initialize_sensor_simulator
import http.server
import socketserver
import webbrowser

class RealTimeSystemLauncher:
    """Main launcher for the real-time system."""
    
    def __init__(self):
        self.websocket_port = 8765
        self.web_port = 8000
        self.is_running = False
        self.threads = []
        
        # Initialize components
        self.system_integration = initialize_system_integration()
        self.websocket_manager = get_websocket_manager()
        
    def start_web_server(self):
        """Start the web server for frontend files."""
        try:
            # Change to frontend directory
            os.chdir(project_root / 'frontend')
            
            # Create handler
            handler = http.server.SimpleHTTPRequestHandler
            
            # Create server
            with socketserver.TCPServer(("", self.web_port), handler) as httpd:
                print(f"🌐 Web server started on http://localhost:{self.web_port}")
                print("📱 Available dashboards:")
                print(f"   • Senior Dashboard: http://localhost:{self.web_port}/senior_dashboard_realtime.html")
                print(f"   • Guardian Dashboard: http://localhost:{self.web_port}/guardian_dashboard_realtime.html")
                print(f"   • Learning Analytics: http://localhost:{self.web_port}/learning_analytics_realtime.html")
                print(f"   • Demo Control Panel: http://localhost:{self.web_port}/demo_control_panel.html")
                print("=" * 60)
                
                httpd.serve_forever()
                
        except Exception as e:
            print(f"❌ Failed to start web server: {e}")
    
    def start_websocket_server(self):
        """Start the WebSocket server."""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(start_websocket_server('localhost', self.websocket_port))
        except Exception as e:
            print(f"❌ Failed to start WebSocket server: {e}")
    
    def start_realtime_system(self):
        """Start the real-time system integration."""
        try:
            success = start_realtime_system()
            if success:
                print("✅ Real-time system started")
            else:
                print("❌ Failed to start real-time system")
        except Exception as e:
            print(f"❌ Failed to start real-time system: {e}")
    
    def start_all_services(self):
        """Start all services in separate threads."""
        print("🚀 Starting SilverCare Real-time System...")
        print("=" * 60)
        
        # Start WebSocket server in thread
        ws_thread = threading.Thread(target=self.start_websocket_server, daemon=True)
        ws_thread.start()
        self.threads.append(ws_thread)
        
        # Wait a moment for WebSocket server to start
        time.sleep(2)
        
        # Start real-time system in thread
        rt_thread = threading.Thread(target=self.start_realtime_system, daemon=True)
        rt_thread.start()
        self.threads.append(rt_thread)
        
        # Start web server in main thread (blocking)
        try:
            self.start_web_server()
        except KeyboardInterrupt:
            print("\n🛑 Shutting down system...")
            self.stop_system()
    
    def stop_system(self):
        """Stop all system components."""
        print("⏹️ Stopping all services...")
        
        # Stop real-time system
        from src.core.realtime_system_integration import stop_realtime_system
        stop_realtime_system()
        
        # Stop WebSocket server
        from src.core.websocket_api import stop_websocket_server
        stop_websocket_server()
        
        print("✅ System stopped")
    
    def open_browser(self):
        """Open browser with demo control panel."""
        time.sleep(3)  # Wait for services to start
        try:
            webbrowser.open(f'http://localhost:{self.web_port}/demo_control_panel.html')
            print("🌐 Demo Control Panel opened in browser")
        except Exception as e:
            print(f"⚠️ Could not open browser: {e}")

def signal_handler(signum, frame):
    """Handle shutdown signals."""
    print("\n🛑 Received shutdown signal")
    launcher.stop_system()
    sys.exit(0)

if __name__ == "__main__":
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and start launcher
    launcher = RealTimeSystemLauncher()
    
    # Start browser in separate thread
    browser_thread = threading.Thread(target=launcher.open_browser, daemon=True)
    browser_thread.start()
    
    # Start all services
    try:
        launcher.start_all_services()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down system...")
        launcher.stop_system()
    except Exception as e:
        print(f"❌ System error: {e}")
        launcher.stop_system()
