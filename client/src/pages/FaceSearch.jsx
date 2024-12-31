import React, { useState } from 'react';
import { Upload, Loader2, AlertCircle } from 'lucide-react';

const FaceSearch = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
      setError('');
      setResults([]);  // Clear previous results
    } else {
      setError('Please select a valid image file');
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) {
      setError('Please select an image first');
      return;
    }
  
    setLoading(true);
    setError('');
    setResults([]);
    
    const formData = new FormData();
    formData.append('file', selectedFile);
  
    try {
      console.log('Starting image search...');
      const response = await fetch('http://localhost:8000/api/search', {
        method: 'POST',
        body: formData,
      });
  
      console.log('Response status:', response.status);
      const responseText = await response.text();
      console.log('Raw response:', responseText);
  
      let data;
      try {
        data = JSON.parse(responseText);
      } catch (e) {
        console.error('Failed to parse JSON:', e);
        throw new Error('Invalid response format');
      }
  
      console.log('Parsed response data:', data);
  
      if (!Array.isArray(data)) {
        throw new Error('Response is not an array');
      }
  
      setResults(data);
    } catch (err) {
      console.error('Search error:', err);
      setError(`Failed to perform image search: ${err.message}`);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  const renderResults = () => {
    if (!Array.isArray(results) || results.length === 0) {
      return null;
    }

    return (
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold mb-4">Similar Faces Found</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.map((result, index) => (
            <div key={index} className="border rounded-lg overflow-hidden hover:shadow-lg transition-shadow">
              <div className="relative">
                <img
                  src={result.url}
                  alt={`Match ${index + 1}`}
                  className="w-full h-48 object-cover"
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = 'https://via.placeholder.com/400x300?text=Image+Load+Error';
                  }}
                />
                <div className="absolute top-2 right-2 bg-blue-600 text-white px-2 py-1 rounded-full text-sm font-medium">
                  {result.similarity.toFixed(1)}% Match
                </div>
              </div>
              
              <div className="p-4">
                <div className="flex items-center justify-between">
                  <a 
                    href={result.source_url} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:text-blue-800 text-sm truncate"
                  >
                    View Source
                  </a>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h1 className="text-2xl font-bold mb-4">Face Search</h1>
          
          {/* Upload Section */}
          <div className="mb-6">
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
              <input
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
                id="imageInput"
              />
              <label
                htmlFor="imageInput"
                className="cursor-pointer flex flex-col items-center"
              >
                <Upload className="w-12 h-12 text-gray-400 mb-2" />
                <span className="text-gray-600">Upload a photo with a face</span>
                <span className="text-sm text-gray-500">PNG, JPG, WEBP supported</span>
              </label>
            </div>
          </div>

          {/* Preview Section with Face Detection */}
          {preview && (
            <div className="mb-6">
              <h2 className="text-lg font-semibold mb-2">Preview</h2>
              <div className="relative inline-block">
                <img
                  src={preview}
                  alt="Preview"
                  className="max-w-xs rounded-lg shadow-sm"
                />
              </div>
            </div>
          )}

          {error && (
            <div className="bg-red-50 text-red-600 p-4 rounded-md mb-4 flex items-center">
              <AlertCircle className="w-5 h-5 mr-2" />
              {error}
            </div>
          )}

          <button
            onClick={handleSubmit}
            disabled={loading || !selectedFile}
            className={`w-full py-3 px-4 rounded-md text-white flex items-center justify-center ${
              loading || !selectedFile
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700'
            }`}
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                Searching...
              </>
            ) : (
              'Find Similar Faces'
            )}
          </button>
        </div>

        {renderResults()}
      </div>
    </div>
  );
};

export default FaceSearch;