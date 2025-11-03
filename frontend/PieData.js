import PieChart from "./PieChart"

const PieData = () => {
  const dataset = [/* Category -> Amount */
    { label: "DoS", value: 30 },
    { label: "SQL Injection", value: 15 },
    { label: "Buffer Overflow", value: 10 },
    { label: "CSRF", value: 45 },
  ]

  return (
    <div className="flex flex-col items-center space-y-4">
      <PieChart data={dataset} width={300} height={300} />
    </div>
  )
}

export default PieData
