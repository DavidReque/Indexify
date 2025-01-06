"use client";

import React from "react";
import { AlertCircle, History, TrendingUp } from "lucide-react";
import Link from "next/link";
import { useSearch } from "@/hooks/useSearch";
import { useSuggestions } from "@/hooks/useSuggestions";
import { Suggestion } from "@/types";
import { SearchBar } from "@/components/SearchBar";

export default function Home() {
  const {
    searchQuery,
    setSearchQuery,
    searchResults,
    isLoading,
    error,
    searchHistory,
    handleSearch,
  } = useSearch();

  const { suggestions, showSuggestions, setShowSuggestions } =
    useSuggestions(searchQuery);

  const handleSuggestionClick = (suggestion: Suggestion): void => {
    setSearchQuery(suggestion.text);
    setShowSuggestions(false);
    handleSearch(suggestion.text);
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen bg-gradient-to-br from-white to-gray-50 p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-8 row-start-2 items-center w-full max-w-3xl">
        {/* Header */}
        <div className="flex flex-col items-center gap-4 mb-8">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 bg-clip-text text-transparent">
            Search
          </h1>
        </div>

        <div className="relative w-full">
          {/* Search Bar Component */}
          <SearchBar
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            handleSearch={handleSearch}
            isLoading={isLoading}
            setShowSuggestions={setShowSuggestions}
          />

          {/* Search History */}
          {searchHistory.length > 0 && !showSuggestions && !searchQuery && (
            <div className="absolute w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-100 z-50">
              <div className="p-2 text-sm text-gray-500 border-b flex items-center gap-2">
                <History className="w-4 h-4" />
                Búsquedas recientes
              </div>
              {searchHistory.map((query, index) => (
                <div
                  key={index}
                  className="px-4 py-2 hover:bg-gray-50 cursor-pointer text-gray-700"
                  onClick={() => {
                    setSearchQuery(query);
                    handleSearch(query);
                  }}
                >
                  {query}
                </div>
              ))}
            </div>
          )}

          {/* Suggestions */}
          {showSuggestions && suggestions.length > 0 && (
            <div className="absolute w-full mt-2 bg-white rounded-lg shadow-lg border border-gray-100 z-50">
              {suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className="px-4 py-3 hover:bg-gray-50 cursor-pointer flex items-center gap-3"
                  onClick={() => handleSuggestionClick(suggestion)}
                >
                  <TrendingUp
                    className={`w-4 h-4 ${
                      suggestion.trending ? "text-red-500" : "text-gray-400"
                    }`}
                  />
                  <div>
                    <div className="font-medium">{suggestion.text}</div>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Error Message */}
          {error.show && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700">
              <AlertCircle className="w-5 h-5" />
              <span>{error.message}</span>
            </div>
          )}

          {/* Search Results */}
          {searchResults.length > 0 && (
            <div className="mt-8">
              <h2 className="text-xl font-semibold mb-4">Results</h2>
              <div className="space-y-4">
                {searchResults.map((result, index) => (
                  <div
                    key={index}
                    className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
                  >
                    <Link href={`${result.content}`}>
                      <h3 className="text-lg font-medium text-blue-600 hover:underline">
                        {result.title}
                      </h3>
                    </Link>
                    <p className="text-gray-600 mt-2">{result.abstract}</p>
                    {result.keywords && result.keywords.length > 0 && (
                      <div className="flex flex-wrap gap-2 mt-2">
                        {result.keywords.map((keyword, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 bg-gray-100 text-gray-600 text-sm rounded"
                          >
                            {keyword}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Loading Spinner */}
          {isLoading && (
            <div className="flex justify-center mt-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
