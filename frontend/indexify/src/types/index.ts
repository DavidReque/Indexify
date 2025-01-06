export interface SearchResult {
  title: string;
  abstract: string;
  keywords?: string[];
  content: string;
}

export interface Suggestion {
  text: string;
  count: number;
  trending: boolean;
}

export interface SearchError {
  message: string;
  show: boolean;
}
