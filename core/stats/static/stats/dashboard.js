const dashboardSlug = document.getElementById('dashboard-slug').textContent.trim()
const user = document.getElementById('user').textContent.trim()
const submitBtn = document.getElementById('submit-btn')
const dataInput = document.getElementById('data-input')
const dataBox = document.getElementById('data-box')



const socket = new WebSocket(`ws://${window.location.host}/ws/${dashboardSlug}/`); // Отправляет запрос
// на подключение к вебсокет-соединению по адресу в аргументе


socket.onmessage = function(e){ // Получение сообщения от сервера 
    const {sender,message} = JSON.parse(e.data)
    dataBox.innerHTML +=  `<p>${sender}:${message}</p>`
    updateChart()
    
    
};

submitBtn.addEventListener('click', ()=>{ // Прослушивание клика по кнопке
    const dataValue = dataInput.value
        socket.send(JSON.stringify({ // Отправка сообщения на сервер по сокету
            'message' : dataValue,
            'sender': user
        }))
    })

const ctx = document.getElementById('myChart').getContext('2d');
let chart;

const fetchChartData = async() => {
    const response = await fetch(window.location.href + 'chart/')
    const data = await response.json()
    return data
}

const drawChart = async() => {
    const data = await fetchChartData()
    const {chartData, chartLabels} = data

    chart = new Chart(ctx, {
        type:'pie',
        data:{
            labels:chartLabels,
            datasets: [{
            label: "% of contribution",
            data:chartData,
            borderWidth: 1
            }]
        },
        options:{
            scales:{
                y:{
                    beginAtZero:true
                } 
            }
        }
    });
}

const updateChart = async() => {
    if (chart) {
        chart.desytoy()
    }

    await drawChart()
}

drawChart()

