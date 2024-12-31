"use client";
import React, { useState } from "react";
import { Search, X, Clock, Sparkles, TrendingUp } from "lucide-react";

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [isFocused, setIsFocused] = useState(false);

  const recentSearches = ["iPhone 14", "MacBook Pro", "AirPods Pro"];
  const trendingSearches = [
    "PlayStation 5",
    "Nintendo Switch",
    "Xbox Series X",
  ];

  const handleClear = () => {
    setSearchQuery("");
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen bg-gradient-to-br from-white to-gray-50 p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center w-full max-w-3xl">
        <div className="flex flex-col items-center gap-4 mb-8">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 bg-clip-text text-transparent">
            Búsqueda
          </h1>
          <p className="text-gray-500 text-lg">
            Encuentra lo que necesitas en segundos
          </p>
        </div>

        {/* Contenedor con altura fija para evitar saltos */}
        <div className="relative w-full">
          <div className="relative flex items-center w-full group">
            <div className="absolute left-4 w-5 h-5 text-gray-400 transition-transform duration-200 group-focus-within:text-blue-500">
              <Search className="w-full h-full" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onFocus={() => setIsFocused(true)}
              onBlur={() => setTimeout(() => setIsFocused(false), 200)}
              placeholder="¿Qué estás buscando?"
              className="w-full py-5 px-12 rounded-2xl border border-gray-200 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent shadow-lg shadow-gray-100/50 text-lg placeholder:text-gray-400 transition-all hover:shadow-xl"
            />
            {searchQuery && (
              <button
                onClick={handleClear}
                className="absolute right-4 p-2 hover:bg-gray-100 rounded-full transition-all duration-200 hover:scale-110"
              >
                <X className="w-5 h-5 text-gray-400" />
              </button>
            )}
          </div>

          {/* Panel de sugerencias con posición absoluta y animación de opacidad */}
          <div
            className={`absolute w-full mt-2 transition-all duration-200 ${
              isFocused
                ? "opacity-100 visible translate-y-0"
                : "opacity-0 invisible -translate-y-2"
            }`}
          >
            <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-4 divide-y divide-gray-100">
              {/* Búsquedas recientes */}
              <div className="pb-4">
                <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
                  <Clock className="w-4 h-4" />
                  <span>Búsquedas recientes</span>
                </div>
                <div className="flex flex-col gap-2">
                  {recentSearches.map((search) => (
                    <button
                      key={search}
                      className="flex items-center gap-2 px-3 py-2 hover:bg-gray-50 rounded-lg text-gray-700 text-left transition-colors"
                      onClick={() => setSearchQuery(search)}
                    >
                      <Clock className="w-4 h-4 text-gray-400" />
                      {search}
                    </button>
                  ))}
                </div>
              </div>

              {/* Trending */}
              <div className="pt-4">
                <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
                  <TrendingUp className="w-4 h-4" />
                  <span>Tendencias</span>
                </div>
                <div className="flex flex-col gap-2">
                  {trendingSearches.map((trend) => (
                    <button
                      key={trend}
                      className="flex items-center gap-2 px-3 py-2 hover:bg-gray-50 rounded-lg text-gray-700 text-left transition-colors"
                      onClick={() => setSearchQuery(trend)}
                    >
                      <Sparkles className="w-4 h-4 text-gray-400" />
                      {trend}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Sugerencias de categorías con transición suave */}
        <div
          className={`flex flex-wrap gap-2 justify-center mt-4 transition-opacity duration-200 ${
            !searchQuery && !isFocused ? "opacity-100" : "opacity-0"
          }`}
        >
          <button className="px-6 py-3 rounded-xl bg-white shadow-md shadow-gray-100/50 text-gray-700 hover:shadow-lg hover:scale-105 transition-all duration-200">
            Tecnología
          </button>
          <button className="px-6 py-3 rounded-xl bg-white shadow-md shadow-gray-100/50 text-gray-700 hover:shadow-lg hover:scale-105 transition-all duration-200">
            Ropa y Accesorios
          </button>
          <button className="px-6 py-3 rounded-xl bg-white shadow-md shadow-gray-100/50 text-gray-700 hover:shadow-lg hover:scale-105 transition-all duration-200">
            Hogar
          </button>
        </div>
      </main>
    </div>
  );
}
