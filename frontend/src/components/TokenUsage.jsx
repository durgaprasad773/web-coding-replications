import React from 'react';
import { Activity, TrendingUp, RotateCcw } from 'lucide-react';

const TokenUsage = ({ usage, onResetSession }) => {
  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    }
    if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  const estimateCost = (tokens) => {
    // Rough estimate for GPT-3.5-turbo: ~$0.002 per 1K tokens
    const costPer1K = 0.002;
    return ((tokens / 1000) * costPer1K).toFixed(4);
  };

  return (
    <div className="flex items-center space-x-6 text-sm">
      {/* Session Usage */}
      <div className="flex items-center space-x-2">
        <Activity className="h-4 w-4 text-primary-600" />
        <div className="text-center">
          <div className="font-medium text-gray-900">
            {formatNumber(usage.session_tokens)}
          </div>
          <div className="text-xs text-gray-500">Session</div>
        </div>
      </div>

      {/* Total Usage */}
      <div className="flex items-center space-x-2">
        <TrendingUp className="h-4 w-4 text-gray-600" />
        <div className="text-center">
          <div className="font-medium text-gray-900">
            {formatNumber(usage.total_tokens)}
          </div>
          <div className="text-xs text-gray-500">Total</div>
        </div>
      </div>

      {/* Estimated Cost */}
      <div className="text-center">
        <div className="font-medium text-gray-900">
          ${estimateCost(usage.total_tokens)}
        </div>
        <div className="text-xs text-gray-500">Est. Cost</div>
      </div>

      {/* Reset Session Button */}
      {usage.session_tokens > 0 && (
        <button
          onClick={onResetSession}
          className="flex items-center space-x-1 px-2 py-1 text-xs text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded transition-colors"
          title="Reset session tokens"
        >
          <RotateCcw className="h-3 w-3" />
          <span>Reset Session</span>
        </button>
      )}
    </div>
  );
};

export default TokenUsage;