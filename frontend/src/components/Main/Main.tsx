import React, { useState, useEffect } from 'react'
import { InputNumber } from 'primereact/inputnumber';
import { Calendar } from 'primereact/calendar';
import { Button } from 'primereact/button';
import "primereact/resources/themes/lara-light-indigo/theme.css";
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import './Main.scss'
import Diagram from '../Diagram/Diagram';

export default function Main(methods: any) {
  const [numDays, setNumDays] = useState<any>(1);
  const [date, setDate] = useState<any>('2023-10-01');
  const [isSubmitForm, setIsSubmitForm] = useState(false)

  function handleSubmit(evt: any) {
    evt.preventDefault()

    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2);
    const day = ('0' + date.getDate()).slice(-2);

    const formattedDate = year + '-' + month + '-' + day;

    methods.getPredictions(formattedDate, numDays)
      .then((res: any) => {
        setIsSubmitForm(true)

        const hystoricalData: any[] = []
        const predictedData: any[] = []
        const dates: any[] = []

        res.forEach((item: any) => {
          if (item) {
            if (item['historical_value']) {
              hystoricalData.push(item['historical_value'])
              dates.push(item['date'])
            }
            else if (item['predicted_value']) {
              predictedData.push(item['predicted_value'])
              dates.push(item['date'])
            }
          }
        })

        predictedData.unshift(hystoricalData[hystoricalData.length - 1])
        predictedData.unshift(...Array(hystoricalData.length - 1).fill(null))

        const documentStyle = getComputedStyle(document.documentElement);
        const data = {
          labels: dates,
          datasets: [
            {
              label: 'Исторические цены',
              data: hystoricalData,
              fill: false,
              borderColor: documentStyle.getPropertyValue('--blue-500'),
              tension: 0
            },
            {
              label: 'Прогнозируемые цены',
              data: predictedData,
              fill: false,
              borderColor: documentStyle.getPropertyValue('--pink-500'),
              tension: 0
            }
          ]
        };

        console.log(data)

        methods.setCharData(data)
      })
      .catch((err: any) => {
        console.log(err)
      })
  }

  function goBack() {
    setIsSubmitForm(false)
  }

  useEffect(() => {
    setDate(new Date(Date.now() - 30 * 24 * 60 * 60 * 1000))
  }, [])

  return (
    <main className='main'>
      <h1>Прогнозирование цен на нефть</h1>
      {!isSubmitForm && (
        <form onSubmit={handleSubmit}>
          <div className="flex-auto">
            <label htmlFor="mile" className="font-bold block mb-2 flex-auto__num-days">Какое количество дней вперед?</label>
            <InputNumber inputId="mile" value={numDays} onValueChange={(e) => setNumDays(e.value)} suffix=" дней"
              showButtons min={1} max={7} />
          </div>
          <div className="flex-auto">
            <label htmlFor="mile" className="font-bold block mb-2 flex-auto__date">С какой даты получить исторические цены?</label>
            <Calendar value={date} onChange={(e) => setDate(e.value)} dateFormat="yy-mm-dd" showIcon />
          </div>
          <Button label="Получить прогноз" type="submit" icon="pi pi-check" />
        </form>)}
      {isSubmitForm && (
        <>
          <Diagram></Diagram>
          <Button label="Назад" type='button' onClick={goBack} />
        </>)}
    </main>
  )
}
