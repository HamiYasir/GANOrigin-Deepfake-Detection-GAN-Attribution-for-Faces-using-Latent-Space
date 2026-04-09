interface ProbabilityCardProps {
  probabilities: Record<string, number>;
}

const ProbabilityCard: React.FC<ProbabilityCardProps> = ({
  probabilities,
}) => {
  return (
    <div className="mt-8">
      <h3 className="text-gray-700 font-medium mb-4">
        Probability Breakdown
      </h3>

      {Object.entries(probabilities).map(([label, value]) => (
        <div key={label} className="mb-4">
          <div className="flex justify-between text-sm text-gray-600 mb-1">
            <span>{label}</span>
            <span>{(value * 100).toFixed(2)}%</span>
          </div>

          <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
            <div
              className="bg-gray-900 h-2 transition-all duration-700"
              style={{ width: `${value * 100}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProbabilityCard;
