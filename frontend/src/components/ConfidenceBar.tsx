interface ConfidenceBarProps {
  confidence: number;
}

const ConfidenceBar: React.FC<ConfidenceBarProps> = ({ confidence }) => {
  const percent = confidence * 100;

  return (
    <div className="mt-6">
      <div className="flex justify-between text-sm text-gray-600 mb-2">
        <span>Confidence</span>
        <span>{percent.toFixed(2)}%</span>
      </div>

      <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
        <div
          className="bg-black h-2 transition-all duration-700"
          style={{ width: `${percent}%` }}
        />
      </div>
    </div>
  );
};

export default ConfidenceBar;
