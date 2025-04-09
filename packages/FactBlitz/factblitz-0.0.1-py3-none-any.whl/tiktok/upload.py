import requests
from youtube.video_urls import YoutubeVideoURLS


# TikTok API endpoint for video upload
url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/init/"


headers = {
    "Authorization": "Bearer act.example12345Example12345Example",
    "Content-Type": "application/json"
}

wheat_url = YoutubeVideoURLS.WHEAT.value

# Data payload (modify with your actual video URL)
data = {
    "post_info": {
        "title": "Your Video Title Here",  # Caption for the TikTok video
        "privacy_level": "PUBLIC",  # Can be PUBLIC, FRIENDS_ONLY, PRIVATE
        "disable_duet": False,  # Set True to disable duets
        "disable_stitch": False,  # Set True to disable stitches
        "disable_comment": False  # Set True to disable comments
    },
    "source_info": {
        "source": "PULL_FROM_URL",
        "video_url": wheat_url
    }
}

response = requests.post(url, json=data, headers=headers)

print(response.json())