/*** Code inspired by https://www.d3-graph-gallery.com/graph/ridgeline_template.html ***/

// set the dimensions and margins of the graph
    /** NOTE: These margins are used in every other javascript file, but are only declared here**/
let margin = {top: 80, right: 30, bottom: 50, left:110},
    width = 950 - margin.left - margin.right,
    height = 800 - margin.top - margin.bottom;

// Create an svg object
let svg = d3.select("#hypernyms")
    .append("svg")
    .attr("width", width + margin.left + margin.right + 100)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        `translate(${margin.left + 120}, ${margin.top})`);

// Read data, then perform actions after storing it in data
d3.csv("hypernym_occurences.csv").then(function(data) {
    // Set the categories
    const categories = ["activity", "time_period", "institution", "person", "computer_network", "large_integer", "collection", "instrumentality" ,"message", "gregorian_calendar_month"];
    const n = categories.length;

    // Compute the mean of each group
    let means = [];
    for(i in categories) {
        currentGroup = categories[i];
        mean = d3.mean(data, function(d) { return +d[currentGroup]; });
        means.push(mean);
    }

    // Generate the X axis
    const x = d3.scaleLinear()
        .domain([-10, 1400])
        .range([ 0, width ]);
    svg.append("g")
        .attr("class", "xAxis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickValues([210, 420, 630, 840, 1050, 1260]).tickFormat((d, i) => ["feb", "apr", "jun", "aug", "oct", "dec"][i]).tickSize(-height) )
        .style("font-size", "16px")
        .select(".domain").remove();

    // Add X axis label
    svg.append("text")
        .attr("text-anchor", "end")
        .attr("x", width / 2)
        .attr("y", height + 50)
        .style("font-size", "22px")
        .style("fill", "#acadd1")
        .text("Months");

    // Create a Y scale for frequency peaks
    const y = d3.scaleLinear()
        .domain([0, 0.25])
        .range([ height, 0]);

    // Generate the Y axis with categories at tick marks
    const yName = d3.scaleBand()
        .domain(categories)
        .range([0, height])
        .paddingInner(1);
    svg.append("g")
        .call(d3.axisLeft(yName).tickSize(0))
        .style("font-size", "16px")
        .select(".domain").remove();

    // Compute kernel density estimation for each column (not like KDE Plasma D:, I use GNOME though ;)
    const kde = kernelDensityEstimator(kernelEpanechnikov(7), x.ticks(40)); // increase this 40 for more accurate density.
    const allDensity = [];
    for (i = 0; i < n; i++) {
        key = categories[i];
        density = kde(data.map(function(d){ return d[key]; }));
        allDensity.push({key: key, density: density});
    }

    // Add areas
    svg.selectAll("areas")
        .data(allDensity)
        .join("path")
        .attr("transform", function(d){ return(`translate(0, ${(yName(d.key)-height)})`); })
        .attr("fill", function(d){
            grp = d.key ;
            index = categories.indexOf(grp)
            value = means[index]
            return "mediumspringgreen"
        })
        .datum(function(d){ return(d.density); })
        .attr("opacity", 0.7)
        .attr("stroke", "#000")
        .attr("stroke-width", 0.1)
        .attr("d",  d3.line()
            .curve(d3.curveBasis)
            .x(function(d) { return x(d[0]); })
            .y(function(d) { return y(d[1]); })
        );

})

// Method to compute the KDE from kernel and X position
function kernelDensityEstimator(kernel, X) {
    return function(V) {
        return X.map(function(x) {
            return [x, d3.mean(V, function(v) { return kernel(x - v); })];
        });
    };
}

function kernelEpanechnikov(k) {
    return function(v) {
        return Math.abs(v /= k) <= 1 ? 0.75 * (1 - v * v) / k : 0;
    };
}
