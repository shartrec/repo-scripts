# author: realcopacetic

from xbmc import Player

from resources.lib.script.actions import clean_filename
from resources.lib.service.art import ImageEditor
from resources.lib.utilities import condition, json_call, log, window_property


class PlayerMonitor(Player):
    def __init__(self):
        Player.__init__(self)
        self.clearlogo_cropper = ImageEditor().clearlogo_cropper

    def onAVStarted(self):
        if self.isPlayingVideo() and condition('String.IsEmpty(Window(home).Property(Trailer_Autoplay))'):
            # Crop clearlogo for use on fullscreen info or pause
            self.clearlogo_cropper(source='VideoPlayer',
                                   reporting=window_property)
            # Clean filename
            item = self.getPlayingItem()
            label = item.getLabel()
            if label:
                clean_filename(label=label)
            else:
                window_property('Return_Label', clear=True)
            
            # Get set id
            tag = self.getVideoInfoTag()
            dbid = tag.getDbId()
            if dbid and condition('VideoPlayer.Content(movie)'):
                query = json_call(
                    'VideoLibrary.GetMovieDetails',
                    params={'properties': [
                        'setid'], 'movieid': dbid},
                    parent='get_set_id'
                )
                if query['result'].get('moviedetails', None):
                    setid = int(query['result']['moviedetails']['setid'])
                    window_property('VideoPlayer_SetID', set=setid)


        # Get user rating on music playback
        if self.isPlayingAudio():
            tag = self.getMusicInfoTag()
            user_rating = tag.getUserRating()
            album_artist = tag.getAlbumArtist()
            window_property('MusicPlayer_UserRating', set=user_rating)
            window_property('MusicPlayer_AlbumArtist', set=album_artist)

    def onPlayBackStopped(self):
        # Clean properties
        window_property('MusicPlayer_UserRating', clear=True)
        window_property('MusicPlayer_AlbumArtist', clear=True)
        window_property('VideoPlayer_SetID', clear=True)
        window_property('Return_Label', clear=True)
