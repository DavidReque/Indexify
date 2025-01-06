"use client";

import React, { useState, KeyboardEvent, JSX, useEffect } from "react";
import { Search, X, AlertCircle, TrendingUp, History } from "lucide-react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { SearchError, SearchResult, Suggestion } from "@/types";

export default function Home(): JSX.Element {
  const router = useRouter();
  const searchParams = useSearchParams();

  const [searchQuery, setSearchQuery] = useState<string>("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<SearchError>({ message: "", show: false });
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [showSuggestions, setShowSuggestions] = useState<boolean>(false);
  const [searchHistory, setSearchHistory] = useState<string[]>([]);

  // Cargar resultados previos del localStorage al iniciar
  useEffect(() => {
    const savedResults = localStorage.getItem("searchResults");
    const savedQuery = localStorage.getItem("lastQuery");
    const savedHistory = localStorage.getItem("searchHistory");

    if (savedResults && savedQuery) {
      setSearchResults(JSON.parse(savedResults));
      setSearchQuery(savedQuery);
    }

    if (savedHistory) {
      setSearchHistory(JSON.parse(savedHistory));
    }

    // Recuperar query de URL si existe
    const queryParam = searchParams.get("q");
    if (queryParam && queryParam !== savedQuery) {
      setSearchQuery(queryParam);
      handleSearch(queryParam);
    }
  }, []);

  useEffect(() => {
    const fetchSuggestions = async () => {
      if (searchQuery.length < 2) {
        setSuggestions([]);
        return;
      }

      try {
        const response = await fetch(
          `${process.env.NEXT_PUBLIC_BACKEND_URL_SUGGESTIONS}?query=${searchQuery}`,
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
    handleSearch(suggestion.text);
  };

  const handleSearch = async (query: string = searchQuery): Promise<void> => {
    if (!query.trim()) return;

    setIsLoading(true);
    setError({ message: "", show: false });

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/search`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          credentials: "include",
          body: JSON.stringify({
            query: query,
            size: 10,
          }),
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Error en la búsqueda");
      }

      const data = await response.json();

      if (!data.results) {
        throw new Error("No se recibieron resultados del servidor");
      }

      setSearchResults(data.results);

      // Guardar resultados en localStorage
      localStorage.setItem("searchResults", JSON.stringify(data.results));
      localStorage.setItem("lastQuery", query);

      // Actualizar historial de búsqueda
      const updatedHistory = [
        query,
        ...searchHistory.filter((q) => q !== query),
      ].slice(0, 5);
      setSearchHistory(updatedHistory);
      localStorage.setItem("searchHistory", JSON.stringify(updatedHistory));

      // Actualizar URL
      router.push(`?q=${encodeURIComponent(query)}`);

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
    setError({ message: "", show: false });
    // No limpiamos los resultados para mantener el contexto
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      if (showSuggestions && suggestions.length > 0) {
        e.preventDefault();
        handleSuggestionClick(suggestions[0]);
      } else {
        handleSearch();
      }
    }
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen bg-gradient-to-br from-white to-gray-50 p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-8 row-start-2 items-center w-full max-w-3xl">
        <div className="flex flex-col items-center gap-4 mb-8">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 bg-clip-text text-transparent">
            Búsqueda
          </h1>
          <p className="text-gray-500 text-lg">
            Encuentra lo que necesitas en segundos
          </p>
        </div>

        <div className="relative w-full">
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

          {/* Historial de búsqueda */}
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

          {/* Sugerencias */}
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

          {error.show && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-700">
              <AlertCircle className="w-5 h-5" />
              <span>{error.message}</span>
            </div>
          )}

          {searchResults.length > 0 && (
            <div className="mt-8">
              <h2 className="text-xl font-semibold mb-4">Resultados</h2>
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
