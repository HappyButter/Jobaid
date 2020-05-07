console.log("hello there from statistics script");

const chartDiv = document.querySelector('.chart__example');

const data = [{
    x: [1, 2, 3, 4, 5],
    y: [1, 2, 4, 8, 16] 
}];

const layout = {
    margin: { 
        t: 0 
    }
}

Plotly.newPlot( chartDiv, data, layout);
