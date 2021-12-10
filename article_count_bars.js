/*** Tooltips code adapted from Chapter 10 of Fundamentals of Data Visualization for the Web by Scott Murray ***/

// append the svg object to the body of the page
const b_svg = d3.select("#line_chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

let counter = 0;

// Parse the Data
d3.csv("article_count.csv",
    function(d) {
        return {date: d3.timeParse("%Y-%m-%d")(d.date), value : d.value }
    }).then(

    function(data) {

        const x = d3.scaleTime()
            .domain(d3.extent(data, function(d) { return d.date; }))
            .range([ 0, width ]);
        b_svg.append("g")
            .attr("transform", `translate(0, ${height})`)
            .style("font-size", "16px")
            .call(d3.axisBottom(x));

        b_svg.append("text")
            .attr("text-anchor", "end")
            .attr("x", width / 2)
            .attr("y", height + 50)
            .style("font-size", "24px")
            .style("fill", "#e0b2cf")
            .text("Year");

        // Add Y axis
        const y = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) { return +d.value; })])
            .range([ height, 0]);
        b_svg.append("g")
            .style("font-size", "16px")
            .call(d3.axisLeft(y));

        b_svg.append("text")
            .attr("class", "y label")
            .attr("text-anchor", "end")
            .attr("y", -100)
            .attr("x", -280)
            .attr("dy", ".75em")
            .attr("transform", "rotate(-90)")
            .style("font-size", "24px")
            .style("fill", "#e0b2cf")
            .text("# of Articles");

        // Bars
        b_svg.selectAll("bar")
            .data(data)
            .join("rect")
            .attr("x", d => x(d.date))
            .attr("y", d => y(d.value))
            .attr("width", 20)
            .attr("height", d => height - y(d.value))
            .attr("fill", "#69b3a2")
            .on("mouseover", function(d) {

                //Get this bar's x/y values, then augment for the tooltip
                var xPosition = parseFloat(d3.select(this).attr("x"));
                var yPosition = parseFloat(d3.select(this).attr("y")) + 20;

                //Update the tooltip position and value
                d3.select("#tooltip")
                    .style("left", xPosition + "px")
                    .style("top", yPosition + "px")
                    .select("#value")
                    .text(d.originalTarget.__data__.value);

                //Show the tooltip
                d3.select("#tooltip").classed("hidden", false);
            })
            .on("mouseout", function(d) {
                d3.select("#tooltip").classed("hidden", true);
            });

})
