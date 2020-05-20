console.log("hello there from statistics script");

const chartDiv = document.querySelector('.chart__example');
// Plotly.newPlot(chartDiv, {}, {});

const fetchData = async (url) => {
    const response = await fetch(url);
    return await response.json();
}

const createPlot = async (url, chartDiv) => {
    const statistics = await fetchData(url);
    console.log(statistics);

    const values = Object.values(statistics);
    const labels = Object.keys(statistics);

    const total = values.reduce((sum, value) => sum + value, 0);
    const normalized = values.map(value => value/total * 100)

    // const data = [{
    //     values,
    //     labels,
    //     type: 'pie'
    // }];
    const data = [
        {
            x: labels,
            y: normalized,
            histfunc: 'count',
            opacity: 0.8,
            type: 'bar',
            marker: {
                color: 'darkblue'
            }
        }
    ]

    const layout = {
        margin: { 
            t: 20 
        }
    }

    Plotly.newPlot(chartDiv, data, layout);
}


createPlot('http://127.0.0.1:8000/statistics/example/', chartDiv);
