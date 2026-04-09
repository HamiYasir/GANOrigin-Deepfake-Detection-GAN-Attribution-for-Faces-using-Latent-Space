import ConfidenceBar from "./ConfidenceBar";

interface ResultCardProps {
  prediction: string;
  confidence: number;
}

const ResultCard: React.FC<ResultCardProps> = ({
  prediction,
  confidence,
}) => {
  return (
    <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-xl mx-auto mt-10 transition-all duration-300 hover:shadow-2xl">
      <h2 className="text-xl font-semibold text-slate-700">
        Prediction
      </h2>

      <p className="text-3xl font-bold text-blue-600 mt-2">
        {prediction}
      </p>

      <ConfidenceBar confidence={confidence} />
    </div>
  );
};

export default ResultCard;
