from pytube import YouTube


def download_video_by_url(url: str, output_dir: str, filename):
    YouTube(url).streams.get_highest_resolution().download(output_path=output_dir, filename=filename)
