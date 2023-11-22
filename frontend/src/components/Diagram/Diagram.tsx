
import React, { useState, useEffect, useContext } from 'react';
import { Chart } from 'primereact/chart';
import "primereact/resources/themes/lara-light-indigo/theme.css";
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import './Diagram.scss'
import { ChartDataContext } from '../../contexts/ChartDataContext';

const Diagram = (methods: any) => {
  const [chartOptions, setChartOptions] = useState({});

  const chartData = useContext(ChartDataContext)

  useEffect(() => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    const options = {
      maintainAspectRatio: false,
      aspectRatio: 0.6,
      plugins: {
        legend: {
          labels: {
            color: textColor
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder
          }
        },
        y: {
          ticks: {
            color: textColorSecondary
          },
          grid: {
            color: surfaceBorder
          }
        }
      }
    };

    setChartOptions(options);
  }, []);

  return (
    <div className="chart">
      <Chart type="line" data={chartData} options={chartOptions} />
    </div>
  );
}

export default Diagram;