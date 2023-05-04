//import {select, csv } from 'd3';
const svg = d3.select('svg');
const width = +svg.attr('width');
const height = +svg.attr('height');

const render = data => {
    const xScale = d3.scaleLinear()
    .domain([0,d3.max(data, d=> d.WOOD)])
    .range([0,width])

    const yScale = d3.scaleBand()
    .domain(data.map(d => d.EGID))
    .range([0,height]);

    console.log(yScale.domain());

    svg.selectAll('rect').data(data)
        .enter().append('rect')
        .attr('y', d => yScale(d.EGID))
        .attr('width', d => xScale(d.WOOD))
        .attr('height', yScale.bandwidth());
};

d3.csv("./DF_all_materials.csv").then(data => {
        data.forEach(d => {
            d.WOOD = +d.WOOD * 1000;
            d.GLASS = +d.GLASS * 1000;
            d.MINERAL = +d.MINERAL * 1000;
            d.METAL = +d.METAL * 1000;
            d.ROOFTILE = +d.ROOFTILE * 1000;
        });
        render(data);
        //console.log(data)
    });
