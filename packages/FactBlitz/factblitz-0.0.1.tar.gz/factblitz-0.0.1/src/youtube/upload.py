from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import google.auth
import google_auth_oauthlib.flow
import googleapiclient.discovery


def upload_video_to_youtube(video_file, title, description, category_id="22", privacy_status="public"):
    """
    Uploads a video to YouTube using the YouTube Data API v3.

    :param video_file: Path to the video file
    :param title: Title of the video
    :param description: Description of the video
    :param category_id: YouTube category ID (default is "22" for People & Blogs)
    :param privacy_status: "public", "private", or "unlisted"
    """

    CLIENT_SECRETS_FILE = "client_secret.json"
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

    # Authenticate using OAuth 2.0
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = build("youtube", "v3", credentials=credentials)

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True, mimetype="video/*")

    try:
        request = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media
        )
        response = request.execute()
        print(f"Upload successful! Video ID: {response['id']}")
        return response
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None
