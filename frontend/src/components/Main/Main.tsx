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
    setIsSubmitForm(true)
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
            <label htmlFor="mile" className="font-bold block mb-2">Какое количество дней вперед?</label>
            <InputNumber inputId="mile" value={numDays} onValueChange={(e) => setNumDays(e.value)} suffix=" дней"
              showButtons min={1} max={30} />
          </div>
          <div className="flex-auto">
            <label htmlFor="mile" className="font-bold block mb-2">С какой даты получить исторические цены?</label>
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
