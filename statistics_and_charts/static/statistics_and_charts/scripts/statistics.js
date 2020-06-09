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

    const pieChartDivs = [chartDivLanguages, chartDivLevel, chartDivConstracts]
    const piePlotNames = ['Languages', 'Experience Level', 'Contract Type']

    let i = 0;
    for(statistics in pieChartsData){

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
            paper_bgcolor:"#FFF0",
            width: 500,
            height: 500,
            font: {
                family: 'Poppins, sans-serif',
                size: 18,
                color: '#d1d1d1'
            },
        }
    
        Plotly.newPlot(pieChartDivs[i], data, layout, {staticPlot: true});
        i++;
    }
}


const createBarCharts = async (url) => {
    const barChartsData = await fetchData(url);

    const barChartDivs = [chartDivTechnologies, chartDivCompanySize];
    const barPlotNames = ['Top10 Technologies', 'Company Size'];
    const barPlotXaxis = ['Technologies', 'Number of employees']

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
                    color: '#5f2ce8'
                }
            }
        ]
    
        const layout = {
            title: barPlotNames[i],
            margin: { 
                t: 50 
            },
            xaxis: {
                title: barPlotXaxis[i],    
                automargin: true,
                titlefont: { size:30 },
            },
            yaxis: {
                title: 'Percent',    
                automargin: true,
                titlefont: { size:30 },
            },
            font: {
                family: 'Poppins, sans-serif',
                size: 18,
                color: '#d1d1d1'
            },
            paper_bgcolor:"#FFF0",
            plot_bgcolor:"#FFF0",
        }
    
        Plotly.newPlot(barChartDivs[i], data, layout, {staticPlot: true});
        i++;
    }
}

createPieCharts("http://127.0.0.1:8000/statistics/data/pie");
createBarCharts("http://127.0.0.1:8000/statistics/data/bar");