import React, { useRef, useState } from 'react';
import { Image, StyleSheet, Platform, Pressable } from 'react-native';
import { Audio, InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';

import ParallaxScrollView from '@/components/ParallaxScrollView';
import { Collapsible } from '@/components/Collapsible';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function HomeScreen() {
  const [sound, setSound] = useState<Audio.Sound | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  // Configure the audio to allow playback in background on iOS
  Audio.setAudioModeAsync({
    allowsRecordingIOS: false,
    staysActiveInBackground: false,
    interruptionModeIOS: InterruptionModeIOS.DoNotMix,
    playsInSilentModeIOS: true,
    shouldDuckAndroid: true,
    interruptionModeAndroid: InterruptionModeAndroid.DoNotMix,
    playThroughEarpieceAndroid: false,
  });

  async function handlePlayPause() {
    try {
      if (sound && isPlaying) {
        // If audio is playing, pause it
        await sound.pauseAsync();
        setIsPlaying(false);
      } else if (sound && !isPlaying) {
        // If audio is loaded but paused, resume it
        await sound.playAsync();
        setIsPlaying(true);
      } else {
        // If there is no sound loaded, load it, then play
        const { sound: newSound } = await Audio.Sound.createAsync(
          require('@/assets/audio/sample-podcast.mp3') // Replace with your podcast file
        );
        setSound(newSound);
        setIsPlaying(true);
        await newSound.playAsync();
      }
    } catch (error) {
      console.error('Audio Player Error:', error);
    }
  }

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
      {/* Title Section */}
      <ThemedView style={styles.titleContainer}>
        <ThemedText type="title">Today's Podcast</ThemedText>
      </ThemedView>

      {/* Podcast Player Section */}
      <ThemedView style={styles.playerContainer}>
        <Pressable onPress={handlePlayPause} style={styles.playButton}>
          <ThemedText type="subtitle">
            {isPlaying ? 'Pause Podcast' : 'Play Podcast'}
          </ThemedText>
        </Pressable>
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
});
