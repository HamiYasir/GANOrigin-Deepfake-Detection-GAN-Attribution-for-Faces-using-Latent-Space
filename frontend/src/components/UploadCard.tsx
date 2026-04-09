interface UploadCardProps {
  preview: string | null;
  onFileChange: (file: File) => void;
  onAnalyze: () => void;
  loading: boolean;
}

const UploadCard: React.FC<UploadCardProps> = ({
  preview,
  onFileChange,
  onAnalyze,
  loading,
}) => {
  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) onFileChange(file);
  };

  return (
    <div
      onDragOver={(e) => e.preventDefault()}
      onDrop={handleDrop}
      className="bg-white/70 backdrop-blur-lg shadow-xl rounded-3xl p-10 w-full max-w-xl mx-auto transition-all duration-300"
    >
      <div className="border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center">
        <p className="text-gray-500">
          Drag & Drop image or click below
        </p>

        <label className="mt-4 w-full bg-green-500 text-white py-3 rounded-2xl font-medium hover:opacity-80 hover:bg-white hover:text-green-500 border-2 border-white hover:border-green-500 transition-all duration-500 text-center block cursor-pointer">
            Choose File
            <input 
            type="file" 
            className="hidden"
            onChange={(e) => {
                const file = e.target.files?.[0];
                if (file) onFileChange(file);
            }}
            />
        </label>

        {/* <input
          type="file"
          accept="image/*"
          className="mt-4 w-full bg-black text-white py-3 rounded-2xl font-medium hover:opacity-80 transition-all duration-200 text-center"
          onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) onFileChange(file);
          }}
        /> */}
      </div>

      {preview && (
        <img
          src={preview}
          alt="Preview"
          className="rounded-2xl mt-8 mx-auto max-h-64 object-contain"
        />
      )}

      <button
        onClick={onAnalyze}
        disabled={loading}
        className="mt-8 w-full bg-black text-white py-3 rounded-2xl font-medium hover:opacity-80 transition-all duration-200"
      >
        {loading ? "Analyzing..." : "Analyze Image"}
      </button>
    </div>
  );
};

export default UploadCard;
