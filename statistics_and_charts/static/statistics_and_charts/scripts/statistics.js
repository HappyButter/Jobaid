console.log("hello there from statistics script");

const chartDivLanguages = document.querySelector('.chart__languages');
const chartDivLevel = document.querySelector('.chart__level');
const chartDivTechnologies = document.querySelector('.chart__technologies');
const chartDivConstracts = document.querySelector('.chart__constracts');
const chartDivCompanySize = document.querySelector('.chart__company_size');


const fetchData = async (url) => {
    const response = await fetch(url);
    return await response.json();
}

const createPieCharts = async (url) => {
    const pieChartsData = await fetchData(url);
    console.log(pieChartsData) 

    const pieChartDivs = [chartDivLanguages, chartDivLevel, chartDivConstracts]
    const piePlotNames = ['Languages', 'Experience Level', 'Contract Type']

    let i = 0;
    for(statistics in pieChartsData){
        console.log(statistics)
        const values = Object.values(pieChartsData[statistics]);
        const labels = Object.keys(pieChartsData[statistics]);
    
        const data = [
            {
                values: values,
                labels: labels,
                hole: .9,
                title: piePlotNames[i],
                textinfo: "label+percent",
                textposition: "outside",
                type: 'pie'
            }
        ]
    
        const layout = {
            showlegend: false,
            plot_bgcolor:"black",
            paper_bgcolor:"#FFF0"
        }
    
        Plotly.newPlot(pieChartDivs[i], data, layout);
        i++;
    }
}


const createBarCharts = async (url) => {
    const barChartsData = await fetchData(url);
    console.log(barChartsData) 
    const barChartDivs = [chartDivTechnologies, chartDivCompanySize];
    const barPlotNames = ['Top10 Technologies', 'Company Size'];
    
    let i = 0; 
    for(statistics in barChartsData){
        const values = Object.values(barChartsData[statistics]);
        const labels = Object.keys(barChartsData[statistics]);

        const total = values.reduce((sum, value) => sum + value, 0);
        const normalized = values.map(value => value/total * 100);
    
        const data = [
            {
                x: labels,
                y: normalized,
                type: 'bar',
                marker: {
                    color: 'darkblue'
                }
            }
        ]
    
        const layout = {
            title: barPlotNames[i],
            margin: { 
                t: 30 
            }
        }
    
        Plotly.newPlot(barChartDivs[i], data, layout);
        i++;
    }
}

createPieCharts("http://127.0.0.1:8000/statistics/data/pie");
createBarCharts("http://127.0.0.1:8000/statistics/data/bar");