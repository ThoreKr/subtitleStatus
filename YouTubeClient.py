"""This file provides a client to interact with youtube, trying to abstract their garbage API
"""

import datetime
import io
import os

import httplib2
from apiclient.discovery import build
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from isodate import parse_duration
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow


class UploadError(Exception):
    """An error occured while uploading
    """
    pass


class YouTubeClient:
    """Provide API interfaces to interact with YouTube
    """
    # This OAuth 2.0 access scope allows an application to upload files to the
    # authenticated user's YouTube channel, but doesn't allow other types of access.
    SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube.force-ssl"]


    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    # This variable defines a message to display if the secrets_path is
    # missing.
    MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0

    To make this sample run you will need to populate the client_secrets.json file
    found at:

       %s

    with information from the API Console
    https://console.developers.google.com/

    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """ % os.path.abspath(os.path.join(os.path.dirname(__file__), 'client_secrets.json'))

    def __init__(self, secrets_path='client_secrets.json'):
        """Initialize and set up an authenticated client

        Keyword Arguments:
            secrets_path {str} -- Path to the google api client secrets (default: {'client_secrets.json'})
        """
        flow = flow_from_clientsecrets(secrets_path, scope=self.SCOPES, message=self.MISSING_CLIENT_SECRETS_MESSAGE)

        self.storage = Storage("ytc-oauth2.json")
        credentials = self.storage.get()

        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, self.storage)

        self.credentials = credentials

        self.client = build(self.YOUTUBE_API_SERVICE_NAME, self.YOUTUBE_API_VERSION, http=self.credentials.authorize(httplib2.Http()))

    def upload(self, video_file: str, title: str, description: str) -> str:
        """Upload a video to youtube (always as private)

        Arguments:
            video_file {str} -- Path to the video
            title {str} -- Title of the new video
            description {str} -- Description to be used

        Raises:
            UploadError: The upload failed

        Returns:
            str -- The video ID
        """

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': None,
                'categoryId': 22
            },
            'status': {
                'privacyStatus': 'private'
            }
        }

        # Call the API's videos.insert method to create and upload the video.
        insert_request = self.client.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=MediaFileUpload(video_file, chunksize=-1, resumable=True)
        )

        # Now upload
        response = None
        try:
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    return response['id']
            raise UploadError
        except:
            raise UploadError

    def getVideoLength(self, video_id: str) -> datetime.timedelta:
        """Get the length of a youtube video

        Arguments:
            video_id {str} -- YT key of the video

        Returns:
            datetime.timedelta -- Length of the video as timedelta object
        """
        request = self.client.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        )
        response = request.execute()

        duration = response['items'][0]['contentDetails']['duration']

        return parse_duration(duration)

    def uploadCaption(self, video_id: str, caption_path: str, language: str, caption_name: str, sync=True, draft=True):
        """Add captions to a youtube video

        see https://developers.google.com/youtube/v3/docs/captions/insert

        Arguments:
            video_id {str} -- YT video key
            caption_path {str} -- Path to captions file
            language {str} -- Language shorthand for the given captions
            caption_name {str} -- Description to be shown for this captions

        Keyword Arguments:
            sync {bool} -- Should this upload be auto-synced (default: {True})
            draft {bool} -- Should this be uploaded as draft (default: {True})

        Returns:
            Unknown -- Response from YouTube
        """
        request = self.client.captions().insert(
            part="snippet",
            sync=sync,
            body={
                "snippet": {
                    "language": language,
                    "name": caption_name,
                    "videoId": video_id,
                    "isDraft": draft
                }
            },

            media_body=MediaFileUpload(caption_path)
        )
        response = request.execute()
        return response

    def downloadCaption(self, caption_id: str, target_path: str):
        """Download a given caption from youtube

        see: https://developers.google.com/youtube/v3/docs/captions/download

        Arguments:
            caption_id {str} -- YT ID assigned to the requested caption
            target_path {str} -- path to save captions to
        """
        request = self.client.captions().download(
            id=caption_id
        )


        with io.FileIO(target_path, "wb") as fh:
            download = MediaIoBaseDownload(fh, request)
            complete = False
            while not complete:
                status, complete = download.next_chunk()
