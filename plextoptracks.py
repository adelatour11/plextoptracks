from plexapi.server import PlexServer

# Function to create a playlist with top tracks of albums matching the genre
def create_playlist_with_top_tracks(plex_token, plex_server_ip, genre_word):
    try:
        # Connect to Plex server
        plex = PlexServer(f"http://{plex_server_ip}:32400", plex_token)
        
        # Get all albums
        albums = plex.library.section('Musique').albums()
        
        # List to store top tracks information
        top_tracks = []
        
        # Iterate through each album
        for album in albums:
            album_genres = [genre.tag for genre in album.genres]
            
            # Check if the genre word is in any of the album's genres
            if any(genre_word.lower() in genre.lower() for genre in album_genres):
                # Get all tracks of the album
                tracks = album.tracks()
                
                # List to store track names and their rating counts
                track_info = []
                for track in tracks:
                    track_name = track.title
                    rating_count = track.ratingCount
                    if rating_count is not None:
                        track_info.append((track, rating_count))
                
                # Sort tracks by rating count
                track_info.sort(key=lambda x: x[1], reverse=True)
                
                # Add top tracks to the playlist
                top_tracks.extend(track_info[:3])
        
        # Create a playlist with top tracks
        playlist_title = f"Top Tracks - {genre_word.capitalize()}"
        playlist = plex.createPlaylist(playlist_title, items=[track[0] for track in top_tracks])
        
        return playlist
    except Exception as e:
        print("An error occurred:", e)
        return None

# Example usage
plex_token = "XXXXX"
plex_server_ip = "XXXX"
genre_word = "rock"
playlist = create_playlist_with_top_tracks(plex_token, plex_server_ip, genre_word)
if playlist:
    print(f"Playlist '{playlist.title}' created successfully with top tracks of the genre '{genre_word}'.")
else:
    print(f"Failed to create playlist with top tracks of the genre '{genre_word}'.")
