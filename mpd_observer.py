import subprocess
import time
import os

def wait_player_event():
    subprocess.run(['mpc', 'idle', 'player'])

def monitor_mpd(output_dir, method):
    while True:
        wait_player_event() 
        music_file = subprocess.check_output(['mpc', '--format', '%file%', 'current']).decode('utf-8').strip()
        if music_file:
            subprocess.run(['python3', script_path, music_dir+music_file, output_dir, '--display', '--method', method])

if __name__ == '__main__':
    music_dir = '/home/crystal-ryu/Músicas/'
    script_path = "./extract_cover.py"
    output_dir = './cover/'
    method = 'chafa'# ou 'catimg'
    monitor_mpd(output_dir, method)

