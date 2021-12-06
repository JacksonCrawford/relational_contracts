// CODE ADAPTED FROM https://www.d3-graph-gallery.com/graph/barplot_button_data_hard.html

const activity = [
    {group: "work", value: 20},
    {group: "game", value: 12},
    // {group: "aid", value: 3},
    {group: "attempt", value: 15},
    // {group: "practice", value: 3},
    // {group: "market", value: 6},
    // {group: "creation", value: 2},
    {group: "use", value: 10},
    // {group: "occupation", value: 4},
    // {group: "education", value: 1},
    // {group: "support", value: 1},
    {group: "behavior", value: 12},
    {group: "procedure", value: 7},
    // {group: "search", value: 1},
    // {group: "measurement", value: 2},
    // {group: "dismantling", value: 1}
];

const person = [
    // {group: "white.", value: 1},
    // {group: "expert.", value: 2},
    // {group: "ruler.", value: 1},
    // {group: "longer", value: 7},
    {group: "user", value: 8},
    // {group: "visionary.", value: 1},
    // {group: "censor.", value: 1},
    {group: "engineer", value: 5},
    // {group: "heterosexual.", value: 1},
    {group: "scientist", value: 6},
    // {group: "creditor.", value: 1},
    // {group: "dead_person.", value: 1},
    // {group: "dissenter.", value: 1},
    {group: "peer", value: 5},
    {group: "intellectual", value: 6},
    {group: "friend", value: 3},
    // {group: "closer.", value: 1},
    // {group: "traveler.", value: 1},
    // {group: "nonpartisan.", value: 1},
    // {group: "national.", value: 1},
    // {group: "picker.", value: 1},
    // {group: "killer.", value: 1},
    // {group: "ward.", value: 1},
    // {group: "modern.", value: 2},
    // {group: "amateur.", value: 1},
    // {group: "leader.", value: 1},
    // {group: "adventurer.", value: 1},
    // {group: "disentangler.", value: 1},
    // {group: "copycat.", value: 1},
    // {group: "rich_person.", value: 1}
];

const sequence = [
    {group: "gene", value: 63},
    {group: "codon", value: 1}
];

const message = [
    // {group: "offer", value: 2},
    {group: "subject", value: 6},
    {group: "narrative", value: 6},
    {group: "information", value: 33},
    {group: "statement", value: 2},
    {group: "wit", value: 4},
    {group: "request", value: 3},
    // {group: "respects", value: 1},
    // {group: "meaning", value: 2},
    // {group: "guidance", value: 1}
]

const natural_object = [
    {group: "universe", value: 36},
    {group: "body", value: 16},
    {group: "rock", value: 1},
    {group: "nest", value: 5}
]

const content = [
    // {group: "tradition", value: 1},
    {group: "goal", value: 4},
    {group: "idea", value: 38},
    {group: "issue", value: 8},
    {group: "belief", value: 4},
    {group: "representation", value: 2},
    // {group: "kernel", value: 1}
]

// append the svg object to the body of the page
const bb_svg = d3.select("#breakdown_bars")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

// Initialize the X axis
const x = d3.scaleBand()
    .range([ 0, width ])
    .padding(0.2);
const xAxis = bb_svg.append("g")
    .attr("transform", `translate(0,${height})`)

// Initialize the Y axis
const y = d3.scaleLinear()
    .range([ height, 0]);
const yAxis = bb_svg.append("g")
    .attr("class", "myYaxis")


// A function that create / update the plot for a given variable:
function update(data) {

    // Update the X axis
    x.domain(data.map(d => d.group))
    xAxis.call(d3.axisBottom(x))

    // Update the Y axis
    y.domain([0, d3.max(data, d => d.value) ]);
    yAxis.transition().duration(1000).call(d3.axisLeft(y));

    // Create the u variable
    var u = bb_svg.selectAll("rect")
        .data(data)

    u
        .join("rect") // Add a new rect for each new elements
        .transition()
        .duration(1000)
        .attr("x", d => x(d.group))
        .attr("y", d => y(d.value))
        .attr("width", x.bandwidth())
        .attr("height", d => height - y(d.value))
        .attr("fill", "#69b3a2")
}

// Initialize the plot with the first dataset
update(activity)
