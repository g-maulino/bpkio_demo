import sys
import socketserver
import multiprocessing
import webbrowser
import time
import datetime as dt
from datetime import timezone, timedelta
import http.server

from bpkioAPI import bpkio

# Define a local HTTP server for hosting the test player

def start_server():
    httpd = socketserver.TCPServer(('0.0.0.0', 3838), http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever(poll_interval=0.5)
    return


# Main program that creates the virtual channel

def main():
  
  api_token = input("Please enter your API Token: ")
  
  bpkioAPI = bpkio(api_token)

  print("**************  CREATE VIRTUAL CHANNEL FROM LIVE AND VOD SOURCES  *************")

  # Create sources for the virtual channel
  live_url = input("Please enter the URL of the main live channel: ")
  asset1_url = input("Please enter the URL of the asset nb#1: ")
  asset2_url = input("Please enter the URL of the asset nb#2: ")

  resp = bpkioAPI.create_live_source("main_live", "This is the main base live channel", live_url, None)
  
  live_id = resp.get("id")

  resp = bpkioAPI.create_asset_source("repl_asset1", "This is the first asset for content replacement", asset1_url, None)

  id_asset1 = resp.get("id")

  resp = bpkioAPI.create_asset_source("repl_asset2", "This is the second asset for content replacement", asset2_url, None)
  
  id_asset2 = resp.get("id")

  # Create the virtual channel

  resp = bpkioAPI.create_virtual_channel("myTestChannel", "Lab", live_id)

  id_virtual_channel_dash = resp.get("id")
  vchan_url = resp.get("url")

  print("**************  SCHEDULING TIME SLOTS  *************")

  asset1_start = int(input("Please set the time you want to start asset nb#1 in nb of second from now (consider at least 60 s to give the time to start playback): "))
  asset1_duration = int(input("Please set the duration you want of asset nb#1 in nb of second: "))
  asset2_start = int(input("Please set the time you want to start asset nb#2 in nb of second from end of asset 2: "))
  asset2_duration = int(input("Please set the duration you want of asset nb#2 in nb of second: "))

  # get current time
  current_start_slot = dt.datetime.now(timezone.utc)

  # Insert Asset 1
  # --------------

  bpkioAPI.create_slot("Video #1", id_virtual_channel_dash,
                         (current_start_slot + timedelta(seconds = asset1_start)).replace(microsecond=0).isoformat(),
                         asset1_duration,
                         id_asset1)

  # Insert Asset 2
  # --------------
  
  bpkioAPI.create_slot("Video #2", id_virtual_channel_dash,
                         (current_start_slot + timedelta(seconds = asset1_start) + timedelta(seconds = asset1_duration) + timedelta(seconds = asset2_start)).replace(microsecond=0).isoformat(),
                         asset1_duration,
                         id_asset2)

  # Now start the HTTP server and open the player in a browser
  p = multiprocessing.Process(target=start_server, args=())
  p.daemon = True
  p.start()

  webbrowser.open_new('http://127.0.0.1:3838/player/?url=' + vchan_url)

  while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
