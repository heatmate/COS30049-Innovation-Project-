import PieChart from "./PieChart"

const PieData = ({data}) => {
  if (!data) return null;

  // Convert to an array 
  const dataset = Object.entries(data).map(([label, value]) => ({
    label,
    value: value * 100, //convert to %
  }));

  return (
    <div className="flex flex-col items-center space-y-4 mt-6">
      <h3 className="font-semibold">Probability Distribution</h3>
      <PieChart data={dataset} width={350} height={350} />
    </div>
  );
};

export default PieData;