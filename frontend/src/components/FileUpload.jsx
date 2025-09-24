import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertCircle } from 'lucide-react';
import toast from 'react-hot-toast';

const FileUpload = ({ onUpload }) => {
  const onDrop = useCallback((acceptedFiles) => {
    const file = acceptedFiles[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const jsonData = JSON.parse(e.target.result);
          
          // Handle both array and object formats
          let questionData;
          
          if (Array.isArray(jsonData)) {
            // If it's an array, take the first question
            if (jsonData.length === 0) {
              toast.error('JSON array is empty. Please provide at least one question.');
              return;
            }
            questionData = jsonData[0];
            if (jsonData.length > 1) {
              toast.success(`Found ${jsonData.length} questions. Using the first one for replica generation.`);
            }
          } else {
            // If it's already an object, use it directly
            questionData = jsonData;
          }
          
          // Validate required fields
          const requiredFields = ['question_text', 'short_text', 'solutions_metadata', 'test_cases'];
          const missingFields = requiredFields.filter(field => !questionData[field]);
          
          if (missingFields.length > 0) {
            toast.error(`Missing required fields: ${missingFields.join(', ')}`);
            return;
          }
          
          // Validate solutions_metadata structure
          if (!Array.isArray(questionData.solutions_metadata) || questionData.solutions_metadata.length === 0) {
            toast.error('solutions_metadata must be a non-empty array');
            return;
          }
          
          const solution = questionData.solutions_metadata[0];
          if (!solution.code_details || !Array.isArray(solution.code_details)) {
            toast.error('code_details must be an array within solutions_metadata');
            return;
          }
          
          // Validate test_cases structure
          if (!Array.isArray(questionData.test_cases)) {
            toast.error('test_cases must be an array');
            return;
          }
          
          onUpload(questionData);
        } catch (error) {
          toast.error('Invalid JSON file. Please check the file format.');
        }
      };
      reader.readAsText(file);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
    onDrop,
    accept: {
      'application/json': ['.json']
    },
    multiple: false,
    maxSize: 10 * 1024 * 1024 // 10MB
  });

  return (
    <div className="card">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Upload Question JSON
        </h2>
        <p className="text-gray-600">
          Upload a JSON file containing your web coding question data
        </p>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors duration-200 ${
          isDragActive
            ? isDragReject
              ? 'border-red-400 bg-red-50'
              : 'border-primary-400 bg-primary-50'
            : 'border-gray-300 hover:border-primary-400 hover:bg-primary-50'
        }`}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center">
          {isDragReject ? (
            <AlertCircle className="h-16 w-16 text-red-400 mb-4" />
          ) : (
            <Upload className={`h-16 w-16 mb-4 ${isDragActive ? 'text-primary-500' : 'text-gray-400'}`} />
          )}
          
          {isDragActive ? (
            <p className="text-lg font-medium text-primary-600">
              Drop the JSON file here...
            </p>
          ) : (
            <div>
              <p className="text-lg font-medium text-gray-700 mb-2">
                Drag and drop your JSON file here
              </p>
              <p className="text-gray-500 mb-4">or</p>
              <button className="btn-primary">
                Choose File
              </button>
            </div>
          )}
          
          <p className="text-sm text-gray-500 mt-4">
            Supports JSON files up to 10MB
          </p>
        </div>
      </div>

      {/* Example Format */}
      <div className="mt-8 p-4 bg-gray-50 rounded-lg">
        <h3 className="text-sm font-medium text-gray-900 mb-2 flex items-center">
          <FileText className="h-4 w-4 mr-2" />
          Expected JSON Format
        </h3>
        <pre className="text-xs text-gray-600 overflow-x-auto">
{`// Option 1: Single question object
{
  "question_text": "Create a chocolate calculator...",
  "short_text": "Chocolate Calculator",
  "solutions_metadata": [{
    "code_details": [
      {
        "default_code": true,
        "code_data": "<!DOCTYPE html>...",
        "language": "HTML"
      },
      {
        "default_code": true,
        "code_data": "body { ... }",
        "language": "CSS"
      },
      {
        "default_code": true,
        "code_data": "document.getElementById...",
        "language": "JAVASCRIPT"
      }
    ]
  }],
  "test_cases": [...]
}

// Option 2: Array of questions (first one will be used)
[
  {
    "question_text": "Create a chocolate calculator...",
    "short_text": "Chocolate Calculator",
    "solutions_metadata": [...],
    "test_cases": [...]
  }
]`}
        </pre>
      </div>
    </div>
  );
};

export default FileUpload;