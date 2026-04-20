import { z } from 'zod';

export const loanSchema = z.object({
  userId: z.string(),
  loanAmount: z.number().positive(),
  monthlyIncome: z.number().positive(),
  employmentType: z.string().min(2),
  purpose: z.string().optional(),
  creditScore: z.number().int().min(300).max(900).optional(),
  existingEmi: z.number().nonnegative().optional().default(0),
  newDevice: z.boolean().optional().default(false),
  deviceId: z.string().optional(),
  ipAddress: z.string().optional(),
  failedAttemptsLast24h: z.number().int().nonnegative().optional().default(0)
});
