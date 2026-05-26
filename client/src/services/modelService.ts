const API_URL = 'http://127.0.0.1:8000';

export async function getModels(): Promise<string[]> {
  const res = await fetch(`${API_URL}/models`);
  return res.json();
}