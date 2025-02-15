import { Link, Stack } from 'expo-router';
import { StyleSheet, Pressable } from 'react-native';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';
import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';
import { useState, useEffect } from 'react';

// Import the bundled audio file using relative path
const PODCAST_AUDIO = require('@assets/audio/test_podcast.mp3');

// API endpoint for future use
// const API_BASE_URL = 'http://your-backend-url/api';
// const PODCAST_API_ENDPOINT = `${API_BASE_URL}/audio/podcast`;

export default function LoginScreen() {
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  // const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Initialize audio
    const initAudio = async () => {
      try {
        await Audio.setAudioModeAsync({
          playsInSilentModeIOS: true,
          staysActiveInBackground: true,
          interruptionModeIOS: InterruptionModeIOS.DoNotMix,
          interruptionModeAndroid: InterruptionModeAndroid.DoNotMix,
        });
      } catch (error) {
        console.error('Error initializing audio:', error);
      }
    };

    initAudio();

    // Cleanup function
    return () => {
      if (sound) {
        sound.unloadAsync();
      }
    };
  }, []);

  const playSound = async () => {
    try {
      if (sound) {
        if (isPlaying) {
          await sound.pauseAsync();
          setIsPlaying(false);
        } else {
          await sound.playAsync();
          setIsPlaying(true);
        }
      } else {
        // Current implementation: Using bundled audio
        const { sound: newSound } = await Audio.Sound.createAsync(
          PODCAST_AUDIO,
          { shouldPlay: true }
        );
        setSound(newSound);
        setIsPlaying(true);

        // Future API implementation:
        /*
        setIsLoading(true);
        try {
          const response = await fetch(PODCAST_API_ENDPOINT);
          if (!response.ok) {
            throw new Error('Failed to fetch audio');
          }
          const audioBlob = await response.blob();
          const audioUri = URL.createObjectURL(audioBlob);
          
          const { sound: newSound } = await Audio.Sound.createAsync(
            { uri: audioUri },
            { shouldPlay: true }
          );
          setSound(newSound);
          setIsPlaying(true);
        } catch (error) {
          console.error('Error loading audio from API:', error);
        } finally {
          setIsLoading(false);
        }
        */
      }
    } catch (error) {
      console.error('Error playing sound:', error);
    }
  };

  return (
    <ThemedView style={styles.container}>
      <Stack.Screen options={{ title: 'Login' }} />
      <ThemedText type="title">Welcome to AI Podcasts</ThemedText>
      
      <Pressable 
        onPress={playSound}
        style={[styles.playButton, /* isLoading && styles.disabledButton */]}
        // disabled={isLoading}
      >
        <ThemedText type="link">
          {/*isLoading ? 'Loading...' : */}{isPlaying ? 'Pause Audio' : 'Play Audio'}
        </ThemedText>
      </Pressable>

      <Link href="/(tabs)" style={styles.link}>
        <ThemedText type="link">Continue to Podcasts</ThemedText>
      </Link>
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  link: {
    marginTop: 15,
    paddingVertical: 15,
  },
  playButton: {
    marginTop: 20,
    padding: 10,
    borderRadius: 5,
  },
  disabledButton: {
    opacity: 0.5,
  },
}); 