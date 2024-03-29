// set the dimensions and cb_margins of the graph
const cb_margin = {top: 100, right: 0, bottom: 0, left: 0},
    cb_width = 460 - cb_margin.left - cb_margin.right,
    cb_height = 460 - cb_margin.top - cb_margin.bottom,
    innerRadius = 130,
    outerRadius = Math.min(cb_width, cb_height) / 2;   // the outerRadius goes from the middle of the SVG area to the border

// append the svg object
const cbs_svg = d3.select("#circular_bars_syn")
    .append("svg")
    .attr("width", cb_width + cb_margin.left + cb_margin.right)
    .attr("height", cb_height + cb_margin.top + cb_margin.bottom)
    .append("g")
    .attr("transform", `translate(${cb_width/2+cb_margin.left}, ${cb_height/2+cb_margin.top})`);

d3.csv("collection_syn.csv").then( function(data) {

    // Scales
    const x = d3.scaleBand()
        .range([0, 2 * Math.PI])    // X axis goes from 0 to 2pi = all around the circle. If I stop at 1Pi, it will be around a half circle
        .align(0)                  // This does nothing
        .domain(data.map(d => d.Country)); // The domain of the X axis is the list of states.
    const y = d3.scaleRadial()
        .range([innerRadius, outerRadius])   // Domain will be define later.
        .domain([0, 14000]); // Domain of Y is from 0 to the max seen in the data

    // Add the bars
    cbs_svg.append("g")
        .selectAll("path")
        .data(data)
        .join("path")
        .attr("fill", "#69b3a2")
        .attr("d", d3.arc()     // imagine your doing a part of a donut plot
            .innerRadius(innerRadius)
            .outerRadius(d => y((d['Value']) * 15))
            .startAngle(d => x(d.Country))
            .endAngle(d => x(d.Country) + x.bandwidth())
            .padAngle(0.01)
            .padRadius(innerRadius))

    // Add the labels
    cbs_svg.append("g")
        .selectAll("g")
        .data(data)
        .join("g")
        .attr("text-anchor", function(d) { return (x(d.Country) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "end" : "start"; })
        .attr("transform", function(d) { return "rotate(" + ((x(d.Country) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ")"+"translate(" + (y(d['Value'])+10) + ",0)"; })
        .append("text")
        .text(function(d){return(d.Country)})
        .attr("transform", function(d) { return (x(d.Country) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "rotate(180)" : "rotate(0)"; })
        .style("font-size", "11px")
        .attr("alignment-baseline", "middle")

});

const cbw_svg = d3.select("#circular_bars_words")
    .append("svg")
    .attr("width", cb_width + cb_margin.left + cb_margin.right)
    .attr("height", cb_height + cb_margin.top + cb_margin.bottom)
    .append("g")
    .attr("transform", `translate(${cb_width/2+cb_margin.left}, ${cb_height/2+cb_margin.top})`);

d3.csv("collection_words.csv").then( function(data) {

    // Scales
    const x = d3.scaleBand()
        .range([0, 2 * Math.PI])    // X axis goes from 0 to 2pi = all around the circle. If I stop at 1Pi, it will be around a half circle
        .align(0)                  // This does nothing
        .domain(data.map(d => d.Country)); // The domain of the X axis is the list of states.
    const y = d3.scaleRadial()
        .range([innerRadius, outerRadius])   // Domain will be define later.
        .domain([0, 14000]); // Domain of Y is from 0 to the max seen in the data

    // Add the bars
    cbw_svg.append("g")
        .selectAll("path")
        .data(data)
        .join("path")
        .attr("fill", "#69b3a2")
        .attr("d", d3.arc()     // imagine your doing a part of a donut plot
            .innerRadius(innerRadius)
            .outerRadius(d => y((d['Value']) * 15))
            .startAngle(d => x(d.Country))
            .endAngle(d => x(d.Country) + x.bandwidth())
            .padAngle(0.01)
            .padRadius(innerRadius))

    // Add the labels
    cbw_svg.append("g")
        .selectAll("g")
        .data(data)
        .join("g")
        .attr("text-anchor", function(d) { return (x(d.Country) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "end" : "start"; })
        .attr("transform", function(d) { return "rotate(" + ((x(d.Country) + x.bandwidth() / 2) * 180 / Math.PI - 90) + ")"+"translate(" + (y(d['Value'])+10) + ",0)"; })
        .append("text")
        .text(function(d){return(d.Country)})
        .attr("transform", function(d) { return (x(d.Country) + x.bandwidth() / 2 + Math.PI) % (2 * Math.PI) < Math.PI ? "rotate(180)" : "rotate(0)"; })
        .style("font-size", "11px")
        .attr("alignment-baseline", "middle")

});