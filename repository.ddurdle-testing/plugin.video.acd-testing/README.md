Amazon Cloud Drive for KODI / XBMC
==================================

Amazon Cloud Drive add-on for KODI / XBMC

A video add-on for XBMC that enables playback of videos stored in an Amazon Cloud Drive account.

Supports [Tested on]:
All XBMC 12/13/14 including Linux, Windows, OS X, Android, Pivos, iOS (including ATV2)

The plugin uses the Amazon Cloud Drive API

Getting Started:
1) download the .zip file
2) transfer the .zip file to XBMC
3) in Video Add-on, select Install from .zip

Before starting the add-on for the first time, either "Configure" or right click and select "Add-on Settings".
Visit www.dmdsoftware.net for directions on setting up an OAUTH2 login.

Acount activation:
To authorize the plugin via OAUTH2, visit:
https://www.amazon.com/ap/oa?client_id=amzn1.application-oa2-client.10e85701795347a5800fc706aeb6343f&scope=clouddrive%3Aread_all&response_type=code&redirect_uri=https://script.google.com/macros/s/AKfycby7lHhHKawU5dZM538MGXDK-cGtcvV22jd5v3Q_rtDREBs9T8dm/exec

Modes:
1) standard index
- starting the plugin via video add-ons will display a directory containing all video files within the Google Drive account or those that are shared to that account
- click on the video to playback
- don't create favourites from the index, as the index will contain a URL that will expire after 12-24 hours
2) mode=playvideo
- you can create .strm or .m3u files that run Google Drive videos direct
- create .strm or .m3u files containing the following: plugin://plugin.video.acd?mode=playvideo&amp;title=Title_of_video
- if your video is composed of multiple clips, you can create a .m3u that makes the above plugin:// call, one line for each clip.  You can then create a .strm file that points to the .m3u.  XBMC can index movies and shows contained in your Google Drive account by either a .strm containing a single plugin:// call to the video, or a .strm that points to a local .m3u file that contains a list of plugin:// calls representing the video

FAQ:

1) Is there support for multiple accounts?
Yes, 9+ accounts are supposed

2) Does thie add-on support Pictures or other filetypes?
Yes, video, music and photos are supported


