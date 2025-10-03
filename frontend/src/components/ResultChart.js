import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function ResultChart({ chartData }) {
  const data = {
    labels: chartData.labels,
    datasets: [
      {
        label: chartData.label || 'Count',
        data: chartData.data,
        backgroundColor: 'rgba(0, 123, 255, 0.5)',
        borderColor: 'rgba(0, 123, 255, 1)',
        borderWidth: 1,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: chartData.title || 'Query Results',
      },
    },
    scales: {
        y: {
            beginAtZero: true
        }
    }
  };

  return <Bar options={options} data={data} />;
}

export default ResultChart;
