import { env } from '../config/env.js';
import { runLocalDecision } from './local.engine.js';

export async function orchestrateDecision(context) {
  try {
    const response = await fetch(`${env.orchestratorUrl}/orchestrate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(context)
    });
    if (!response.ok) {
      throw new Error(`Orchestrator failed with status ${response.status}`);
    }
    return await response.json();
  } catch (_error) {
    return runLocalDecision(context);
  }
}
