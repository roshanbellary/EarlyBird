import React, { useRef, useState, useEffect } from 'react';
import { Image, StyleSheet, Platform, Pressable } from 'react-native';
import TrackPlayer, { 
  useTrackPlayerEvents, 
  Event, 
  State, 
  usePlaybackState,
  useProgress
} from 'react-native-track-player';

import ParallaxScrollView from '@/components/ParallaxScrollView';
import { Collapsible } from '@/components/Collapsible';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

const SAMPLE_AUDIO = require('@assets/audio/test_podcast.mp3');

// Setup the player
async function setupPlayer() {
  try {
    // Reset any existing player state first
    await TrackPlayer.reset();
    
    // Initialize the player
    const setup = await TrackPlayer.setupPlayer({
      autoHandleInterruptions: true,
      waitForBuffer: true,
    });
    
    if (!setup) {
      throw new Error('Failed to setup player');
    }
    
    // Add track
    await TrackPlayer.add({
      id: 'podcastTrack',
      url: SAMPLE_AUDIO,
      title: "Today's Podcast",
      artist: 'Early Bird',
      artwork: require('@/assets/images/partial-react-logo.png'),
      duration: 0,
      pitchAlgorithm: Platform.select({ ios: 'PITCH_ALGORITHM_TIMEDELTA', android: 'PITCH_ALGORITHM_SONIC' }),
    });

    await TrackPlayer.updateOptions({
      capabilities: [
        'play',
        'pause',
        'stop',
        'seekTo',
      ],
      compactCapabilities: ['play', 'pause', 'stop'],
      progressUpdateEventInterval: 1,
    });

    return true;
  } catch (error) {
    console.error('Error setting up player:', error);
    throw error;
  }
}

export default function HomeScreen() {
  const playbackState = usePlaybackState();
  const progress = useProgress();
  const [isPlayerReady, setIsPlayerReady] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const playerInitialized = useRef(false);

  // Initialize player when component mounts
  useEffect(() => {
    let mounted = true;

    async function initializePlayer() {
      try {
        if (!playerInitialized.current) {
          await setupPlayer();
          playerInitialized.current = true;
          if (mounted) setIsPlayerReady(true);
        }
      } catch (err) {
        if (mounted) {
          console.error('Player initialization error:', err);
          setError(err instanceof Error ? err.message : 'Failed to setup player');
          setIsPlayerReady(false);
        }
      }
    }

    initializePlayer();

    return () => {
      mounted = false;
      TrackPlayer.reset();
      playerInitialized.current = false;
    };
  }, []);

  const handlePlayPause = async () => {
    try {
      if (!isPlayerReady || !playerInitialized.current) {
        console.log('Player not ready, attempting to initialize...');
        await setupPlayer();
        playerInitialized.current = true;
        setIsPlayerReady(true);
      }

      const state = await TrackPlayer.getState();
      if (state === State.Playing) {
        await TrackPlayer.pause();
      } else {
        await TrackPlayer.play();
      }
    } catch (error) {
      console.error('Playback Error:', error);
      setError(error instanceof Error ? error.message : 'Playback error occurred');
    }
  };

  // Track player events
  useTrackPlayerEvents([Event.PlaybackError], async (event) => {
    if (event.type === Event.PlaybackError) {
      console.error('Playback error:', event.message);
    }
  });

  const isPlaying = playbackState === State.Playing;

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/partial-react-logo.png')}
          style={styles.reactLogo}
        />
      }
    >
      {error && (
        <ThemedView style={styles.errorContainer}>
          <ThemedText style={styles.errorText}>{error}</ThemedText>
        </ThemedView>
      )}

      {/* Title Section */}
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Today's Podcast</ThemedText>
      </ThemedView>

      {/* Podcast Player Section */}
      <ThemedView style={styles.playerContainer}>
        <Pressable 
          onPress={handlePlayPause} 
          style={styles.playButton}
          disabled={!isPlayerReady}
        >
          <ThemedText type="subtitle">
            {isPlaying ? 'Pause Podcast' : 'Play Podcast'}
          </ThemedText>
        </Pressable>

        {/* Progress Bar */}
        <ThemedView style={styles.progressContainer}>
          <ThemedView 
            style={[
              styles.progressBar, 
              { width: `${(progress.position / progress.duration) * 100}%` }
            ]} 
          />
        </ThemedView>
        
        {/* Duration */}
        <ThemedText style={styles.duration}>
          {formatTime(progress.position)} / {formatTime(progress.duration)}
        </ThemedText>
      </ThemedView>

      {/* Expandable Sections for Stories */}
      <ThemedView style={styles.section}>
        <ThemedText type="subtitle">Featured Stories</ThemedText>

        {/* Example Story 1 */}
        <Collapsible title="Story 1: Big News Update">
          <Image
            source={require('@/assets/images/news-example-1.png')} // Replace with an actual image
            style={styles.storyImage}
            resizeMode="cover"
          />
          <ThemedText>
            A brief summary of the story, including key points and context. This
            is just a placeholder. You can also add sources, e.g.,{' '}
            <ThemedText type="defaultSemiBold">
              BBC News, CNN, Reuters
            </ThemedText>{' '}
            etc.
          </ThemedText>
        </Collapsible>

        {/* Example Story 2 */}
        <Collapsible title="Story 2: Tech Stocks Rally">
          <Image
            source={require('@/assets/images/news-example-2.png')} // Replace with an actual image
            style={styles.storyImage}
            resizeMode="cover"
          />
          <ThemedText>
            Another engaging story. Provide brief context, why it matters, and
            potential impact. Add relevant source links or citations as
            needed.
          </ThemedText>
        </Collapsible>

        {/* Example Story 3 */}
        <Collapsible title="Story 3: Sports Highlights">
          <Image
            source={require('@/assets/images/news-example-3.png')} // Replace with an actual image
            style={styles.storyImage}
            resizeMode="cover"
          />
          <ThemedText>
            Talk about the game, the score, the star players, and any
            interesting anecdotes or controversies. Include links or references
            for more details.
          </ThemedText>
        </Collapsible>
      </ThemedView>

      {/* Additional Episode Details */}
      <ThemedView style={styles.section}>
        <ThemedText type="subtitle">Episode Details</ThemedText>
        <ThemedText>
          Provide more insight on today's podcast or any relevant announcements.
        </ThemedText>
      </ThemedView>
    </ParallaxScrollView>
  );
}

// Helper function to format time
function formatTime(seconds: number): string {
  if (!seconds) return '00:00';
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}

const styles = StyleSheet.create({
  reactLogo: {
    height: 178,
    width: 290,
    bottom: 0,
    left: 0,
    position: 'absolute',
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    paddingHorizontal: 16,
    paddingVertical: 8,
  },
  playerContainer: {
    margin: 16,
    padding: 16,
    borderRadius: 8,
    backgroundColor: 'rgba(255,255,255,0.1)',
    alignItems: 'center',
  },
  playButton: {
    backgroundColor: '#3A86FF',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 8,
    marginTop: 8,
  },
  section: {
    marginVertical: 16,
    padding: 16,
    borderRadius: 8,
    backgroundColor: 'rgba(255,255,255,0.1)',
  },
  storyImage: {
    width: '100%',
    height: 180,
    marginTop: 8,
    marginBottom: 8,
    borderRadius: 8,
  },
  progressContainer: {
    height: 4,
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: 2,
    marginTop: 16,
    width: '100%',
  },
  progressBar: {
    height: '100%',
    backgroundColor: '#3A86FF',
    borderRadius: 2,
  },
  duration: {
    marginTop: 8,
    fontSize: 12,
    textAlign: 'center',
  },
  errorContainer: {
    margin: 16,
    padding: 12,
    backgroundColor: '#ff000020',
    borderRadius: 8,
  },
  errorText: {
    color: '#ff0000',
    textAlign: 'center',
  },
});
