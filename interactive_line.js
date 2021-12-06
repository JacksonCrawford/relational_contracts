// append the svg object to the body of the page
const b_svg = d3.select("#line_chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

let counter = 0;

// Parse the Data
// d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/7_OneCatOneNum_header.csv").then( function(data) {
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
            // .style("stroke", "black")
            .style("font-size", "12px")
            .call(d3.axisBottom(x));

        b_svg.append("text")
            .attr("text-anchor", "end")
            .attr("x", width / 2)
            .attr("y", height + 40)
            .text("Year");


        // Add Y axis
        const y = d3.scaleLinear()
            .domain([0, d3.max(data, function(d) { return +d.value; })])
            .range([ height, 0]);
        b_svg.append("g")
            .call(d3.axisLeft(y));

        // console.log("domain: ", d3.max(data,))

    // Bars
        b_svg.selectAll("mybar")
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
                // console.log(d);
                // console.log(d.originalTarget.__data__.value);

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
