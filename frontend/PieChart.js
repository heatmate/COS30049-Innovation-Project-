import React, { useEffect, useRef } from "react"
import * as d3 from "d3"

const PieChart = ({ data, width = 300, height = 300 }) => {
  const ref = useRef()

  useEffect(() => {
    if (!data || data.length === 0) return

    const radius = Math.min(width, height) / 2
    const color = d3.scaleOrdinal(d3.schemeCategory10)

    // Clear previous chart
    d3.select(ref.current).selectAll("*").remove()

    const svg = d3
      .select(ref.current)
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${width / 2}, ${height / 2})`)

    const pie = d3
      .pie()
      .sort(null)
      .value((d) => d.value)

    const arc = d3.arc().innerRadius(0).outerRadius(radius)

    // Remove existing tooltip if any (to avoid duplicates)
    d3.select("body").selectAll(".tooltip").remove()

    // Create tooltip
    const tooltip = d3
      .select("body")
      .append("div")
      .attr("class", "tooltip")
      .style("position", "absolute")
      .style("background", "white")
      .style("padding", "1px 5px")
      .style("border", "1px solid #ccc")
      .style("border-radius", "6px")
      .style("pointer-events", "none")
      .style("box-shadow", "0px 2px 6px rgba(0,0,0,0.2)")
      .style("opacity", 0)

    // Draw slices
    svg
      .selectAll("path")
      .data(pie(data))
      .join("path")
      .attr("d", arc)
      .attr("fill", (d) => color(d.data.label))
      .style("opacity", 0.8)
      .on("mouseover", function (event, d) {
        d3.select(this).style("opacity", 1)
        tooltip
          .style("opacity", 1)
          .html(`<strong>${d.data.label}</strong>: ${d.data.value}`)
          .style("left", event.pageX + 10 + "px")
          .style("top", event.pageY - 20 + "px")
      })
      .on("mousemove", function (event) {
        tooltip
          .style("left", event.pageX + 10 + "px")
          .style("top", event.pageY - 20 + "px")
      })
      .on("mouseout", function () {
        d3.select(this).style("opacity", 0.8)
        tooltip.transition().duration(200).style("opacity", 0)
      })

    // Labels
    svg
      .selectAll("text")
      .data(pie(data))
      .join("text")
      .text((d) => d.data.label)
      .attr("transform", (d) => `translate(${arc.centroid(d)})`)
      .style("text-anchor", "middle")
      .style("font-size", "12px")
  }, [data, width, height])

  return <svg ref={ref}></svg>
}

export default PieChart
