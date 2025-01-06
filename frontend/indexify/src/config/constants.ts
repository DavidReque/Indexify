export const API_ENDPOINTS = {
  SEARCH: `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/search`,
  SUGGESTIONS: `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/suggestions`,
} as const;
