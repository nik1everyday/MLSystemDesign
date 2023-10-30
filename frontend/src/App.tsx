import api from './utils/api'
import Main from './components/Main/Main'
import { useEffect, useState } from 'react'
import './App.scss';
import React from 'react';

function App() {
    function getPredictions(startDate: string, numNextDays: number) {
        return api.getPredictions(startDate, numNextDays)
    }

    return (
        <div className="page">
            <Main getPredictions={getPredictions} />
        </div>
    )
}

export default App
