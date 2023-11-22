import api from './utils/api'
import Main from './components/Main/Main'
import { useEffect, useState } from 'react'
import './App.scss';
import React from 'react';
import { ChartDataContext } from './contexts/ChartDataContext';
import { tempData } from './utils/constants';

function App() {
    const [chartData, setCharData] = useState<any>(tempData)

    function getPredictions(startDate: string, numNextDays: number) {
        return api.getPredictions(startDate, numNextDays)
    }

    return (
        <ChartDataContext.Provider value={chartData}>
            <div className="page">
                <Main getPredictions={getPredictions} setCharData={setCharData} />
            </div>
        </ChartDataContext.Provider>
    )
}

export default App
