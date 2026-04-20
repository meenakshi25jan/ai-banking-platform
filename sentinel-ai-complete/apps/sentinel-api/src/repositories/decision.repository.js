import { randomUUID } from 'node:crypto';
import { readJson, writeJson } from './fs.repository.js';

const FILE = 'storage/decisions.json';

export async function createDecisionRecord(data) {
  const items = await readJson(FILE);
  const record = { id: randomUUID(), ...data, createdAt: new Date().toISOString() };
  items.push(record);
  await writeJson(FILE, items);
  return record;
}

export async function getDecisionById(id) {
  const items = await readJson(FILE);
  return items.find((item) => item.id === id) || null;
}
