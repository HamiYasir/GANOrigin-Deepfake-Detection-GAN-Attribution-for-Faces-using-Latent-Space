const Header = () => {
  return (
    <div className="text-center mt-24 mb-16 animate-fade">
      <div className="flex justify-center items-center gap-3">
        <div className="w-8 h-8 bg-black rounded-full" />
        <h1 className="text-4xl font-semibold text-gray-900">
          GAN Attribution
        </h1>
      </div>

      <p className="text-gray-500 mt-4 text-lg">
        Latent-Space Architecture Detection
      </p>

      {/* <div className="mt-6 inline-block px-4 py-1 text-sm bg-gray-200 rounded-full text-gray-600">
        Model Accuracy: 97.1%
      </div> */}
    </div>
  );
};

export default Header;
