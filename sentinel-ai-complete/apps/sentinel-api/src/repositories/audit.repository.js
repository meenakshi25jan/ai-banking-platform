import { randomUUID } from 'node:crypto';
import { readJson, writeJson } from './fs.repository.js';

const FILE = 'storage/audits.json';

export async function createAuditEvent(data) {
  const items = await readJson(FILE);
  const record = { id: randomUUID(), ...data, createdAt: new Date().toISOString() };
  items.push(record);
  await writeJson(FILE, items);
  return record;
}

export async function getAuditEventsByDecisionId(decisionId) {
  const items = await readJson(FILE);
  return items.filter((item) => item.decisionId === decisionId).sort((a, b) => a.createdAt.localeCompare(b.createdAt));
}
