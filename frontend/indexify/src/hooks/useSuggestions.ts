"use client";
import { API_ENDPOINTS } from "@/config/constants";
import { Suggestion } from "@/types/index";
import { useState, useEffect } from "react";

export const useSuggestions = (searchQuery: string) => {
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
          `${API_ENDPOINTS.SUGGESTIONS}?query=${searchQuery}`,
          {
            method: "GET",
            headers: { Accept: "application/json" },
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

  return {
    suggestions,
    showSuggestions,
    setShowSuggestions,
  };
};
