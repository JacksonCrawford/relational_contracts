/*** Code inspired by https://www.d3-graph-gallery.com/graph/ridgeline_template.html ***/

// Create an svg object
const other_svg = d3.select("#new_words")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
        `translate(${margin.left}, ${margin.top})`);

// Read data, then perfrom actions after storing it in variable "data"
d3.csv("new_word_occurrences.csv").then(function(data) {
    // Get the different categories and count them
    const categories = ["microsoft","aol","amazon","ibm","at&t","ecommerce","intel","san francisco","ebay","dow"];
    const n = categories.length;

    // Compute the mean of each group
    let means = [];
    for (i in categories) {
        currentGroup = categories[i];
        mean = d3.mean(data, function(d) { return +d[currentGroup]; });
        means.push(mean);
    }

    // Generate the X axis
    const x = d3.scaleLinear()
        .domain([-10, 380])
        .range([ 0, width ]);
    other_svg.append("g")
        .attr("class", "xAxis")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).tickValues([65, 130, 195, 260, 325, 390]).tickFormat((d, i) => ["feb", "apr", "jun", "aug", "oct", "dec"][i]).tickSize(-height))
        .style("font-size", "22px")
        .select(".domain").remove();

    // Add X axis label:
    other_svg.append("text")
        .attr("text-anchor", "end")
        .attr("x", width / 2 + 60)
        .attr("y", height + 50)
        .style("font-size", "22px")
        .style("fill", "#b4b5df")
        .text("Months");

    // Create a Y scale for frequency peaks
    const y = d3.scaleLinear()
        .domain([0, 0.25])
        .range([ height, 0]);

    // Generat ethe Y axis with categories by the tick marks
    const yName = d3.scaleBand()
        .domain(categories)
        .range([0, height])
        .paddingInner(1);
    other_svg.append("g")
        .call(d3.axisLeft(yName).tickSize(0))
        .style("font-size", "16px")
        .select(".domain").remove();

    // Compute kernel density estimation for each column:
    const kde = kernelDensityEstimator(kernelEpanechnikov(7), x.ticks(40)); // increase this 40 for more accurate density.
    const allDensity = [];
    for (i = 0; i < n; i++) {
        key = categories[i];
        density = kde( data.map(function(d){  return d[key]; }) );
        allDensity.push({key: key, density: density});
    }

    // Add areas
    other_svg.selectAll("areas")
        .data(allDensity)
        .join("path")
        .attr("transform", function(d){return(`translate(0, ${(yName(d.key)-height)})`)})
        .attr("fill", function(d) {
            grp = d.key;
            index = categories.indexOf(grp);
            value = means[index];
            return "springgreen";
        })
        .datum(function(d){ return(d.density); })
        .attr("opacity", 0.7)
        .attr("stroke", "#000")
        .attr("stroke-width", 0.1)
        .attr("d",  d3.line()
            .curve(d3.curveBasis)
            .x(function(d) { return x(d[0]); })
            .y(function(d) { return y(d[1]); })
        )

})

// Method to compute the Kde from kernel and X position
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