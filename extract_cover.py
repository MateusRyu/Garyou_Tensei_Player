import os
import argparse
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from mutagen.mp4 import MP4
from mutagen.flac import FLAC
from mutagen.wave import WAVE
import subprocess

def save_cover_art(cover_art, file_extension, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cover_filename = os.path.join(output_dir, f'cover.{file_extension}')
    with open(cover_filename, 'wb') as img_file:
        img_file.write(cover_art)
    print(f'Cover art saved to {cover_filename}')
    return cover_filename

def extract_cover_art(music_file, output_dir):
    file_extension = os.path.splitext(music_file)[-1].lower()
    cover_filename = False

    if file_extension == '.mp3':
        audio = MP3(music_file, ID3=ID3)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                cover_art = tag.data
                file_extension = tag.mime.split('/')[-1]
                return save_cover_art(cover_art, file_extension, output_dir)
    elif file_extension == '.m4a':
        audio = MP4(music_file)
        if 'covr' in audio:
            cover_art = audio['covr'][0]
            file_extension = 'jpg' if cover_art.imageformat == 13 else 'png'
            return  save_cover_art(cover_art, file_extension, output_dir)

    elif file_extension == '.flac':
        audio = FLAC(music_file)
        if audio.pictures:
            cover_art = audio.pictures[0].data
            file_extension = audio.pictures[0].mime.split('/')[-1]
            return save_cover_art(cover_art, file_extension, output_dir)

    elif file_extension == '.wav':
        audio = WAVE(music_file)
        if 'ICMT' in audio.tags:  # Exemplo de tag comum em WAV
            print("WAV file has metadata.")
            return cover_filename
        print(f'No cover art found in the music file: {music_file}')

def display_cover_art(cover_filename, method):
    if method not in ['chafa', 'catimg']:
        print(f"method {method} not supported")
        return False
    try:
        subprocess.run([method, cover_filename])
    except FileNotFoundError:
        print("chafa is not installed. You can install it with your package manager.")
        returnprint(f'No cover art found in the music file: {music_file}')

def main():
    parser = argparse.ArgumentParser(description='Extract cover art from a music file.')
    parser.add_argument('music_file', type=str, help='Path to the music file.')
    parser.add_argument('output_dir', type=str, help='Directory where the cover art will be saved.')
    parser.add_argument('--display', action='store_true', help='Optionally display the cover art in the terminal.')
    parser.add_argument('--method', type=str, help="Method to display the cover art")

    args = parser.parse_args()
    cover_filename = extract_cover_art(args.music_file, args.output_dir)
    if args.display and cover_filename:
        display_cover_art(cover_filename, args.method)

if __name__ == '__main__':
    main()

