import { z } from 'zod';

export const assistantSchema = z.object({
  userId: z.string(),
  message: z.string().min(1),
  channel: z.enum(['private', 'public']).optional().default('private'),
  newDevice: z.boolean().optional().default(false),
  deviceId: z.string().optional(),
  ipAddress: z.string().optional(),
  geo: z.string().optional(),
  expediteRequested: z.boolean().optional().default(false)
});
