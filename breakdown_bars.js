// CODE ADAPTED FROM https://www.d3-graph-gallery.com/graph/barplot_button_data_hard.html
/*
    This file contains the data and code that generates and animates the
        bars for the final bar chart that breaks down the top hypernyms into
        their subcategories.
 */


/*** DATA ***/
const activity = [
    {group: "work", value: 20},
    {group: "game", value: 12},
    {group: "attempt", value: 15},
    {group: "use", value: 10},
    {group: "behavior", value: 12},
    {group: "procedure", value: 7},
];

const person = [
    {group: "user", value: 8},
    {group: "engineer", value: 5},
    {group: "scientist", value: 6},
    {group: "peer", value: 5},
    {group: "intellectual", value: 6},
    {group: "friend", value: 3},
];

const sequence = [
    {group: "gene", value: 63},
    {group: "codon", value: 1}
];

const message = [
    {group: "subject", value: 6},
    {group: "narrative", value: 6},
    {group: "information", value: 33},
    {group: "statement", value: 2},
    {group: "wit", value: 4},
    {group: "request", value: 3},
]

const natural_object = [
    {group: "universe", value: 36},
    {group: "body", value: 16},
    {group: "rock", value: 1},
    {group: "nest", value: 5}
]

const content = [
    {group: "goal", value: 4},
    {group: "idea", value: 38},
    {group: "issue", value: 8},
    {group: "belief", value: 4},
    {group: "representation", value: 2},
]


/*** CODE ***/

// Create an svg object named bb_svg within the #breakddown_bars div
const bb_svg = d3.select("#breakdown_bars")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Generate the X axis
const x = d3.scaleBand()
    .range([ 0, width ])
    .padding(0.2);
const xAxis = bb_svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .style("font-size", "16px");

// Generate the Y axis
const y = d3.scaleLinear()
    .range([ height, 0]);
const yAxis = bb_svg.append("g")
    .attr("class", "myYaxis")
    .style("font-size", "16px");

// Add label to y axis
bb_svg.append("text")
    .attr("class", "y label")
    .attr("text-anchor", "end")
    .attr("y", -83)
    .attr("x", -320)
    .attr("dy", ".75em")
    .attr("transform", "rotate(-90)")
    .style("text-size", "16px")
    .style("fill", "#baaed9")
    .text("Frequency");


// A function that create / update the plot for a given variable:
function update(data) {

    // Update the X axis
    x.domain(data.map(d => d.group))
    xAxis.call(d3.axisBottom(x))

    // Update the Y axis
    y.domain([0, d3.max(data, d => d.value) ]);
    yAxis.transition().duration(1000).call(d3.axisLeft(y));

    // Create the u variable
    var u = bb_svg.selectAll("rect").data(data)

    // Use the u variable to update the bars with the new argued data
    u
        .join("rect")
        .transition()
        .duration(1000)
        .attr("x", d => x(d.group))
        .attr("y", d => y(d.value))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.value))
        .attr("fill", "#69b3a2")
}

// Initialize the plot with the first dataset
// update(activity)
