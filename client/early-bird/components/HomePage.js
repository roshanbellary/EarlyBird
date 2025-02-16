import React, { useEffect, useState } from 'react';
import { View, Text, ScrollView, StyleSheet } from 'react-native';

const HomePage = () => {
    const [podcasts, setPodcasts] = useState([]);

    useEffect(() => {
        // Fetch podcasts from an API or database
        fetch('https://example.com/api/podcasts') // Replace with your API endpoint
            .then(response => response.json())
            .then(data => setPodcasts(data))
            .catch(error => console.error('Error fetching podcasts:', error));
    }, []);

    return (
        <ScrollView style={styles.container}>
            <Text style={styles.header}>Welcome to EarlyBird</Text>
            <Text style={styles.subHeader}>Your personalized podcast generator</Text>
            <View style={styles.podcastList}>
                {podcasts.length > 0 ? (
                    podcasts.map(podcast => (
                        <View key={podcast.id} style={styles.podcastItem}>
                            <Text style={styles.title}>{podcast.title}</Text>
                            <Text style={styles.description}>{podcast.description}</Text>
                            <Text style={styles.host}><strong>Host:</strong> {podcast.host}</Text>
                            <Text style={styles.duration}><strong>Duration:</strong> {podcast.duration} mins</Text>
                        </View>
                    ))
                ) : (
                    <Text>No podcasts available</Text>
                )}
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 16,
        backgroundColor: '#fff',
    },
    header: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 8,
        alignSelf: 'center',
        marginTop: 30, // Added marginTop to the header
    },
    subHeader: {
        fontSize: 18,
        marginBottom: 16,
    },
    podcastList: {
        marginTop: 16,
    },
    podcastItem: {
        marginBottom: 16,
        padding: 16,
        backgroundColor: '#f9f9f9',
        borderRadius: 8,
    },
    title: {
        fontSize: 20,
        fontWeight: 'bold',
    },
    description: {
        fontSize: 16,
        marginTop: 4,
    },
    host: {
        fontSize: 14,
        marginTop: 4,
    },
    duration: {
        fontSize: 14,
        marginTop: 4,
    },
});

export default HomePage;