import React, { useEffect, useRef } from "react";
import * as d3 from "d3";

const HeatmapChart = ({ data }) => {
  const ref = useRef();

  useEffect(() => {
    if (!data || data.length === 0) return;

    // Clear any previous chart
    d3.select(ref.current).selectAll("*").remove();

    const margin = { top: 40, right: 20, bottom: 60, left: 120 };
    const width = 500 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const svg = d3
      .select(ref.current)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Extract unique labels
    const modules = Array.from(new Set(data.map((d) => d.module)));
    const categories = Array.from(new Set(data.map((d) => d.category)));

    // X scale
    const x = d3.scaleBand().domain(modules).range([0, width]).padding(0.05);
    svg
      .append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(d3.axisBottom(x))
      .selectAll("text")
      .attr("transform", "rotate(-45)")
      .style("text-anchor", "end");

    // Y scale
    const y = d3.scaleBand().domain(categories).range([height, 0]).padding(0.05);
    svg.append("g").call(d3.axisLeft(y));

    // Color scale
    const color = d3
      .scaleSequential()
      .interpolator(d3.interpolateOrRd)
      .domain([0, d3.max(data, (d) => d.count)]);

    // Tooltip
    const tooltip = d3
      .select("body")
      .append("div")
      .style("position", "absolute")
      .style("visibility", "hidden")
      .style("padding", "8px")
      .style("background", "rgba(0,0,0,0.7)")
      .style("color", "#fff")
      .style("border-radius", "4px")
      .style("font-size", "12px");

    // Draw cells
    svg
      .selectAll()
      .data(data, (d) => d.module + ":" + d.category)
      .enter()
      .append("rect")
      .attr("x", (d) => x(d.module))
      .attr("y", (d) => y(d.category))
      .attr("width", x.bandwidth())
      .attr("height", y.bandwidth())
      .style("fill", (d) => color(d.count))
      .style("stroke", "#fff")
      .style("stroke-width", "1px")
      .on("mouseover", function (event, d) {
        tooltip
          .style("visibility", "visible")
          .html(
            `<b>${d.module}</b><br>${d.category}<br>Count: ${d.count}`
          );
        d3.select(this).style("stroke", "#000").style("stroke-width", "2px");
      })
      .on("mousemove", (event) => {
        tooltip
          .style("top", event.pageY - 10 + "px")
          .style("left", event.pageX + 10 + "px");
      })
      .on("mouseout", function () {
        tooltip.style("visibility", "hidden");
        d3.select(this).style("stroke", "#fff").style("stroke-width", "1px");
      });

    // Legend
    const legendWidth = 300;
    const legendHeight = 10;
    const legendsvg = svg.append("g").attr("transform", `translate(0, -30)`);

    const legendScale = d3
      .scaleLinear()
      .domain(color.domain())
      .range([0, legendWidth]);

    const legendAxis = d3
      .axisBottom(legendScale)
      .ticks(5)
      .tickFormat(d3.format("d"));

    const defs = legendsvg.append("defs");
    const linearGradient = defs
      .append("linearGradient")
      .attr("id", "legend-gradient");
    linearGradient
      .selectAll("stop")
      .data([
        { offset: "0%", color: color.range()[0] },
        { offset: "100%", color: color.range()[1] },
      ])
      .enter()
      .append("stop")
      .attr("offset", (d) => d.offset)
      .attr("stop-color", (d) => d.color);

    legendsvg
      .append("rect")
      .attr("width", legendWidth)
      .attr("height", legendHeight)
      .style("fill", "url(#legend-gradient)");

    legendsvg
      .append("g")
      .attr("transform", `translate(0, ${legendHeight})`)
      .call(legendAxis);

    return () => {
      tooltip.remove(); // cleanup
    };
  }, [data]);

  return <div ref={ref} className="w-full overflow-x-auto"></div>;
};

export default HeatmapChart;
