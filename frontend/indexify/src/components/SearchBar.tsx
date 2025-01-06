import React from "react";
import { Search, X } from "lucide-react";

interface SearchBarProps {
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  handleSearch: () => void;
  isLoading: boolean;
  setShowSuggestions: (show: boolean) => void;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  searchQuery,
  setSearchQuery,
  handleSearch,
  isLoading,
  setShowSuggestions,
}) => {
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
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
          onClick={() => setSearchQuery("")}
          className="absolute right-4 p-2 hover:bg-gray-100 rounded-full transition-all duration-200 hover:scale-110"
          disabled={isLoading}
        >
          <X className="w-5 h-5 text-gray-400" />
        </button>
      )}
    </div>
  );
};
