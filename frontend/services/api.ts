const API_BASE = "http://127.0.0.1:8000";

export async function getStocks() {
  const response = await fetch(`${API_BASE}/stocks`);

  if (!response.ok) {
    throw new Error("Failed to fetch stocks");
  }

  return response.json();
}
