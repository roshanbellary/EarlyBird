"use client"
import React, { useEffect, useState } from 'react';
import Plot from 'react-plotly.js';

interface Node {
  id: number;
  position: [number, number, number];
}

const PodcastGraph: React.FC = () => {
  const [nodes, setNodes] = useState<Node[]>([]);
  const [x, setX] = useState<number[]>([]);
  const [y, setY] = useState<number[]>([]);
  const [z, setZ] = useState<number[]>([]);

  useEffect(() => {
    const fetchNodes = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/graph_data?mode=init');
        const data = await response.json();
        setNodes(data.nodes);
      } catch (error) {
        console.error('Error fetching graph data:', error);
      }
    };

    fetchNodes();
  }, []);

  // Separate useEffect for updating coordinates when nodes change
  useEffect(() => {
    if (nodes.length > 0) {
      setX(nodes.map((node) => node.position[0]));
      setY(nodes.map((node) => node.position[1]));
      setZ(nodes.map((node) => node.position[2]));
    }
  }, [nodes]); // This dependency array ensures the effect runs when nodes changes

  return (
    <div>
      <h1>Podcast Data Visualization</h1>
      <Plot
        data={[
          {
            x,
            y,
            z,
            mode: 'markers',
            marker: { size: 5, color: 'red' },
            type: 'scatter3d',
          },
        ]}
        layout={{ 
          title: '3D Scatter Plot of Podcast Data',
          width: 800,
          height: 600
        }}
      />
    </div>
  );
};

export default PodcastGraph;