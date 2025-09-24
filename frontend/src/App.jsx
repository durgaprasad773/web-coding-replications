import React, { useState, useEffect } from 'react';
import { Upload, Download, FileText, Code, Activity, Settings } from 'lucide-react';
import toast from 'react-hot-toast';
import FileUpload from './components/FileUpload';
import ReplicaForm from './components/ReplicaForm';
import ResultsDisplay from './components/ResultsDisplay';
import TokenUsage from './components/TokenUsage';
import { generateReplicas, downloadExcel, getTokenUsage, resetSessionTokens } from './services/api';

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [uploadedData, setUploadedData] = useState(null);
  const [replicaConfig, setReplicaConfig] = useState({
    type: 'webcoding',
    numReplicas: 3
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [tokenUsage, setTokenUsage] = useState({ session_tokens: 0, total_tokens: 0 });

  useEffect(() => {
    // Load token usage on component mount
    loadTokenUsage();
  }, []);

  const loadTokenUsage = async () => {
    try {
      const usage = await getTokenUsage();
      setTokenUsage(usage);
    } catch (error) {
      console.error('Failed to load token usage:', error);
    }
  };

  const handleFileUpload = (data) => {
    setUploadedData(data);
    setCurrentStep(2);
    toast.success('File uploaded successfully!');
  };

  const handleConfigSubmit = async (config) => {
    setReplicaConfig(config);
    setLoading(true);
    
    try {
      const response = await generateReplicas({
        ...uploadedData,
        replica_type: config.type,
        num_replicas: config.numReplicas
      });
      
      setResults(response);
      setTokenUsage(response.session_usage);
      setCurrentStep(3);
      toast.success(`Generated ${config.numReplicas} replicas successfully!`);
    } catch (error) {
      toast.error(`Failed to generate replicas: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadExcel = async () => {
    try {
      await downloadExcel(results.replicas);
      toast.success('Excel file downloaded successfully!');
    } catch (error) {
      toast.error(`Failed to download Excel: ${error.message}`);
    }
  };

  const handleResetSession = async () => {
    try {
      const result = await resetSessionTokens();
      if (result.success) {
        setTokenUsage(result.current_usage);
        toast.success('Session tokens reset successfully!');
      } else {
        toast.error('Failed to reset session tokens');
      }
    } catch (error) {
      toast.error(`Failed to reset session tokens: ${error.message}`);
    }
  };

  const resetProcess = () => {
    setCurrentStep(1);
    setUploadedData(null);
    setResults(null);
    setReplicaConfig({ type: 'webcoding', numReplicas: 3 });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Code className="h-8 w-8 text-primary-600 mr-3" />
              <h1 className="text-2xl font-bold text-gray-900">
                Web Coding Replication
              </h1>
            </div>
            <TokenUsage usage={tokenUsage} onResetSession={handleResetSession} />
          </div>
        </div>
      </header>

      {/* Progress Steps */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-center mb-8">
          <div className="flex items-center space-x-4">
            {[1, 2, 3].map((step) => (
              <div key={step} className="flex items-center">
                <div
                  className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-medium ${
                    step <= currentStep
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-500'
                  }`}
                >
                  {step === 1 && <Upload className="w-5 h-5" />}
                  {step === 2 && <Settings className="w-5 h-5" />}
                  {step === 3 && <FileText className="w-5 h-5" />}
                </div>
                {step < 3 && (
                  <div
                    className={`w-16 h-1 mx-2 ${
                      step < currentStep ? 'bg-primary-600' : 'bg-gray-200'
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Step Labels */}
        <div className="flex justify-center mb-8">
          <div className="flex space-x-24 text-sm">
            <span className={currentStep >= 1 ? 'text-primary-600 font-medium' : 'text-gray-500'}>
              Upload JSON
            </span>
            <span className={currentStep >= 2 ? 'text-primary-600 font-medium' : 'text-gray-500'}>
              Configure
            </span>
            <span className={currentStep >= 3 ? 'text-primary-600 font-medium' : 'text-gray-500'}>
              Results
            </span>
          </div>
        </div>

        {/* Content */}
        <div className="max-w-4xl mx-auto">
          {currentStep === 1 && (
            <FileUpload onUpload={handleFileUpload} />
          )}

          {currentStep === 2 && (
            <ReplicaForm
              config={replicaConfig}
              onSubmit={handleConfigSubmit}
              loading={loading}
              uploadedData={uploadedData}
            />
          )}

          {currentStep === 3 && results && (
            <ResultsDisplay
              results={results}
              onDownloadExcel={handleDownloadExcel}
              onReset={resetProcess}
            />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;