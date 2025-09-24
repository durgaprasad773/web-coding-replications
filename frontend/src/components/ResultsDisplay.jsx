import React, { useState } from 'react';
import { Download, FileSpreadsheet, FileText, RefreshCw, CheckCircle, Code, Eye, EyeOff, Edit, Save, X, Play } from 'lucide-react';

const ResultsDisplay = ({ results, onDownloadExcel, onReset }) => {
  const [expandedReplica, setExpandedReplica] = useState(null);
  const [codeView, setCodeView] = useState('html'); // html, css, js
  const [editingReplica, setEditingReplica] = useState(null);
  const [editedReplicas, setEditedReplicas] = useState({});
  const [previewReplica, setPreviewReplica] = useState(null);

  const replicas = results?.replicas || {};
  const replicaKeys = Object.keys(replicas);

  const toggleReplica = (replicaKey) => {
    setExpandedReplica(expandedReplica === replicaKey ? null : replicaKey);
  };

  const formatCode = (code) => {
    if (!code) return 'No code available';
    return code.length > 200 ? `${code.substring(0, 200)}...` : code;
  };

  const getFullCode = (replica, type) => {
    const replicaKey = Object.keys(replicas).find(key => replicas[key] === replica);
    const editedReplica = editedReplicas[replicaKey];
    
    if (editedReplica) {
      switch (type) {
        case 'html':
          return editedReplica.html_solution || editedReplica.html_code || 'No HTML code';
        case 'css':
          return editedReplica.css_solution || editedReplica.css_code || 'No CSS code';
        case 'js':
          return editedReplica.js_solution || editedReplica.js_code || 'No JavaScript code';
        default:
          return '';
      }
    }
    
    switch (type) {
      case 'html':
        return replica.html_solution || replica.html_code || 'No HTML code';
      case 'css':
        return replica.css_solution || replica.css_code || 'No CSS code';
      case 'js':
        return replica.js_solution || replica.js_code || 'No JavaScript code';
      default:
        return '';
    }
  };

  const handleEditReplica = (replicaKey) => {
    setEditingReplica(replicaKey);
    if (!editedReplicas[replicaKey]) {
      setEditedReplicas(prev => ({
        ...prev,
        [replicaKey]: { ...replicas[replicaKey] }
      }));
    }
  };

  const handleSaveEdit = () => {
    setEditingReplica(null);
  };

  const handleCancelEdit = () => {
    setEditingReplica(null);
  };

  const handleCodeChange = (replicaKey, codeType, value) => {
    setEditedReplicas(prev => ({
      ...prev,
      [replicaKey]: {
        ...prev[replicaKey],
        [codeType]: value,
        [`${codeType.split('_')[0]}_solution`]: value
      }
    }));
  };

  const handlePreview = (replicaKey) => {
    setPreviewReplica(replicaKey);
  };

  const getPreviewHTML = (replicaKey) => {
    const replica = editedReplicas[replicaKey] || replicas[replicaKey];
    const htmlCode = replica.html_solution || replica.html_code || '';
    const cssCode = replica.css_solution || replica.css_code || '';
    const jsCode = replica.js_solution || replica.js_code || '';

    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview</title>
    <style>
        ${cssCode}
    </style>
</head>
<body>
    ${htmlCode}
    <script>
        ${jsCode}
    </script>
</body>
</html>
    `;
  };

  const getCurrentReplicas = () => {
    const current = {};
    Object.keys(replicas).forEach(key => {
      current[key] = editedReplicas[key] || replicas[key];
    });
    return current;
  };

  const handleDownloadModified = () => {
    const modifiedResults = {
      ...results,
      replicas: getCurrentReplicas()
    };
    onDownloadExcel(modifiedResults);
  };

  return (
    <div className="space-y-6">
      {/* Success Header */}
      <div className="card bg-green-50 border-green-200">
        <div className="flex items-center mb-4">
          <CheckCircle className="h-8 w-8 text-green-600 mr-3" />
          <div>
            <h2 className="text-2xl font-bold text-green-900">
              Generation Complete!
            </h2>
            <p className="text-green-700">
              Successfully generated {replicaKeys.length} unique replica{replicaKeys.length > 1 ? 's' : ''}
            </p>
          </div>
        </div>

        {/* Token Usage Summary */}
        {results.token_usage && (
          <div className="bg-white rounded-lg p-4 mb-4">
            <h3 className="font-medium text-gray-900 mb-2">Token Usage for this Generation</h3>
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <span className="text-gray-500">Input Tokens:</span>
                <p className="font-medium">{results.token_usage.input_tokens}</p>
              </div>
              <div>
                <span className="text-gray-500">Output Tokens:</span>
                <p className="font-medium">{results.token_usage.output_tokens}</p>
              </div>
              <div>
                <span className="text-gray-500">Total Tokens:</span>
                <p className="font-medium">{results.token_usage.total_tokens}</p>
              </div>
            </div>
          </div>
        )}

        {/* Download Actions */}
        <div className="flex gap-4">
          <button
            onClick={() => handleDownloadModified()}
            className="btn-primary flex items-center"
          >
            <FileSpreadsheet className="h-4 w-4 mr-2" />
            Download Excel {Object.keys(editedReplicas).length > 0 && '(Modified)'}
          </button>
          <button
            onClick={onReset}
            className="btn-secondary flex items-center ml-auto"
          >
            <RefreshCw className="h-4 w-4 mr-2" />
            Generate New
          </button>
        </div>
      </div>

      {/* Replicas List */}
      <div className="space-y-4">
        <h3 className="text-xl font-bold text-gray-900">Generated Replicas</h3>
        
        {replicaKeys.map((replicaKey, index) => {
          const replica = replicas[replicaKey];
          const isExpanded = expandedReplica === replicaKey;
          
          return (
            <div key={replicaKey} className="card">
              <div className="flex items-center justify-between">
                <div 
                  className="flex items-center flex-1 cursor-pointer"
                  onClick={() => toggleReplica(replicaKey)}
                >
                  <div className="w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center text-sm font-medium mr-3">
                    {index + 1}
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900">
                      {(editedReplicas[replicaKey] || replica).short_text || `Replica ${index + 1}`}
                      {editedReplicas[replicaKey] && <span className="text-orange-600 text-sm ml-2">(Modified)</span>}
                    </h4>
                    <p className="text-sm text-gray-500">
                      {replica.subtopic && `${replica.subtopic} • `}
                      {replica.course && `${replica.course} • `}
                      Click to {isExpanded ? 'collapse' : 'expand'}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center gap-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handlePreview(replicaKey);
                    }}
                    className="btn-icon text-blue-600 hover:bg-blue-50"
                    title="Preview"
                  >
                    <Play className="h-4 w-4" />
                  </button>
                  
                  {editingReplica === replicaKey ? (
                    <>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleSaveEdit();
                        }}
                        className="btn-icon text-green-600 hover:bg-green-50"
                        title="Save"
                      >
                        <Save className="h-4 w-4" />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleCancelEdit();
                        }}
                        className="btn-icon text-red-600 hover:bg-red-50"
                        title="Cancel"
                      >
                        <X className="h-4 w-4" />
                      </button>
                    </>
                  ) : (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleEditReplica(replicaKey);
                      }}
                      className="btn-icon text-gray-600 hover:bg-gray-50"
                      title="Edit"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                  )}
                  
                  {isExpanded ? (
                    <EyeOff className="h-5 w-5 text-gray-400" />
                  ) : (
                    <Eye className="h-5 w-5 text-gray-400" />
                  )}
                </div>
              </div>

              {isExpanded && (
                <div className="mt-6 space-y-4">
                  {/* Question Text */}
                  <div>
                    <h5 className="font-medium text-gray-900 mb-2">Question</h5>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <p className="text-sm text-gray-700">
                        {replica.question_text || 'No question text available'}
                      </p>
                    </div>
                  </div>

                  {/* Code Preview/Editor */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <h5 className="font-medium text-gray-900">
                        {editingReplica === replicaKey ? 'Code Editor' : 'Code Preview'}
                      </h5>
                      <div className="flex bg-gray-100 rounded-lg p-1">
                        <button
                          onClick={() => setCodeView('html')}
                          className={`px-3 py-1 text-xs font-medium rounded ${
                            codeView === 'html' 
                              ? 'bg-white text-primary-700 shadow-sm' 
                              : 'text-gray-600 hover:text-gray-900'
                          }`}
                        >
                          HTML
                        </button>
                        <button
                          onClick={() => setCodeView('css')}
                          className={`px-3 py-1 text-xs font-medium rounded ${
                            codeView === 'css' 
                              ? 'bg-white text-primary-700 shadow-sm' 
                              : 'text-gray-600 hover:text-gray-900'
                          }`}
                        >
                          CSS
                        </button>
                        <button
                          onClick={() => setCodeView('js')}
                          className={`px-3 py-1 text-xs font-medium rounded ${
                            codeView === 'js' 
                              ? 'bg-white text-primary-700 shadow-sm' 
                              : 'text-gray-600 hover:text-gray-900'
                          }`}
                        >
                          JS
                        </button>
                      </div>
                    </div>
                    
                    {editingReplica === replicaKey ? (
                      <textarea
                        value={getFullCode(editedReplicas[replicaKey] || replica, codeView)}
                        onChange={(e) => handleCodeChange(replicaKey, `${codeView}_code`, e.target.value)}
                        className="w-full h-64 bg-gray-900 text-green-400 rounded-lg p-4 font-mono text-xs resize-none border border-gray-300 focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
                        placeholder={`Enter ${codeView.toUpperCase()} code here...`}
                      />
                    ) : (
                      <div className="bg-gray-900 text-green-400 rounded-lg p-4 font-mono text-xs overflow-x-auto">
                        <pre className="whitespace-pre-wrap">
                          {getFullCode(replica, codeView)}
                        </pre>
                      </div>
                    )}
                  </div>

                  {/* Test Cases Preview */}
                  {replica.test_cases && (
                    <div>
                      <h5 className="font-medium text-gray-900 mb-2">Test Cases</h5>
                      <div className="bg-gray-50 rounded-lg p-3">
                        {Array.isArray(replica.test_cases) ? (
                          <div className="space-y-2">
                            {replica.test_cases.map((testCase, index) => (
                              <div key={testCase.id || index} className="bg-white rounded p-2 border border-gray-200">
                                <div className="flex items-start justify-between">
                                  <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                                    Test {testCase.order || index + 1}
                                  </span>
                                  <span className="text-xs text-gray-500">
                                    Weight: {testCase.weightage || 10}
                                  </span>
                                </div>
                                <p className="text-sm text-gray-700 mt-2">
                                  {testCase.display_text || 'No description available'}
                                </p>
                                {testCase.criteria && (
                                  <details className="mt-2">
                                    <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-700">
                                      View Criteria
                                    </summary>
                                    <pre className="text-xs bg-gray-100 p-2 rounded mt-1 overflow-auto max-h-32">
                                      {testCase.criteria}
                                    </pre>
                                  </details>
                                )}
                              </div>
                            ))}
                          </div>
                        ) : (
                          <p className="text-sm text-gray-700">
                            {typeof replica.test_cases === 'string' 
                              ? formatCode(replica.test_cases)
                              : 'Test cases available in download'}
                          </p>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Metadata */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-gray-200">
                    <div>
                      <span className="text-xs text-gray-500">Subtopic</span>
                      <p className="text-sm font-medium">{replica.subtopic || 'N/A'}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500">Course</span>
                      <p className="text-sm font-medium">{replica.course || 'N/A'}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500">Module</span>
                      <p className="text-sm font-medium">{replica.module || 'N/A'}</p>
                    </div>
                    <div>
                      <span className="text-xs text-gray-500">Unit</span>
                      <p className="text-sm font-medium">{replica.unit || 'N/A'}</p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Error Display */}
      {results?.replicas?.error && (
        <div className="card bg-red-50 border-red-200">
          <h3 className="font-medium text-red-900 mb-2">Generation Error</h3>
          <p className="text-sm text-red-700 mb-4">{results.replicas.error}</p>
          {results?.replicas?.raw_response && (
            <details className="mt-4">
              <summary className="cursor-pointer text-sm font-medium text-red-900">
                View Raw Response
              </summary>
              <pre className="mt-2 text-xs text-red-700 bg-red-100 p-3 rounded overflow-x-auto">
                {results.replicas.raw_response}
              </pre>
            </details>
          )}
        </div>
      )}

      {/* Preview Modal */}
      {previewReplica && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-2">
          <div className="bg-white rounded-lg max-w-7xl w-full h-[95vh] flex flex-col">
            <div className="flex items-center justify-between p-4 border-b flex-shrink-0">
              <h3 className="text-lg font-medium text-gray-900">
                Preview: {(editedReplicas[previewReplica] || replicas[previewReplica]).short_text}
              </h3>
              <button
                onClick={() => setPreviewReplica(null)}
                className="btn-icon text-gray-600 hover:bg-gray-50"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="flex-1 overflow-hidden min-h-0">
              <iframe
                srcDoc={getPreviewHTML(previewReplica)}
                className="w-full h-full border-0"
                title="Preview"
                sandbox="allow-scripts allow-same-origin"
              />
            </div>
            <div className="p-3 border-t bg-gray-50 flex-shrink-0">
              <p className="text-sm text-gray-600">
                This is a live preview of your replica. You can edit the code and preview changes in real-time.
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsDisplay;