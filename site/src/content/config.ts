import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const reviews = defineCollection({
  loader: glob({ pattern: '**/*.md', base: '../resources/reviews' }),
  schema: z.object({
    title: z.string(),
    url: z.string().url(),
    author: z.string(),
    date_evaluated: z.coerce.date(),
    verdict: z.enum(['adopt', 'adapt', 'watch', 'catalog', 'skip']),
    tags: z.array(z.string()),
  }),
});

export const collections = { reviews };
