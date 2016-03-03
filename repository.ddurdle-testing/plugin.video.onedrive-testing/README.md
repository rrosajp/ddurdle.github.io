KODI-OneDrive
=============

An OneDrive (SkyDrive) Video/Music add-on for Kodi / XBMC

A video add-on that enables playback of video and music files stored in a OneDrive account.

This is a very early release.  I need people to help test and help me improvement the plugin.

What is implemented?
- Playback of audio/video from root folder
- Multiple account support (up to 10)
- Supports Microsoft Live Personal accounts
- Limited Folder Support (folders with non-video or non-music, such as office docs and photos may cause directory listings to be duplicated)

What is coming very shortly?
- Transcode support (support playback of streams)
- Speed up by saving cookies/sessions between runs
- Creation of STRM files (to support playback from XBMC library or other plugins)
- Encrypted file support

What is missing?
- Support for "business" accounts

Supports [Tested on]: All XBMC / Kodi 13, 14 including Linux, Windows, OS X, Android, Pivos, iOS (including ATV2), Raspberry Pi

Note for Raspberry Pi users: Due to a bug in libcurl with HTTPS streams, playback of content on these devices may not work. I have tested on various Raspberry Pi distributions and have personally witnessed about a 90% failure rate for playback of videos over HTTPS. HTTP is unaffected. "Disk Cache", when implemented, will bypass this problem. It is not implemented at this time.

If you are getting login errors and you validated your credentials, ensure that you select the proper protocol type (HTTP or HTTPS).


Getting Started:

Installing the plugin only (no automatic updates):
1) download the .zip file
2) transfer the .zip file to XBMC
3) in Video Add-on, select Install from .zip

master (latest - 0.1.1)
https://github.com/ddurdle/KODI-OneDrive/archive/master.zip

Before starting the add-on for the first time, either "Configure" or right click and select "Add-on Settings". Enter your fully-qualified Username (your email address registered with Microsoft) and Password.

FAQ:

1) Is there support for multiple accounts?
Yes, up to 10 accounts.

2) Does this add-on support Pictures or other filetypes?
Music and video files are supported; pictures/images will be added shortly.

