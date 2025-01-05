"use client";

import React, { useState, KeyboardEvent, JSX, useEffect } from "react";
import { Search, X, AlertCircle, TrendingUp } from "lucide-react";
import Link from "next/link";

interface SearchResult {
  title: string;
  abstract: string;
  keywords?: string[];
  content: string;
}

interface Suggestion {
  text: string;
  count: number;
  trending: boolean;
}

interface SearchError {
  message: string;
  show: boolean;
}

export default function Home(): JSX.Element {
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [isFocused, setIsFocused] = useState<boolean>(false);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<SearchError>({ message: "", show: false });
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (searchQuery.length < 2) {
        setSuggestions([]);
        return;
      }

      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/suggestions?query=${searchQuery}`,
          {
            method: "GET",
            headers: {
              Accept: "application/json",
            },
            credentials: "include",
          }
        );

        if (!response.ok) throw new Error("Error fetching suggestions");

        const data = await response.json();
        setSuggestions(data.suggestions);
      } catch (error) {
        console.error("Error fetching suggestions:", error);
      }
    };

    const debounceTimer = setTimeout(fetchSuggestions, 300);
    return () => clearTimeout(debounceTimer);
  }, [searchQuery]);

  const handleSuggestionClick = (suggestion: Suggestion): void => {
    setSearchQuery(suggestion.text);
    setShowSuggestions(false);
    handleSearch();
  };

  const handleSearch = async (): Promise<void> => {
    if (!searchQuery.trim()) return;

    setIsLoading(true);
    setError({ message: "", show: false });
    setSearchResults([]);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        mode: "cors", // Especificar explícitamente el modo CORS
        credentials: "include", // Incluir credenciales si es necesario
        body: JSON.stringify({
          query: searchQuery,
          size: 10,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Error en la búsqueda");
      }

      const data = await response.json();

      if (!data.results) {
        throw new Error("No se recibieron resultados del servidor");
      }

      setSearchResults(data.results);

      if (data.results.length === 0) {
        setError({
          message: "No se encontraron resultados para tu búsqueda",
          show: true,
        });
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Error en la búsqueda";
      setError({
        message: errorMessage,
        show: true,
      });
      console.error("Error searching:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = (): void => {
    setSearchQuery("");
    //setSearchResults([]);
    setError({ message: "", show: false });
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      if (showSuggestions && suggestions.length > 0) {
        e.preventDefault();
        handleSuggestionClick(suggestions[0]); // Seleccionar la primera sugerencia automáticamente
      } else {
        handleSearch();
      }
    }
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen bg-gradient-to-br from-white to-gray-50 p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-8 row-start-2 items-center w-full max-w-3xl">
        {/* Header section remains the same */}
        <div className="flex flex-col items-center gap-4 mb-8">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 bg-clip-text text-transparent">
            Búsqueda
          </h1>
          <p className="text-gray-500 text-lg">
            Encuentra lo que necesitas en segundos
          </p>
        </div>

        <div className="relative w-full">
          {/* Search input section */}
          <div className="relative flex items-center w-full group">
            <div className="absolute left-4 w-5 h-5 text-gray-400 transition-transform duration-200 group-focus-within:text-blue-500">
              <Search className="w-full h-full" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
              onFocus={() => setShowSuggestions(true)}
              onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
              placeholder="¿Qué estás buscando?"
              className="w-full py-5 px-12 rounded-2xl border border-gray-200 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-lg shadow-gray-100/50 text-lg placeholder:text-gray-400 transition-all hover:shadow-xl"
              disabled={isLoading}
            />
            {searchQuery && (
              <button
                onClick={handleClear}
                className="absolute right-4 p-2 hover:bg-gray-100 rounded-full transition-all duration-200 hover:scale-110"
                disabled={isLoading}
              >
                <X className="w-5 h-5 text-gray-400" />
              </button>
            )}
          </div>

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

          {/* Error message */}
          {error.show && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700">
              <AlertCircle className="w-5 h-5" />
              <span>{error.message}</span>
            </div>
          )}

          {/* Search Results */}
          {searchResults.length > 0 && (
            <div className="mt-8">
              <h2 className="text-xl font-semibold mb-4">Resultados</h2>
              <div className="space-y-4">
                {searchResults.map((result, index) => (
                  <div
                    key={index}
                    className="p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow"
                  >
                    <Link content="" href={`${result.content}`}>
                      <h3 className="text-lg font-medium text-blue-600">
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

          {/* Loading State */}
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
