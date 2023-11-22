export const tempData = {
  labels: [new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), new Date()],
  datasets: [
    {
      label: 'First Dataset',
      data: [65, 59, 80, 81, 56, 55, 40],
      fill: false,
      // borderColor: documentStyle.getPropertyValue('--blue-500'),
      tension: 0.4
    },
    {
      label: 'Second Dataset',
      data: [28, 48, 40, 19, 86, 27, 90],
      fill: false,
      // borderColor: documentStyle.getPropertyValue('--pink-500'),
      tension: 0.4
    }
  ]
};