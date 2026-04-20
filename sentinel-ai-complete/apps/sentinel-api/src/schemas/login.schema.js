import { z } from 'zod';

export const loginSchema = z.object({
  userId: z.string(),
  deviceId: z.string(),
  ipAddress: z.string(),
  geo: z.string().optional(),
  failedAttemptsLast24h: z.number().int().nonnegative().optional().default(0),
  newDevice: z.boolean().optional().default(false)
});
