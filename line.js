// const margin = {top: 10, right: 30, bottom: 30, left: 60},
//     width = 460 - margin.left - margin.right,
//     height = 400 - margin.top - margin.bottom;

// append the svg object to the body of the page
const line_svg = d3.select("#line_chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

//Read the data
d3.csv("article_count.csv",
    // When reading the csv, I must format variables:
    function(d){
        return { date : d3.timeParse("%Y-%m-%d")(d.date), value : d.value }
    }).then(

    // Now I can use this dataset:
    function(data) {

        // Add X axis --> it is a date format
        const x = d3.scaleTime()
            .domain(d3.extent(data, function(d) { return d.date; }))
            .range([ 0, width ]);
        line_svg.append("g")
            .attr("transform", `translate(0, ${height})`)
            .call(d3.axisBottom(x));

        line_svg.append("text")
            .attr("text-anchor", "end")
            .attr("x", width / 2)
            .attr("y", height + 40)
            .text("Year");

        // Add Y axis
        const y = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) { return +d.value; })])
            .range([ height, 0 ]);
        line_svg.append("g")
            .call(d3.axisLeft(y));

        // Add the line
        line_svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "steelblue")
            .attr("stroke-width", 3.5)
            .attr("d", d3.line()
                .x(function(d) { return x(d.date) })
                .y(function(d) { return y(d.value) })
            )

        line_svg.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "end")
            .attr("y", -70)
            .attr("x", -320)
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
            .text("count");

    })