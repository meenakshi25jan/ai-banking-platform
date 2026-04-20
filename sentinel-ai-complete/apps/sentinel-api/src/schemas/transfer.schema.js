import { z } from 'zod';

export const transferSchema = z.object({
  userId: z.string(),
  accountId: z.string(),
  beneficiaryId: z.string(),
  amount: z.number().positive(),
  currency: z.string().min(3).max(3),
  newDevice: z.boolean().optional().default(false),
  crossBorder: z.boolean().optional().default(false),
  purpose: z.string().optional(),
  ipAddress: z.string().optional(),
  deviceId: z.string().optional(),
  geo: z.string().optional(),
  failedAttemptsLast24h: z.number().int().nonnegative().optional().default(0),
  expediteRequested: z.boolean().optional().default(false)
});
