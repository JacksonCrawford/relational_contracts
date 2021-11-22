// var margin = {top: 20, right: 120, bottom: 20, left: 120},
//     width = 960 - margin.right - margin.left,
//     height = 500 - margin.top - margin.bottom;

var i = 0;

var tree = d3.layout.tree()
    .size([height, width]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

let tree_svg = d3.select("#dendrogram")
    .append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// load the external data
d3.json("results.json", function(error, treeData) {
    console.log(treeData);
    root = treeData[0];
    update(root);
});

function update(source) {

    // Compute the new tree layout.
    var nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);

    // Normalize for fixed-depth.
    nodes.forEach(function(d) { d.y = d.depth * 180; });

    // Declare the nodes…
    var node = tree_svg.selectAll("g.node")
        .data(nodes, function(d) { return d.id || (d.id = ++i); });

    // Enter the nodes.
    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function(d) {
            return "translate(" + d.y + "," + d.x + ")"; });

    nodeEnter.append("circle")
        .attr("r", 10)
        .style("fill", "#fff");

    nodeEnter.append("text")
        .attr("x", function(d) {
            return d.children || d._children ? -13 : 13; })
        .attr("dy", ".35em")
        .attr("text-anchor", function(d) {
            return d.children || d._children ? "end" : "start"; })
        .text(function(d) { return d.name; })
        .style("fill-opacity", 1);

    // Declare the links…
    var link = tree_svg.selectAll("path.link")
        .data(links, function(d) { return d.target.id; });

    // Enter the links.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("d", diagonal);

}








// // set the dimensions and margins of the graph
// // const width = 460
// // const height = 460
// const radius = width / 2 // radius of the dendrogram
//
// // append the svg object to the body of the page
// const dend_svg = d3.select("#dendrogram")
//     .append("svg")
//     .attr("width", width)
//     .attr("height", height)
//     .append("g")
//     .attr("transform", `translate(${radius},${radius})`);
//
// // read json data
// d3.json("https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/data_dendrogram.json").then( function(data) {
//
//     // Create the cluster layout:
//     const cluster = d3.cluster()
//         .size([360, radius - 60]);  // 360 means whole circle. radius - 60 means 60 px of margin around dendrogram
//
//     // Give the data to this cluster layout:
//     const root = d3.hierarchy(data, function(d) {
//         return d.children;
//     });
//     cluster(root);
//
//     // Features of the links between nodes:
//     const linksGenerator = d3.linkRadial()
//         .angle(function(d) { return d.x / 180 * Math.PI; })
//         .radius(function(d) { return d.y; });
//
//     // Add the links between nodes:
//     dend_svg.selectAll('path')
//         .data(root.links())
//         .join('path')
//         .attr("d", linksGenerator)
//         .style("fill", 'none')
//         .attr("stroke", '#ccc')
//
//
//     // Add a circle for each node.
//     dend_svg.selectAll("g")
//         .data(root.descendants())
//         .join("g")
//         .attr("transform", function(d) {
//             return `rotate(${d.x-90})
//           translate(${d.y})`;
//         })
//         .append("circle")
//         .attr("r", 17)
//         .style("fill", "#69b3a2")
//         .attr("stroke", "black")
//         .style("stroke-width", 2)
//         .attr("dx",function(d) { return -20; })
//         .text("banana")
//
// })