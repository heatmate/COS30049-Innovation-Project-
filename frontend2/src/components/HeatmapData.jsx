import HeatmapChart from "./HeatmapChart"

const HeatmapData = ({data}) => {
  if (!data) return null;

  // Const probabilities into a format the heatmap will expect 
  const dataset = Object.entries(data).map(([category, value]) => ({
    module: "Prediction",
    category,
    count: Math.round(value * 100),
  }));

  return (
    <div className="flex flex-col items-center space-y-4 mt-8">
      <h3 className="font-semibold">Category Confidence Heatmap</h3>
      <HeatmapChart data={dataset} />
    </div>
  );
};

export default HeatmapData;
