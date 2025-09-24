import React, { useState } from 'react';
import { Settings, Code, Palette, ArrowRight, Loader2 } from 'lucide-react';

const ReplicaForm = ({ config, onSubmit, loading, uploadedData }) => {
  const [formData, setFormData] = useState(config);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Extract info from uploaded data for display
  const getCodeLanguages = () => {
    if (!uploadedData?.solutions_metadata?.[0]?.code_details) return [];
    return uploadedData.solutions_metadata[0].code_details.map(code => code.language);
  };

  const hasJavaScript = getCodeLanguages().includes('JAVASCRIPT');

  return (
    <div className="card">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Configure Replica Generation
        </h2>
        <p className="text-gray-600">
          Set up how you want to generate your code replicas
        </p>
      </div>

      {/* Upload Summary */}
      <div className="bg-gray-50 rounded-lg p-4 mb-6">
        <h3 className="font-medium text-gray-900 mb-2">Uploaded Question Summary</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-500">Short Text:</span>
            <p className="font-medium">{uploadedData?.short_text}</p>
          </div>
          <div>
            <span className="text-gray-500">Languages:</span>
            <div className="flex gap-2 mt-1">
              {getCodeLanguages().map(lang => (
                <span key={lang} className="px-2 py-1 bg-primary-100 text-primary-700 rounded text-xs">
                  {lang}
                </span>
              ))}
            </div>
          </div>
          <div>
            <span className="text-gray-500">Test Cases:</span>
            <p className="font-medium">{uploadedData?.test_cases?.length || 0} tests</p>
          </div>
          <div>
            <span className="text-gray-500">Detected Type:</span>
            <p className="font-medium">{hasJavaScript ? 'Web Coding' : 'Responsive'}</p>
          </div>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Replica Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            <Settings className="inline h-4 w-4 mr-2" />
            Replica Type
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div
              className={`p-4 border-2 rounded-lg cursor-pointer transition-colors ${
                formData.type === 'webcoding'
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => handleInputChange('type', 'webcoding')}
            >
              <div className="flex items-center mb-2">
                <Code className="h-5 w-5 text-primary-600 mr-2" />
                <h3 className="font-medium">Web Coding</h3>
              </div>
              <p className="text-sm text-gray-600">
                HTML + CSS + JavaScript replicas with full interactivity
              </p>
              <div className="mt-2">
                <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded">
                  {hasJavaScript ? 'Recommended' : 'Available'}
                </span>
              </div>
            </div>

            <div
              className={`p-4 border-2 rounded-lg cursor-pointer transition-colors ${
                formData.type === 'responsive'
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
              onClick={() => handleInputChange('type', 'responsive')}
            >
              <div className="flex items-center mb-2">
                <Palette className="h-5 w-5 text-primary-600 mr-2" />
                <h3 className="font-medium">Responsive</h3>
              </div>
              <p className="text-sm text-gray-600">
                HTML + CSS only replicas focusing on responsive design
              </p>
              <div className="mt-2">
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                  {!hasJavaScript ? 'Recommended' : 'Available'}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Number of Replicas */}
        <div>
          <label htmlFor="numReplicas" className="block text-sm font-medium text-gray-700 mb-2">
            Number of Replicas
          </label>
          <select
            id="numReplicas"
            value={formData.numReplicas}
            onChange={(e) => handleInputChange('numReplicas', parseInt(e.target.value))}
            className="select-field"
          >
            <option value={1}>1 Replica</option>
            <option value={2}>2 Replicas</option>
            <option value={3}>3 Replicas</option>
            <option value={4}>4 Replicas</option>
            <option value={5}>5 Replicas</option>
            <option value={6}>6 Replicas</option>
            <option value={7}>7 Replicas</option>
            <option value={8}>8 Replicas</option>
            <option value={9}>9 Replicas</option>
            <option value={10}>10 Replicas</option>
          </select>
          <p className="text-sm text-gray-500 mt-1">
            More replicas will consume more tokens and take longer to generate
          </p>
        </div>

        {/* Generation Options */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-medium text-blue-900 mb-2">Generation Options</h3>
          <ul className="text-sm text-blue-800 space-y-1">
            <li>• Each replica will have unique visual themes and content</li>
            <li>• All functionality and test cases will be preserved</li>
            <li>• Generated replicas will be downloadable in Excel and JSON formats</li>
            <li>• Token usage will be tracked and displayed</li>
          </ul>
        </div>

        {/* Submit Button */}
        <div className="flex justify-center pt-4">
          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex items-center px-8 py-3 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="h-5 w-5 mr-2 animate-spin" />
                Generating Replicas...
              </>
            ) : (
              <>
                Generate {formData.numReplicas} Replica{formData.numReplicas > 1 ? 's' : ''}
                <ArrowRight className="h-5 w-5 ml-2" />
              </>
            )}
          </button>
        </div>

        {loading && (
          <div className="text-center mt-4">
            <p className="text-sm text-gray-600">
              This may take 30-60 seconds depending on the complexity and number of replicas...
            </p>
          </div>
        )}
      </form>
    </div>
  );
};

export default ReplicaForm;