import HeatmapChart from "./HeatmapChart"

const HeatmapData = () => {
  const dataset = [
    { module: "Auth", category: "SQL Injection", count: 12 },
    { module: "Database", category: "Buffer Overflow", count: 4 },
    { module: "UI", category: "Cross-Site Scripting", count: 9 },
    { module: "UI", category: "CSRF", count: 3 },
    { module: "Network", category: "DoS", count: 2 },
];

  return (
    <div className="flex flex-col items-center space-y-4">
      <HeatmapChart data={dataset} width={300} height={300} />
    </div>
  )
}

export default HeatmapData
