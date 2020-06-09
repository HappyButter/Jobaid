console.log("hello there from statistics script");

// const chartDivLanguages = document.querySelector('.chart__languages');
// const chartDivLevel = document.querySelector('.chart__level');
// const chartDivTechnologies = document.querySelector('.chart__technologies');
// const chartDivConstracts = document.querySelector('.chart__constracts');
// const chartDivCompanySize = document.querySelector('.chart__company_size');


// const fetchData = async (url) => {
//     const response = await fetch(url);
//     return await response.json();
// }

// const createPlotLanguages = async (url, chartDivLanguages) => {
//     const statistics = await fetchData(url);
//     console.log(statistics);

//     const values = Object.values(statistics);
//     const labels = Object.keys(statistics);

//     const total = values.reduce((sum, value) => sum + value, 0);
//     const normalized = values.map(value => value/total * 100);

//     const data = [
//         {
//             values: normalized,
//             labels: labels,
//             hoverinfo: 'percent',
//             hole: .9,
//             title: 'Languages',
//             textinfo: "label",
//             textposition: "outside",
//             type: 'pie'
//         }
//     ]

//     const layout = {
//         showlegend: false,
//         plot_bgcolor:"black",
//         paper_bgcolor:"#FFF0"
//     }

//     Plotly.newPlot(chartDivLanguages, data, layout);
// }

// const createPlotLevel = async (url, chartDivLevel) => {
//     const statistics = await fetchData(url);
//     console.log(statistics);

//     const values = Object.values(statistics);
//     const labels = Object.keys(statistics);

//     const data = [
//         {
//             values: values,
//             labels: labels,
//             hole: .9,
//             title: 'Level',
//             hoverinfo: 'percent',
//             textinfo: "label",
//             textposition: "outside",
//             type: 'pie'
//         }
//     ]

//     const layout = {
//         showlegend: false,
//         plot_bgcolor:"black",
//         paper_bgcolor:"#FFF0"
//     }

//     Plotly.newPlot(chartDivLevel, data, layout);
// }


// const createPLotTechnologies = async (url, chartDivTechnologies) => {
//     const statistics = await fetchData(url);
//     console.log(statistics);
    
//     const values = Object.values(statistics);
//     const labels = Object.keys(statistics);
    

//     const data = [
//         {
//             x: labels,
//             y: values,
//             opacity: 0.8,
//             type: 'bar',
//             marker: {
//                 color: 'darkblue'
//             }
//         }
//     ]

//     const layout = {
//         title:'Top10 technologies',
//         margin: { 
//             t: 30 
//         }
//     }

//     Plotly.newPlot(chartDivTechnologies, data, layout);
// }


// const createPlotConstracts = async (url, chartDivConstracts) => {
//     const statistics = await fetchData(url);
//     console.log(statistics);

//     const values = Object.values(statistics);
//     const labels = Object.keys(statistics);

//     const data = [
//         {
//             values: values,
//             labels: labels,
//             hole: .9,
//             title: 'Contract Type',
//             textinfo: "label+percent",
//             textposition: "outside",
//             type: 'pie'
//         }
//     ]

//     const layout = {
//         showlegend: false,
//         plot_bgcolor:"black",
//         paper_bgcolor:"#FFF0"
//     }

//     Plotly.newPlot(chartDivConstracts, data, layout);
// }



// const createPlotCompanySize = async (url, chartDivCompanySize) => {
//     const statistics = await fetchData(url);
//     console.log(statistics);

//     const values = Object.values(statistics);
//     const labels = Object.keys(statistics);
    
//     const total = values.reduce((sum, value) => sum + value, 0);
//     const normalized = values.map(value => value/total * 100);

//     const data = [
//         {
//             x: labels,
//             y: normalized,
//             type: 'bar',
//             marker: {
//                 color: 'darkblue'
//             }
//         }
//     ]

//     const layout = {
//         title: 'Company Size',
//         margin: { 
//             t: 30 
//         }
//     }

//     Plotly.newPlot(chartDivCompanySize, data, layout);
// }


// createPlotLanguages('http://127.0.0.1:8000/statistics/languages/', chartDivLanguages);
// createPlotLevel('http://127.0.0.1:8000/statistics/level/', chartDivLevel);
// createPLotTechnologies('http://127.0.0.1:8000/statistics/technologies/', chartDivTechnologies);
// createPlotConstracts('http://127.0.0.1:8000/statistics/constracts/', chartDivConstracts);
// createPlotCompanySize('http://127.0.0.1:8000/statistics/company_size/', chartDivCompanySize);