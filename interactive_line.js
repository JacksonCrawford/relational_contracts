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

})







// // append the svg object to the body of the page
// const b_svg = d3.select("#line_chart")
//     .append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//     .append("g")
//     .attr("transform", `translate(${margin.left}, ${margin.top})`);
//
// // Parse the Data
// d3.csv("https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/7_OneCatOneNum_header.csv").then ( function(data) {
//
//     // sort data
//     data.sort(function(b, a) {
//         return a.Value - b.Value;
//     });
//
//     // X axis
//     const x = d3.scaleBand()
//         .range([ 0, width ])
//         .domain(data.map(d => d.Country))
//         .padding(0.2);
//     b_svg.append("g")
//         .attr("transform", `translate(0, ${height})`)
//         .call(d3.axisBottom(x))
//         .selectAll("text")
//         .attr("transform", "translate(-10,0)rotate(-45)")
//         .style("text-anchor", "end");
//
//     // Add Y axis
//     const y = d3.scaleLinear()
//         .domain([0, 13000])
//         .range([ height, 0]);
//     b_svg.append("g")
//         .call(d3.axisLeft(y));
//
//     // Bars
//     b_svg.selectAll("mybar")
//         .data(data)
//         .enter()
//         .append("rect")
//         .attr("x", d => x(d.Country))
//         .attr("y", d => y(d.Value))
//         .attr("width", x.bandwidth())
//         .attr("height", d => height - y(d.Value))
//         .attr("fill", "#69b3a2")
//         .on("mouseover", function(d) {
//             var xPosition = parseFloat(d3.select(this).attr("x"));
//             var yPosition = parseFloat(d3.select(this).attr("y") + 40);
//
//             d3.select("#tooltip")
//                 .style("left", xPosition + "px")
//                 .style("top", yPosition + "px")
//                 .select("#value")
//                 .text("banana");
//                 // .text(d.value);
//
//             d3.select("#tooltip").classed("hidden", false);
//         })
//         .on("mouseout", function() {
//             d3.select("#tooltip").classed("hidden", true);
//
//         });
//
// })








// // const margin = {top: 10, right: 30, bottom: 30, left: 60},
// //     width = 460 - margin.left - margin.right,
// //     height = 400 - margin.top - margin.bottom;
//
// // append the svg object to the body of the page
// const line_svg = d3.select("#line_chart")
//     .append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
//     .append("g")
//     .style("stroke", "black")
//     .attr("transform", `translate(${margin.left},${margin.top})`);
//
// //Read the data
// d3.csv("article_count.csv",
//     // When reading the csv, I must format variables:
//     function(d){
//         return { date : d3.timeParse("%Y-%m-%d")(d.date), value : d.value }
//     }).then(
//
//     // Now I can use this dataset:
//     function(data) {
//
//         // Add X axis --> it is a date format
//         const x = d3.scaleTime()
//             .domain(d3.extent(data, function(d) { return d.date; }))
//             .range([ 0, width ]);
//         line_svg.append("g")
//             .attr("transform", `translate(0, ${height})`)
//             .style("stroke", "black")
//             .style("font-size", "12px")
//             .call(d3.axisBottom(x));
//
//         line_svg.append("text")
//             .attr("text-anchor", "end")
//             .attr("x", width / 2)
//             .attr("y", height + 40)
//             .text("Year");
//
//         // Add Y axis
//         const y = d3.scaleLinear()
//             .domain([0, d3.max(data, function(d) { return +d.value; })])
//             .range([ height, 0 ]);
//         line_svg.append("g")
//             .style("font-size", "12px")
//             .call(d3.axisLeft(y));
//
//         // Add the line
//         line_svg.append("path")
//             .datum(data)
//             .attr("fill", "none")
//             .attr("stroke", "steelblue")
//             .attr("stroke-width", 3.5)
//             .attr("d", d3.line()
//                 .x(function(d) { return x(d.date) })
//                 .y(function(d) { return y(d.value) })
//             )
//             .on("mouseover", function(d) {
//                 var xPosition = parseFloat(d3.select(this).attr("x"));
//                 var yPosition = parseFloat(d3.select(this).attr("y") + 40);
//
//                 d3.select("#tooltip")
//                     .style("left", xPosition + "px")
//                     .style("top", yPosition + "px")
//                     .select("#value")
//                     .text("banana");
//                     // .text(d.value);
//
//                 d3.select("#tooltip").classed("hidden", false);
//             })
//             .on("mouseout", function() {
//                 d3.select("#tooltip").classed("hidden", true);
//             });
//
//         line_svg.append("text")
//             .attr("class", "y label")
//             .attr("text-anchor", "end")
//             .attr("y", -83)
//             .attr("x", -320)
//             .attr("dy", ".75em")
//             .attr("transform", "rotate(-90)")
//             .text("# of Articles");
//
//     })