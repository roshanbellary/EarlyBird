import { Link, Stack } from 'expo-router';
import { StyleSheet } from 'react-native';
import { ThemedText } from '@/components/ThemedText';
import { ThemedView } from '@/components/ThemedView';

export default function LoginScreen() {
  return (
    <ThemedView style={styles.container}>
      <Stack.Screen options={{ title: 'Login' }} />
      <ThemedText type="title">Welcome to AI Podcasts</ThemedText>
      {/* Add your login form components here */}
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
}); 