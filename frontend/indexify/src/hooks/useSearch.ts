"use client";
import { useState, useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { SearchError, SearchResult } from "@/types/index";
import { API_ENDPOINTS } from "@/config/constants";

export const useSearch = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<SearchError>({ message: "", show: false });
  const [searchHistory, setSearchHistory] = useState<string[]>([]);

  useEffect(() => {
    loadInitialState();
  }, []);

  const loadInitialState = () => {
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

    const queryParam = searchParams.get("q");
    if (queryParam && queryParam !== savedQuery) {
      setSearchQuery(queryParam);
      handleSearch(queryParam);
    }
  };

  const handleSearch = async (query: string = searchQuery): Promise<void> => {
    if (!query.trim()) return;

    setIsLoading(true);
    setError({ message: "", show: false });

    try {
      const response = await fetch(API_ENDPOINTS.SEARCH, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ query, size: 10 }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Error en la búsqueda");
      }

      const data = await response.json();
      handleSearchSuccess(data, query);
    } catch (error) {
      handleSearchError(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearchSuccess = (
    data: { results: SearchResult[] },
    query: string
  ) => {
    if (!data.results) {
      throw new Error("No se recibieron resultados del servidor");
    }

    setSearchResults(data.results);
    updateLocalStorage(data.results, query);
    updateSearchHistory(query);
    router.push(`?q=${encodeURIComponent(query)}`);

    if (data.results.length === 0) {
      setError({
        message: "No se encontraron resultados para tu búsqueda",
        show: true,
      });
    }
  };

  const handleSearchError = (error: unknown) => {
    const errorMessage =
      error instanceof Error ? error.message : "Error en la búsqueda";
    setError({ message: errorMessage, show: true });
    console.error("Error searching:", error);
  };

  const updateLocalStorage = (results: SearchResult[], query: string) => {
    localStorage.setItem("searchResults", JSON.stringify(results));
    localStorage.setItem("lastQuery", query);
  };

  const updateSearchHistory = (query: string) => {
    const updatedHistory = [
      query,
      ...searchHistory.filter((q) => q !== query),
    ].slice(0, 5);
    setSearchHistory(updatedHistory);
    localStorage.setItem("searchHistory", JSON.stringify(updatedHistory));
  };

  return {
    searchQuery,
    setSearchQuery,
    searchResults,
    isLoading,
    error,
    searchHistory,
    handleSearch,
  };
};
