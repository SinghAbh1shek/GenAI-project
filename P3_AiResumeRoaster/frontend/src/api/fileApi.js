const BASE_URL = 'http://localhost:8000';

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    throw new Error('Upload failed');
  }

  return res.json();
}

export async function getFileById(fileId) {
  const res = await fetch(`${BASE_URL}/${fileId}`);

  if (!res.ok) {
    throw new Error('Failed to fetch file status');
  }

  return res.json();
}
