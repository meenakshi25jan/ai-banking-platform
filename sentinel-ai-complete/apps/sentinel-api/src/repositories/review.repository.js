import { randomUUID } from 'node:crypto';
import { readJson, writeJson } from './fs.repository.js';

const FILE = 'storage/reviews.json';

export async function createReviewRecord(data) {
  const items = await readJson(FILE);
  const record = {
    id: randomUUID(),
    status: 'OPEN',
    assignedTo: null,
    resolution: null,
    resolvedBy: null,
    resolvedAt: null,
    createdAt: new Date().toISOString(),
    ...data
  };
  items.push(record);
  await writeJson(FILE, items);
  return record;
}

export async function getReviewCases() {
  const items = await readJson(FILE);
  return items.sort((a, b) => b.createdAt.localeCompare(a.createdAt));
}

export async function updateReviewCase(id, patch) {
  const items = await readJson(FILE);
  const index = items.findIndex((item) => item.id === id);
  if (index === -1) return null;
  items[index] = { ...items[index], ...patch, updatedAt: new Date().toISOString() };
  await writeJson(FILE, items);
  return items[index];
}
