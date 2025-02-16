"use client";
import React, { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });


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
    fetch(`/api/graph_init`)
      .then(response => response.json())
      .then(data => {
          setNodes(data.nodes);
      }).catch(error => {
            console.error('Error fetching audio file:', error);
        });
}, []);

  // Separate useEffect for updating coordinates when nodes change
  useEffect(() => {
    if (nodes && nodes.length > 0) {
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